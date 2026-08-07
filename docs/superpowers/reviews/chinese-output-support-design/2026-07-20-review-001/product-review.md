# 产品审核

## 审核元数据

### 审核 ID

PR-2026-07-20-001

### 审核员

yy-product-reviewer

### 审核类型

PRODUCT_REVIEW

### 设计规格

docs/superpowers/specs/2026-07-20-chinese-output-support-design.md

### 审核日期

2026-07-20

### 审核状态

COMPLETED

---

## 审核范围

本次审核从产品正确性、业务规则完整性、用户行为、工作流完整性和操作可用性角度评估该设计规格。

本次审核不评估：
* 实现质量
* 源代码质量
* 详细系统架构
* 技术选型
* 基础设施设计
* 性能优化
* 测试实现细节

本次审核的目的是识别产品层面的需求模糊、不完整、矛盾、不安全或定义不足的问题。

---

## 发现

### PR-001 — 中文输出指令对 LLM 的约束力未验证

#### 严重度

P1

#### 证据等级

MATERIAL_RISK

#### 置信度

MEDIUM

#### 位置

设计规格 § 改动清单 → 1. 输出模板增加输出语言指令块

#### 差距

设计规格假设在模板头部增加 `## 输出语言` 指令块后，LLM 会可靠地遵循中文输出要求。但规格未定义：当 LLM 未遵循该指令（即输出中包含英文描述性内容）时的检测和处理机制。

这是一个产品层面的行为完整性问题：规格定义了"期望行为"（中文输出），但未定义"异常行为"（英文泄漏）的处理方式。

#### 触发场景

1. 用户运行 yy-spec-review 对一个规格进行审核
2. Subagent 接收到包含中文输出指令的模板
3. LLM 在生成 Finding 时，部分描述性内容使用了英文（例如 Finding 标题写为 "Retry Amplification Risk" 而非 "重试放大风险"）
4. 审核输出文件中混入英文描述性内容
5. 规格未定义此情况下应如何处理——是接受、重试、还是标记为质量缺陷

#### 后果

* 中文团队收到的审核报告中混入英文内容，降低可读性
* 不同次审核的输出语言一致性无法保证
* 用户对审核结果的信任度可能降低

#### 建议

定义中文输出质量检查机制，至少包括：
* 在 Phase 2 的格式验证清单中增加"描述性内容是否使用中文"的检查项
* 定义检查失败时的处理方式（允许重试或标记为质量警告）

#### 证据

设计规格 § 改动清单 → 1 和 § 风险与缓解中提到"LLM 偶尔输出英文描述"作为风险，但仅以"三层约束降低概率"作为缓解，未定义检测和处理机制。

#### 假设

* INFERRED — LLM 对中文输出指令的遵循度不是 100%，这是基于 LLM 行为的普遍观察

#### 来源引用

* 设计规格 § 改动清单 → 1. 输出模板增加输出语言指令块
* 设计规格 § 风险与缓解 → "LLM 偶尔输出英文描述"

---

### PR-002 — 枚举值保持英文的范围可能不完整

#### 严重度

P2

#### 证据等级

MATERIAL_RISK

#### 置信度

MEDIUM

#### 位置

设计规格 § 改动清单 → 1. 输出模板增加输出语言指令块 → "以下内容保持英文"

#### 差距

指令块中列出的"保持英文"的枚举值列表可能不完整。例如：
* `REQUIRES_REVIEW`（审核结果枚举，出现在模板的 Review Result 中）
* `COMPLETED`（审核状态枚举）
* `AVAILABLE` / `MISSING`（源审核状态）
* `MERGED` / `KEPT_SEPARATE` / `REQUIRES_CLARIFICATION`（合并决策枚举）
* `NO_CONFLICT` / `MINOR_INTERPRETATION_DIFFERENCE` / `MATERIAL_CONFLICT` / `UNRESOLVED_CONFLICT`（冲突状态枚举）
* `NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED` / `NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED`（特殊标记）
* `NONE_IDENTIFIED`（影响类别标记）
* `CARRIED_FORWARD` / `STILL_OPEN` / `RESOLVED`（跨轮次状态枚举）

这些枚举值在模板中出现但未被列入"保持英文"的列表中。

#### 触发场景

1. LLM 生成审核输出
2. 遇到未在"保持英文"列表中明确列出的枚举值（如 REQUIRES_REVIEW）
3. LLM 可能将其翻译为中文（如 "需要审核"）
4. 导致 Machine-Readable YAML 索引中的枚举值不一致，影响自动化解析

#### 后果

* YAML 索引中可能出现中文枚举值，破坏自动化工具的解析
* 跨轮次追溯可能因枚举值不一致而中断

#### 建议

在指令块的"保持英文"列表中补充所有遗漏的枚举值，或使用通配规则如"所有大写下划线格式的枚举值保持英文"。

#### 证据

设计规格 § 改动清单 → 1 中列出了部分枚举值，但对照 `templates/consolidated-review.md` 和 `templates/index.md` 中的实际枚举值，存在遗漏。

#### 假设

