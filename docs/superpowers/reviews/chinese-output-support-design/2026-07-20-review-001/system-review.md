# 系统审核

## 审核元数据

### 审核 ID

SC-2026-07-20-001

### 审核员

yy-system-critic

### 审核类型

SYSTEM_REVIEW

### 设计规格

docs/superpowers/specs/2026-07-20-chinese-output-support-design.md

### 审核日期

2026-07-20

### 审核状态

COMPLETED

---

## 审核范围

本次审核从系统可靠性、安全性、数据完整性、操作弹性、架构复杂度、可逆性和长期可维护性角度评估该设计规格。

本次审核不：
* 重新设计系统
* 产出实现计划
* 审核源代码风格
* 优化实现细节
* 做出最终批准决定
* 替代详细安全测试或生产验证

---

## 发现

### SC-001 — 中文输出指令与现有格式验证清单的交互未定义

#### 严重度

P1

#### 证据等级

MATERIAL_RISK

#### 置信度

HIGH

#### 位置

设计规格 § 改动清单 → 1. 输出模板增加输出语言指令块；对比 protocols/review-orchestrator-protocol.md § 4 格式验证清单

#### 风险

设计规格在模板中增加了中文输出指令，但未更新 `review-orchestrator-protocol.md` 中的格式验证清单（Format Validation Checklist）。现有验证清单检查的是结构完整性（Review ID 存在、Finding ID 格式正确等），但不检查内容语言。

如果中文输出指令导致 LLM 将枚举值意外翻译为中文（如将 `CONFIRMED_DEFECT` 写为 `已确认缺陷`），现有验证清单不会捕获此错误，因为清单只检查"字段是否存在"，不检查"字段值是否在允许的枚举范围内"。

#### 触发条件

1. Subagent 生成审核输出
2. LLM 将某个枚举值翻译为中文（如 Evidence Class 写为 "已确认缺陷"）
3. 格式验证清单检查通过（因为字段存在且非空）
4. 合并阶段尝试解析该枚举值时失败
5. 或 Machine-Readable YAML 索引中的枚举值与协议定义不一致

#### 后果

* 合并阶段可能因无法识别中文枚举值而产生错误
* YAML 索引的自动化解析可能失败
* 完整性校验可能因枚举值不匹配而误报

#### 可能性

MEDIUM

中文枚举值泄漏的可能性取决于 LLM 对指令的遵循度。Claude 对此类指令的遵循度通常较高，但在复杂输出中偶尔遗漏是有可能的。

#### 可逆性

REVERSIBLE

发现后可以手动修正输出文件中的枚举值。

#### 建议

在格式验证清单中增加枚举值范围检查，或至少增加一条"描述性内容是否使用中文、枚举值是否保持英文"的检查项。

#### 证据

`protocols/review-orchestrator-protocol.md` § 4 中的格式验证清单仅检查结构完整性，不检查值域。

#### 假设

* CONFIRMED — 格式验证清单的内容可通过阅读协议文件确认
* INFERRED — LLM 偶尔将枚举值翻译为中文是基于 LLM 行为的普遍观察

#### 可逆性分析

* 输出文件中的枚举值错误可以手动修正
* 不涉及不可逆的数据变更
* 修正后重新运行完整性校验即可

#### 操作影响

* 需要人工检查和修正输出文件
* 可能延迟审核完成时间

#### 安全影响

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### 维护影响

* 如果格式验证清单不更新，每次审核都需要人工检查语言一致性
* 长期来看增加了操作负担

#### 来源引用

* protocols/review-orchestrator-protocol.md § 4
* 设计规格 § 改动清单 → 1

---

### SC-002 — 三层中文约束的冗余性增加维护成本

#### 严重度

P2

#### 证据等级

MATERIAL_RISK

#### 置信度

HIGH

#### 位置

设计规格 § 改动清单 → 1, 2, 3

#### 风险

设计规格在三个位置定义了中文输出规则：
1. 模板头部的 `## 输出语言` 指令块
2. SKILL.md 的 `### Output Language` 段落
3. review-orchestrator-protocol.md 的 Prompt Critical Constraints 第 6 条

这三处规则的内容需要保持同步。如果将来修改中文输出的范围（例如增加或删除一个需要保持英文的枚举值），必须同时更新三处，否则会出现不一致。

#### 触发条件

1. 需要修改中文输出规则（例如新增一个枚举值）
2. 开发者只更新了模板中的指令块
3. SKILL.md 和 review-orchestrator-protocol.md 中的规则未同步更新
4. Subagent 收到的 Prompt 约束与模板指令不一致
5. LLM 可能遵循 Prompt 约束而非模板指令，或反之

#### 后果

* 三处规则不一致时，LLM 的行为不可预测
* 维护时容易遗漏某一处

#### 可能性

MEDIUM

多位置同步维护是常见的维护风险。

#### 可逆性

REVERSIBLE

不一致可以修正，但需要发现不一致的位置。

#### 建议

