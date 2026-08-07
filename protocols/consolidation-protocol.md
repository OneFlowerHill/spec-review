# Consolidation Protocol

## Purpose

This protocol defines the universal contract for consolidating independent reviewer Findings into a single, coherent, traceable review record.

The purpose of consolidation is to transform:

```text
Independent Review Findings
        ↓
Cross-Reviewer Analysis
        ↓
Duplicate Detection
        ↓
Root-Cause Analysis
        ↓
Conflict Detection
        ↓
Consolidated Findings
```

The Consolidation phase must preserve the meaning and origin of every reviewer Finding while eliminating unnecessary duplication and making relationships between Findings explicit.

This protocol does not decide whether a Finding should ultimately be accepted, rejected, deferred, partially accepted, duplicated, or invalidated.

Those decisions belong to the Decision Protocol.

---

## 1. Consolidation Principles

Consolidation is not simple summarization.

The Consolidator must determine:

1. Which Findings represent the same underlying problem.
2. Which Findings are related but materially distinct.
3. Which Findings are independent.
4. Which Findings are consequences of a deeper root cause.
5. Which Findings contradict each other.
6. Which Findings are based on different assumptions.
7. Which Findings should remain separately traceable.
8. Which Finding should become the authoritative consolidated issue.

The objective is:

```text
Preserve Signal
        +
Remove Redundancy
        +
Expose Relationships
        +
Preserve Traceability
```

Consolidation must not weaken a Finding merely because multiple reviewers identified it.

Consolidation must not merge Findings merely because they discuss the same component or feature.

---

## 2. Input Contract

The Consolidator receives:

```text
Input
├── Design Spec
├── Product Review Findings
├── System Critic Findings
└── Test Designer Findings
```

Each independent Finding should conform to the Finding Protocol.

The Consolidator must treat the Design Spec as the authoritative context for determining relationships between Findings.

The Consolidator must not rely solely on reviewer summaries.

---

## 3. Output Contract

The Consolidator produces:

```text
Consolidated Review
├── Review Metadata
├── Consolidated Findings
│   ├── CR-001
│   ├── CR-002
│   └── CR-003
├── Finding Relationship Map
├── Conflicts
├── Coverage Analysis
└── Consolidation Summary
```

The output must preserve:

```text
Reviewer Finding
        ↓
Consolidated Finding
        ↓
Decision
```

The Consolidator must not make the final decision on whether a Finding is accepted or rejected.

The consolidated output must be ready for the Decision Protocol.

---

## 4. Consolidated Finding Identity

Every consolidated Finding receives a global ID (`CR-ID`).

The format is fixed as `CR-<NNN>` (`CR-001`, `CR-002`, `CR-003`); no other prefix may be used.

`CR` means Consolidated Review Finding.

The global ID is assigned only during consolidation.

Independent reviewer IDs remain unchanged.

Example:

```text
CR-001
├── PR-001
├── SC-003
└── TD-002
```

The global ID must remain stable within the review record.

If the consolidated review is regenerated, existing Finding IDs should be preserved whenever the underlying Finding remains substantively the same.

Do not renumber Findings merely because their order changes.

---

## 5. Source Finding Preservation

Every Consolidated Finding must identify all source Findings that contributed to it.

Required:

```text
### Source Findings

- PR-001
- SC-003
- TD-002
```

The source Findings must remain individually identifiable.

Do not replace the original Findings with the consolidated version.

The consolidated Finding is an additional analytical layer.

---

## 6. Finding Relationship Classification

> 证据等级四值见 `references/common.md` §2；合并协议须能识别全部四值（含 `CONFIRMED_GAP`），否则视为一致性缺陷。

Every source Finding must receive a relationship classification relative to other Findings.

Use one of the following:

```text
DUPLICATE
SAME_ROOT_CAUSE
RELATED
INDEPENDENT
CONTRADICTORY
SUBSET
CONSEQUENCE
```

---

### DUPLICATE

Two Findings are duplicates when they identify substantively the same problem — Root Problem, Trigger Condition, and Material Consequence should generally be the same.

