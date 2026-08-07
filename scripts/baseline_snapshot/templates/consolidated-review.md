# Consolidated Review

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

## Review Metadata

### Review ID

<REVIEW_ID>

### Review Type

CONSOLIDATED_REVIEW

### Design Spec

<PATH_TO_DESIGN_SPEC>

### Consolidation Date

<YYYY-MM-DD>

### Consolidator

<CONSOLIDATOR_ID>

### Review Status

COMPLETED

---

## Consolidation Scope

This document consolidates the independent reviews produced by:

* `yy-product-reviewer`
* `yy-system-critic`
* `yy-test-designer`

The purpose of consolidation is to:

1. identify findings that describe the same underlying problem;
2. merge duplicate findings without losing important evidence;
3. preserve findings that are materially different;
4. identify conflicts between reviewers;
5. establish a unified finding identity;
6. preserve the original reviewer perspectives;
7. prepare a single review document for the Design Spec owner or
   Superpowers workflow;
8. provide a stable structure for recording the final decision for every
   finding.

This document is a consolidation artifact.

It is not a replacement for the original reviewer reports.

The original reviewer findings remain the source of their respective
perspectives.

---

## Source Reviews

| Reviewer            | Review Type    | Review ID   | Source File | Status              |
| ------------------- | -------------- | ----------- | ----------- | ------------------- |
| yy-product-reviewer | PRODUCT_REVIEW | <REVIEW_ID> | <PATH>      | AVAILABLE / MISSING |
| yy-system-critic    | SYSTEM_REVIEW  | <REVIEW_ID> | <PATH>      | AVAILABLE / MISSING |
| yy-test-designer    | TEST_REVIEW    | <REVIEW_ID> | <PATH>      | AVAILABLE / MISSING |

---

## Consolidation Principles

The Consolidator must apply the following principles:

### 1. Findings Are Not Merged by Similar Keywords

Two findings must not be merged merely because they:

* mention the same component;
* have similar wording;
* have the same severity;
* produce similar consequences.

They may only be merged when they describe the same underlying problem or
failure mechanism.

### 2. Preserve Independent Perspectives

If Product, System, and Test Reviewers identify different aspects of the same
underlying problem, consolidate them into one finding while preserving the
distinct perspectives.

For example:

```text
Product Reviewer:
The business rule is undefined.

System Critic:
Different interpretations can produce inconsistent system state.

Test Designer:
No objective acceptance criterion can be written.
```

These may be one underlying problem with three independent supporting
perspectives.

The consolidated Finding must not erase any of these perspectives.

### 3. Do Not Force Consolidation

If two findings are genuinely independent, keep them separate.

The purpose of consolidation is to remove duplication, not reduce the number
of findings artificially.

### 4. Do Not Resolve Conflicts Silently

When reviewers disagree about:

* whether a risk exists;
* severity;
* likelihood;
* consequence;
* interpretation of a requirement;
* recommended resolution;

the disagreement must be explicitly recorded.

### 5. Evidence Takes Priority Over Reviewer Authority

A finding must not be accepted merely because:

* it was identified by a particular reviewer;
* it has a high severity;
* multiple reviewers mention it.

The Consolidator must evaluate the evidence and reasoning.

### 6. Uncertainty Must Remain Visible

Do not convert:

* inferred behavior into confirmed behavior;
* possible consequences into certain consequences;
* assumptions into requirements.

---

## Consolidator Predispositions

<!--
Record the key judgments formed by the main agent during Phase 1 (Context
Acquisition) that may influence consolidation. This makes potential cognitive
bias auditable.

Example:
- "The Design Spec assumes synchronous external dependency responses — this
  assumption may bias consolidation toward confirming timeout-related findings."
- "The Design Spec emphasizes data integrity over availability — this
  may affect severity assessment of availability-related findings."
-->

### Predisposition 1

<Description of key judgment and how it might influence consolidation>

---

# Consolidated Findings

<!--
Assign no more than 15 consolidated findings unless the review process
explicitly permits a larger number.

The number of consolidated findings may be smaller than the sum of findings
from the three source reviews.

One consolidated finding may reference findings from multiple reviewers.
-->

## CR-001 — <Short Descriptive Title>

