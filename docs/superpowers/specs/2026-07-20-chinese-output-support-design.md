# Design Spec: yy-spec-review 中文输出支持

## 问题陈述

yy-spec-review 技能当前的所有审核输出文件均使用英文撰写。对于中文团队来说，英文审核报告增加了阅读和理解成本，降低了审核结果的可操作性。

需要一种方式，使审核输出文件中的描述性内容使用中文，同时保持技术标识符和枚举值的英文不变，以确保与自动化工具和协议的兼容性。

## 期望结果

- 审核输出文件（product-review.md、system-review.md、test-review.md、consolidated-review.md、index.md）中的所有描述性内容使用中文撰写
- 技术标识符（Finding ID、严重度枚举、证据等级枚举等）保持英文
- Machine-Readable YAML 索引的 key 和枚举值保持英文，描述性字段使用中文
- 协议文件和角色定义文件不做改动，保持英文以确保 LLM 指令遵循度
- 改动范围最小化，仅在输出层增加中文约束

## 设计方案：模板头部注入中文输出指令

### 核心思路

在输出模板和调度指令中增加明确的中文输出规则，利用 LLM 对指令的遵循能力实现中文输出，而不需要改动协议/角色等指令性文件。

### 改动清单

#### 1. 输出模板增加输出语言指令块

在以下 5 个模板文件的顶部（Review Metadata 章节之前）增加 `## 输出语言` 指令块：

- `templates/product-review.md`
- `templates/system-review.md`
- `templates/test-review.md`
- `templates/consolidated-review.md`
- `templates/index.md`

指令块内容：

```markdown
## 输出语言

本审核的所有描述性内容必须使用中文撰写，包括但不限于：

- Finding 标题
- The Gap / Risk / Verification Gap 等问题描述
- Trigger Scenario / Trigger Condition 中的场景描述
- Consequence 中的影响分析
- Recommendation / Recommended Resolution 中的建议
- Evidence 中的证据描述
- Assumptions 中的假设说明
- Review Scope、Review Limitations、Reviewer Conclusion 等章节内容
- Unresolved Questions、Irreversible Decisions 等章节内容
- Consolidator Predispositions 中的偏差说明
- Superpowers Instructions 中的操作指引

以下内容保持英文：

- Finding ID（PR-001, SC-001, TD-001, CR-001）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_DEFECT, MATERIAL_RISK, CONFIRMED_GAP
  - 置信度：HIGH, MEDIUM, LOW
  - 决策状态：PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
  - Finding Type：ACCEPTANCE_TEST, UNTESTABLE_REQUIREMENT, BLIND_SPOT
  - 关系分类：DUPLICATE, SAME_ROOT_CAUSE, RELATED, INDEPENDENT, CONTRADICTORY, SUBSET, CONSEQUENCE
  - 可逆性：REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE, UNKNOWN
  - 审核结果：REQUIRES_REVIEW, COMPLETED
  - 审核状态：AVAILABLE, MISSING
  - 合并决策：MERGED, KEPT_SEPARATE, DUPLICATE, REQUIRES_CLARIFICATION
  - 冲突状态：NO_CONFLICT, MINOR_INTERPRETATION_DIFFERENCE, MATERIAL_CONFLICT, UNRESOLVED_CONFLICT
  - 特殊标记：NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED, NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED, NONE_IDENTIFIED
  - 跨轮次状态：CARRIED_FORWARD, STILL_OPEN, RESOLVED
  - 表格状态：REVIEWED, NOT_APPLICABLE
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 和 description 等描述性字段使用中文。
```

#### 1a. 中文输出验证标准

为使中文输出要求可客观验证，定义以下最小验证标准：

1. **Finding 标题**：必须包含至少一个中文字符。允许技术术语保留英文（如 "Retry 放大风险"）。
2. **描述性段落**：必须以中文为主语言。允许技术术语保留英文，但应在首次出现时提供中文对照或上下文足以推断含义。
3. **枚举值**：所有大写下划线格式的标识符（如 `CONFIRMED_DEFECT`、`REQUIRES_REVIEW`、`NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED`）必须保持英文，不得翻译。
4. **YAML 索引**：key 和枚举值保持英文；`title`、`description` 等描述性字段使用中文。

#### 1b. 格式验证清单更新

在 `protocols/review-orchestrator-protocol.md` § 4 的格式验证清单中增加以下检查项：

