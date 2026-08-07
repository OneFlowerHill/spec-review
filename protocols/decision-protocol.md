# Decision Protocol

## Purpose

This protocol defines the universal contract for making, recording, and tracking decisions about consolidated review findings.

The purpose of this protocol is to ensure that every consolidated Finding receives an explicit, traceable, and auditable decision.

A decision must answer:

> What is the final disposition of this Finding, why was that decision made, and what is the resulting status of the Design Spec?

**Supersession Note**: The decision state enumeration defined in this protocol
(PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE,
INVALIDATED) supersedes all other state enumerations in the project. Any
conflicting state values in other files (OPEN as a Finding decision state,
READY_FOR_DECISION, RESOLVED, SUPERSEDED) are deprecated and must not be used.
OPEN remains valid for non-Finding entities (Questions, Irreversible Decisions,
Complexity Risks).

This protocol does not define:

* how individual reviewers discover Findings;
* how independent Findings are consolidated;
* how technical implementation should be designed;
* how the Design Spec itself should be rewritten;
* whether a reviewer is correct merely because their Finding exists.

Those responsibilities belong to the Finding Protocol, Consolidation Protocol, and the spec owner or decision-maker.

---

## 1. Decision Principles

Every consolidated Finding must receive an explicit decision.

A Finding must never disappear silently.

Each Finding must end in one of the following states: `ACCEPTED` / `REJECTED` / `DEFERRED` / `PARTIALLY_ACCEPTED` / `DUPLICATE` / `INVALIDATED`.

The decision must be based on the Finding itself, the available evidence, the context of the Design Spec, and the impact of the decision.

The existence of a Finding does not automatically mean that the Finding must be accepted.

The existence of disagreement does not automatically mean that the Finding should be rejected.

The decision-maker must evaluate the actual problem and its consequences.

---

## 2. Decision States

> 决策状态枚举的权威定义与流转见 `references/common.md` §6 及本文件 §4；状态枚举为全局权威（设计规格 §4 第 2 条）。

### ACCEPTED

Use when the decision-maker agrees that the Finding represents a valid issue or risk and the required change must be incorporated into the Design Spec or implementation requirements.

An Accepted Finding means: Finding is valid → risk or gap is acknowledged → required action is accepted → Design Spec or implementation requirements must change.

Examples:

* an undefined business rule must be clarified;
* a missing failure state must be added;
* a data consistency constraint must be defined;
* an acceptance criterion must be added;
* a security boundary must be explicitly specified.

An Accepted Finding should normally include a required resolution.

---

### REJECTED

Use when the decision-maker determines that the Finding should not result in a change.

A Rejected Finding must have a specific reason.

Valid reasons may include:

* the Finding is based on an incorrect interpretation;
* the described scenario is impossible under the actual constraints;
* the consequence is not material;
* the risk is already addressed elsewhere;
* the proposed behavior is intentional and acceptable;
* the recommendation would create greater risk than the Finding itself;
* the Finding conflicts with an explicit higher-priority business decision.

Do not reject a Finding with vague statements such as "Not needed.", "We don't think this is a problem.", or "The current design is fine."

The decision must explain why the Finding does not require action.

---

### DEFERRED

Use when the Finding is valid or potentially valid, but the decision to resolve it is intentionally postponed.

A Deferred Finding must specify:

* why it is being deferred;
* what conditions will trigger reconsideration;
* when or during which phase it should be reconsidered;
* who or what is responsible for the follow-up.

A Deferred Finding must not be used as a way to avoid making a decision.

Valid examples:

* the risk is outside the scope of the current release;
* additional evidence is required before a final decision;
* the current implementation intentionally postpones the capability;
* the risk is accepted temporarily under a defined operating constraint.

A Deferred Finding must not be treated as resolved.

---

### PARTIALLY_ACCEPTED

Use when only part of the Finding is accepted.

This state is necessary when a Finding contains multiple distinct consequences or recommendations and the decision-maker accepts only a subset.

Example: for a Finding covering duplicate operation handling, recovery behavior, and historical reconciliation — duplicate operation handling is accepted, historical reconciliation is deferred, and the proposed recovery behavior is rejected because the scenario is not applicable to this system.