### Consolidated Severity

P0 / P1 / P2

### Consolidation Confidence

HIGH / MEDIUM / LOW

### Finding Status

PENDING_DECISION

Allowed values:

* PENDING_DECISION
* ACCEPTED
* REJECTED
* DEFERRED
* PARTIALLY_ACCEPTED
* DUPLICATE
* INVALIDATED

The initial status must be `PENDING_DECISION`.

The Consolidator must not make the final product or engineering decision unless
explicitly instructed by the Decision Protocol.

---

### Underlying Problem

<Describe the single underlying problem represented by this consolidated
Finding.>

This section must answer:

> What is the actual problem, independent of which reviewer discovered it?

Do not simply concatenate the original findings.

---

### Evidence

Present the strongest evidence supporting the Finding.

Separate evidence into:

#### Confirmed Evidence

* <Evidence explicitly present in the Design Spec>

#### Inferred Evidence

* <Logical conclusions derived from the documented behavior>

#### Unknowns

* <Important facts that cannot currently be verified>

---

### Trigger Scenario

Describe the concrete scenario that exposes the underlying problem.

1. <Initial state>
2. <Action or event>
3. <Condition>
4. <System or user behavior>
5. <Failure, ambiguity, or risk>

The scenario must be specific enough for the problem to be independently
evaluated.

---

### Consequence

Describe the material impact of the problem.

Classify the impact where applicable:

* Business Impact: <Impact>
* User Impact: <Impact>
* Data Impact: <Impact>
* Security Impact: <Impact>
* Availability Impact: <Impact>
* Operational Impact: <Impact>
* Maintenance Impact: <Impact>
* Verification Impact: <Impact>

Use `NONE_IDENTIFIED` when a category has no material impact.

Do not exaggerate consequences beyond the evidence.

---

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

* <PR-001>

**Assessment:**

<What the Product Reviewer identified and how it relates to the underlying
problem>

#### System Perspective

**Source Findings:**

* <SC-001>

**Assessment:**

<What the System Critic identified and how it relates to the underlying
problem>

#### Test Perspective

**Source Findings:**

* <TD-001>

**Assessment:**

<What the Test Designer identified and how it relates to the underlying
problem>

---

### Relationship Classification

Select exactly one:

* `DUPLICATE` — findings describe the same problem with substantially overlapping evidence;
* `SAME_ROOT_CAUSE` — findings have different manifestations but share one root cause;
* `RELATED` — findings are connected but independently actionable;
* `INDEPENDENT` — findings should not be consolidated;
* `CONTRADICTORY` — findings reach opposite conclusions about the same issue;
* `SUBSET` — one finding's scope is entirely contained within another;
* `CONSEQUENCE` — one finding is a direct causal consequence of another.

#### Relationship Explanation

<Explain why the source findings were consolidated or kept separate.>

---

### Conflict Analysis

#### Conflict Status

* `NO_CONFLICT`
* `MINOR_INTERPRETATION_DIFFERENCE`
* `MATERIAL_CONFLICT`
* `UNRESOLVED_CONFLICT`

#### Conflicting Positions

<Describe disagreements between reviewers, if any.>

#### Conflict Evidence

<Identify the requirement text, assumption, or missing information causing the
disagreement.>

#### Resolution

<Explain whether the conflict can be resolved from the available evidence.>

If it cannot be resolved, state:

`PENDING_DECISION`

Do not silently select one reviewer position without explaining why.

---

### Recommended Resolution

<Define the minimum change, clarification, constraint, or decision required to
eliminate or materially reduce the underlying problem.>

The recommendation must focus on the problem.

It must not unnecessarily redesign the entire system.

If multiple valid resolution strategies exist, record the decision that must be
made rather than arbitrarily selecting one.

---

### Source References

#### Product Review

* <PR-ID>

#### System Review

* <SC-ID>

#### Test Review

* <TD-ID>

#### Design Spec References

* <Section>
* <Requirement ID>
* <Workflow Step>

---

### Consolidation Decision

Select one:

* `MERGED`
* `KEPT_SEPARATE`
* `DUPLICATE`
* `REQUIRES_CLARIFICATION`

#### Decision Rationale

<Explain the consolidation decision.>

