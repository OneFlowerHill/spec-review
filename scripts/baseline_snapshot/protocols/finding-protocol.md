# Finding Protocol

## Purpose

This protocol defines the universal contract for findings produced by independent Design Spec reviewers.

A **Finding** is a structured statement of a material problem, risk, ambiguity, contradiction, or verification gap identified during the review of a Design Spec.

This protocol defines only the structure and quality requirements of an individual Finding.

This protocol does not define:

* how Product Reviewers identify product problems;
* how System Critics identify system risks;
* how Test Designers identify verification gaps;
* how multiple findings are consolidated;
* whether a finding should ultimately be accepted;
* whether the Design Spec should be approved.

Those responsibilities belong to the reviewer roles, the Consolidation Protocol, and the Decision Protocol.

---

## 1. Definition of a Finding

A Finding must identify a concrete problem in the relationship between:

```text
Design Spec
    ↓
Expected Behavior
    ↓
Actual or Possible Scenario
    ↓
Material Consequence
```

A Finding must answer:

1. What is wrong or missing?
2. Under what condition does the problem appear?
3. What happens because of it?
4. Why does the consequence matter?
5. What evidence supports the Finding?
6. What minimum clarification, rule, constraint, or decision is required?

A Finding is not:

* a general opinion;
* a design preference;
* a vague concern;
* a duplicate of another Finding;
* a request for additional detail without a material reason;
* a theoretical possibility with no credible consequence;
* an implementation suggestion without an identified problem.

---

## 2. Finding Quality Standard

A valid Finding must contain a causal chain:

```text
Trigger Condition
        ↓
Design Spec Behavior
        ↓
Problem
        ↓
Consequence
```

Weak Finding:

```text
The architecture may be difficult to maintain.
```

Strong Finding:

```text
The Design Spec introduces three independently configurable retry policies
for the same operation. When the external dependency is unavailable, each
layer retries independently, multiplying requests during the outage. This
can increase downstream load and prolong recovery.
```

A strong Finding identifies:

```text
Trigger:
External dependency unavailable

Design Spec Behavior:
Multiple independent retry policies

Problem:
Retry multiplication

Consequence:
Increased outage impact
```

---

## 3. Evidence Requirement

Every Finding must distinguish what is known from what is inferred.

A Finding must be based on one or more of:

* explicit text in the Design Spec;
* existing system behavior;
* existing code;
* existing data model;
* existing API contract;
* existing deployment constraint;
* existing operational constraint;
* a concrete logical consequence of the Design Spec.

Do not present an assumption as a fact.

### Evidence Class

Every Finding must use one of the following Evidence Classes.

#### CONFIRMED_DEFECT

Use when the problem is directly demonstrated by the available evidence.

Examples:

* the Design Spec contains contradictory rules;
* a required state transition is impossible;
* an existing API cannot support the proposed behavior;
* the Design Spec explicitly lacks a required outcome;
* the defined data flow creates a known inconsistency.

#### MATERIAL_RISK

Use when the problem is not directly proven as an existing defect, but the Design Spec creates a credible and consequential risk.

Examples:

* failure behavior is undefined;
* a dependency failure may produce an unknown outcome;
* a future data volume may exceed an implicit limit;
* an important behavior lacks observable verification.

#### DESIGN_PREFERENCE

Use only internally during analysis.

Do not normally output a Finding based solely on a Design Preference.

A different design is not automatically a problem.

#### CONFIRMED_GAP

Use when a specific verification gap has been identified — a required behavior
has no observable test, or an acceptance criterion cannot be objectively verified.

This Evidence Class is primarily used by the Test Designer role.

Examples:

* an acceptance criterion describes desired behavior but provides no
  observable outcome to verify against;
* a required state transition has no test coverage and no production
  telemetry;
* a business rule is stated but no input/output combination can confirm
  compliance.

---

## 4. Finding Severity

Every Finding must have exactly one severity.

### P0

Critical risk.