A Partially Accepted Finding must explicitly identify:

* which part is accepted;
* which part is rejected;
* which part is deferred, if applicable.

Do not use PARTIALLY_ACCEPTED merely because the implementation differs from the reviewer's recommendation.

The problem may be accepted while the original recommendation is not.

---

### DUPLICATE

Use when the Finding is substantively covered by another consolidated Finding.

A Duplicate Finding must reference the authoritative Finding.

Example:

```text
CR-007
Status: DUPLICATE
Duplicate Of: CR-003
```

A Duplicate Finding must not disappear from the review record.

Its original identity and source reviewers must remain traceable.

A Duplicate status means: the Finding was reviewed → the issue is already represented elsewhere → no independent decision is required → the authoritative Finding owns the decision.

---

### INVALIDATED

Use when new evidence demonstrates that the Finding is not actually applicable.

This differs from REJECTED.

Use REJECTED when:

> The Finding is understood and intentionally not acted upon.

Use INVALIDATED when:

> The factual basis of the Finding has been disproven or no longer exists.

Examples:

* the referenced behavior does not exist in the actual system;
* a dependency previously believed to exist is not part of the final design;
* new evidence proves that the alleged state transition is impossible;
* the Finding was based on an outdated version of the Design Spec.

An Invalidated Finding must record the evidence that invalidated it.

---

## 3. Decision Authority

The decision-maker must be explicitly identified.

The decision-maker may be:

* the Spec Owner;
* the Product Owner;
* the Technical Owner;
* an Architecture Review Board;
* a designated Review Orchestrator;
* another explicitly authorized role.

The reviewer who discovered the Finding is not automatically the decision-maker.

The Consolidator is not automatically the decision-maker.

The role responsible for deciding must be explicit.

Required field: `Decision Owner: <person or role>`.

If no authorized decision-maker is available, the Finding must not be silently marked as accepted or rejected.

Use `Decision Status: PENDING_DECISION` until an authorized decision is made.

---

## 4. Decision Status Lifecycle

A consolidated Finding follows this lifecycle:

```text
CONSOLIDATED
      ↓
PENDING_DECISION
      ↓
┌───────────────────┐
│ ACCEPTED          │
│ REJECTED          │
│ DEFERRED          │
│ PARTIALLY_ACCEPTED│
│ DUPLICATE         │
│ INVALIDATED       │
└───────────────────┘
```

A Finding may be reopened when new evidence becomes available.

Example:

```text
REJECTED
    ↓
New evidence
    ↓
REOPENED
    ↓
PENDING_DECISION
```

A decision should not be changed silently.

Any changed decision must preserve:

* previous status;
* previous decision;
* reason for change;
* new evidence or trigger;
* new decision;
* new decision-maker;
* decision timestamp.

---

## 5. Required Decision Structure

Every consolidated Finding must contain a decision record.

Use the following structure:

```markdown
## CR-<NUMBER> — <Consolidated Finding Title>

### Decision Status

ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED / PENDING_DECISION

### Decision Owner

<person or authorized role>

### Decision

State the final decision in one or more precise sentences.

### Decision Rationale

Explain why this decision was made.

The rationale must directly address:

- the validity of the Finding;
- the materiality of the consequence;
- the relevant evidence;
- the relationship between the Finding and the Design Spec.

### Accepted Scope

If applicable, specify exactly which part of the Finding is accepted.

### Rejected Scope

If applicable, specify exactly which part of the Finding is rejected.

### Deferred Scope

If applicable, specify exactly which part of the Finding is deferred.

### Required Action

If the Finding is accepted, describe the required change or decision that must be reflected in the Design Spec or implementation requirements.

Do not prescribe unnecessary implementation details.

### Deferral Conditions

Required when the status is DEFERRED.

Specify:

- why the Finding is deferred;
- when it must be reconsidered;
- what evidence or condition triggers reconsideration;
- who is responsible for follow-up.

### Duplicate Of

Required when the status is DUPLICATE.

Reference the authoritative consolidated Finding ID.

### Invalidation Evidence

Required when the status is INVALIDATED.

Describe the evidence that proves the Finding is no longer applicable or was based on an incorrect premise.

### Decision Consequence

Describe the effect of this decision on:

- the Design Spec;
- implementation requirements;
- testing requirements;
- operational requirements;
- future review work.

### Decision Timestamp

<timestamp>

### Decision History

Record previous decisions if the Finding was previously decided and later reopened or changed.
```

