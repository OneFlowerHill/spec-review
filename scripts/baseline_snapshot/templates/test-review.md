# Test Review

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

## Review Metadata

### Review ID

<REVIEW_ID>

### Reviewer

yy-test-designer

### Review Type

TEST_REVIEW

### Design Spec

<PATH_TO_DESIGN_SPEC>

### Review Date

<YYYY-MM-DD>

### Review Status

COMPLETED

---

## Review Scope

This review evaluates whether the Design Spec can be
objectively verified before implementation begins.

The review focuses on:

* missing acceptance criteria;
* untestable requirements;
* undefined expected outcomes;
* missing boundary conditions;
* failure recovery gaps;
* data integrity verification gaps;
* state transition verification gaps;
* backward compatibility verification gaps;
* operational observability gaps;
* long-term regression risks.

This review does not:

* review code quality;
* redesign the system architecture;
* prescribe implementation technologies;
* create a complete test plan;
* replace security testing, performance testing, or production validation;
* make the final approval decision.

The purpose of this review is to determine whether the Design Spec defines
observable behavior clearly enough to be verified objectively.

A requirement that cannot be objectively verified is not sufficiently defined.

---

## Findings

<!--

Output no more than 5 high-value findings. Prioritize:

- P0 and P1 findings over P2
- Core business behavior verification over peripheral behavior
- Silent failure risks over easily detectable failures
- Data integrity and security verification over minor usability
- High-confidence gaps over speculative concerns

Do not manufacture findings. If fewer than 5 material findings exist,
output fewer.

-->

### TD-001 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_GAP / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Finding Type

ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT

#### Location

<Specific document section, requirement ID, workflow step, or Design Spec section>

#### Verification Gap

<What cannot currently be objectively verified. Be specific — do not write
vague statements like "testing will be difficult".>

For ACCEPTANCE_TEST: Describe the concrete scenario and the expected observable
result that should be verifiable.

For UNTESTABLE_REQUIREMENT: Describe the missing acceptance criterion or the
ambiguous expected outcome that prevents objective verification.

For BLIND_SPOT: Describe the production scenario that may silently fail and
why ordinary testing may miss it.

#### Trigger Scenario

1. <Preconditions>
2. <Action or event>
3. <Expected behavior that should be determined>
4. <The point at which the Design Spec becomes ambiguous or unobservable>

#### Expected Verification

<What a tester should be able to verify: specific business state, API response,
database condition, event, audit record, log, metric, report, or user-visible
result.>

For BLIND_SPOT: What must be observable in production to detect the failure.

#### Verification Method

<Exactly where and how to verify. If no method exists:>

No objective verification method is currently defined.

#### Consequence

<What happens if the gap remains unresolved: incorrect behavior passes testing,
regression goes undetected, production failure remains silent, etc.>

#### Evidence

<Cite the relevant requirement or Design Spec behavior. Distinguish explicit
evidence from inference.>

#### Recommendation

<Minimum acceptance criterion, expected behavior, or observable evidence that
must be defined. Do not redesign the system.>

#### Source References

* <Document section>
* <Requirement ID>
* <Workflow step>
* <Design Spec section>

#### Reviewer Notes

Optional. Use only for important uncertainty or assumptions.

---

### TD-002 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_GAP / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Finding Type

ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT

#### Location

<Location>

#### Verification Gap

<Gap description>

#### Trigger Scenario

1. <Step>
2. <Step>
3. <Step>

#### Expected Verification

<Expected verification>

#### Verification Method

<Method or "No objective verification method is currently defined.">

#### Consequence

<Consequence>

#### Evidence

<Evidence>

#### Recommendation

<Recommendation>

#### Source References

* <References>

#### Reviewer Notes

<Notes or omit>

---

<!-- Repeat for additional findings. Do not create empty placeholder findings. -->

---

## Testability Coverage

Record which verification dimensions were evaluated.

| Verification Dimension                 | Status                    | Finding IDs |
| -------------------------------------- | ------------------------- | ----------- |
| Happy Path Verification                | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Boundary and Limit Verification        | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Duplicate and Idempotency Verification | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Invalid Input Verification             | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Failure and Timeout Verification       | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Partial Failure Verification           | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Data Integrity Verification            | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| State Transition Verification          | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Permission Boundary Verification       | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Backward Compatibility Verification    | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Temporal Verification                  | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Migration Verification                 | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| External Dependency Verification       | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Observability Verification             | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |
| Recovery Verification                  | REVIEWED / NOT_APPLICABLE | <TD-IDs>    |

If a dimension is marked NOT_APPLICABLE, provide a brief reason.

---

## Unresolved Verification Questions

List important questions that affect testability but cannot currently be
answered from the Design Spec.

### Q-001 — <Question>

#### Question

<Specific unresolved verification question>

#### Why It Matters

<Impact on objective verification>

#### Required Clarification

<Information or decision required>

#### Status

OPEN

---

## Review Limitations

List information limitations that materially affected the review.

Do not use limitations to excuse weak analysis.

Only record limitations that materially affect the confidence of a finding.

---

## Reviewer Conclusion

### Critical Testability Finding Count

* P0: <COUNT>
* P1: <COUNT>
* P2: <COUNT>

### Finding Type Breakdown

* Acceptance Tests: <COUNT>
* Untestable Requirements: <COUNT>
* Blind Spots: <COUNT>

### Review Result

REQUIRES_REVIEW

This review identifies verification gaps, untestable requirements, and
production blind spots that must be considered by the Consolidation phase.

The Test Designer does not determine whether the Findings are ultimately
accepted, rejected, deferred, or otherwise resolved.

Final disposition is determined by the Decision Protocol.

---

## Machine-Readable Finding Index

<!--
This section provides a compact index for automated consolidation.
It must remain synchronized with the detailed review sections above.
-->

```yaml
review:
  review_id: "<REVIEW_ID>"
  reviewer: "yy-test-designer"
  review_type: "TEST_REVIEW"
  status: "COMPLETED"

findings:
  - id: "TD-001"
    severity: "P0|P1|P2"
    evidence_class: "CONFIRMED_GAP|MATERIAL_RISK"
    confidence: "HIGH|MEDIUM|LOW"
    finding_type: "ACCEPTANCE_TEST|UNTESTABLE_REQUIREMENT|BLIND_SPOT"
    title: "<Short Descriptive Title>"
    source_references:
      - "<Reference>"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "<Question>"
```

---

## Template Completion Rules

1. Output no more than 5 high-value findings unless the review process
   explicitly permits a larger number.

2. Every finding must have a unique ID using the format:
   `TD-001`, `TD-002`, `TD-003`, etc.

3. Every finding must include a Finding Type:
   ACCEPTANCE_TEST, UNTESTABLE_REQUIREMENT, or BLIND_SPOT.

4. Every finding must define all required fields: Severity, Evidence Class,
   Confidence, Finding Type, Location, Verification Gap, Trigger Scenario,
   Expected Verification, Verification Method, Consequence, Evidence,
   Recommendation.

5. Prioritize findings by severity (P0 > P1 > P2), then by core business
   behavior impact, then by silent failure risk.

6. Do not create findings solely because a theoretical edge case exists.

7. Do not invent system behavior, thresholds, states, or acceptance criteria
   absent from the Design Spec.

8. Do not redesign the system to make it easier to test.

9. Do not prescribe specific implementation technologies.

10. Do not convert uncertainty into fact.

11. Expected results must not rely on undefined subjective language.

12. The Machine-Readable Finding Index must accurately reflect the detailed
    review sections.

13. The Test Designer must not make final acceptance or rejection decisions.

14. The output must be directly consumable by the Consolidation Protocol.
