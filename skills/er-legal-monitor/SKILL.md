---
name: er-legal-monitor
label: ER法规动态监控
description: |
  员工关系（ER）法规动态监控与合规速报工具。把"外部法律/政策变化"系统性地转化为"内部该改什么、谁改、何时改"的可执行清单。
  适用人群：HR合规、HRBP、员工关系负责人、法务BP。
  触发场景：(1)跟踪劳动法/社保/个保新规 (2)解读最高法指导案例与各地审判纪要 (3)评估新规对现有制度/流程的影响
  (4)生成面向管理层的合规速报 (5)维护法规监控台账 (6)制度修订立项。
  关键词：ER、员工关系、法规监控、合规、劳动法、社保、个保、新规解读、审判纪要、指导案例、制度修订、合规速报、监管动态。
  不用于：对具体案件的合法性终局判断、出具法律意见书——本 Skill 提供监控框架与影响评估方法，最终以专业法律意见为准。
version: 1
author: huguangqin
license: MIT
tags: [employee-relations, er, compliance, legal-monitor, regulatory, hr]
metadata:
  hermes:
    tags: [employee-relations, er, compliance, legal-monitor]
    related_skills: [er-case-analysis, er-case-communication, er-risk-assessment]
  source:
    origin: 企业内部定制版（员工关系法规监控指引，初版基于 HR 合规实践梳理）
    note: 提供监控框架与影响评估方法，不构成法律意见；具体制度修订与个案定性请以专业法律意见和当地司法实践为准。
---

# ER 法规动态监控

> 本 Skill 解决一个被多数 HR 团队忽视的痛点：**法规变了，但公司的制度和流程还停在三年前**。等到出事才翻法条，往往已经踩了坑。

## 核心逻辑

外部立法/司法环境是 ER 工作的"地基"。地基一动，上面的制度、流程、话术（见 `er-case-communication`）、案件处置尺度（见 `er-case-analysis`）全部要复核。本 Skill 把这件事从"凭感觉刷新闻"变成一套**可排期、可追踪、可汇报**的监控机制。

```
外部变化（法/规/案/口径）
   ↓ 监控（按频率）
   ↓ 分类（8 类监控对象）
   ↓ 影响评估（change-impact-matrix）
   ↓ 落地（制度修订 / 流程卡点 / 培训）
   ↓ 汇报（合规速报）
```

## 硬性约束

1. **不做法律意见。** 输出的是"监控到什么变化 + 可能对我们产生什么影响 + 建议动作"，最终定性以法务/律师意见为准。
2. **不臆测未生效条文。** 征求意见稿、草案要标注"草案，未生效"，不得当作已实施要求落地。
3. **标注地域口径。** 同一问题各地高院纪要可能相反（如加班费、竞业限制），评估时必须标 `local=待核实`。
4. **时效优先。** 生效日距今 ≤ 60 天的变更一律标 🔴 高紧迫，先出速报再补细则。

## 工作流程

### 步骤 1 — 确定监控范围与频率

按 `references/monitoring-framework.md` 的"监控对象分类 + 信息源目录 + 监测频率"建立监控清单。国家级立法/司法解释按月巡检，地方性法规/审判纪要按季度，重大突发事件（如最高法紧急批复）即时响应。

### 步骤 2 — 捕获变化并登记台账

每捕捉到一条可能影响 ER 的变更，立即写入 `assets/regulatory-tracker.csv`：

| 字段 | 说明 |
|---|---|
| `change_id` | 编号，格式 `LR-年份-三位` |
| `date_published` / `date_effective` | 发布日 / 生效日 |
| `title` / `source` | 标题 / 来源（带 URL 优先） |
| `category` | 8 类监控对象之一（见 framework） |
| `affected_scenarios` | 影响的 ER 场景（解除/绩效/调岗/工时/社保/个保…） |
| `severity` | 影响等级 `高/中/低` |
| `status` | `监测中/已评估/整改中/已闭环` |

### 步骤 3 — 影响评估

对每条变更跑 `references/change-impact-matrix.md` 的四维评估（影响范围 × 紧迫性 × 适配度 × 违规成本），产出：

- 是否需要改制度/流程（是/否/待定）
- 行动项 + 责任人 + 截止日
- 对现有案件（见 `er-case-analysis` 台账）是否有追溯影响

### 步骤 4 — 生成合规速报

```bash
python scripts/gen_bulletin.py assets/regulatory-tracker.csv --out 合规速报
```

零依赖（标准库），输出：

- `合规速报.md` — 按严重度分组的变化清单 + 逾期预警 + 待办行动项

### 步骤 5 — 推动落地

将评估结论转入制度修订立项或流程卡点整改，更新台账 `status` 至 `整改中 → 已闭环`。重大变更同步触发 `er-case-communication` 的话术与清单复核、`er-risk-assessment` 的评分权重复核。

## 监控频率建议（默认）

| 层级 | 对象 | 频率 |
|---|---|---|
| 国家级 | 法律/行政法规/司法解释/人社部规章 | 月度 |
| 地方级 | 高院审判纪要/仲裁委口径/社保细则 | 季度 |
| 突发事件 | 最高法批复、监管紧急通知、重大指导案例 | 即时 |

## 参考文件

- `references/monitoring-framework.md` — 8 类监控对象分类、信息源目录、监测频率
- `references/change-impact-matrix.md` — 变化影响四维评估矩阵与行动项生成规则
- `references/bulletin-template.md` — 面向管理层的合规速报模板
- `assets/regulatory-tracker.csv` — 法规监控台账模板
- `scripts/gen_bulletin.py` — 零依赖速报生成脚本