---

## 6. Decision Rationale Requirements

A decision rationale must explain the decision, not repeat the Finding.

Weak: "Rejected because this is not necessary."

Strong:

```text
Rejected because the proposed workflow is intentionally single-consumer.
The scenario requires concurrent consumers, which are explicitly excluded
by the current business constraint. No change is required for the current
scope.
```

The rationale must distinguish Finding Validity → Risk Materiality → Decision, for example: the risk is technically possible → the affected operation is explicitly limited to one execution per business day → the consequence is bounded and operationally recoverable → the Finding is rejected for the current scope.

---

## 7. Acceptance Requirements

An Accepted Finding must produce a concrete consequence.

A Finding must not be marked ACCEPTED if the decision-maker agrees with the problem but does not define what changes as a result.

Bad: `Status: ACCEPTED` with rationale "Good point."

Good:

```text
Status:
ACCEPTED

Required Action:
Define the authoritative source of customer status and specify the
conflict-resolution rule when the external system and local system disagree.
The Design Spec must explicitly include this rule before implementation.
```

Acceptance means: problem acknowledged → action required → change must be traceable.

---

## 8. Rejection Requirements

A Rejected Finding must identify the basis for rejection.

Use one or more of the following rejection grounds:

### INCORRECT_PREMISE

The Finding is based on a fact or assumption that is not true.

### INAPPLICABLE_SCENARIO

The trigger scenario cannot occur under the actual system or business constraints.

### IMMATERIAL_CONSEQUENCE

The consequence exists but does not justify a change within the current scope.

### ALREADY_ADDRESSED

The issue is already explicitly addressed by another requirement, constraint, or design decision.

### INTENTIONAL_BEHAVIOR

The behavior is intentional and the associated risk is explicitly accepted.

### OUT_OF_SCOPE

The issue is valid but intentionally outside the scope of the current Design Spec.

Use OUT_OF_SCOPE only when the issue is intentionally excluded.

If the issue should be reconsidered later, use DEFERRED rather than simply REJECTED.

---

## 9. Deferral Requirements

A Deferred Finding must have an explicit follow-up condition.

A valid Deferred decision must answer: why is it not being resolved now? when will it be reconsidered? what evidence or event triggers reconsideration? who is responsible?

Example:

```text
Decision Status:
DEFERRED

Decision Rationale:
The risk is valid but affects the high-volume scenario that is outside
the current release scope.

Deferral Conditions:
Reconsider before the system exceeds 100,000 daily operations or before
the high-volume capability is enabled.

Follow-up Owner:
Technical Owner
```

Invalid: `Decision Status: DEFERRED` with rationale "We'll handle it later."

---

## 10. Partial Acceptance Requirements

Use PARTIALLY_ACCEPTED only when the Finding contains separable parts.

Example: a Finding covering (1) duplicate operation behavior, (2) timeout recovery behavior, (3) historical reconciliation may be decided as — Accepted: duplicate operation behavior; Deferred: historical reconciliation; Rejected: the proposed timeout scenario, because the operation is synchronous and the relevant timeout cannot occur under the current system boundary.

The decision record must make each part independently traceable.

Do not use partial acceptance to obscure an unclear decision.

If the Finding is too broad to decide clearly, the Finding should first be split during consolidation.

---

## 11. Duplicate Decision Requirements

A Finding may be marked DUPLICATE only when another consolidated Finding represents the same substantive issue.

The decision must identify the authoritative Finding (`Duplicate Of: CR-003`).

The following are not sufficient reasons to mark a Finding as duplicate:

* similar wording;
* same general topic;
* same component;
* same consequence;
* same reviewer;
* same severity.