A P0 Finding can cause:

* data loss;
* data corruption;
* security breach;
* critical authorization bypass;
* major production outage;
* irrecoverable system state;
* failure of a core business workflow;
* inability to recover from a normal failure.

P0 Findings should normally block implementation or require explicit resolution before the affected capability proceeds.

### P1

Major risk.

A P1 Finding can cause:

* significant business failure;
* major operational burden;
* substantial data inconsistency;
* serious security weakness;
* major user impact;
* significant maintenance cost;
* serious compatibility failure;
* high-impact recovery failure.

P1 Findings should normally be resolved before implementation.

### P2

Moderate risk or improvement opportunity.

A P2 Finding can cause:

* bounded edge-case failure;
* moderate operational burden;
* limited maintainability problems;
* non-critical observability gaps;
* moderate user confusion;
* recoverable technical debt.

P2 Findings may be deferred if the risk is explicitly understood.

Do not inflate P2 issues to higher severities.

---

## 5. Confidence

Every Finding must include a confidence level.

### HIGH

The Finding is directly supported by explicit Design Spec content, existing system evidence, or a clear logical contradiction.

### MEDIUM

The Finding is strongly plausible but depends on one or more assumptions that are not fully verified.

### LOW

The Finding is possible but depends on significant uncertainty.

Low-confidence Findings should normally not be prioritized over higher-confidence Findings with similar consequences.

Do not use confidence to reduce severity automatically.

A low-confidence P0 risk may still require explicit investigation.

---

## 6. Finding Identity

Each reviewer assigns a reviewer-local ID.

Product Reviewer:

```text
PR-001
PR-002
PR-003
```

System Critic:

```text
SC-001
SC-002
SC-003
```

Test Designer:

```text
TD-001
TD-002
TD-003
```

The reviewer-local ID is stable within that review output.

The Consolidation phase may assign a global ID:

```text
CR-001
CR-002
CR-003
```

The global ID represents the consolidated issue, not an individual reviewer's Finding.

Do not manually assign global IDs during independent review.

---

## 7. Required Finding Structure

Every Finding must follow this structure:

```markdown
## <LOCAL_ID> — <Short Descriptive Title>

### Severity

P0 / P1 / P2

### Evidence Class

CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE

### Confidence

HIGH / MEDIUM / LOW

### Location

Identify the relevant location in the Design Spec.

This may be:

- section;
- requirement;
- workflow;
- component;
- data flow;
- state transition;
- API;
- integration;
- deployment behavior;
- operational process.

If an exact location cannot be identified, state the relevant conceptual area.

### Problem

State the exact problem.

The Problem must be specific enough that another reviewer can understand what is wrong without reconstructing the entire analysis.

Do not use vague statements such as:

- "This may cause issues."
- "This is risky."
- "This should be improved."
- "The design is complex."

### Trigger Scenario

Describe the concrete condition that exposes the problem.

Use:

1. Preconditions.
2. Action or event.
3. Relevant system behavior.
4. Point at which the problem occurs.

### Causal Chain

Explain:

Trigger Condition
    ↓
Design Spec Behavior
    ↓
Problem
    ↓
Consequence

### Consequence

Describe the concrete impact.

Possible impacts include:

- data loss;
- data corruption;
- incorrect business result;
- security exposure;
- production outage;
- user confusion;
- operational burden;
- maintenance cost;
- compatibility failure;
- inability to verify correctness.

### Evidence

State the evidence supporting the Finding.

Clearly distinguish:

- explicit evidence;
- existing system evidence;
- logical inference;
- assumption.

### Recommendation

Describe the minimum clarification, rule, constraint, or decision required to address the Finding.

The Recommendation must not unnecessarily prescribe implementation details.

Do not redesign the entire Design Spec.

### Reviewer Notes

Optional.

Use only for:

- important uncertainty;
- assumptions;
- evidence limitations;
- questions requiring later investigation.
```

---

## 8. Problem Statement Requirements