考虑将中文输出规则定义为单一来源（Single Source of Truth），例如：
* 仅在模板中定义完整规则，SKILL.md 和 protocol 中引用模板
* 或在 SKILL.md 中定义规则，模板和 protocol 中引用

#### 证据

设计规格 § 改动清单 → 1, 2, 3 分别定义了三处规则，内容有重叠但不完全相同。

#### 假设

* CONFIRMED — 三处规则的存在和内容可通过阅读规格确认

#### 可逆性分析

* 规则不一致可以修正
* 不涉及数据变更

#### 操作影响

* 维护时需要检查三处规则的一致性

#### 安全影响

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### 维护影响

* 三处规则的同步维护增加了长期维护成本
* 如果规则演进频繁，不一致的风险会随时间增加

#### 来源引用

* 设计规格 § 改动清单 → 1, 2, 3

---

## 发现汇总

| 发现 ID | 严重度 | 证据等级 | 置信度 | 可能性 | 可逆性 | 简述 |
| ------- | ------ | -------- | ------ | ------ | ------ | ---- |
| SC-001 | P1 | MATERIAL_RISK | HIGH | MEDIUM | REVERSIBLE | 中文输出指令与格式验证清单的交互未定义 |
| SC-002 | P2 | MATERIAL_RISK | HIGH | MEDIUM | REVERSIBLE | 三层中文约束的冗余性增加维护成本 |

---

## 系统风险覆盖

| 风险维度 | 状态 | 发现 ID |
| -------- | ---- | ------- |
| 数据完整性和一致性 | REVIEWED | SC-001 |
| 安全边界 | NOT_APPLICABLE | — |
| 认证和授权 | NOT_APPLICABLE | — |
| 可用性和弹性 | NOT_APPLICABLE | — |
| 故障恢复 | NOT_APPLICABLE | — |
| 外部依赖 | NOT_APPLICABLE | — |
| 并发和竞态条件 | NOT_APPLICABLE | — |
| 数据生命周期和迁移 | NOT_APPLICABLE | — |
| 向后兼容性 | NOT_APPLICABLE | — |
| 操作复杂度 | REVIEWED | SC-001 |
| 维护负担 | REVIEWED | SC-002 |
| 不可逆决策 | NOT_APPLICABLE | — |
| 过度工程 | REVIEWED | SC-002 |
| 可观测性和诊断 | NOT_APPLICABLE | — |

---

## 不可逆决策

无

---

## 过度工程和复杂度风险

### OC-001 — 三层中文约束

#### 复杂度

在三个位置（模板、SKILL.md、protocol）定义相同的中文输出规则，增加了同步维护的复杂度。

#### 证据

三处规则内容有重叠，但措辞和详细程度不同。维护时需要确保三处一致。

#### 简化机会

将中文输出规则集中到单一来源（如模板），其他位置引用而非重复定义。

#### 保留复杂度的风险

维护时遗漏某一处更新，导致规则不一致。

#### 置信度

HIGH

#### 状态

OPEN

---

## 未解决的系统问题

无

---

## 审核限制

* 未实际测试中文输出指令对 LLM 行为的影响
* 维护成本评估基于经验推断

---

## 审核员结论

### 关键发现计数

* P0: 0
* P1: 1
* P2: 1

### 风险汇总

* 安全风险: 0
* 数据完整性风险: 0
* 可用性和弹性风险: 0
* 操作风险: 1
* 维护风险: 1
* 不可逆决策: 0
* 过度工程风险: 1

### 审核结果

REQUIRES_REVIEW

本次审核识别了系统层面的风险，需要合并阶段考虑。

系统审核员不决定发现最终是被接受、拒绝、延迟还是其他处置。

最终处置由决策协议决定。

---

## 机器可读发现索引

```yaml
review:
  review_id: "SC-2026-07-20-001"
  reviewer: "yy-system-critic"
  review_type: "SYSTEM_REVIEW"
  status: "COMPLETED"

findings:
  - id: "SC-001"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "中文输出指令与格式验证清单的交互未定义"
    location: "改动清单 → 1; review-orchestrator-protocol.md § 4"
    likelihood: "MEDIUM"
    reversibility: "REVERSIBLE"
    source_references:
      - "protocols/review-orchestrator-protocol.md § 4"
      - "设计规格 § 改动清单 → 1"
    risk_dimensions:
      - "数据完整性和一致性"
      - "操作复杂度"
    status: "PENDING_DECISION"

  - id: "SC-002"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "三层中文约束的冗余性增加维护成本"
    location: "改动清单 → 1, 2, 3"
    likelihood: "MEDIUM"
    reversibility: "REVERSIBLE"
    source_references:
      - "设计规格 § 改动清单 → 1, 2, 3"
    risk_dimensions:
      - "维护负担"
      - "过度工程"
    status: "PENDING_DECISION"

irreversible_decisions: []

complexity_risks:
  - id: "OC-001"
    status: "OPEN"
    title: "三层中文约束"

open_questions: []
```
