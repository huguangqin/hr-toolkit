---
name: er-risk-assessment
label: ER个案风险预判
description: |
  员工关系（ER）个案风险预判与处置策略工具。在采取任何处分/解除动作前，对单案的败诉概率、赔偿敞口、协商vs诉讼策略给出量化预判。
  适用人群：HRBP、员工关系负责人、HR合规、法务BP。
  触发场景：(1)违纪/协商解除前评估胜算 (2)测算违法解除2N与协商补偿的盈亏平衡点 (3)决定"打还是谈"
  (4)量化个案赔偿敞口（N/2N/年假/社保补缴/股权） (5)识别必谈/必打红旗信号 (6)生成个案风险报告供管理层决策。
  关键词：ER、员工关系、风险预判、败诉概率、违法解除、2N、N+1、协商解除、赔偿敞口、诉讼期望值、合规、劳动仲裁。
  不用于：对具体案件的合法性终局判断、出具法律意见书——本 Skill 提供量化预判框架，最终以专业法律意见及当地司法实践为准。
version: 1
author: huguangqin
license: MIT
tags: [employee-relations, er, risk, termination, litigation, hr, compliance]
metadata:
  hermes:
    tags: [employee-relations, er, risk, litigation]
    related_skills: [er-case-analysis, er-case-communication, er-legal-monitor]
  source:
    origin: 企业内部定制版（员工关系个案风险预判指引，初版基于 ER 实务与败诉复盘梳理）
    note: 提供量化预判框架，不构成法律意见；各地裁判口径差异大，输出中的"当地倾向"字段必须标注待法务核实。
---

# ER 个案风险预判

> 本 Skill 解决一个高频痛点：**动作已经做了，才发现会输**。它把"这个案子能不能动"从拍脑袋变成一套可量化、可复盘、可汇报的预判。

## 核心逻辑

在 `er-case-communication` 给出"怎么谈"、 `er-case-analysis` 给出"历史怎么判"之后，本 Skill 回答第三个问题：**"这一个具体案子，动还是不动、谈还是打、要准备多少钱？"**

```
单个在办案件
   ↓ 输入 7 维因子（证据/程序/保护期/律师/当地/处置类型/金额）
   ↓ 风险评分（0–100）→ 败诉概率区间
   ↓ 敞口测算（N / 2N / +1 / 年假 / 补缴 / 股权）
   ↓ 策略决策（协商上限 vs 诉讼期望值）
   ↓ 输出《个案风险报告》
```

## 硬性约束

1. **不做法律意见。** 输出是"基于输入因子的概率与敞口测算"，不是定性结论；终局以法务/律师意见为准。
2. **当地口径必须标注 `待核实`。** 同一因子（如加班费举证、竞业限制）京沪粤可能相反，评分中的 `local_tendency` 默认 `未知`，由用户/法务补全，禁止假装知道。
3. **证据等级从严。** 证据链 C/D 级一律拉高风险分，不因"员工没闹"而低估——这和 `er-case-analysis` 的"没被挑战≠处理得当"一致。
4. **保护期零容忍。** 医疗期/孕期/工伤期等法定保护期内启动解除，直接触发必谈红旗，不进入"低成本协商"测算。

## 工作流程

### 步骤 1 — 采集 7 维因子

逐案填写 `assets/risk-input.csv`，字段含义见 `references/risk-scoring.md`：

| 因子 | 取值 | 说明 |
|---|---|---|
| `evidence_grade` | A/B/C/D | 证据链完整度（同 analysis 评级） |
| `procedure_compliant` | 合规/部分/不合规 | 工会通知/送达/民主程序 |
| `protected_period` | 无/不确定/在保护期 | 法定保护期 |
| `employee_lawyered` | 无/威胁/已委托 | 员工法律准备度 |
| `local_tendency` | 未知/有利/不利 | 当地裁判口径（标 `待核实`） |
| `action_type` | 协商解除/过失性解除/违纪处分/绩效PIP/调岗 | 拟采取的处置 |
| `amount_involved` | 数值 | 涉案/争议金额（可选） |

### 步骤 2 — 运行评分

```bash
python scripts/score_case.py assets/risk-input.csv --out 风险报告
```

零依赖（标准库），输出：

- `风险报告.md` — 每案：风险分、败诉概率带、敞口区间、策略建议、红旗信号

### 步骤 3 — 解读与决策

按 `references/settlement-vs-fight.md` 把评分转成动作：

- **算协商上限**：诉讼期望值 + 确定性溢价（15–30%）+ 管理费
- **比价决策**：员工要价 ≤ 上限 → 谈；> 上限 → 评估是否值得打
- **红旗必谈**：证据 C/D、保护期、当地不利、已委托律师 → 不低价硬解
- **红旗必打**：原则性/群体性/示范效应且证据充分 → 即便贵也要立标杆

### 步骤 4 — 联动

- 评分高的在办案 → 回写 `er-case-analysis` 台账风险敞口列
- 若触发"当地口径不利" → 转 `er-legal-monitor` 核实最新审判纪要
- 决定谈话 → 调 `er-case-communication` 对应场景话术

## 参考文件

- `references/risk-scoring.md` — 7 维评分模型、权重、概率区间映射
- `references/settlement-vs-fight.md` — 协商vs诉讼决策树、敞口测算公式
- `references/local-adjudication.md` — 京沪粤等地裁判口径差异提示（必标待核实）
- `assets/risk-input.csv` — 个案输入模板
- `scripts/score_case.py` — 零依赖评分与敞口测算脚本