### Severity Change Rationale

<!-- MANDATORY: If consolidated severity differs from any source Finding
severity, explain why. Must reference specific source Finding evidence,
not generalized reasoning.

Example:
"Source findings PR-001 (P1) and SC-003 (P0) differ. Upgraded to P0 because
SC-003 demonstrates that the undefined behavior can cause irreversible data
corruption (SC-003 Trigger Scenario step 4), which is more severe than the
originally identified operational impact." -->

<Explanation or "No severity change from source findings.">

---

## CR-002 — <Short Descriptive Title>

### Consolidated Severity

P0 / P1 / P2

### Consolidation Confidence

HIGH / MEDIUM / LOW

### Finding Status

PENDING_DECISION

### Underlying Problem

<Single underlying problem>

### Evidence

#### Confirmed Evidence

* <Evidence>

#### Inferred Evidence

* <Evidence>

#### Unknowns

* <Unknown>

### Trigger Scenario

1. <Step>
2. <Step>
3. <Step>

### Consequence

* Business Impact: <Impact>
* User Impact: <Impact>
* Data Impact: <Impact>
* Security Impact: <Impact>
* Availability Impact: <Impact>
* Operational Impact: <Impact>
* Maintenance Impact: <Impact>
* Verification Impact: <Impact>

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

* <PR-ID>

**Assessment:**

<Product perspective>

#### System Perspective

**Source Findings:**

* <SC-ID>

**Assessment:**

<System perspective>

#### Test Perspective

**Source Findings:**

* <TD-ID>

**Assessment:**

<Test perspective>

### Relationship Classification

DUPLICATE / SAME_ROOT_CAUSE / RELATED / INDEPENDENT / CONTRADICTORY / SUBSET / CONSEQUENCE

#### Relationship Explanation

<Explanation>

### Conflict Analysis

#### Conflict Status

NO_CONFLICT / MINOR_INTERPRETATION_DIFFERENCE / MATERIAL_CONFLICT /
UNRESOLVED_CONFLICT

#### Conflicting Positions

<Positions>

#### Conflict Evidence

<Evidence>

#### Resolution

<Resolution>

### Recommended Resolution

<Minimum resolution>

### Source References

* <References>

### Consolidation Decision

MERGED / KEPT_SEPARATE / DUPLICATE / REQUIRES_CLARIFICATION

#### Decision Rationale

<Rationale>

### Severity Change Rationale

<Explanation or "No severity change from source findings.">

---

<!--
Repeat for additional consolidated findings.

Do not create empty placeholder findings.
-->

# Unmerged Source Findings

This section records source findings that were intentionally not merged into
another Consolidated Finding.

## UF-001 — <Source Finding ID>

### Source Reviewer

PRODUCT / SYSTEM / TEST

### Original Finding

<Original finding title>

### Reason Not Merged

<Explain why this is an independent problem or why consolidation would lose
meaningful information.>

### Current Status

PENDING_DECISION

### Related Consolidated Findings

* <CR-ID or NONE>

---

# Duplicate and Superseded Findings

This section records findings that were not retained as independent
Consolidated Findings.

## DS-001 — <Source Finding ID>

### Source Reviewer

PRODUCT / SYSTEM / TEST

### Original Finding

<Original finding title>

### Disposition

DUPLICATE / REPRESENTED_ELSEWHERE

### Canonical Finding

<CR-ID>

### Reason

<Explain why the finding is represented by another Consolidated Finding.>

---

# Cross-Reviewer Conflicts

This section records material disagreements that cannot be resolved through
simple consolidation.

## CF-001 — <Short Descriptive Conflict Title>

### Conflict

<Describe the disagreement>

### Reviewer Position A

<Position>

### Reviewer Position B

<Position>

### Evidence

<Relevant evidence from the Design Spec>

### What Is Known

<Confirmed facts>

### What Is Uncertain

<Unknowns and assumptions>

### Required Decision

<Specific decision required from the Spec owner, Product owner, or
Superpowers workflow>

### Status

PENDING_DECISION

---

# Coverage Gaps

<!--
Record risk dimensions that cannot be assessed due to MISSING source reviews.
Only populate when a source review is MISSING.

