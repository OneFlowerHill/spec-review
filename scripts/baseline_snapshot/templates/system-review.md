# System Review

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

## Review Metadata

### Review ID

<REVIEW_ID>

### Reviewer

yy-system-critic

### Review Type

SYSTEM_REVIEW

### Design Spec

<PATH_TO_DESIGN_SPEC>

### Review Date

<YYYY-MM-DD>

### Review Status

COMPLETED

---

## Review Scope

This review evaluates the Design Spec from the
perspective of system reliability, security, data integrity, operational
resilience, architectural complexity, reversibility, and long-term
maintainability.

This review does not:

* redesign the system;
* produce an implementation plan;
* review source-code style;
* optimize implementation details;
* make the final approval decision;
* replace detailed security testing or production validation.

The purpose of this review is to identify system-level risks that could cause
data loss, security breaches, production outages, unrecoverable failures,
excessive operational burden, or unnecessary architectural complexity.

The review assumes that the Design Spec will eventually be implemented and
operated in production.

---

## Findings

<!--
Output no more than 5 findings.

Prioritize P0 and P1 findings.

Each Finding must represent one independently identifiable system risk.

Do not merge unrelated risks merely because they affect the same component.

Do not create findings for theoretical concerns without a plausible trigger
condition and material consequence.
-->

### SC-001 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Location

<Specific architecture component, design decision, workflow, data flow,
integration, security boundary, operational process, or Design Spec section>

#### Risk

<Precisely describe the system weakness, architectural risk, hidden
assumption, irreversible decision, security weakness, data integrity risk,
operational risk, or unnecessary complexity.>

The Risk must identify the actual system-level problem.

Do not describe the issue merely as:

* "This may cause problems."
* "This is not ideal."
* "This architecture is complex."
* "This could be improved."

State the specific failure mechanism or structural risk.

#### Trigger Condition

Describe the concrete condition or sequence of events required to expose the
risk.

1. <Initial system state>
2. <Relevant event or action>
3. <Failure condition or boundary condition>
4. <System behavior>
5. <Point at which the risk becomes observable>

The Trigger Condition must be concrete enough that another engineer can
independently evaluate the reasoning.

#### Consequence

Describe the resulting:

* data integrity impact;
* security impact;
* availability impact;
* operational impact;
* maintenance impact;
* recovery impact;
* business impact.

Clearly distinguish between:

* confirmed consequences;
* logical consequences;
* possible consequences.

Do not exaggerate consequences beyond the available evidence.

#### Likelihood

HIGH / MEDIUM / LOW

Explain the basis for the likelihood assessment.

Consider:

* frequency of the trigger condition;
* complexity of the required conditions;
* exposure to normal user behavior;
* exposure to operational events;
* dependence on external systems;
* historical or structural probability.

#### Reversibility

REVERSIBLE / PARTIALLY_REVERSIBLE / IRREVERSIBLE / UNKNOWN

Describe whether the consequence can be fully recovered after the failure.

#### Recommendation

Define the minimum architectural constraint, system rule, boundary,
operational requirement, or design clarification required to eliminate or
materially reduce the risk.

The recommendation should focus on the risk that must be addressed.

Do not automatically prescribe a specific technology or implementation
pattern unless it is necessary to explain the constraint.

Do not redesign the entire system.

#### Evidence

List the relevant evidence from the Design Spec.

Examples:

* explicit architecture decision;
* missing failure-handling rule;
* undefined data ownership;
* undefined consistency boundary;
* missing authorization boundary;
* external dependency assumption;
* irreversible migration decision;
* unnecessary abstraction;
* operational process not defined.

#### Assumptions

List assumptions required for this Finding to be valid.

Use:

* CONFIRMED — explicitly supported by the Design Spec;
* INFERRED — logically derived from the Design Spec;
* UNKNOWN — cannot currently be verified.

#### Reversibility Analysis

Explain:

* what can be rolled back;
* what cannot be rolled back;
* what data or state may remain after rollback;
* whether recovery requires manual intervention;
* whether recovery depends on unavailable systems or information.

#### Operational Impact

Describe the effect on:

* deployment;
* monitoring;
* alerting;
* incident response;
* recovery;
* maintenance;
* on-call operations.

If no material operational impact is identified, state:

`NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED`

#### Security Impact

Describe any impact involving:

* authentication;
* authorization;
* privilege boundaries;
* data exposure;
* trust boundaries;
* input abuse;
* tenant isolation;
* auditability.