Different wording or reviewer perspective does not make Findings independent.

Worked example:

```text
Product Reviewer:
Duplicate submission behavior is undefined.

System Critic:
Retry may create duplicate side effects.

Test Designer:
There is no testable rule defining whether duplicate requests
produce one or multiple business operations.
```

These may represent one consolidated Finding:

```text
CR-001:
Repeated requests for one logical operation have undefined semantics.
```

---

### SAME_ROOT_CAUSE

Use when multiple Findings have the same underlying cause but materially different consequences (example: both rooted in "no authoritative source of customer status", one causing conflicting customer status, the other inconsistent reporting).

These may be consolidated if the root problem is the primary issue and the consequences can be preserved.

---

### RELATED

Use when Findings are connected but resolving one does not necessarily resolve the other (example: "retry behavior is undefined" vs "operational monitoring for retries is undefined").

These are related but may require separate decisions.

---

### INDEPENDENT

Use when two Findings have different root causes and resolving one does not resolve the other (example: "authorization boundary is undefined" vs "historical data migration is undefined").

These should remain separate.

---

### CONTRADICTORY

Use when Findings assert incompatible requirements, behaviors, or conclusions (example: Product requires duplicate requests to be rejected, while System identifies a workflow in which repeated requests must create independent business events).

The Consolidator must not choose one silently.

The contradiction must be recorded for decision.

---

### SUBSET

Use when one Finding is completely contained within another broader Finding (example: broad "state transition rules are incomplete" contains specific "the Design Spec does not define what happens when an approval expires").

The specific Finding may become a source Finding of the broader Finding if the broader Finding fully represents the issue.

Do not discard the specific Finding's unique evidence.

---

### CONSEQUENCE

Use when one Finding primarily describes a consequence of another Finding (example: root "data ownership is undefined" → consequence "reports may contain conflicting values").

The consequence may be incorporated into the root Finding if it does not represent an independently actionable problem.

---

## 7. Root Cause Analysis

The Consolidator must distinguish:

```text
Root Cause
    ↓
Mechanism
    ↓
Failure
    ↓
Consequence
```

Example:

```text
Root Cause:
No defined ownership of authoritative state.

Mechanism:
Two systems independently update the same entity.

Failure:
Values diverge.

Consequence:
Reports and downstream automation use inconsistent data.
```

The Consolidated Finding should normally focus on the deepest actionable root problem.

However, the consolidation must preserve significant consequences.

Do not merge unrelated problems merely because they eventually produce the same consequence (example: "database corruption → incorrect report" vs "missing business rule → incorrect report").

The same consequence does not imply the same Finding.

---

## 8. Consolidation Decision Tree

For every pair of Findings, ask:

```text
1. Do they identify the same underlying problem?
        │
        ├── Yes → DUPLICATE or SAME_ROOT_CAUSE
        │
        └── No
              ↓
2. Does resolving one automatically resolve the other?
        │
        ├── Yes → SUBSET or CONSEQUENCE
        │
        └── No
              ↓
3. Are they materially connected?
        │
        ├── Yes → RELATED
        │
        └── No → INDEPENDENT
```

If the Findings assert incompatible requirements:

```text
CONTRADICTORY
```

---

## 9. Consolidation Rules

### Rule 1: Do Not Merge by Topic Alone

"Database issue" / "database performance issue" / "database migration issue" / "database authorization issue" are not automatically the same Finding.

A shared component does not establish a shared root cause.

---

### Rule 2: Do Not Merge by Consequence Alone

"Data loss caused by retry duplication" and "data loss caused by migration failure" are not automatically the same Finding.

The consequence is similar.

The root causes are different.

---

### Rule 3: Do Not Merge by Severity Alone

Two P1 Findings are not necessarily one Finding.

Severity is not an identity criterion.

---

### Rule 4: Do Not Merge by Reviewer Agreement Alone

If three reviewers identify the same problem, that increases confidence.

It does not automatically determine the final wording.

The Consolidator must preserve the strongest causal chain.

---

### Rule 5: Do Not Suppress Minority Findings