If all three reviews are available, write:
"No coverage gaps — all three source reviews are available."
-->

## CG-001 — <Missing Reviewer> Perspective

### Missing Reviewer

PRODUCT / SYSTEM / TEST

### Unassessable Risk Dimensions

<List the risk dimensions that this reviewer would normally assess but
cannot be evaluated without their review.>

### Impact on Consolidation Confidence

<Explain how the missing review affects confidence in the consolidated
findings.>

---

# Coverage Matrix

This matrix shows which review perspectives contributed to each consolidated
Finding.

| Consolidated Finding | Product | System | Test    | Primary Risk Area |
| -------------------- | ------- | ------ | ------- | ----------------- |
| CR-001               | PR-001  | SC-001 | TD-001  | <Area>            |
| CR-002               | PR-002  | —      | TD-002  | <Area>            |

Use `—` when a reviewer did not identify a corresponding finding.

The absence of a finding from one reviewer does not prove that the risk does
not exist.

---

# Review Coverage Summary

| Review Dimension       | Product  | System   | Test     | Consolidated Findings |
| ---------------------- | -------- | -------- | -------- | --------------------- |
| Business Rules         | REVIEWED | —        | REVIEWED | <IDs>                 |
| User Workflow          | REVIEWED | —        | REVIEWED | <IDs>                 |
| State Transitions      | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Data Integrity         | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Security               | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Availability           | —        | REVIEWED | REVIEWED | <IDs>                 |
| Failure Recovery       | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Backward Compatibility | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Temporal Behavior      | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Operational Complexity | REVIEWED | REVIEWED | REVIEWED | <IDs>                 |
| Testability            | —        | REVIEWED | REVIEWED | <IDs>                 |
| Observability          | —        | REVIEWED | REVIEWED | <IDs>                 |

---

# Superpowers Instructions

<!--
This section tells the reader (typically the spec owner using superpowers)
what to do with this consolidated review.
-->

## What to Read

- **Consolidated Review**: This document
- **Source Reviews**: See Source Reviews table above for file paths

## What to Decide

For each Consolidated Finding in the Decision Queue below, set a decision:

| CR-ID | Title | Severity | Decision (choose one) |
|-------|-------|----------|----------------------|
| CR-001 | <title> | P0 | ___ |
| CR-002 | <title> | P1 | ___ |

**Decision options**: PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED

## Decision Template

For each finding, copy and fill in the following in the Decision Records
section below:

```markdown
## DR-<NNN> — CR-<NNN>

### Decision Status

PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

### Decision Owner

<your name or role>

### Decision Rationale

<Why this decision was made — must address the finding's validity, materiality,
and evidence>

### Required Action

<If ACCEPTED: what must change in the Design Spec>

### Decision Date

<YYYY-MM-DD>
```

## Hard Rules

1. A Finding with status PENDING_DECISION cannot have a final review state of
   APPROVED
2. All P0 findings must be resolved (not PENDING_DECISION) before the final
   review state can be anything other than BLOCKED
3. Every decision must have a Decision Owner, Rationale, and Date

## Final Review State

After all decisions are recorded, determine the final review state:

| Condition | State |
|-----------|-------|
| Any unresolved P0 finding | BLOCKED |
| Accepted P1/P2 changes outstanding | CHANGES_REQUIRED |
| No blocking finding, conditions remain | CONDITIONAL_APPROVAL |
| All required changes incorporated | APPROVED |
| Review records incomplete | INCOMPLETE |

Write the final review state at the bottom of the Consolidation Conclusion section.

---

# Decision Queue

This section contains the findings that require a final decision from the
Spec owner or Superpowers workflow.

Only findings with the following statuses should appear here:

* PENDING_DECISION
* REQUIRES_CLARIFICATION

## DQ-001 — CR-001

### Problem

<Short description of the consolidated problem>

### Severity

P0 / P1 / P2

### Evidence Summary

<Concise evidence summary>

### Recommended Resolution

<Recommended minimum resolution>

### Decision Required

<Specific decision that must be made>

### Decision Status

PENDING

---

# Decision Records

This section must be updated after the Spec owner or Superpowers
workflow makes a decision.

Every Consolidated Finding must eventually have a decision record unless it is
still `PENDING_DECISION`.

