#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
er-risk-assessment：个案风险评分与敞口测算（零第三方依赖，仅标准库）

读取个案输入 CSV，输出 Markdown 风险报告：风险分、败诉概率带、敞口区间、策略建议、红旗信号。

用法：
  python score_case.py <输入csv> [--out 输出名] [--social-avg 社平工资] [--maintain-cost 管理费]

说明：
  - 评分模型见 references/risk-scoring.md；决策与敞口公式见 references/settlement-vs-fight.md
  - 所有金额测算为管理参考，实际以法务口径与最新社平工资为准
  - local_tendency 默认"未知"按保守计；非"未知"取值须附核实来源（脚本不校验，报告提示）
"""
import csv
import sys
import os
import argparse

# ---- 因子计分映射 ----
EVIDENCE = {"A": 0, "B": 1, "C": 2, "D": 3}
PROCEDURE = {"合规": 0, "部分": 2, "不合规": 3}
PROTECTED = {"无": 0, "不确定": 2, "在保护期": 3}
LAWERED = {"无": 0, "威胁": 1, "已委托": 3}
LOCAL = {"未知": 1, "有利": 0, "不利": 3}
ACTION = {"协商解除": 0, "调岗": 1, "绩效PIP": 1, "违纪处分": 2, "过失性解除": 3}
ACTION_WEIGHT = 2
WEIGHTS = {
    "evidence": 3, "procedure": 2, "protected": 3, "lawyered": 2,
    "local": 2, "action": 2, "amount": 1,
}
MAX_POINTS = (3 * WEIGHTS["evidence"] + 3 * WEIGHTS["procedure"] +
              3 * WEIGHTS["protected"] + 3 * WEIGHTS["lawyered"] +
              3 * WEIGHTS["local"] + 3 * WEIGHTS["action"] + 2 * WEIGHTS["amount"])


def norm(v, mapping, default=0):
    return mapping.get((v or "").strip(), default)


def amount_points(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0
    if x <= 0:
        return 0
    if x <= 300000:
        return 1
    return 2


def n_months(tenure):
    try:
        y = float(tenure)
    except (TypeError, ValueError):
        return 0
    full = int(y)
    rem = y - full
    if rem >= 0.5:
        return full + 1
    elif rem > 0:
        return full + 0.5
    return full


def band(score):
    if score >= 70:
        return "🔴 高", "70%–90%"
    if score >= 45:
        return "🟠 中高", "45%–70%"
    if score >= 25:
        return "🟡 中", "25%–45%"
    return "🟢 低", "<25%"


def red_flags(row):
    flags = []
    if norm(row.get("evidence_grade"), EVIDENCE) == 3:
        flags.append("证据链D级(无实质证据)")
    if norm(row.get("procedure_compliant"), PROCEDURE) == 3:
        flags.append("程序不合规(未通知工会/未送达)")
    if norm(row.get("protected_period"), PROTECTED) == 3:
        flags.append("法定保护期内")
    if (norm(row.get("employee_lawyered"), LAWERED) == 3 and
            (row.get("action_type") or "").strip() == "过失性解除"):
        flags.append("已委托律师+过失性解除")
    if (norm(row.get("local_tendency"), LOCAL) == 3 and
            (row.get("action_type") or "").strip() == "过失性解除"):
        flags.append("当地口径不利+过失性解除")
    return flags


def exposure(row, social_avg):
    try:
        base = float(row.get("monthly_base") or 0)
    except ValueError:
        base = 0
    try:
        leave = float(row.get("unpaid_leave_days") or 0)
    except ValueError:
        leave = 0
    nm = n_months(row.get("tenure_years"))
    cap = min(base, 3 * social_avg) if social_avg else base
    comp_n = nm * cap
    comp_2n = 2 * comp_n
    leave_pay = leave * (cap / 21.75) * 2 if cap else 0
    at = (row.get("action_type") or "").strip()
    if at == "协商解除":
        conservative = comp_n
        pessimistic = comp_n + leave_pay
    elif at in ("过失性解除", "违纪处分"):
        conservative = comp_n + leave_pay          # 部分败诉
        pessimistic = comp_2n + leave_pay          # 全败且判2N
    else:  # 调岗 / 绩效PIP
        conservative = 0
        pessimistic = comp_2n + leave_pay          # 若后续升级为解除
    return {
        "n_months": nm, "comp_n": comp_n, "comp_2n": comp_2n,
        "leave_pay": leave_pay, "conservative": conservative,
        "pessimistic": pessimistic,
    }


def strategy(score, flags, at):
    if flags:
        return "⚠️ 红旗：暂停推进，先消除红旗（补证据/补程序/等保护期/转协商）再评估"
    if score >= 70:
        return "诉讼劣势明显，优先协商或先补正再动"
    if score >= 45:
        return "可打可谈，须先强化证据与程序再决定"
    if score >= 25:
        return "略占优，按标准流程推进，谈打皆可"
    return "胜算高，按标准流程推进"


def score_row(row):
    pts = (
        norm(row.get("evidence_grade"), EVIDENCE) * WEIGHTS["evidence"]
        + norm(row.get("procedure_compliant"), PROCEDURE) * WEIGHTS["procedure"]
        + norm(row.get("protected_period"), PROTECTED) * WEIGHTS["protected"]
        + norm(row.get("employee_lawyered"), LAWERED) * WEIGHTS["lawyered"]
        + norm(row.get("local_tendency"), LOCAL) * WEIGHTS["local"]
        + norm(row.get("action_type"), ACTION) * WEIGHTS["action"]
        + amount_points(row.get("amount_involved")) * WEIGHTS["amount"]
    )
    score = round(pts / MAX_POINTS * 100)
    return score, pts


def fmt_money(x):
    return f"¥{x:,.0f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="个案输入 CSV 路径")
    ap.add_argument("--out", default="风险报告", help="输出文件名（不含扩展名）")
    ap.add_argument("--social-avg", type=float, default=0,
                    help="当地社平工资（用于3倍封顶，默认不封顶）")
    ap.add_argument("--maintain-cost", type=float, default=0,
                    help="管理费/律师费基线（用于诉讼期望值，默认0）")
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f)
                if any((v or "").strip() for v in r.values())]
    if not rows:
        print("[warn] 输入为空，未生成报告。")
        return

    lines = ["# 员工关系个案风险报告（自动生成）", ""]
    lines.append(f"- 输入案件：{len(rows)} 个"
                 + (f"｜ 社平工资封顶基数：{fmt_money(3*args.social_avg)}"
                    if args.social_avg else "｜ 未设封顶（按实际基数）"))
    lines.append("- 免责：本报告为管理参考，不构成法律意见；"
                 "local_tendency 非'未知'的取值须附核实来源。")
    lines.append("")

    summary = []
    for r in rows:
        cid = r.get("case_id") or "?"
        score, pts = score_row(r)
        lvl, prob = band(score)
        flags = red_flags(r)
        exp = exposure(r, args.social_avg)
        strat = strategy(score, flags, r.get("action_type"))
        summary.append((cid, score, lvl, prob, exp["conservative"], exp["pessimistic"], strat))

        lines.append(f"## [{cid}] 风险评分 {score}/100（{lvl}）")
        lines.append(f"- **败诉/部分败诉概率区间**：{prob}")
        lines.append(f"- **拟处置**：{r.get('action_type','')}｜证据 {r.get('evidence_grade','')}｜"
                     f"程序 {r.get('procedure_compliant','')}｜保护期 {r.get('protected_period','')}｜"
                     f"员工 {r.get('employee_lawyered','')}｜当地 {r.get('local_tendency','')}")
        lines.append(f"- **赔偿敞口区间**：保守 {fmt_money(exp['conservative'])} "
                     f"— 悲观 {fmt_money(exp['pessimistic'])}"
                     f"（N={exp['n_months']}月，N补偿 {fmt_money(exp['comp_n'])}，"
                     f"2N {fmt_money(exp['comp_2n'])}，年假 {fmt_money(exp['leave_pay'])}）")
        if flags:
            lines.append(f"- **⚠️ 红旗信号**：" + "；".join(flags))
        else:
            lines.append(f"- 红旗信号：无")
        lines.append(f"- **策略建议**：{strat}")
        lines.append("")

    # 汇总表
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 案件 | 风险分 | 等级 | 不利概率 | 敞口保守 | 敞口悲观 | 策略 |")
    lines.append("|---|---|---|---|---|---|---|")
    for cid, score, lvl, prob, cons, pess, strat in summary:
        lines.append(f"| {cid} | {score} | {lvl} | {prob} | {fmt_money(cons)} | "
                     f"{fmt_money(pess)} | {strat} |")
    lines.append("")

    out_path = args.out if args.out.endswith(".md") else args.out + ".md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[ok] 风险报告已生成：{out_path}（{len(rows)} 个案件）")


if __name__ == "__main__":
    main()
