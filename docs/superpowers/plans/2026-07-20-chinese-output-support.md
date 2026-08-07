# 中文输出支持 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 yy-spec-review 的审核输出文件中实现中文输出，保持技术标识符和枚举值为英文。

**Architecture:** 在输出模板头部注入 `## 输出语言` 指令块作为中文输出规则的权威来源（Single Source of Truth）。SKILL.md 和 review-orchestrator-protocol.md 引用模板规则而非重复定义。格式验证清单增加语言检查项。index.md 表头中文化。

**Tech Stack:** Markdown 文件编辑（无代码依赖）

## Global Constraints

- 不修改角色文件（roles/*.md）、协议文件（protocols/finding-protocol.md、consolidation-protocol.md、decision-protocol.md）和 CLAUDE.md
- 所有 UPPERCASE_WITH_UNDERSCORE 格式的标识符和枚举值保持英文
- Machine-Readable YAML 索引的 key 和枚举值保持英文
- 模板中的 `## 输出语言` 指令块是中文输出规则的权威来源
- 语言质量问题不触发 INCOMPLETE 状态

---

## File Structure

| 文件 | 操作 | 职责 |
|------|------|------|
| `templates/product-review.md` | Modify | 产品审核输出模板 — 增加 `## 输出语言` 指令块 |
| `templates/system-review.md` | Modify | 系统审核输出模板 — 增加 `## 输出语言` 指令块 |
| `templates/test-review.md` | Modify | 测试审核输出模板 — 增加 `## 输出语言` 指令块 |
| `templates/consolidated-review.md` | Modify | 合并审核输出模板 — 增加 `## 输出语言` 指令块 |
| `templates/index.md` | Modify | 审核索引模板 — 增加 `## 输出语言` 指令块 + 表头中文化 |
| `SKILL.md` | Modify | 技能主定义 — Phase 2 增加 `### Output Language` 段落 |
| `protocols/review-orchestrator-protocol.md` | Modify | 编排协议 — Prompt 模板增加第 6 条约束 + 格式验证清单增加语言检查项 |

---

### Task 1: 三个独立审核模板增加输出语言指令块

**Files:**
- Modify: `templates/product-review.md:1-2`
- Modify: `templates/system-review.md:1-2`
- Modify: `templates/test-review.md:1-2`

**Interfaces:**
- Produces: `## 输出语言` 指令块作为中文输出规则的权威来源，后续 Task 2、3、4 引用此规则

- [ ] **Step 1: 在 product-review.md 顶部插入输出语言指令块**

在 `# Product Review` 标题之后、`## Review Metadata` 之前，插入以下内容：

```markdown

## 输出语言

本审核的所有描述性内容必须使用中文撰写，包括但不限于：

- Finding 标题
- The Gap 等问题描述
- Trigger Scenario 中的场景描述
- Consequence 中的影响分析
- Recommendation 中的建议
- Evidence 中的证据描述
- Assumptions 中的假设说明
- Review Scope、Review Limitations、Reviewer Conclusion 等章节内容
- Unresolved Product Questions 等章节内容

以下内容保持英文：

- Finding ID（PR-001, SC-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_DEFECT, MATERIAL_RISK
  - 置信度：HIGH, MEDIUM, LOW
  - 审核结果：REQUIRES_REVIEW
  - 审核状态：COMPLETED
  - 表格状态：REVIEWED, NOT_APPLICABLE
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 等描述性字段使用中文。
```

- [ ] **Step 2: 在 system-review.md 顶部插入输出语言指令块**

在 `# System Review` 标题之后、`## Review Metadata` 之前，插入以下内容：

```markdown

## 输出语言

本审核的所有描述性内容必须使用中文撰写，包括但不限于：

- Finding 标题
- Risk 等问题描述
- Trigger Condition 中的场景描述
- Consequence 中的影响分析
- Likelihood 中的可能性说明
- Reversibility Analysis 中的可逆性分析
- Operational Impact、Security Impact、Maintenance Impact 等章节内容
- Recommendation 中的建议
- Evidence 中的证据描述
- Assumptions 中的假设说明
- Irreversible Decisions、Over-Engineering and Complexity Risks 等章节内容
- Unresolved System Questions 等章节内容
- Review Limitations、Reviewer Conclusion 等章节内容

以下内容保持英文：

- Finding ID（SC-001, SC-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_DEFECT, MATERIAL_RISK
  - 置信度：HIGH, MEDIUM, LOW
  - 可能性：HIGH, MEDIUM, LOW
  - 可逆性：REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE, UNKNOWN
  - 审核结果：REQUIRES_REVIEW
  - 审核状态：COMPLETED
  - 特殊标记：NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED, NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED
  - 表格状态：REVIEWED, NOT_APPLICABLE
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 等描述性字段使用中文。
```

- [ ] **Step 3: 在 test-review.md 顶部插入输出语言指令块**

在 `# Test Review` 标题之后、`## Review Metadata` 之前，插入以下内容：

```markdown

## 输出语言

本审核的所有描述性内容必须使用中文撰写，包括但不限于：

- Finding 标题
- Verification Gap 等问题描述
- Trigger Scenario 中的场景描述
- Expected Verification 中的验证期望
- Verification Method 中的验证方法
- Consequence 中的影响分析
- Evidence 中的证据描述
- Recommendation 中的建议
- Reviewer Notes 中的备注
- Testability Coverage、Unresolved Verification Questions 等章节内容
- Review Limitations、Reviewer Conclusion 等章节内容

以下内容保持英文：

- Finding ID（TD-001, TD-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_GAP, MATERIAL_RISK
  - 置信度：HIGH, MEDIUM, LOW
  - Finding Type：ACCEPTANCE_TEST, UNTESTABLE_REQUIREMENT, BLIND_SPOT
  - 审核结果：REQUIRES_REVIEW
  - 审核状态：COMPLETED
  - 表格状态：REVIEWED, NOT_APPLICABLE
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 等描述性字段使用中文。
```

- [ ] **Step 4: 验证三个模板的指令块已正确插入**

运行以下命令确认每个模板文件都包含 `## 输出语言` 段落：

```bash
grep -c "## 输出语言" templates/product-review.md templates/system-review.md templates/test-review.md
```

Expected: 每个文件输出 `1`

- [ ] **Step 5: 提交**

```bash
git add templates/product-review.md templates/system-review.md templates/test-review.md
git commit -m "feat: add output language directive to review templates

Add ## 输出语言 section to product-review.md, system-review.md,
and test-review.md templates. This directive instructs LLMs to
write all descriptive content in Chinese while keeping technical
identifiers and enumerated values in English.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: consolidated-review.md 模板增加输出语言指令块

**Files:**
- Modify: `templates/consolidated-review.md:1-2`

**Interfaces:**
- Consumes: `## 输出语言` 指令块模式来自 Task 1
- Produces: 合并审核模板的中文输出规则

- [ ] **Step 1: 在 consolidated-review.md 顶部插入输出语言指令块**

在 `# Consolidated Review` 标题之后、`## Review Metadata` 之前，插入以下内容：

```markdown

## 输出语言

本审核的所有描述性内容必须使用中文撰写，包括但不限于：

- Consolidated Finding 标题
- Underlying Problem 中的问题描述
- Trigger Scenario 中的场景描述
- Consequence 中的影响分析（包括 Business Impact、User Impact 等各维度）
- Reviewer Perspectives 中各视角的评估说明
- Relationship Explanation 中的关系说明
- Conflict Analysis 中的冲突分析
- Recommended Resolution 中的建议
- Consolidator Predispositions 中的偏差说明
- Coverage Gaps 中的覆盖缺口说明
- Superpowers Instructions 中的操作指引
- Decision Queue 中的问题描述和证据摘要
- Consolidation Conclusion 中的总结

以下内容保持英文：

- Finding ID（CR-001, CR-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_DEFECT, MATERIAL_RISK
  - 置信度：HIGH, MEDIUM, LOW
  - 决策状态：PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
  - 关系分类：DUPLICATE, SAME_ROOT_CAUSE, RELATED, INDEPENDENT, CONTRADICTORY, SUBSET, CONSEQUENCE
  - 冲突状态：NO_CONFLICT, MINOR_INTERPRETATION_DIFFERENCE, MATERIAL_CONFLICT, UNRESOLVED_CONFLICT
  - 合并决策：MERGED, KEPT_SEPARATE, DUPLICATE, REQUIRES_CLARIFICATION
  - 审核状态：COMPLETED, AVAILABLE, MISSING
  - 审核结果：REQUIRES_REVIEW
  - 特殊标记：NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED, NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED, NONE_IDENTIFIED
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 和 description 等描述性字段使用中文。
```

- [ ] **Step 2: 验证指令块已正确插入**

```bash
grep -c "## 输出语言" templates/consolidated-review.md
```

Expected: `1`

- [ ] **Step 3: 提交**

```bash
git add templates/consolidated-review.md
git commit -m "feat: add output language directive to consolidated-review template

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: index.md 模板增加输出语言指令块 + 表头中文化

**Files:**
- Modify: `templates/index.md`

**Interfaces:**
- Consumes: `## 输出语言` 指令块模式来自 Task 1

- [ ] **Step 1: 在 index.md 顶部插入输出语言指令块**

在 `# Review Index — <Spec Name>` 标题之后、`## Design Spec` 之前，插入以下内容：

```markdown

## 输出语言

本审核索引的所有描述性内容必须使用中文撰写。

以下内容保持英文：

- CR-ID（CR-001, CR-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 决策状态：PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
  - 跨轮次状态：CARRIED_FORWARD, STILL_OPEN, RESOLVED
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 等描述性字段使用中文。
```

- [ ] **Step 2: 将 Review Rounds 表格表头中文化**

将：

```markdown
| Round | Date | P0 | P1 | P2 | Accepted | Rejected | Deferred | Status |
```

替换为：

```markdown
| 轮次 | 日期 | P0 | P1 | P2 | 已接受 | 已拒绝 | 已延迟 | 状态 |
```

- [ ] **Step 3: 将 Finding Tracking 表格表头中文化**

将：

```markdown
| CR-ID | Round | Severity | Title | Decision | Previous Round CR-ID | Source Reviewers | Status |
```

替换为：

```markdown
| CR-ID | 轮次 | 严重度 | 标题 | 决策 | 前轮 CR-ID | 来源审核员 | 状态 |
```

- [ ] **Step 4: 验证修改正确**

```bash
grep -c "## 输出语言" templates/index.md
grep "轮次" templates/index.md | head -2
```

Expected: 指令块计数为 `1`，且两行表格表头都包含 "轮次"

- [ ] **Step 5: 提交**

```bash
git add templates/index.md
git commit -m "feat: add output language directive and localize table headers in index template

Add ## 输出语言 section and translate table headers to Chinese:
Round→轮次, Date→日期, Accepted→已接受, Rejected→已拒绝,
Deferred→已延迟, Status→状态, Severity→严重度, Title→标题,
Decision→决策, Source Reviewers→来源审核员,
Previous Round CR-ID→前轮 CR-ID.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: SKILL.md 增加 Output Language 段落

**Files:**
- Modify: `SKILL.md`

**Interfaces:**
- Consumes: 引用 Task 1-3 中模板定义的输出语言规则

- [ ] **Step 1: 在 Phase 2 中插入 Output Language 段落**

在 `SKILL.md` 的 `## Phase 2: Independent Reviews` 章节中，找到 `### After Subagents Complete` 小节，在其之前插入：

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

- [ ] **Step 2: 验证段落已正确插入**

```bash
grep -c "### Output Language" SKILL.md
```

Expected: `1`

- [ ] **Step 3: 提交**

```bash
git add SKILL.md
git commit -m "feat: add Output Language section to SKILL.md Phase 2

References the output language rules defined in templates rather
than duplicating them, following the Single Source of Truth principle.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: review-orchestrator-protocol.md 增加 Prompt 中文约束 + 格式验证清单更新

**Files:**
- Modify: `protocols/review-orchestrator-protocol.md`

**Interfaces:**
- Consumes: 引用 Task 1-3 中模板定义的输出语言规则
- Produces: 格式验证清单的语言检查项，供 Phase 2 After Subagents Complete 使用

- [ ] **Step 1: 在 Section 2 的 Critical Constraints 列表增加第 6 条**

找到 `protocols/review-orchestrator-protocol.md` 中 Section 2 的标准化 prompt 模板，在现有 5 条 Critical Constraints 之后增加第 6 条：

将：

```markdown
5. You must include the Machine-Readable Finding Index at the end
```

替换为：

```markdown
5. You must include the Machine-Readable Finding Index at the end
6. You must follow the output language rules defined in the
   output template. All descriptive content must be written
   in Chinese (中文). All UPPERCASE_WITH_UNDERSCORE identifiers
   must remain in English.
```

- [ ] **Step 2: 在 Section 4 的格式验证清单增加语言检查项**

找到 `protocols/review-orchestrator-protocol.md` 中 Section 4 的 Format Validation Checklist，在现有检查项之后增加三项：

将：

```markdown
- [ ] Machine-Readable Index is present and parseable
```

替换为：

```markdown
- [ ] Machine-Readable Index is present and parseable
- [ ] Descriptive content is written in Chinese (Finding titles, problem descriptions, scenarios, consequences, recommendations, evidence, etc.)
- [ ] YAML index enum values match protocol-defined allowed values (UPPERCASE_WITH_UNDERSCORE format)
- [ ] YAML index descriptive fields (title, description, etc.) are written in Chinese
```

- [ ] **Step 3: 在 Section 4 的 Retry Mechanism 之后增加语言验证失败处理**

找到 Section 4 中 `### Retry Mechanism` 段落之后，在 `### MISSING Hard Rule` 之前，插入：

```markdown
### Language Validation Failure

If format validation finds language issues:

1. Allow one retry: dispatch the same subagent again with the same prompt
2. If the retry also fails language validation, proceed with the output
3. Record the language quality issue in the review output's Review Limitations section
4. Language quality issues do NOT trigger INCOMPLETE status

```

- [ ] **Step 4: 验证修改正确**

```bash
grep -c "Chinese" protocols/review-orchestrator-protocol.md
grep -c "语言" protocols/review-orchestrator-protocol.md
```

Expected: 至少各 `1` 处

- [ ] **Step 5: 提交**

```bash
git add protocols/review-orchestrator-protocol.md
git commit -m "feat: add Chinese output constraint to subagent prompt and validation checklist

- Add Critical Constraint #6 requiring Chinese output per template rules
- Add 3 language validation items to format validation checklist
- Add language validation failure handling section

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: 端到端验证

**Files:**
- No file changes (verification only)

**Interfaces:**
- Consumes: 所有前序 Task 的改动

- [ ] **Step 1: 验证所有模板文件包含输出语言指令块**

```bash
for f in templates/product-review.md templates/system-review.md templates/test-review.md templates/consolidated-review.md templates/index.md; do
  count=$(grep -c "## 输出语言" "$f")
  echo "$f: $count"
done
```

Expected: 每个文件输出 `1`

- [ ] **Step 2: 验证 SKILL.md 包含 Output Language 段落**

```bash
grep -c "### Output Language" SKILL.md
```

Expected: `1`

- [ ] **Step 3: 验证 review-orchestrator-protocol.md 包含 Prompt 约束和格式验证更新**

```bash
grep -c "Chinese" protocols/review-orchestrator-protocol.md
grep -c "UPPERCASE_WITH_UNDERSCORE" protocols/review-orchestrator-protocol.md
```

Expected: 至少各 `1` 处

- [ ] **Step 4: 验证 index.md 表头已中文化**

```bash
grep "轮次" templates/index.md | head -2
```

Expected: 两行表格表头都包含 "轮次"

- [ ] **Step 5: 验证角色文件和核心协议文件未被修改**

```bash
git diff HEAD~5 -- roles/ protocols/finding-protocol.md protocols/consolidation-protocol.md protocols/decision-protocol.md CLAUDE.md
```

Expected: 无输出（这些文件未被修改）

- [ ] **Step 6: 确认所有改动已提交**

```bash
git status
```

Expected: `nothing to commit, working tree clean`