## DR-001 — CR-001

### Decision

PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

### Decision Date

<YYYY-MM-DD>

### Decision Maker

<PERSON_OR_AGENT_ID>

### Decision Rationale

<Why the decision was made>

### Action Taken

<What changed in the Design Spec or review process>

### Final Resolution

<Describe the resulting state>

### Verification

<How the resolution was verified>

### Related Changes

* <Commit>
* <Spec revision>
* <Plan revision>
* <Other reference>

### Processing Status

DECIDED

---

# Finding Lifecycle

The lifecycle of every consolidated finding is:

```text
PENDING_DECISION
  ↓
ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED
```

A Finding must not disappear from the review merely because it was:

* rejected;
* deferred;
* considered unnecessary;
* fixed in a later revision.

Its history must remain available for future analysis.

---

# Review Statistics

## Finding Counts

### By Source Review

* Product Findings: <COUNT>
* System Findings: <COUNT>
* Test Findings: <COUNT>

### After Consolidation

* Consolidated Findings: <COUNT>
* Unmerged Findings: <COUNT>
* Duplicate Findings: <COUNT>
* Superseded Findings: <COUNT>
* Cross-Reviewer Conflicts: <COUNT>

### By Severity

* P0: <COUNT>
* P1: <COUNT>
* P2: <COUNT>

### By Status

* PENDING_DECISION: <COUNT>
* ACCEPTED: <COUNT>
* REJECTED: <COUNT>
* DEFERRED: <COUNT>
* PARTIALLY_ACCEPTED: <COUNT>
* DUPLICATE: <COUNT>
* INVALIDATED: <COUNT>

---

# Consolidation Conclusion

### Consolidation Result

COMPLETED

### Decision Readiness

PENDING_DECISION / REQUIRES_CLARIFICATION

### Summary

<Briefly state whether the source reviews have been successfully consolidated
and whether unresolved conflicts or ambiguities remain.>

The Consolidator must not declare the Design Spec approved or rejected.

Approval, rejection, modification, or deferral is determined by the
Spec owner or the Superpowers workflow.

### Final Review State

BLOCKED / CHANGES_REQUIRED / CONDITIONAL_APPROVAL / APPROVED / INCOMPLETE

<Determine the final review state based on the rules in the Superpowers
Instructions section above.>

---

# Machine-Readable Consolidation Index

<!--
This section provides a compact index for automated processing.

It must remain synchronized with the detailed Consolidated Findings,
Unmerged Findings, Duplicate/Superseded Findings, Conflicts, and Decisions.
-->