If no material security impact is identified, state:

`NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED`

#### Maintenance Impact

Describe the long-term consequences for:

* future changes;
* dependency management;
* operational knowledge;
* debugging;
* migration;
* backward compatibility;
* system ownership.

#### Source References

* <Document section>
* <Architecture component>
* <Data flow>
* <Requirement ID>
* <Design Spec section>

---

### SC-002 — <Short Descriptive Title>

#### Severity

P0 / P1 / P2

#### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK

#### Confidence

HIGH / MEDIUM / LOW

#### Location

<Specific location>

#### Risk

<The exact system-level risk>

#### Trigger Condition

1. <Step>
2. <Step>
3. <Step>

#### Consequence

<Material consequence>

#### Likelihood

HIGH / MEDIUM / LOW

#### Reversibility

REVERSIBLE / PARTIALLY_REVERSIBLE / IRREVERSIBLE / UNKNOWN

#### Recommendation

<Minimum system constraint, clarification, or decision required>

#### Evidence

<Supporting evidence>

#### Assumptions

<Confirmed, inferred, or unknown assumptions>

#### Reversibility Analysis

<Recovery and rollback analysis>

#### Operational Impact

<Operational impact>

#### Security Impact

<Security impact>

#### Maintenance Impact

<Maintenance impact>

#### Source References

* <Reference>

---

<!--
Repeat the same structure for SC-003, SC-004, and SC-005 only when necessary.

Do not create empty placeholder Findings in the final output.
-->

## Finding Summary

| Finding ID | Severity | Evidence Class                 | Confidence      | Likelihood      | Reversibility                                        | Short Description |
| ---------- | -------- | ------------------------------ | --------------- | --------------- | ---------------------------------------------------- | ----------------- |
| SC-001     | P0/P1/P2 | CONFIRMED_DEFECT/MATERIAL_RISK | HIGH/MEDIUM/LOW | HIGH/MEDIUM/LOW | REVERSIBLE/PARTIALLY_REVERSIBLE/IRREVERSIBLE/UNKNOWN | <Description>     |
| SC-002     | P0/P1/P2 | CONFIRMED_DEFECT/MATERIAL_RISK | HIGH/MEDIUM/LOW | HIGH/MEDIUM/LOW | REVERSIBLE/PARTIALLY_REVERSIBLE/IRREVERSIBLE/UNKNOWN | <Description>     |

---

## System Risk Coverage

Record which system risk dimensions were evaluated.

| Risk Dimension                   | Status                    | Finding IDs |
| -------------------------------- | ------------------------- | ----------- |
| Data Integrity and Consistency   | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Security Boundaries              | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Authentication and Authorization | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Availability and Resilience      | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Failure Recovery                 | REVIEWED / NOT_APPLICABLE | <IDs>       |
| External Dependencies            | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Concurrency and Race Conditions  | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Data Lifecycle and Migration     | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Backward Compatibility           | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Operational Complexity           | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Maintenance Burden               | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Irreversible Decisions           | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Over-Engineering                 | REVIEWED / NOT_APPLICABLE | <IDs>       |
| Observability and Diagnosis      | REVIEWED / NOT_APPLICABLE | <IDs>       |

If a dimension is marked `NOT_APPLICABLE`, provide a brief reason.

---

## Irreversible Decisions

List decisions in the Design Spec that may be difficult or expensive to reverse.

### ID-001 — <Decision>

#### Decision

<Description of the irreversible or difficult-to-reverse decision>

#### Why It Is Difficult to Reverse

<Migration cost, compatibility impact, data impact, operational impact, or
organizational dependency>

#### Reversal Cost

HIGH / MEDIUM / LOW / UNKNOWN

#### Risk

<What could go wrong if the decision is incorrect>

#### Recommendation

<What must be clarified or validated before committing to the decision>

#### Status

OPEN

---

## Over-Engineering and Complexity Risks

List architectural complexity that appears disproportionate to the stated
requirements.

Only include complexity when there is evidence that it creates material
engineering, operational, or maintenance risk.

### OC-001 — <Complexity Area>

#### Complexity

<Describe the abstraction, component, dependency, process, or architectural
layer that may be unnecessarily complex>

#### Evidence

<Why the complexity appears unnecessary or disproportionate>

#### Simplification Opportunity

<Describe the simpler capability or design constraint that may satisfy the
requirement>

Do not redesign the system.

#### Risk of Keeping the Complexity

<Maintenance, operational, debugging, deployment, or reliability risk>