* CONFIRMED — 通过对比模板文件中的实际枚举值确认了遗漏

#### 来源引用

* 设计规格 § 改动清单 → 1. 输出模板增加输出语言指令块
* templates/consolidated-review.md 中的枚举值
* templates/index.md 中的跨轮次状态枚举

---

### PR-003 — index.md 表头中文化后与 YAML 索引的字段对应关系未明确

#### 严重度

P2

#### 证据等级

MATERIAL_RISK

#### 置信度

LOW

#### 位置

设计规格 § 改动清单 → 4. index.md 模板表头中文化

#### 差距

设计规格定义了 index.md 表头的中文化映射（如 Round → 轮次），但未明确说明中文化后的表头与 Machine-Readable YAML 索引中字段的对应关系。虽然 YAML key 保持英文，但读者可能需要知道"轮次"对应 YAML 中的 `round`。

#### 触发场景

1. 审核完成后生成 index.md
2. 表头使用中文（轮次、日期、状态等）
3. YAML 索引使用英文 key（round, date, status 等）
4. 自动化工具或人工阅读者需要从中文表头映射到 YAML key，但无明确对应关系定义

#### 后果

* 中英文表头与 YAML key 的映射关系需要读者自行推断
* 自动化工具如果依赖表头名称解析，可能因中文化而失败

#### 建议

此为低风险问题。可以在 index.md 模板中增加注释说明表头与 YAML key 的对应关系，或接受当前设计（YAML 索引本身就是机器可读的，不需要从表头映射）。

#### 证据

设计规格 § 改动清单 → 4 定义了表头中文化映射，但未讨论与 YAML 索引的对应关系。

#### 假设

* INFERRED — 自动化工具通常直接解析 YAML 索引而非 Markdown 表头，因此实际影响可能较小

#### 来源引用

* 设计规格 § 改动清单 → 4. index.md 模板表头中文化

---

## 发现汇总

| 发现 ID | 严重度 | 证据等级 | 置信度 | 简述 |
| ------- | ------ | -------- | ------ | ---- |
| PR-001 | P1 | MATERIAL_RISK | MEDIUM | 中文输出指令对 LLM 的约束力未验证 |
| PR-002 | P2 | MATERIAL_RISK | MEDIUM | 枚举值保持英文的范围可能不完整 |
| PR-003 | P2 | MATERIAL_RISK | LOW | index.md 表头中文化后与 YAML 索引对应关系未明确 |

---

## 产品风险覆盖

| 风险维度 | 状态 | 发现 ID |
| -------- | ---- | ------- |
| 状态机漏洞 | NOT_APPLICABLE | — |
| 硬边界和限制 | REVIEWED | PR-002 |
| 数据生命周期 | NOT_APPLICABLE | — |
| 向后兼容性 | REVIEWED | PR-003 |
| 隐含假设 | REVIEWED | PR-001 |
| 业务规则冲突 | NOT_APPLICABLE | — |
| 时间一致性 | NOT_APPLICABLE | — |
| 用户工作流完整性 | REVIEWED | PR-001 |
| 管理可操作性 | NOT_APPLICABLE | — |
| 滥用和误用场景 | NOT_APPLICABLE | — |

---

## 未解决的产品问题

无

---

## 审核限制

* 未实际测试 LLM 对中文输出指令的遵循度
* 枚举值遗漏的完整性基于人工对比，可能仍有遗漏

---

## 审核员结论

### 关键发现计数

* P0: 0
* P1: 1
* P2: 2

### 审核结果

REQUIRES_REVIEW

本次审核识别了产品层面的差距，需要合并阶段考虑。

产品审核员不决定发现最终是被接受、拒绝、延迟还是其他处置。

最终处置由决策协议决定。

---

## 机器可读发现索引

```yaml
review:
  review_id: "PR-2026-07-20-001"
  reviewer: "yy-product-reviewer"
  review_type: "PRODUCT_REVIEW"
  status: "COMPLETED"

findings:
  - id: "PR-001"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "中文输出指令对 LLM 的约束力未验证"
    location: "改动清单 → 1. 输出模板增加输出语言指令块"
    source_references:
      - "设计规格 § 改动清单 → 1"
      - "设计规格 § 风险与缓解"
    risk_dimensions:
      - "隐含假设"
      - "用户工作流完整性"
    status: "PENDING_DECISION"

  - id: "PR-002"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "枚举值保持英文的范围可能不完整"
    location: "改动清单 → 1. 输出模板增加输出语言指令块"
    source_references:
      - "设计规格 § 改动清单 → 1"
      - "templates/consolidated-review.md"
      - "templates/index.md"
    risk_dimensions:
      - "硬边界和限制"
    status: "PENDING_DECISION"

  - id: "PR-003"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "LOW"
    title: "index.md 表头中文化后与 YAML 索引对应关系未明确"
    location: "改动清单 → 4. index.md 模板表头中文化"
    source_references:
      - "设计规格 § 改动清单 → 4"
    risk_dimensions:
      - "向后兼容性"
    status: "PENDING_DECISION"

open_questions: []
```
