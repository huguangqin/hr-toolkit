#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
er-legal-monitor：合规速报生成器（零第三方依赖，仅标准库）

读取法规监控台账 CSV，输出面向管理层的 Markdown 合规速报。

用法：
  python gen_bulletin.py <台账csv> [--out 输出名] [--today YYYY-MM-DD]

输出：
  <输出名>.md  —— 按严重度分组的变化清单 + 逾期预警 + 行动项
并在 stdout 打印本期概要（条数 / 逾期数）。
"""
import csv
import sys
import os
import argparse
import datetime

SEV_ORDER = {"高": 0, "中": 1, "低": 2, "观察": 3}
SEV_ICON = {"高": "🔴", "中": "🟠", "低": "🟡", "观察": "⏸"}
VALID_SEV = set(SEV_ORDER.keys())


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def load_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            # 跳过完全空行
            if not any((v or "").strip() for v in r.values()):
                continue
            rows.append(r)
    return rows


def severity_of(row):
    s = (row.get("severity") or "").strip()
    if s not in VALID_SEV:
        return "观察"
    return s


def is_overdue(row, today):
    st = (row.get("status") or "").strip()
    if st in ("已闭环", "已关闭", "归档"):
        return False
    dl = parse_date(row.get("deadline"))
    if dl is None:
        return False
    return dl < today


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="法规监控台账 CSV 路径")
    ap.add_argument("--out", default="合规速报", help="输出文件名（不含扩展名）")
    ap.add_argument("--today", default=None, help="基准日期 YYYY-MM-DD，默认今天")
    args = ap.parse_args()

    today = parse_date(args.today) or datetime.date.today()
    rows = load_rows(args.csv)
    if not rows:
        print("[warn] 台账为空，未生成速报。")
        return

    # 分组
    groups = {"高": [], "中": [], "低": [], "观察": []}
    for r in rows:
        groups[severity_of(r)].append(r)

    overdue = [r for r in rows if is_overdue(r, today)]

    # 统计
    counts = {k: len(v) for k, v in groups.items()}
    status_counts = {}
    for r in rows:
        st = (r.get("status") or "未填").strip() or "未填"
        status_counts[st] = status_counts.get(st, 0) + 1

    lines = []
    lines.append("# 员工关系合规速报（自动生成）")
    lines.append("")
    lines.append(f"- **生成日期**：{today.isoformat()}")
    lines.append(f"- **台账条目**：共 {len(rows)} 条")
    lines.append(f"- **严重度分布**：🔴高 {counts['高']} / 🟠中 {counts['中']} / "
                 f"🟡低 {counts['低']} / ⏸观察 {counts['观察']}")
    lines.append(f"- **状态分布**：" + "、".join(f"{k} {v}" for k, v in status_counts.items()))
    lines.append(f"- **逾期预警**：⚠️ {len(overdue)} 条")
    lines.append("")

    # 高危逐条
    lines.append("## 一、🔴 高影响变更（须阅）")
    lines.append("")
    if groups["高"]:
        for r in groups["高"]:
            lines.append(f"### [{r.get('change_id','?')}] {r.get('title','')}")
            lines.append(f"- **来源**：{r.get('source','')}")
            eff = parse_date(r.get("date_effective"))
            eff_txt = eff.isoformat() if eff else "未定"
            days = (eff - today).days if eff else None
            days_txt = f"（距今 {days} 天）" if days is not None else ""
            lines.append(f"- **生效日**：{eff_txt}{days_txt}")
            lines.append(f"- **影响场景**：{r.get('affected_scenarios','')}")
            lines.append(f"- **对我们的影响**：{r.get('impact_summary','')}")
            lines.append(f"- **建议动作**：{r.get('action_required','')}")
            lines.append(f"- **责任人 / 截止日**：{r.get('owner','')} / {r.get('deadline','')} "
                         f"｜ 状态：{r.get('status','')}")
            lines.append("")
    else:
        lines.append("（本期无高影响变更）")
        lines.append("")

    # 中低观察表
    lines.append("## 二、🟠 中 / 🟡 低 / ⏸ 观察（备查）")
    lines.append("")
    lines.append("| 编号 | 标题 | 类别 | 影响场景 | 严重度 | 状态 |")
    lines.append("|---|---|---|---|---|---|")
    for sev in ("中", "低", "观察"):
        for r in groups[sev]:
            lines.append(f"| {r.get('change_id','')} | {r.get('title','')} | "
                         f"{r.get('category','')} | {r.get('affected_scenarios','')} | "
                         f"{SEV_ICON[sev]}{sev} | {r.get('status','')} |")
    lines.append("")

    # 逾期预警
    lines.append("## 三、逾期 / 临近预警")
    lines.append("")
    if overdue:
        lines.append("| 编号 | 动作 | 责任人 | 截止日 | 状态 |")
        lines.append("|---|---|---|---|---|")
        for r in overdue:
            dl = r.get("deadline", '')
            lines.append(f"| {r.get('change_id','')} | {r.get('action_required','')} | "
                         f"{r.get('owner','')} | {dl} | ⚠️ 逾期 |")
    else:
        lines.append("（无逾期项）")
    lines.append("")

    # 待办总表
    lines.append("## 四、全部行动项")
    lines.append("")
    lines.append("| 编号 | 严重度 | 动作 | 责任人 | 截止日 | 状态 |")
    lines.append("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: SEV_ORDER[severity_of(x)]):
        lines.append(f"| {r.get('change_id','')} | {SEV_ICON[severity_of(r)]}{severity_of(r)} | "
                     f"{r.get('action_required','')} | {r.get('owner','')} | "
                     f"{r.get('deadline','')} | {r.get('status','')} |")
    lines.append("")

    lines.append("> 免责声明：本速报为内部合规管理参考，不构成法律意见；"
                 "制度修订与个案定性请以专业法律意见及当地司法实践为准。")

    out_path = args.out if args.out.endswith(".md") else args.out + ".md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[ok] 速报已生成：{out_path}")
    print(f"     条目 {len(rows)} | 🔴{counts['高']} 🟠{counts['中']} "
          f"🟡{counts['低']} ⏸{counts['观察']} | 逾期 {len(overdue)}")


if __name__ == "__main__":
    main()