A Finding identified by only one reviewer must not be discarded merely because other reviewers did not identify it.

The absence of a Finding from another review is not evidence that the Finding is invalid.

---

### Rule 6: Do Not Inflate Findings During Consolidation

The consolidated Finding must not claim more than the source Findings establish.

Do not convert "possible risk" into "confirmed failure" without evidence.

---

### Rule 7: Preserve Reviewer-Specific Evidence

Different reviewers may provide different evidence for the same root issue (product: business rule undefined; system: multiple services may independently update the state; test: no objective acceptance criterion exists).

The consolidated Finding should preserve relevant evidence from each source; combined, they strengthen one consolidated Finding.

---

## 10. Consolidated Finding Structure

Every Consolidated Finding must use the following structure:

```markdown
## CR-<NUMBER> — <Short Descriptive Title>

### Severity

P0 / P1 / P2

### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK

### Confidence

HIGH / MEDIUM / LOW

### Source Findings

- <Reviewer Local ID>
- <Reviewer Local ID>

### Finding Type

ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT / N/A

Required only when a source Finding is from the Test Designer.
Use N/A for Findings sourced exclusively from Product or System reviews.
This field preserves the semantic distinction of Test Designer findings
during consolidation.

### Primary Review Perspectives

- Product
- System
- Test

Include only the perspectives that materially contributed to this Finding.

### Location

The relevant location in the Design Spec.

### Consolidated Problem

State the unified problem represented by this Finding.

The statement must preserve the common root issue without losing important
specificity.

### Root Cause

Identify the underlying requirement, assumption, design gap, or rule that
creates the problem.

### Trigger Scenarios

Describe the most important scenarios identified by the source Findings.

### Causal Chain

Trigger Condition
    ↓
Design Spec Behavior
    ↓
Root Problem
    ↓
Consequence

### Consequence

Describe the material business, technical, operational, user, or
verification impact.

### Evidence Synthesis

Combine the strongest supporting evidence from the source Findings.

Clearly distinguish:

- confirmed facts;
- logical inferences;
- assumptions;
- unresolved uncertainties.

### Recommendation Synthesis

Describe the minimum clarification, rule, constraint, or decision required to
address the consolidated issue.

Do not prescribe unnecessary implementation details.

### Source Relationship

Explain how the source Findings relate to each other.

Examples:

- Same root cause.
- Duplicate observations from different perspectives.
- Product issue with independent system consequence.
- Related but separate risks.

### Consolidation Notes

Record important reasoning, uncertainty, or boundaries that affect later
decision-making.
```

---

## 11. Consolidated Severity

The consolidated severity must be determined from the material consequence of the unified Finding.

Do not simply copy the highest source severity automatically.

Evaluate: Source Findings → Unified Root Problem → Combined Consequences → Consolidated Severity.

A consolidated Finding may:

* retain the highest source severity;
* be lower than the highest source severity if the original severity was based on a mistaken interpretation;
* be higher if the combined evidence demonstrates a more serious consequence.

Any severity change must be explicitly explained.

Example:

```text
Source Findings:
PR-001: P1
SC-002: P0
TD-003: P1

Consolidated Severity:
P0

Reason:
The System Critic evidence demonstrates that the undefined behavior can
cause irreversible data corruption, which is more severe than the originally
identified operational impact.
```

---

## 12. Consolidated Confidence

Confidence should reflect the combined quality of evidence.

Multiple reviewers agreeing does not automatically produce HIGH confidence.

Evaluate: Evidence Strength + Evidence Independence + Assumption Count + Contradictory Evidence.

Examples:

* three reviewers independently identify the same issue, the Design Spec explicitly supports the trigger scenario, and no contradictory evidence exists → Confidence: HIGH;
* three reviewers identify a similar theoretical risk, but the actual dependency behavior is unknown → Confidence: MEDIUM.

---

## 13. Evidence Synthesis

The Consolidator must classify evidence.

### CONFIRMED

Directly supported by:

* explicit Design Spec text;
* existing system behavior;
* verified code or data;
* confirmed external contract.