The Problem section must describe the gap, not the solution.

Bad:

```text
Add Redis to prevent duplicate requests.
```

This is not a valid Problem statement.

Good:

```text
The Design Spec does not define how duplicate requests for the same logical
operation are identified or handled. A retry after an unknown timeout may
therefore create a second business operation.
```

The problem is:

```text
Undefined duplicate-operation behavior
```

The Recommendation may later state:

```text
Define the business rule and system constraint that guarantees one logical
operation produces the intended number of business effects.
```

---

## 9. Trigger Scenario Requirements

Every Finding must include a credible trigger scenario.

The scenario should be concrete enough to answer:

> Under what conditions would this problem actually occur?

Good:

```text
1. User submits the operation.
2. The external dependency completes the operation.
3. The response is lost due to a timeout.
4. The caller retries.
5. The Design Spec does not define whether the second request is treated as a duplicate.
```

Weak:

```text
In some edge cases, duplicate requests may occur.
```

The trigger scenario should not invent conditions incompatible with the Design Spec.

---

## 10. Consequence Requirements

The consequence must be material.

Do not stop at:

```text
This could cause an error.
```

Explain the actual impact:

```text
Duplicate request
    ↓
Two business operations created
    ↓
Incorrect customer history
    ↓
Subsequent reporting and automation use incorrect data
```

The consequence should identify:

* who or what is affected;
* what becomes incorrect;
* whether the problem is recoverable;
* whether the problem can be detected;
* whether the impact accumulates over time.

---

## 11. Recommendation Requirements

A Recommendation should describe the minimum decision required to remove ambiguity or risk.

Prefer:

```text
Define the authoritative source of truth and the expected behavior when the
two systems disagree.
```

Over:

```text
Rewrite the architecture so that Service A owns the database and Service B
uses Kafka.
```

The Recommendation should answer:

> What must be clarified or constrained before this risk can be considered resolved?

It should not automatically answer:

> What exact code should engineering write?

---

## 12. Finding Independence

Independent Reviewers must create Findings independently.

A reviewer must not:

* read another reviewer's findings;
* copy another reviewer's wording;
* suppress a Finding because another reviewer may discover it;
* manufacture a different Finding merely to avoid overlap.

Different reviewers may identify the same underlying problem from different perspectives.

For example:

Product Reviewer:

```text
PR-001:
Duplicate submission has no defined business outcome.
```

System Critic:

```text
SC-003:
Retry behavior can create duplicate side effects.
```

Test Designer:

```text
TD-002:
The system has no objective way to verify whether one logical operation
produced one result.
```

These are valid independent Findings.

The Consolidation phase determines whether they represent:

```text
One root issue
```

or:

```text
Multiple related issues
```

---

## 13. Overlap and Duplication

Do not attempt to perform global deduplication during independent review.

However, each reviewer must avoid duplicating the same issue within their own output.

Before creating a new Finding, ask:

> Is this genuinely a separate problem, or merely another consequence of an existing Finding?

If it is the same root problem with a different consequence, prefer one Finding with a complete causal chain.

Create separate Findings when:

* the trigger condition is materially different;
* the root cause is materially different;
* the consequence is independently significant;
* resolving one issue would not resolve the other.

---

## 14. Finding Boundaries

A Finding should normally represent one primary problem.

Avoid combining unrelated issues:

```text
The Design Spec has unclear authorization, weak retry handling,
poor observability, and complex configuration.
```

This should become separate Findings if each issue is independently material.

A Finding may include multiple symptoms when they share one root cause.

Example:

```text
Undefined ownership of the authoritative state causes:

- conflicting data;
- inconsistent reports;
- ambiguous recovery.
```

This can remain one Finding if the root cause is the same.

---

## 15. Severity Must Reflect Consequence

Do not assign severity based on how technically interesting the problem is.

Severity should reflect the consequence.

For example:

```text
Complex configuration
```

is not automatically P1.

But:

```text
Complex configuration causes operators to apply inconsistent rules,
which silently routes users to the wrong business workflow.
```

may be P1.

Always evaluate:

```text
Problem
    ↓
Impact
    ↓
Severity
```

---

## 16. Confidence Must Reflect Evidence

Do not use HIGH confidence merely because the Finding sounds plausible.

Use:

```text
HIGH
```

when the evidence directly supports the Finding.

Use:

```text
MEDIUM
```

when the causal chain is strong but one or more assumptions remain.

Use:

```text
LOW
```

when the Finding depends heavily on uncertain conditions.

Example:

```text
The Design Spec explicitly states that both systems independently update the
same business status.

Confidence: HIGH
```

Example:

```text
The Design Spec may experience stale reads under high concurrency, but the actual
transaction isolation behavior is not yet known.

Confidence: MEDIUM
```

---

## 17. Finding Quality Gate

Before outputting a Finding, verify:

```text
[ ] Is there a concrete problem?
[ ] Is there a credible trigger scenario?
[ ] Is there a causal chain?
[ ] Is the consequence material?
[ ] Is the evidence identified?
[ ] Is fact distinguished from inference?
[ ] Is the severity justified?
[ ] Is confidence justified?
[ ] Is the recommendation focused on the minimum required decision?
[ ] Is this a separate problem rather than a duplicate within this review?
```

If any answer is "No", revise or discard the Finding.

---

## 18. Output Rules

Independent reviewers must:

* output only their own review Findings;
* use reviewer-local IDs;
* follow the required Finding structure;
* prioritize material issues;
* distinguish evidence from inference;
* avoid duplicate Findings within their own output;
* avoid design preferences presented as risks;
* avoid implementation details unless necessary to explain the risk.

Independent reviewers must not:

* consolidate other reviewers' Findings;
* assign global Finding IDs;
* decide whether a Finding is accepted;
* decide whether a Finding is rejected;
* modify the Design Spec;
* produce the final review decision.

---

## 19. Maximum Finding Count

Each reviewer should normally output no more than 5 Findings.

The reviewer may output fewer than 5 Findings.

Do not create weak Findings to reach 5.

The priority order is:

1. P0 over P1.
2. P1 over P2.
3. Higher material consequence.
4. Higher likelihood.
5. Higher confidence when consequences are comparable.
6. Risks that become more expensive to fix after implementation.

---

## 20. Final Reviewer Output Contract

The output of an independent reviewer must be a collection of Findings conforming to this protocol.

Conceptually:

```text
Review Output
    ├── Reviewer
    ├── Review Scope
    ├── Findings
    │   ├── Local ID
    │   ├── Severity
    │   ├── Evidence Class
    │   ├── Confidence
    │   ├── Location
    │   ├── Problem
    │   ├── Trigger Scenario
    │   ├── Causal Chain
    │   ├── Consequence
    │   ├── Evidence
    │   ├── Recommendation
    │   └── Reviewer Notes
    └── Completion Status
```

The reviewer may include a short review header containing:

```text
Reviewer:
Review Scope:
Source Design Spec:
```

The reviewer should not include:

* general praise;
* a summary of strengths;
* unrelated architecture discussion;
* a complete implementation plan;
* a final approval decision.

---

## 21. Protocol Completion Criteria

A Finding Protocol-compliant review is complete when:

* every Finding has a reviewer-local ID;
* every Finding has a severity;
* every Finding has an evidence class;
* every Finding has a confidence level;
* every Finding identifies a location;
* every Finding describes a concrete problem;
* every Finding contains a credible trigger scenario;
* every Finding contains a causal chain;
* every Finding describes a material consequence;
* every Finding identifies supporting evidence;
* every Finding contains a focused recommendation;
* facts and inferences are distinguished;
* design preferences are not presented as material risks;
* duplicate Findings within the same review have been removed;
* no global consolidation decision has been made.

This protocol defines the Finding contract.

It does not define consolidation or final decision-making.
