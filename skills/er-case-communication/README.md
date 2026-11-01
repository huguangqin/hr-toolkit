# er-case-communication —— 员工关系（ER）案件沟通指引 Skill

员工关系案件全流程沟通指引 Skill。覆盖**违纪解除、协商解除/劝退、绩效改进（PIP）、调岗调薪、员工投诉**五大场景，每个场景都有完整的分步操作流程、话术模板与检查清单。

> 初版基于某业务线定制实践，适用于 HRBP、HR 专员及各级管理者处理员工关系场景。

## 三步合规底线

1. **合法** —— 有法律依据（见 `references/legal-basis.md`）
2. **合理** —— 处罚与违纪程度匹配，避免"小错重罚"（见 `references/case-assessment.md`）
3. **合情** —— 尊重员工、沟通有温度（见 `references/communication-templates.md`）

## 五大场景

| 场景 | 说明 | 文件 |
|---|---|---|
| A 违纪解除 | 红黄线违纪处理与谈话 | `references/scenario-discipline.md` |
| B 协商解除 / 劝退 | 协商解除沟通与谈判 | `references/scenario-negotiation.md` |
| C 绩效不胜任 / PIP | 绩效改进计划启动与沟通 | `references/scenario-pip.md` |
| D 调岗调薪 | 调岗调薪沟通 | `references/scenario-transfer.md` |
| E 员工投诉 / 申诉 | 投诉受理与处理 | `references/scenario-complaint.md` |

## 结合败诉案例的实战经验

- **处罚过重（33%）** → 内置「处罚适配评估矩阵」，8 个维度逐项打分
- **证据链断裂（25%）** → 内置证据保全 SOP，按证据类型明确保全要求
- **程序瑕疵（17%）** → 内置程序合规核查清单，逐项打勾
- **管理漏洞（25%）** → 明确区分真实违纪 vs 借名处理

## 文件结构

```
er-case-communication/
├── SKILL.md                          # 核心流程与入口
└── references/
    ├── legal-basis.md                # 法律依据与败诉风险防控
    ├── case-assessment.md            # 案件评估框架与处罚适配矩阵
    ├── communication-templates.md    # 各场景沟通话术模板
    ├── scenario-discipline.md        # 场景A：违纪解除（红黄线）
    ├── scenario-negotiation.md       # 场景B：协商解除 / 劝退
    ├── scenario-pip.md               # 场景C：绩效不胜任 / PIP
    ├── scenario-transfer.md          # 场景D：调岗调薪
    └── scenario-complaint.md         # 场景E：员工投诉 / 申诉
```

## 安装

### WorkBuddy

```bash
cp -r er-case-communication ~/.workbuddy/skills/
```

Windows：`C:\Users\<用户名>\.workbuddy\skills\`

### Hermes

```bash
cp -r er-case-communication ~/.hermes/skills/
```

## 触发词

ER / 员工关系 / 违纪 / 解除 / 辞退 / 劝退 / 沟通 / 谈话 / PIP / 绩效改进 / 调岗 / 调薪 / 劳动仲裁

## 边界与免责

本 Skill 提供的是**操作流程与沟通框架**，**不构成法律意见**。具体案件的合法性判断、证据充分性认定，以及各地裁判口径差异，请以专业法律意见和当地司法实践为准。

## License

MIT