#### Confidence

HIGH / MEDIUM / LOW

#### Status

OPEN

---

## Unresolved System Questions

List important system questions that were identified during review but could not
be converted into a sufficiently evidenced Finding.

Each question must use the following format:

### Q-001 — <Question>

#### Question

<Specific unresolved system question>

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

* The external system contract was not provided.
* Production traffic characteristics are unknown.
* Existing data volume is unknown.
* Current deployment and rollback capabilities were not provided.
* Security trust boundaries are not documented.
* Existing operational procedures are unknown.
* Failure behavior of a dependency has not been verified.

Do not use limitations to excuse weak analysis.

Only record limitations that materially affect the confidence of a Finding.

---

## Reviewer Conclusion

### Critical Finding Count

* P0: <COUNT>
* P1: <COUNT>
* P2: <COUNT>

### Risk Summary

* Security risks: <COUNT>
* Data integrity risks: <COUNT>
* Availability and resilience risks: <COUNT>
* Operational risks: <COUNT>
* Maintenance risks: <COUNT>
* Irreversible decisions: <COUNT>
* Over-engineering risks: <COUNT>

### Review Result

REQUIRES_REVIEW

This review identifies system-level risks that must be considered by the
Consolidation phase.

The System Critic does not determine whether the Findings are ultimately
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
  reviewer: "yy-system-critic"
  review_type: "SYSTEM_REVIEW"
  status: "COMPLETED"

findings:
  - id: "SC-001"
    severity: "P0|P1|P2"
    evidence_class: "CONFIRMED_DEFECT|MATERIAL_RISK"
    confidence: "HIGH|MEDIUM|LOW"
    title: "<Short Descriptive Title>"
    location: "<Location>"
    likelihood: "HIGH|MEDIUM|LOW"
    reversibility: "REVERSIBLE|PARTIALLY_REVERSIBLE|IRREVERSIBLE|UNKNOWN"
    source_references:
      - "<Reference>"
    risk_dimensions:
      - "<Dimension>"
    status: "PENDING_DECISION"

  - id: "SC-002"
    severity: "P0|P1|P2"
    evidence_class: "CONFIRMED_DEFECT|MATERIAL_RISK"
    confidence: "HIGH|MEDIUM|LOW"
    title: "<Short Descriptive Title>"
    location: "<Location>"
    likelihood: "HIGH|MEDIUM|LOW"
    reversibility: "REVERSIBLE|PARTIALLY_REVERSIBLE|IRREVERSIBLE|UNKNOWN"
    source_references:
      - "<Reference>"
    risk_dimensions:
      - "<Dimension>"
    status: "PENDING_DECISION"

irreversible_decisions:
  - id: "ID-001"
    status: "OPEN"
    title: "<Decision>"

complexity_risks:
  - id: "OC-001"
    status: "OPEN"
    title: "<Complexity Area>"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "<Question>"
```

---

## Template Completion Rules

The System Critic must comply with the following rules:

1. The final review must contain no more than 5 Findings.

2. Every Finding must have a unique ID using the format:

   `SC-001`, `SC-002`, `SC-003`, etc.

3. Finding IDs must be sequential within the review.

4. Every Finding must have a severity.

5. Every Finding must have an Evidence Class.

6. Every Finding must have a Confidence level.

7. Every Finding must have a specific Trigger Condition.

8. Every Finding must have a Likelihood assessment.

9. Every Finding must have a Reversibility assessment.

10. Every Finding must distinguish the system risk from its consequence.

11. Every Finding must provide the minimum constraint, clarification, or
    decision required to address the risk.

12. Findings must be independently actionable.

13. Do not merge unrelated system risks into one Finding.

14. Do not create a Finding solely because a different architecture could be
    imagined.

15. Do not treat architectural unfamiliarity as evidence of risk.

16. Do not convert uncertainty into fact.

17. Do not invent system behavior that is absent from the Design Spec.
    Design Spec.

18. Do not prescribe specific technologies merely because they are familiar or
    preferred.

19. Do not silently discard a significant concern because it does not fit into
    the top 5 Findings.

20. Irreversible decisions must be recorded separately when they do not
    constitute an immediate Finding.

21. Over-engineering concerns must be supported by evidence of material
    complexity, cost, or maintenance risk.

22. The Machine-Readable Finding Index must accurately reflect the detailed
    Findings.

23. The System Critic must not make final acceptance or rejection decisions.

24. The output must be directly consumable by the Consolidation Protocol.