### INFERRED

A logical consequence of confirmed facts (example: confirmed "two systems can independently update the same entity" → inference "their values may diverge if no conflict rule exists").

### ASSUMED

A condition required for the Finding but not verified (example: "the external dependency may return success after the client timeout").

### UNKNOWN

A fact that cannot currently be determined.

Unknown information must not be presented as confirmed evidence.

---

## 14. Contradiction Handling

When Findings conflict, the Consolidator must create an explicit Conflict Record.

Use:

```markdown
### Conflict C-<NUMBER>

#### Conflicting Findings

- <Finding ID>
- <Finding ID>

#### Conflict

Describe the exact contradiction.

#### Conflict Type

- Business Rule Conflict
- Scope Conflict
- State Behavior Conflict
- Ownership Conflict
- Technical Constraint Conflict
- Evidence Conflict

#### Why the Conflict Matters

Describe the consequence of leaving the contradiction unresolved.

#### Required Decision

State what must be decided.

#### Decision Status

PENDING_DECISION
```

Example:

```markdown
### Conflict C-001

#### Conflicting Findings

- PR-001
- SC-004

#### Conflict

PR-001 assumes that a repeated request represents the same business
operation and should be rejected.

SC-004 identifies a business workflow in which repeated requests may
represent separate business events.

#### Conflict Type

Business Rule Conflict

#### Why the Conflict Matters

The implementation cannot correctly determine whether to reject or create a
new business operation without a rule distinguishing these cases.

#### Required Decision

Define the identity of a logical operation and the rule distinguishing
duplicates from independent business events.

#### Decision Status

PENDING_DECISION
```

The Consolidator must not resolve the conflict by preference.

---

## 15. Finding Splitting

A source Finding should be split into multiple Consolidated Findings when it contains multiple independently actionable problems.

Example: a source Finding stating "the Design Spec lacks ownership rules, retry behavior, monitoring, migration strategy, and authorization boundaries" may become:

```text
CR-001 — Authoritative Data Ownership Undefined
CR-002 — Retry Semantics Undefined
CR-003 — Operational Monitoring Requirements Missing
CR-004 — Migration Strategy Undefined
CR-005 — Authorization Boundary Undefined
```

A Finding should be split when resolving Problem A does not resolve Problem B.

Do not split merely because a Finding has multiple consequences.

---

## 16. Finding Merging

Two or more Findings may be merged when they share: Same Root Problem + Same Material Risk + Same Required Decision.

Example: PR-001 ("business rule for duplicate operations is undefined"), SC-002 ("retry can create duplicate effects"), and TD-003 ("duplicate operation behavior cannot be objectively verified") may become `CR-001 — Semantics of repeated requests for one logical operation are undefined`.

The consolidated Finding must preserve Product Impact, System Impact, and Verification Impact.

---

## 17. Related Finding Handling

Related Findings should remain separate when their decisions may differ.

Example: `CR-001` ("data ownership is undefined") and `CR-002` ("monitoring for ownership conflicts is missing") are related, but "CR-001 Accepted / CR-002 Deferred" may be a valid outcome.

If they were merged, independent decision tracking would be lost.

The Consolidator should prefer separate Findings when independent decision outcomes are likely.

---

## 18. Consequence Handling

A consequence may be merged into the root Finding when it is merely a direct result of the root problem (example: root "state transition rules are incomplete" → consequence "users may become stuck in an undefined state").

However, the consequence should remain separate when it introduces an independent requirement (example: same root, but "no monitoring can detect entities stuck in invalid states" is an independent operational problem).

These may require separate Findings.

---

## 19. Review Perspective Coverage

The Consolidator should record which perspectives identified each Finding (`### Primary Review Perspectives`: Product Reviewer / System Critic / Test Designer).

Perspective coverage can indicate:

* Product only → business interpretation issue;
* System only → technical or operational risk;
* Test only → verification or observability gap;
* all three → cross-domain issue with broad impact.

Perspective coverage is evidence of breadth.

It is not a substitute for severity or validity.

A Finding identified by one reviewer may still be P0.

---

