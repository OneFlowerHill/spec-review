# Product Review

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

> Finding 字段契约（共享必填 + Product 差异字段 `The Gap`/`Trigger Scenario`）见 `references/common.md` §3。

## Review Metadata

### Review ID

<REVIEW_ID>

### Reviewer

product-reviewer

### Review Type

PRODUCT_REVIEW

### Design Spec

<PATH_TO_DESIGN_SPEC>

### Review Date

<YYYY-MM-DD>

### Review Status

COMPLETED

---

## Review Scope

This review evaluates the Design Spec from a product
correctness, business-rule completeness, user-behavior, workflow integrity,
and operational usability perspective.

This review does not evaluate:

* implementation quality;
* source code quality;
* detailed system architecture;
* technology selection;
* infrastructure design;
* performance optimization;
* test implementation details.

The purpose of this review is to identify product-level requirements that are
ambiguous, incomplete, contradictory, unsafe, or insufficiently defined for
implementation.

---

## Findings

<!--
Output no more than 5 findings.

Prioritize P0 and P1 findings.

Each Finding must represent one independently identifiable product problem.

Do not merge unrelated problems merely because they have similar consequences.

Do not create findings for general opinions, preferences, or vague concerns.
-->

### PR-001 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Location

<Specific section, requirement, workflow, rule, or behavior in the
Design Spec>

#### The Gap

<Precisely describe the missing requirement, ambiguity, contradiction,
undefined behavior, or product flaw.>

The statement must identify what the Design Spec fails to define or what rules
are inconsistent.

Do not describe the issue merely as:

* "This may cause problems."
* "This is not ideal."
* "This could be improved."

State the actual requirement gap.

#### Trigger Scenario

1. <Initial state or action>
2. <User or system action>
3. <Relevant condition>
4. <Action that exposes the gap>
5. <Resulting undefined or incorrect behavior>

The scenario must be concrete enough that another reviewer can independently
reproduce the reasoning.

#### Consequence

Describe the resulting:

* business impact;
* user impact;
* operational impact;
* data or workflow impact.

Do not exaggerate consequences beyond the evidence.

Clearly distinguish between:

* confirmed consequences;
* logical consequences;
* possible consequences.

#### Recommendation

Define the minimum business rule, requirement clarification, constraint, or
decision required to eliminate the ambiguity or risk.

The recommendation must focus on what must be defined.

Do not prescribe implementation details unless the implementation choice is
necessary to resolve the product-level problem.

#### Evidence

List the relevant evidence from the Design Spec.

Examples:

* explicit requirement text;
* missing rule;
* contradictory requirements;
* undefined state;
* undefined actor responsibility;
* undefined lifecycle behavior.

#### Assumptions

List assumptions required for this Finding to be valid.

Use:

* CONFIRMED — explicitly supported by the Design Spec;
* INFERRED — logically derived from the Design Spec;
* UNKNOWN — cannot currently be verified.

#### Source References

* <Document section>
* <Requirement ID>
* <Workflow step>
* <Design Spec section>

---

### PR-002 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Location

<Specific location>

#### The Gap

<The exact product or business gap>

#### Trigger Scenario

1. <Step>
2. <Step>
3. <Step>

#### Consequence

<Material impact>

#### Recommendation

<Minimum clarification or rule required>

#### Evidence

<Supporting evidence>

#### Assumptions

<Confirmed, inferred, or unknown assumptions>

#### Source References

* <Reference>

---

<!--
Repeat the same structure for PR-003, PR-004, and PR-005 only when necessary.
Do not create empty placeholder Findings in the final output.
-->

## Finding Summary

| Finding ID | Severity | Evidence Class                 | Confidence      | Short Description |
| ---------- | -------- | ------------------------------ | --------------- | ----------------- |
| PR-001     | P0/P1/P2 | CONFIRMED_DEFECT/MATERIAL_RISK | HIGH/MEDIUM/LOW | <Description>     |
| PR-002     | P0/P1/P2 | CONFIRMED_DEFECT/MATERIAL_RISK | HIGH/MEDIUM/LOW | <Description>     |

---

## Product Risk Coverage

Record which product risk dimensions were evaluated.