```yaml
review:
  review_id: "<REVIEW_ID>"
  review_type: "CONSOLIDATED_REVIEW"
  status: "COMPLETED"
  design_spec: "<PATH_TO_DESIGN_SPEC>"
  round: 1
  spec_stem: "<SPEC_STEM>"
  final_review_state: null

source_reviews:
  - reviewer: "yy-product-reviewer"
    review_type: "PRODUCT_REVIEW"
    review_id: "<REVIEW_ID>"
    source_file: "<PATH>"
    status: "AVAILABLE|MISSING"

  - reviewer: "yy-system-critic"
    review_type: "SYSTEM_REVIEW"
    review_id: "<REVIEW_ID>"
    source_file: "<PATH>"
    status: "AVAILABLE|MISSING"

  - reviewer: "yy-test-designer"
    review_type: "TEST_REVIEW"
    review_id: "<REVIEW_ID>"
    source_file: "<PATH>"
    status: "AVAILABLE|MISSING"

consolidated_findings:
  - id: "CR-001"
    title: "<Short Descriptive Title>"
    severity: "P0|P1|P2"
    confidence: "HIGH|MEDIUM|LOW"
    status: "PENDING_DECISION|ACCEPTED|REJECTED|DEFERRED|PARTIALLY_ACCEPTED|DUPLICATE|INVALIDATED"
    source_findings:
      product:
        - "PR-001"
      system:
        - "SC-001"
      test:
        - "TD-001"
    finding_type: "ACCEPTANCE_TEST|UNTESTABLE_REQUIREMENT|BLIND_SPOT|N/A"
    relationship_classification: "DUPLICATE|SAME_ROOT_CAUSE|RELATED|INDEPENDENT|CONTRADICTORY|SUBSET|CONSEQUENCE"
    conflict_status: "NO_CONFLICT|MINOR_INTERPRETATION_DIFFERENCE|MATERIAL_CONFLICT|UNRESOLVED_CONFLICT"
    source_references:
      - "<Reference>"
    processing_status: "PENDING_DECISION"
    severity_escalation: false
    severity_change_rationale: null

unmerged_findings:
  - id: "UF-001"
    source_finding_id: "<Source Finding ID>"
    reviewer: "PRODUCT|SYSTEM|TEST"
    reason: "<Reason>"
    status: "PENDING_DECISION"

duplicate_or_represented:
  - id: "DR-001"
    source_finding_id: "<Source Finding ID>"
    disposition: "DUPLICATE|REPRESENTED_ELSEWHERE"
    canonical_finding_id: "CR-001"
    reason: "<Reason>"

conflicts:
  - id: "CF-001"
    title: "<Conflict Title>"
    status: "PENDING_DECISION"
    related_findings:
      - "CR-001"

decision_queue:
  - id: "DQ-001"
    finding_id: "CR-001"
    severity: "P0|P1|P2"
    processing_status: "PENDING_DECISION"

decisions:
  - id: "DR-001"
    finding_id: "CR-001"
    decision: "ACCEPTED|REJECTED|DEFERRED|PARTIALLY_ACCEPTED|DUPLICATE|INVALIDATED"
    processing_status: "PENDING_DECISION|DECIDED"

statistics:
  source_findings:
    product: 0
    system: 0
    test: 0
  consolidated_findings: 0
  unmerged_findings: 0
  duplicate_findings: 0
  represented_elsewhere_findings: 0
  conflicts: 0
  p0: 0
  p1: 0
  p2: 0
```

---

# Template Completion Rules

The Consolidator must comply with the following rules:

1. Every source review must be explicitly recorded in `Source Reviews`.

2. Every source Finding must have one of the following dispositions:

   * represented by a Consolidated Finding;
   * recorded as Unmerged;
   * recorded as Duplicate;
   * recorded as Superseded.

3. No source Finding may silently disappear.

4. Consolidated Finding IDs must be unique and sequential:

   `CR-001`, `CR-002`, `CR-003`, etc.

5. A Consolidated Finding must represent one underlying problem.

6. Findings must not be merged solely because they share:

   * a component;
   * a keyword;
   * a severity;
   * a consequence.

7. Independent reviewer perspectives must be preserved.

8. If multiple reviewers identify different aspects of the same underlying
   problem, preserve each perspective under `Reviewer Perspectives`.

9. Conflicts between reviewers must be explicitly recorded.

10. The Consolidator must not resolve a material conflict by silently choosing
    one reviewer.

11. Confirmed evidence, inferred evidence, and unknowns must remain separate.

12. The Consolidator must not convert assumptions into facts.

13. The Consolidator must not invent requirements, system behavior, test
    criteria, or business rules.

14. Severity must be assigned based on the materiality of the underlying
    consolidated problem, not by mechanically selecting the highest severity
    from the source findings.

15. The Consolidator must preserve the strongest evidence from all relevant
    source reviews.

16. A finding that was rejected, deferred, duplicated, or superseded must remain
    traceable in the review history.

17. The Decision Queue must contain every finding requiring a final decision.

18. The Consolidator must not make the final acceptance or rejection decision
    unless explicitly authorized by the Decision Protocol.

19. Every final decision must have:

    * a decision;
    * a decision maker;
    * a decision date;
    * a rationale;
    * an action taken;
    * a final resolution.

20. Decision records must not overwrite the original Finding.

21. The Machine-Readable Consolidation Index must accurately reflect the
    detailed review.

22. Review statistics must be consistent with the actual findings and
    dispositions.

23. The final output must be directly consumable by the Decision Protocol.

24. The consolidated review must preserve enough traceability to answer:

    * Which reviewer found this problem?
    * What was the original finding?
    * Why was it merged?
    * What evidence supports it?
    * Were reviewers in conflict?
    * What decision was made?
    * Who made the decision?
    * What changed afterward?
    * Was the resolution verified?