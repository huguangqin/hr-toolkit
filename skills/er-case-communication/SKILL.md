---
name: er-case-communication
label: ER案件沟通指引
description: |
  员工关系（ER）案件全流程沟通指引。覆盖违纪解除、协商解除、绩效改进、调岗调薪等场景的逐步操作指南，确保合法合规、合理合情。
  适用人群：HRBP、HR专员、前台/后台管理者。
  触发场景：(1)员工违纪处理与沟通 (2)解除劳动合同沟通 (3)协商解除/劝退谈话 (4)绩效不胜任处理 (5)调岗调薪沟通 (6)员工投诉/申诉处理 (7)劳动仲裁应对准备 (8)员工关系风险预防。
  关键词：ER、员工关系、违纪、解除、辞退、劝退、沟通、谈话、PIP、绩效改进、调岗、调薪、劳动仲裁、合规、红黄线、处罚、N+1、2N、经济补偿、赔偿金。
  不用于：具体案件的合法性终局判断、诉讼代理、法律意见书出具——本 Skill 提供流程与话术框架，不替代专业法律意见。
version: 1
author: huguangqin
license: MIT
tags: [employee-relations, er, termination, pip, hr, compliance, communication]
metadata:
  hermes:
    tags: [employee-relations, er, termination, pip, hr, compliance, communication]
    related_skills: [er-case-analysis, er-legal-monitor, er-risk-assessment]
  source:
    origin: 贝壳整装事业线定制版（员工关系案件沟通指引）
    migrated_from: github.com/huguangqin/ER-case-communication.skill
    note: 提供操作流程与沟通框架，不构成法律意见；具体案件的合法性判断、证据充分性认定与各地裁判口径差异，请以专业法律意见和当地司法实践为准。
---

# ER 案件沟通指引

> 本 Skill 为贝壳整装事业线定制，适用于 HRBP、HR 专员及各级管理者处理员工关系场景。

## 核心原则

1. **合法** — 所有操作必须有法律依据，参见 [references/legal-basis.md](references/legal-basis.md)
2. **合理** — 处罚与违纪程度匹配，避免"小错重罚"
3. **合情** — 尊重员工，沟通有温度，参见 [references/communication-templates.md](references/communication-templates.md)

## 使用方式

当用户描述一个 ER 场景时，按以下流程引导：

### Step 1：识别场景类型

询问或判断属于以下哪类场景，加载对应的详细指引：

| 场景代码 | 场景名称 | 参考文件 |
|---------|---------|---------|
| `A` | 违纪解除（红黄线） | [references/scenario-discipline.md](references/scenario-discipline.md) |
| `B` | 协商解除 / 劝退 | [references/scenario-negotiation.md](references/scenario-negotiation.md) |
| `C` | 绩效不胜任 / PIP | [references/scenario-pip.md](references/scenario-pip.md) |
| `D` | 调岗调薪 | [references/scenario-transfer.md](references/scenario-transfer.md) |
| `E` | 员工投诉 / 申诉 | [references/scenario-complaint.md](references/scenario-complaint.md) |

### Step 2：事实收集与风险评估

对每个场景，首先引导用户收集关键事实：

1. **员工基本信息**：姓名、工号、入职日期、合同期限、岗位、所在城市
2. **事件经过**：时间、地点、具体行为、证人
3. **制度依据**：触犯了哪条制度、制度是否已民主程序+公示签收
4. **历史表现**：既往绩效、是否有过警告/处分记录
5. **特殊情况**：是否在医疗期、孕期、工伤期等法定保护期内

### Step 3：执行合规检查清单

在进入沟通前，逐项核查（参见 [references/legal-basis.md](references/legal-basis.md) 中的完整清单）：

```
□ 制度依据是否经过民主程序（职工代表大会/全体职工讨论）
□ 制度是否已向该员工公示/签收
□ 违纪事实是否有充分证据支撑
□ 处罚力度与违纪情节是否匹配
□ 是否已通知工会（违纪解除必须）
□ 是否存在法定保护期（医疗期/孕期/工伤等）
□ 经济补偿金/赔偿金是否已计算
□ 面谈时间和地点是否合适
□ 是否有第二人在场（HR/法务）
```

**任一不通过 → 暂停，先补正再沟通。**

### Step 4：沟通准备

1. 根据场景类型，从 [references/communication-templates.md](references/communication-templates.md) 选取话术模板
2. 明确沟通目标：通知？协商？取证？
3. 预判员工可能的反应，准备应对方案
4. 确定参与人：建议至少2人（HR + 业务主管）

### Step 5：面谈执行

按所选场景的话术模板执行，遵循：
- 开场建立信任 → 陈述事实 → 说明依据 → 告知决定 → 倾听回应 → 确认后续
- 全程录音/录像需提前告知（部分城市要求双方同意）
- 做好面谈记录，双方签字确认

### Step 6：文书与归档

面谈结束后完成：
1. 相关文书签署（解除通知/协商协议/PIP 计划等）
2. 面谈记录归档
3. 系统状态更新
4. 后续跟进事项记录

## 败诉风险预警

基于整装事业线24-26年实际败诉案例，以下模式**高风险**：

| 风险模式 | 占比 | 典型表现 | 预防措施 |
|---------|------|---------|---------|
| 处罚过重 | 33% | 轻微违纪直接红线解除 | 做处罚适配评估 |
| 证据链断裂 | 25% | 监控视频无原始载体 | 按证据保全SOP操作 |
| 程序瑕疵 | 17% | 未通知工会、未送达 | 走程序核查清单 |
| 管理漏洞 | 25% | 借违纪名义处理非违纪问题 | 区分真实原因 |

详细分析参见 [references/legal-basis.md](references/legal-basis.md)。

## 关键数字速查

- **经济补偿金 N**：工作年限 × 月平均工资（月工资上限为当地社平工资3倍）
- **违法解除赔偿金 2N**：N × 2
- **N 的计算**：每满1年计1个月，6个月以上不满1年按1年计，不满6个月按0.5个月计
- **通知工会**：违纪解除前必须完成，否则程序违法
- **仲裁时效**：劳动争议发生之日起1年内
- **举证责任**：用人单位对解除理由承担举证责任