| Risk Dimension                | Status                    | Finding IDs |
| ----------------------------- | ------------------------- | ----------- |
| State Machine Vulnerabilities | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Hard Boundaries and Limits    | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Data Lifecycle                | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Backward Compatibility        | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Implicit Assumptions          | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Business Rule Conflicts       | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Temporal Consistency          | REVIEWED / NOT_APPLICABLE | <IDs>       |
| User Workflow Integrity       | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Administrative Operability    | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Abuse and Misuse Scenarios    | REVIEWED / NOT_APPLICABLE | <IDs>       |

If a dimension is marked `NOT_APPLICABLE`, provide a brief reason.

---

## Unresolved Product Questions

List important product questions that were identified during review but could
not be converted into a sufficiently evidenced Finding.

Each question must use the following format:

### Q-001 — <Question>

#### Question

<Specific unresolved question>

#### Why It Matters

<Impact of leaving the question unanswered>

#### Required Clarification

<Information or decision required>

#### Status

OPEN

---

## Review Limitations

List information limitations that affected the review.

Examples:

* The Design Spec does not define the external system contract.
* Historical behavior of existing data is unknown.
* The current production workflow was not provided.
* The Design Spec references a business rule that is not documented.

Do not use limitations to excuse weak analysis.

Only record limitations that materially affect the confidence of a Finding.

---

## Reviewer Conclusion

### Critical Finding Count

* P0: <COUNT>
* P1: <COUNT>
* P2: <COUNT>

### Review Result

REQUIRES_REVIEW

This review identifies product-level gaps that must be considered by the
Consolidation phase.

The Product Reviewer does not determine whether the Findings are ultimately
accepted, rejected, deferred, or otherwise resolved.

Final disposition is determined by the Decision Protocol.

---

## Machine-Readable Finding Index

<!--
This section provides a compact index for automated consolidation.
It must remain synchronized with the detailed Findings above.
-->

```yaml
review:
  review_id: "<REVIEW_ID>"
  reviewer: "product-reviewer"
  review_type: "PRODUCT_REVIEW"
  status: "COMPLETED"

findings:
  - id: "PR-001"
    severity: "P0|P1|P2"
    evidence_class: "CONFIRMED_DEFECT|MATERIAL_RISK"
    confidence: "HIGH|MEDIUM|LOW"
    title: "<Short Descriptive Title>"
    location: "<Location>"
    source_references:
      - "<Reference>"
    risk_dimensions:
      - "<Dimension>"
    status: "PENDING_DECISION"

  - id: "PR-002"
    severity: "P0|P1|P2"
    evidence_class: "CONFIRMED_DEFECT|MATERIAL_RISK"
    confidence: "HIGH|MEDIUM|LOW"
    title: "<Short Descriptive Title>"
    location: "<Location>"
    source_references:
      - "<Reference>"
    risk_dimensions:
      - "<Dimension>"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "<Question>"
```

---

## Template Completion Rules

The Product Reviewer must comply with the following rules:

1. The final review must contain no more than 5 Findings.

2. Every Finding must have a unique ID using the format:

   `PR-001`, `PR-002`, `PR-003`, etc.

3. Finding IDs must be sequential within the review.

4. Every Finding must have a severity.

5. Every Finding must have an Evidence Class.

6. Every Finding must have a Confidence level.

7. Every Finding must identify a specific location in the Design Spec whenever
   such a location exists.

8. Every Finding must contain a concrete Trigger Scenario.

9. Every Finding must distinguish the product gap from its consequence.

10. Every Finding must provide the minimum clarification or rule required to
    address the gap.

11. Findings must be independently actionable.

12. Do not merge unrelated product problems into one Finding.

13. Do not create a Finding solely because a feature could theoretically be
    improved.

14. Do not convert uncertainty into fact.

15. Do not invent business rules that are absent from the Design Spec.

16. Do not silently discard a significant concern because it does not fit into
    the top 5 Findings.

17. If a significant concern is excluded from the top 5, record it in
    `Unresolved Product Questions` only when it is genuinely unresolved.

18. The Machine-Readable Finding Index must accurately reflect the detailed
    Findings.

19. The Product Reviewer must not make final acceptance or rejection decisions.

20. The output must be directly consumable by the Consolidation Protocol.