The determining question is:

> If the authoritative Finding is resolved, is the substantive problem represented by this Finding also resolved?

If yes, DUPLICATE may be appropriate.

If no, the Findings should remain separate or be represented as related Findings.

---

## 12. Invalidation Requirements

Use INVALIDATED only when new evidence changes the factual basis of the Finding.

Required chain: Original Finding → New Evidence → Original Premise No Longer Holds → Finding Invalidated.

Example: original Finding "the external service may return duplicate records"; new evidence "the confirmed API contract guarantees a globally unique record identifier and the service rejects duplicate creation requests"; decision: INVALIDATED.

Do not use INVALIDATED merely because:

* the risk is inconvenient;
* the team does not want to fix it;
* the risk is accepted;
* the issue is out of scope.

Those cases require REJECTED or DEFERRED.

---

## 13. Decision Impact

Every decision must describe what happens next.

The Decision Consequence should identify whether the decision affects:

### Design Spec

Does the Design Spec need to change?

Examples:

* add a business rule;
* define a state;
* clarify ownership;
* remove an unnecessary requirement;
* change an assumption.

### Implementation Requirements

Does engineering need to implement a specific behavior?

Examples:

* enforce a constraint;
* handle a failure state;
* preserve historical data;
* prevent an invalid transition.

### Testing Requirements

Does the Finding require new verification?

Examples:

* add an acceptance test;
* add a failure scenario;
* verify data integrity;
* verify recovery behavior.

### Operational Requirements

Does the Finding require:

* monitoring;
* logging;
* alerting;
* operational procedures;
* recovery procedures;
* configuration controls?

### Future Review Work

Does the decision create:

* a follow-up item;
* a deferred risk;
* a required architectural review;
* a future migration concern?

A decision is incomplete if its consequences are unknown.

---

## 14. Decision Traceability

Every consolidated Finding must preserve its origin.

The decision record must be traceable through: Design Spec → Reviewer Findings → Consolidated Finding → Decision → Required Change.

Example: `CR-003` with source Findings PR-001 / SC-004 / TD-002, decision ACCEPTED, required action "define duplicate-operation behavior".

The decision process must never destroy the original reviewer Findings.

---

## 15. Source Finding Preservation

When a Finding is `ACCEPTED` / `REJECTED` / `DEFERRED` / `PARTIALLY_ACCEPTED` / `DUPLICATE` / `INVALIDATED`, the following must remain preserved:

* original reviewer;
* reviewer-local Finding ID;
* original Finding title;
* original severity;
* original evidence class;
* original confidence;
* original problem statement;
* original trigger scenario;
* original consequence;
* original recommendation.

The decision layer adds information.

It must not overwrite the original Finding.

---

## 16. Decision Quality Standard

A valid decision must satisfy all of the following:

```text
[ ] An authorized decision-maker is identified.
[ ] The final status is explicit.
[ ] The decision rationale is specific.
[ ] The relevant evidence is considered.
[ ] The Finding's materiality is addressed.
[ ] The decision consequence is documented.
[ ] Accepted actions are explicit.
[ ] Rejected issues have a reason.
[ ] Deferred issues have follow-up conditions.
[ ] Duplicate issues reference the authoritative Finding.
[ ] Invalidated issues include invalidation evidence.
[ ] The original Finding remains traceable.
```

If any required condition is missing, the decision is incomplete.

---

## 17. Decision Priority

When multiple Findings affect the same Design Spec area, decisions should be made in the following order:

1. P0 Findings.
2. P1 Findings.
3. P2 Findings.

Within the same severity:

1. Findings affecting core business correctness.
2. Findings affecting data integrity.
3. Findings affecting security or authorization.
4. Findings affecting production availability.
5. Findings affecting recoverability.
6. Findings affecting compatibility.
7. Findings affecting operational burden.
8. Findings affecting maintainability.
9. Optimization opportunities.

A lower-severity Finding must not be used to justify ignoring a higher-severity Finding.

---

## 18. Conflicting Findings

If consolidated Findings conflict with each other, do not silently choose one.