- [ ] 描述性内容是否以中文撰写（Finding 标题、问题描述、场景、后果、建议等）
- [ ] YAML 索引中的枚举值是否与协议定义一致（英文大写下划线格式）
- [ ] YAML 索引中的描述性字段（title、description 等）是否使用中文

#### 1c. 验证失败处理

如果格式验证发现语言问题：

1. 允许一次重试：重新调度该 subagent
2. 如果重试仍失败，在审核输出的 Review Limitations 中记录语言质量问题
3. 语言质量问题不影响审核完整性（不触发 INCOMPLETE 状态）

---

#### 2. SKILL.md 增加 Output Language 段落

在 SKILL.md 的 **Phase 2: Independent Reviews** 章节，在 "After Subagents Complete" 小节之前增加：

```markdown
### Output Language

All review output files must be written in Chinese (中文).
Follow the detailed output language rules defined in the output templates.

The following must remain in English:

- Finding IDs (PR-001, SC-001, TD-001, CR-001)
- All UPPERCASE_WITH_UNDERSCORE identifiers (enumerated values, status codes, etc.)
- Machine-Readable YAML keys and enum values
- Technical identifiers and file paths

All descriptive content — titles, problem descriptions, scenarios, consequences, recommendations, evidence, and narrative sections — must be written in Chinese.
```

#### 3. review-orchestrator-protocol.md 增加 Prompt 中文输出约束

在 `protocols/review-orchestrator-protocol.md` 的 Section 2 Subagent Prompt Construction 的标准化 prompt 模板中，Critical Constraints 列表增加第 6 条：

```markdown
6. You must follow the output language rules defined in the
   output template. All descriptive content must be written
   in Chinese (中文). All UPPERCASE_WITH_UNDERSCORE identifiers
   must remain in English.
```

#### 4. index.md 模板表头中文化

`templates/index.md` 中 Review Rounds 表格和 Finding Tracking 表格的表头改为中文：

| 当前英文表头 | 改为中文 |
|------------|---------|
| Round | 轮次 |
| Date | 日期 |
| Accepted | 已接受 |
| Rejected | 已拒绝 |
| Deferred | 已延迟 |
| Status | 状态 |
| Severity | 严重度 |
| Title | 标题 |
| Decision | 决策 |
| Source Reviewers | 来源审核员 |
| Previous Round CR-ID | 前轮 CR-ID |

P0, P1, P2 和 CR-ID 保持不变（枚举值/标识符）。

YAML 索引部分 key 保持英文不变。

### 不改动的文件

以下文件不做改动，保持英文：

- `roles/product-reviewer.md`
- `roles/system-critic.md`
- `roles/test-designer.md`
- `protocols/finding-protocol.md`
- `protocols/consolidation-protocol.md`
- `protocols/decision-protocol.md`
- `CLAUDE.md`

### 改动影响分析

- **对 LLM 指令遵循度的影响**：最小化。角色定义和协议文件的英文指令精度不受影响。中文输出规则仅在输出模板和调度 prompt 中注入。
- **对自动化工具的影响**：无。YAML key 和枚举值保持英文，自动化解析不受影响。
- **对跨轮次追溯的影响**：无。Finding ID 和 CR-ID 保持英文格式，跨轮次链接不受影响。
- **对 subagent 上下文隔离的影响**：无。中文输出规则通过 prompt 模板传递，不涉及上下文共享。

### 风险与缓解

| 风险 | 缓解措施 | 决策 |
|------|---------|------|
| LLM 偶尔输出英文描述 | 三层约束（模板指令块 + SKILL.md 规则 + Prompt 约束）降低概率 | CR-001 ACCEPTED：增加验证标准和格式验证清单 |
| 枚举值被意外中文化 | 指令块明确列出所有保持英文的枚举值 + 通配规则 | CR-002 ACCEPTED：补充枚举值列表并增加通配规则 |
| 三处规则同步维护风险 | 集中到模板为权威来源，其他位置引用 | CR-003 ACCEPTED：SKILL.md 和 protocol 引用模板 |
| index.md 表头中文化后 YAML 索引不一致 | YAML 索引 key 保持英文，与表头中文化独立 | CR-004 REJECTED：YAML 索引本身是机器可读的，无需对应关系 |
| 中文输出质量不如英文 | 可接受——中文团队阅读效率提升远大于潜在的表达精度降低 | — |