## 20. Consolidation Priority

Consolidated Findings should be ordered by:

1. P0 severity.
2. P1 severity.
3. P2 severity.

Within the same severity:

1. Core business correctness.
2. Data integrity.
3. Security and authorization.
4. Production availability.
5. Recoverability.
6. Compatibility.
7. Operational burden.
8. Maintainability.
9. Optimization.

The order must not change the Finding IDs — e.g. `CR-007`, `CR-002`, `CR-004` may be displayed in priority order without renumbering them.

---

## 21. Consolidation Quality Requirements

The Consolidator must verify:

```text
[ ] Every source Finding is accounted for.
[ ] Every source Finding has a relationship classification.
[ ] Every source Finding is either consolidated, retained independently,
    marked as a duplicate, or explicitly handled.
[ ] No source Finding has silently disappeared.
[ ] Duplicate Findings have an authoritative consolidated Finding.
[ ] Related Findings are not incorrectly merged.
[ ] Root causes are distinguished from consequences.
[ ] Contradictory Findings are explicitly recorded.
[ ] Evidence and inference are distinguished.
[ ] Consolidated severity is justified.
[ ] Consolidated confidence is justified.
[ ] Source Finding IDs remain traceable.
[ ] The Consolidator has not made final decisions.
```

---

## 22. Source Finding Relationship Matrix

The Consolidator should maintain a relationship matrix.

Example:

| Source Finding | Relationship    | Target |
| -------------- | --------------- | ------ |
| PR-001         | SAME_ROOT_CAUSE | CR-001 |
| SC-003         | SAME_ROOT_CAUSE | CR-001 |
| TD-002         | SAME_ROOT_CAUSE | CR-001 |
| SC-005         | INDEPENDENT     | CR-002 |
| TD-004         | CONSEQUENCE     | CR-001 |
| PR-006         | CONTRADICTORY   | C-001  |

The matrix exists to preserve traceability.

---

## 23. Consolidation Summary

The final Consolidated Review should include a concise summary of the consolidation process.

Example:

```markdown
## Consolidation Summary

### Source Findings

- Product Reviewer: 5
- System Critic: 5
- Test Designer: 5

### Consolidated Findings

- P0: 2
- P1: 4
- P2: 1

### Relationship Summary

- Same Root Cause / Merged: 5
- Independent: 3
- Related: 2
- Duplicate: 3
- Consequence: 2
- Contradictory: 1

### Unresolved Conflicts

- C-001: Business rule conflict regarding duplicate operations.

### Decision Readiness

The consolidated Findings are ready for the Decision Protocol.

One conflict requires an explicit decision before the final review state can
be determined.
```

The summary must not contain final acceptance or rejection decisions.

---

## 24. Consolidated Review Output Example