The conflict must be explicitly recorded.

Example: `CR-004` ("the Design Spec should reject duplicate operations") vs `CR-007` ("the Design Spec must allow duplicate operations for separate business events").

The decision process must determine:

* whether the Findings are actually contradictory;
* whether they apply to different contexts;
* whether one rule has precedence;
* whether the Design Spec is missing a distinguishing condition.

If the conflict cannot be resolved, the relevant Finding status should remain `PENDING_DECISION` until an authorized decision-maker resolves the conflict.

---

## 19. Decision Changes

A decision may change when:

* new evidence becomes available;
* the Design Spec scope changes;
* system constraints change;
* business priorities change;
* a previously rejected risk becomes material;
* a previously deferred issue becomes relevant;
* a previous decision is shown to be incorrect.

A changed decision must preserve the history.

Example:

```text
Decision History:

2026-07-19
Status: REJECTED
Reason: Scenario considered impossible under current constraints.

2026-09-01
New Evidence: External integration scope expanded.

2026-09-02
Status: ACCEPTED
Reason: The previously impossible scenario is now possible.
```

Do not overwrite the original decision.

---

## 20. Decision Record Example

```markdown
## CR-003 — Duplicate Operation Behavior Is Undefined

### Source Findings

- PR-001
- SC-003
- TD-002

### Severity

P0

### Evidence Class

MATERIAL_RISK

### Confidence

HIGH

### Decision Status

ACCEPTED

### Decision Owner

Spec Owner

### Decision

Accept the Finding.

The Design Spec must explicitly define the business behavior and
system constraint for repeated requests representing the same logical
operation.

### Decision Rationale

The Product Reviewer identified that duplicate submission behavior is
undefined. The System Critic identified that a timeout followed by a retry
may produce duplicate side effects. The Test Designer identified that the
Design Spec does not define an objective way to verify the number of resulting
business operations.

The three Findings represent the same underlying gap: the Design Spec does not
define the semantics of repeated requests for one logical operation.

The consequence may include duplicate business effects and inconsistent
downstream data.

### Accepted Scope

- Definition of one logical operation.
- Definition of repeated-request behavior.
- Definition of the expected number of business effects.
- Definition of verification criteria.

### Required Action

Update the Design Spec with explicit duplicate-operation semantics and
observable verification requirements.

The implementation approach remains a subsequent design decision.

### Decision Consequence

Design Spec:
Must be updated.

Implementation Requirements:
Must implement the defined duplicate-operation behavior.

Testing Requirements:
Must verify repeated requests and unknown-timeout retry scenarios.

Operational Requirements:
Must provide sufficient evidence to diagnose unexpected duplicate effects.

Future Review Work:
The updated Design Spec must be re-reviewed if the business semantics change.

### Decision Timestamp

<timestamp>

### Decision History

None.
```

---

## 21. Decision Record for Rejection

```markdown
## CR-006 — Concurrent Modification Conflict

### Severity

P1

### Decision Status

REJECTED

### Decision Owner

Technical Owner

### Decision

Reject the Finding for the current Design Spec.

### Decision Rationale

The Finding assumes that multiple independent actors can modify the same
entity concurrently. The current business and system constraints allow only
one authorized modification workflow for the affected entity.

The described trigger scenario is therefore not applicable to the current
scope.

### Rejection Ground

INAPPLICABLE_SCENARIO

### Decision Consequence

Design Spec:
No change required.

Implementation Requirements:
No additional concurrent-modification behavior required for the current scope.

Testing Requirements:
The described concurrency scenario is not required for the current release.

Future Review Work:
Reconsider if multiple independent modification workflows are introduced.

### Decision Timestamp

<timestamp>
```

---

## 22. Decision Record for Deferral

