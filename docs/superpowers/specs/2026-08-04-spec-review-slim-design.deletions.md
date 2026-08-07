# 删除项清单（方案 B 实现跟踪）

| 文件 | 删除段落/语句 | 类型(约束/禁止/数量上限/说明) | 删除理由 | 是否影响质量约束 |
|---|---|---|---|---|
| roles/product-reviewer.md | # Independence Requirement (独立评审/不读他人产出规则) | 约束 | 抽至 references/common.md §4 | 否 |
| roles/product-reviewer.md | # Evidence Classification (CONFIRMED_DEFECT/MATERIAL_RISK/DESIGN_PREFERENCE 定义) | 说明 | 抽至 references/common.md §2 | 否 |
| roles/product-reviewer.md | # Severity Classification (P0/P1/P2 定义) | 说明 | 抽至 references/common.md §1 | 否 |
| roles/product-reviewer.md | # Required Finding Format (Severity/Evidence Class/Confidence/Location/Gap/Trigger Scenario/Consequence/Evidence/Recommendation/Reviewer Notes 字段模板) | 约束 | 抽至 references/common.md §3 | 否 |
| roles/system-critic.md | # Independence Requirement (独立评审/不读他人产出规则) | 约束 | 抽至 references/common.md §4 | 否 |
| roles/system-critic.md | # Evidence Classification (CONFIRMED_DEFECT/MATERIAL_RISK/DESIGN_PREFERENCE 定义) | 说明 | 抽至 references/common.md §2 | 否 |
| roles/system-critic.md | # Severity Classification (P0/P1/P2 定义) | 说明 | 抽至 references/common.md §1 | 否 |
| roles/system-critic.md | # Required Finding Format (Severity/Evidence Class/Confidence/Location/Risk/Trigger Condition/Causal Chain/Consequence/Likelihood/Evidence/Recommendation/Reviewer Notes 字段模板) | 约束 | 抽至 references/common.md §3 | 否 |
| roles/test-designer.md | # Independence Requirement (独立评审/不读他人产出规则) | 约束 | 抽至 references/common.md §4 | 否 |
| roles/test-designer.md | # Evidence Classification (CONFIRMED_GAP/MATERIAL_RISK/DESIGN_PREFERENCE 定义) | 说明 | 抽至 references/common.md §2 | 否 |
| roles/test-designer.md | # Severity Classification (P0/P1/P2 定义) | 说明 | 抽至 references/common.md §1 | 否 |
| roles/test-designer.md | # Required Finding Format (Severity/Evidence Class/Confidence/Finding Type/Location/Verification Gap/Trigger Scenario/Expected Verification/Verification Method/Consequence/Evidence/Recommendation/Reviewer Notes 字段模板) | 约束 | 抽至 references/common.md §3（Finding Type 枚举仍保留于 # Finding ID 段与 # Example Finding） | 否 |
| protocols/finding-protocol.md | §3 `### Evidence Class` 下 CONFIRMED_DEFECT/MATERIAL_RISK/DESIGN_PREFERENCE/CONFIRMED_GAP 四个 `####` 定义段 | 说明 | 抽至 references/common.md §2，标题锚点与"每个 Finding 恰用一个证据等级"规则保留 | 否 |
| protocols/finding-protocol.md | §4 `### P0/### P1/### P2` 严重度定义与示例清单 | 说明 | 抽至 references/common.md §1，"恰有一个严重度""不得抬高 P2"规则保留 | 否 |
| protocols/finding-protocol.md | §5 `### HIGH/### MEDIUM/### LOW` 置信度定义段 | 说明 | 抽至 references/common.md，置信度须匹配证据（§16）、不得以置信度降severity 等规则保留 | 否 |
| protocols/consolidation-protocol.md | §24 输出示例中的第二个完整 Finding 示例 `CR-002 — Historical Data Behavior After Entity Deletion Is Undefined`（含关系图/摘要中对应行） | 重复示例 | 与同段 CR-001 示例结构完全重复，保留 CR-001 一个 worked example | 否 |
| protocols/consolidation-protocol.md | §24 输出示例中 Conflict C-001 的字段明细（Conflicting Findings / Conflict / Conflict Type / Why the Conflict Matters / Required Decision），改为指向 §14 | 重复示例 | 与 §14 Conflict C-001 完整模板+示例重复；§14 全量保留，示例内保留 C-001 与 PENDING_DECISION | 否 |
| protocols/consolidation-protocol.md | §6 七类关系、§7/§9/§11/§12/§15–§20/§25 中的 ASCII 示例块与解释性散文 | 说明 | 压缩为等义单行陈述；7 类关系标题、Rule 1–7、全部规则陈述句与 DUPLICATE 的 worked example 保留 | 否 |
| protocols/consolidation-protocol.md | §13 CONFIRMED 列表中重复出现的 "explicit Design Spec text" 条目 | 说明 | 原文同一条目重复两次 | 否 |
| protocols/decision-protocol.md | §1/§2/§3/§6–§15/§18 中的 ASCII 流程块与示例代码块（Accepted/Duplicate 语义链、REJECTED 三条空泛措辞示例、PARTIALLY_ACCEPTED/§10 示例、§12 失效链与示例、§14 溯源链与示例树、§15 六状态列表块等） | 说明 | 压缩为等义单行陈述；6 个状态标题、PENDING_DECISION、§4 生命周期、§5 Required Decision Structure、§8 六个拒绝理由、§28 五个最终状态与全部规则陈述句均保留 | 否 |
| SKILL.md | `# Finding Severity` 段（P0/P1/P2 定义与英文示例散文） | 说明 | 抽至 references/common.md §1；新增 `# 共享定义` 段登记 references/ 路径与四引用 | 否 |
| CLAUDE.md | `### Finding 严重等级` 段（P0/P1/P2 中文定义） | 说明 | 抽至 references/common.md §1 | 否 |
| CLAUDE.md | `### Finding 证据等级` 段（四字面量中文定义） | 说明 | 抽至 references/common.md §2 | 否 |