```markdown
# Consolidated Review

## Review Metadata

### Design Spec

specs/2026-07-19-customer-operation.md

### Reviewers

- Product Reviewer
- System Critic
- Test Designer

---

## Consolidated Findings

## CR-001 — Repeated Requests for One Logical Operation Have Undefined Semantics

### Severity

P0

### Evidence Class

MATERIAL_RISK

### Confidence

HIGH

### Source Findings

- PR-001
- SC-003
- TD-002

### Primary Review Perspectives

- Product Reviewer
- System Critic
- Test Designer

### Location

Operation submission workflow and retry behavior.

### Consolidated Problem

The Design Spec does not define how repeated requests representing the same
logical business operation are identified or handled.

As a result, a timeout followed by a retry may either repeat the same business
effect or create a new one, with no defined rule distinguishing the two cases.

### Root Cause

The Design Spec does not define the identity and lifecycle of a logical business
operation independently from individual requests.

### Trigger Scenarios

1. A user submits an operation.
2. The operation is processed.
3. The response is lost because of a timeout.
4. The user or client retries the request.
5. The Design Spec does not define whether the retry represents the same
   operation or a new operation.

### Causal Chain

Unknown operation identity
        ↓
Repeated request cannot be classified
        ↓
Duplicate or ambiguous business effect
        ↓
Incorrect business data and downstream behavior

### Consequence

The system may produce duplicate business effects or fail to produce the
expected effect after a retry.

This can result in incorrect historical data, inconsistent downstream
processing, and difficult recovery.

### Evidence Synthesis

Confirmed:
The Design Spec defines the operation submission flow but does not explicitly
define repeated-request semantics.

Inferred:
A client timeout can occur independently of whether the business operation
has completed.

Unknown:
The external dependency's exact response behavior after a client timeout has
not been verified.

### Recommendation Synthesis

Define:

- what constitutes one logical business operation;
- how repeated requests are classified;
- the expected number of business effects;
- the observable behavior after an unknown timeout.

The implementation approach should be decided after these rules are explicit.

### Source Relationship

PR-001, SC-003, and TD-002 identify the same underlying requirement gap from
product, system, and verification perspectives.

### Consolidation Notes

The System Critic Finding describes a specific failure mechanism.
The Test Designer Finding describes the absence of objective verification.
Both are retained as evidence of the same underlying semantic gap.

---

## Conflicts

### Conflict C-001

Business Rule Conflict between PR-005 and SC-004 regarding repeated
submissions; record all Conflict Record fields as defined in §14.

#### Decision Status

PENDING_DECISION

---

## Finding Relationship Map

| Source Finding | Relationship | Consolidated Target |
|---|---|---|
| PR-001 | SAME_ROOT_CAUSE | CR-001 |
| SC-003 | SAME_ROOT_CAUSE | CR-001 |
| TD-002 | SAME_ROOT_CAUSE | CR-001 |
| PR-005 | CONTRADICTORY | C-001 |
| SC-004 | CONTRADICTORY | C-001 |

---

## Consolidation Summary

### Source Findings

- Product Reviewer: 5
- System Critic: 5
- Test Designer: 5

### Consolidated Findings

- P0: 1

### Relationship Summary

- Same Root Cause / Merged: 3
- Independent: 3
- Contradictory: 2

### Unresolved Conflicts

- C-001: Business rule conflict regarding repeated submissions.

### Decision Readiness

The Consolidated Findings are ready for the Decision Protocol.

Conflict C-001 requires explicit resolution by an authorized decision-maker.
```

---

## 25. Consolidation Anti-Patterns

The Consolidator must not:

### Mechanical Concatenation

"Product Findings + System Findings + Test Findings" is not consolidation.

---

### Majority Voting

"2 reviewers say X, 1 reviewer says Y, therefore X is correct" is invalid — reviewer count does not determine truth.

---

### Severity Voting

"Two P1 Findings and one P0 Finding, therefore P1" is invalid — severity must be determined from evidence and consequence.

---

### Forced Consensus

Do not eliminate disagreement merely to produce a clean document.

Disagreement is information.

---

### Silent Deletion

Do not discard a Finding without recording why it was merged, why it was classified as a duplicate, why it was considered independent, or why it was invalid for consolidation.

---

### Premature Decision

Do not write "Accepted", "Rejected", or "Deferred" during consolidation.

The Consolidator may identify "Requires Decision", but the final disposition belongs to the Decision Protocol.

---

### Solution Redesign

The Consolidator must not redesign the Design Spec.

It may state "the Design Spec must define duplicate-operation semantics"; it must not automatically state "replace the architecture with a specific implementation".

---

## 26. Consolidation Completion Criteria

The Consolidation Protocol is complete when:

* all independent reviewer outputs have been processed;
* every source Finding is traceable;
* every source Finding has a relationship classification;
* duplicate Findings have been consolidated;
* related Findings have been evaluated for independent treatment;
* root causes have been separated from consequences;
* independent Findings remain independently traceable;
* contradictions have been explicitly recorded;
* consolidated Findings have global IDs;
* consolidated severity and confidence are justified;
* evidence and inference are distinguished;
* no Finding has been silently discarded;
* no final decision has been made;
* the resulting review is ready for the Decision Protocol.

This protocol defines how independent review Findings become a coherent, traceable Consolidated Review.

It does not define the final decision regarding those Findings.