```markdown
## CR-009 — High-Volume Historical Query Risk

### Severity

P1

### Decision Status

DEFERRED

### Decision Owner

Technical Owner

### Decision

Defer the Finding until the high-volume usage scenario enters the active
release scope.

### Decision Rationale

The risk is credible and material at the expected future data volume, but the
current release operates below the volume threshold at which the consequence
becomes significant.

The risk is not considered resolved.

### Deferred Scope

High-volume historical query behavior.

### Deferral Conditions

Reconsider before:

- the system exceeds the defined data-volume threshold;
- the high-volume reporting capability is enabled;
- the current data-retention policy is changed.

### Follow-up Owner

Technical Owner

### Decision Consequence

Design Spec:
No immediate change.

Implementation Requirements:
No immediate change for the current release.

Future Review Work:
The risk must be re-evaluated before the deferral conditions are reached.

### Decision Timestamp

<timestamp>
```

---

## 23. Decision Record for Partial Acceptance

```markdown
## CR-011 — Recovery and Historical Reconciliation Are Undefined

### Severity

P1

### Decision Status

PARTIALLY_ACCEPTED

### Decision Owner

Spec Owner

### Decision

Partially accept the Finding.

### Accepted Scope

The Design Spec must define recovery behavior after a partially completed
operation.

### Deferred Scope

Historical reconciliation is deferred until the reporting requirements are
finalized.

### Rejected Scope

The proposed manual recovery workflow is rejected because the current
operational model does not permit manual intervention for this process.

### Decision Rationale

The Finding contains three separable issues. Recovery behavior is required
for the current release. Historical reconciliation depends on future
reporting requirements. The proposed manual recovery approach is not
compatible with the current operational constraints.

### Decision Consequence

Design Spec:
Must define recovery behavior.

Implementation Requirements:
Must implement the accepted recovery rule.

Testing Requirements:
Must verify partial completion and recovery.

Future Review Work:
Historical reconciliation must be reconsidered when reporting requirements
are finalized.

### Decision Timestamp

<timestamp>
```

---

## 24. Decision Record for Duplicate

```markdown
## CR-014 — Retry May Produce Duplicate Side Effects

### Severity

P0

### Decision Status

DUPLICATE

### Decision Owner

Review Orchestrator

### Decision

Mark this Finding as a duplicate of CR-003.

### Decision Rationale

CR-003 already represents the same substantive problem: repeated requests for
one logical operation have undefined business semantics and may produce
duplicate effects.

Resolving CR-003 resolves the problem represented by CR-014.

### Duplicate Of

CR-003

### Decision Consequence

The decision for CR-003 governs this issue.

The original System Critic Finding SC-003 remains preserved as a source Finding
for traceability.

### Decision Timestamp

<timestamp>
```

---

## 25. Decision Record for Invalidation

```markdown
## CR-018 — External API May Return Duplicate Records

### Severity

P1

### Decision Status

INVALIDATED

### Decision Owner

Technical Owner

### Decision

Invalidate the Finding.

### Decision Rationale

The Finding was based on the assumption that the external API permits
duplicate record identifiers.

The confirmed API contract explicitly guarantees globally unique identifiers
and rejects duplicate creation requests.

The factual premise of the Finding is therefore no longer valid.

### Invalidation Evidence

Confirmed external API contract version 3.2 guarantees globally unique record
identifiers and rejects duplicate creation requests.

### Decision Consequence

Design Spec:
No change required.

Implementation Requirements:
No additional duplicate-record handling is required for the described scenario.

Testing Requirements:
The original duplicate-record scenario is not required unless the external
API contract changes.

### Decision Timestamp

<timestamp>
```

---

## 26. Pending Decision

A Finding must remain PENDING_DECISION when:

* no authorized decision-maker has reviewed it;
* required evidence is missing;
* conflicting business decisions exist;
* the Finding cannot yet be classified as accepted, rejected, deferred, duplicate, or invalidated.

PENDING_DECISION is not a final outcome.

A review process must track unresolved Pending Findings explicitly.

Example:

```markdown
## CR-021 — Business Ownership Conflict

### Decision Status

PENDING_DECISION

### Blocking Reason

The Product Owner and Technical Owner have conflicting definitions of the
authoritative source of customer status.

### Required Next Decision

An authorized business owner must define the authoritative source and
precedence rule.

### Decision Owner

Pending assignment
```

---

## 27. Final Decision Output Contract

The final decision output must contain:

```text
Decision Output
    ├── Design Spec Identifier
    ├── Review Identifier
    ├── Decision Summary
    ├── Finding Decisions
    │   ├── Consolidated Finding ID
    │   ├── Source Finding IDs
    │   ├── Severity
    │   ├── Decision Status
    │   ├── Decision Owner
    │   ├── Decision
    │   ├── Decision Rationale
    │   ├── Required Action
    │   ├── Decision Consequence
    │   └── Decision History
    └── Final Review State
```

The final review output must not only state:

```text
3 issues accepted
2 issues rejected
```

It must preserve the relationship:

```text
Source Finding
      ↓
Consolidated Finding
      ↓
Decision
      ↓
Required Change
```

---

## 28. Final Review State

After all consolidated Findings have received decisions, determine the final review state.

### BLOCKED

Use when one or more unresolved P0 Findings remain.

```text
P0 Finding
    ↓
PENDING_DECISION
or
P0 Finding
    ↓
ACCEPTED but required action not yet incorporated
    ↓
BLOCKED
```

### CHANGES_REQUIRED

Use when accepted P1 or P2 Findings require changes before the Design Spec can proceed.

### CONDITIONAL_APPROVAL

Use when the Design Spec may proceed under explicitly documented conditions.

Conditions may include:

* accepted risks;
* required follow-up;
* deferred Findings;
* operational constraints;
* required tests.

### APPROVED

Use only when:

* all blocking Findings are resolved;
* required changes have been incorporated;
* remaining risks are explicitly accepted or appropriately deferred;
* no unresolved decision prevents the next phase.

### INCOMPLETE

Use when the review process itself is incomplete.

Examples:

* Findings have not all been consolidated;
* decisions are missing;
* decision authority is unclear;
* source traceability is broken.

---

## 29. Final Review State Rules

The final review state must be determined from the Finding decisions.

The following rules apply:

```text
Any unresolved P0 Finding
        ↓
BLOCKED
```

```text
Any accepted P0 Finding whose required action
has not yet been incorporated
        ↓
BLOCKED
```

```text
No unresolved P0
+
Accepted P1/P2 changes remain outstanding
        ↓
CHANGES_REQUIRED
```

```text
No blocking Finding
+
Explicit conditions remain
        ↓
CONDITIONAL_APPROVAL
```

```text
All required changes incorporated
+
No unresolved blocking decision
        ↓
APPROVED
```

```text
Review records incomplete
        ↓
INCOMPLETE
```

A review must not be marked APPROVED merely because the number of accepted Findings is low.

---

## 30. Final Decision Quality Gate

Before finalizing the review, verify:

```text
[ ] Every consolidated Finding has a decision status.
[ ] Every decision has an authorized decision owner.
[ ] Every accepted Finding has a required action.
[ ] Every rejected Finding has a specific rejection rationale.
[ ] Every deferred Finding has explicit deferral conditions.
[ ] Every partially accepted Finding identifies accepted and non-accepted scope.
[ ] Every duplicate Finding references an authoritative Finding.
[ ] Every invalidated Finding includes invalidation evidence.
[ ] Every pending decision is explicitly visible.
[ ] Source Findings remain traceable.
[ ] Decision consequences are documented.
[ ] Decision history is preserved.
[ ] The final review state follows the defined rules.
```

If any required condition is missing, the final decision record is incomplete.

---

## 31. Protocol Completion Criteria

The Decision Protocol is complete when:

* every consolidated Finding has an explicit final or pending status;
* every decision has an identified decision owner;
* every decision has a documented rationale;
* every accepted issue has a traceable required action;
* every rejected issue has a documented reason;
* every deferred issue has a follow-up condition;
* every partially accepted issue has explicit scope boundaries;
* every duplicate issue references the authoritative Finding;
* every invalidated issue includes supporting evidence;
* every unresolved issue remains visible;
* every decision remains traceable to its source Findings;
* every decision change preserves historical records;
* the final review state is determined according to the protocol.

This protocol defines how review Findings become explicit, traceable decisions.

It does not define how Findings are discovered or consolidated.
