# Proposal Review Skill v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the proposal-review skill from a multi-terminal manual process into a single-entry subagent-orchestrated review workflow with cross-round statistics.

**Architecture:** Single SKILL.md entry point dispatches 3 subagents in parallel (Product Reviewer, System Critic, Test Designer), each with isolated context. Main agent collects results, consolidates findings, writes output files, and hands off to superpowers via structured instructions.

**Tech Stack:** Claude Code Skill (Markdown), Agent tool (subagent dispatch), YAML indexes (machine-readable metadata)

## Global Constraints

- Finding IDs: Consolidated = `CR-001`, Reviewer-local = `PR-001` / `SC-001` / `TD-001`
- Decision States (authoritative): PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
- Final Review States: BLOCKED, CHANGES_REQUIRED, CONDITIONAL_APPROVAL, APPROVED, INCOMPLETE
- Test Designer Finding Type field: ACCEPTANCE_TEST, UNTESTABLE_REQUIREMENT, BLIND_SPOT
- Output path: `docs/superpowers/reviews/<proposal-stem>/YYYY-MM-DD-review-NNN/`
- Stem extraction: remove leading `YYYY-MM-DD-` prefix and `.md` suffix from proposal filename
- MISSING hard rule: if any review is MISSING, final review state = INCOMPLETE
- All `RV-` references replaced with `CR-` across entire project
- Removed status values: OPEN, READY_FOR_DECISION, RESOLVED, SUPERSEDED
- No automated decision-making — skill stops at consolidated review output
- No Phase 5 detail — one-line note that proposal revision is owner's responsibility

## File Structure

```
SKILL.md                              # REWRITE — main entry point
roles/
  product-reviewer.md                 # UNCHANGED
  system-critic.md                    # UNCHANGED
  test-designer.md                     # MODIFY — TD-001 + Finding Type
protocols/
  finding-protocol.md                 # UNCHANGED
  consolidation-protocol.md           # MODIFY — RV→CR, add Finding Type field
  decision-protocol.md                # MODIFY — RV→CR, add supersession note
  review-orchestrator-protocol.md     # CREATE — orchestration rules
templates/
  product-review.md                   # UNCHANGED
  system-review.md                    # UNCHANGED
  test-review.md                      # REWRITE — TD-001 unified format
  consolidated-review.md              # MODIFY — CR-ID, states, new sections
  index.md                            # CREATE — cross-round summary
CLAUDE.md                             # MODIFY — update docs
```

---

### Task 1: ID Prefix Migration (RV→CR) in Protocols

**Rationale:** The ID prefix is the foundation that all other files reference. Fix it first so subsequent tasks use correct IDs consistently.

**Files:**
- Modify: `protocols/consolidation-protocol.md`
- Modify: `protocols/decision-protocol.md`

**Interfaces:**
- Produces: `CR-001` as the canonical Consolidated Finding ID format across both protocols

- [ ] **Step 1: Replace all RV- references with CR- in consolidation-protocol.md**

In `protocols/consolidation-protocol.md`, replace every occurrence of `RV-` with `CR-`. This includes:
- Section 3 (Output Contract): `RV-001`, `RV-002`, `RV-003` → `CR-001`, `CR-002`, `CR-003`
- Section 4 (Consolidated Finding Identity): all `RV-` examples and format definition
- Section 5 (Source Finding Preservation): `RV-001` example
- Section 10 (Consolidated Finding Structure): `RV-<NUMBER>` → `CR-<NUMBER>`
- Section 11 (Consolidated Severity): `RV-001`, `RV-002` examples
- Section 20 (Consolidation Priority): `RV-007`, `RV-002`, `RV-004` examples
- Section 22 (Source Finding Relationship Matrix): `RV-001`, `RV-002` in table
- Section 24 (Consolidated Review Output Example): all `RV-` references in the full example

Also add a `Finding Type` field to the Consolidated Finding Structure in Section 10, after `Source Findings`:

```markdown
### Finding Type

ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT / N/A

Required only when a source Finding is from the Test Designer.
Use N/A for Findings sourced exclusively from Product or System reviews.
This field preserves the semantic distinction of Test Designer findings
during consolidation.
```

- [ ] **Step 2: Replace all RV- references with CR- in decision-protocol.md**

In `protocols/decision-protocol.md`, replace every occurrence of `RV-` with `CR-`. This includes:
- Section 5 (Required Decision Structure): `RV-<NUMBER>` → `CR-<NUMBER>`
- Section 10 (Partial Acceptance): `RV-011` example
- Section 11 (Duplicate Decision): `RV-014`, `RV-003` examples
- Section 14 (Decision Traceability): `RV-003` example
- Section 18 (Conflicting Findings): `RV-004`, `RV-007` examples
- Section 20 (Decision Record Example): `RV-003` full example
- Section 22 (Decision Record for Deferral): `RV-009`
- Section 24 (Decision Record for Duplicate): `RV-014`, `RV-003`
- Section 25 (Decision Record for Invalidation): `RV-018`
- Section 26 (Pending Decision): `RV-021`

Also add a supersession note at the top of Section 1 (Decision Principles), after the existing introduction paragraph:

```markdown
**Supersession Note**: The decision state enumeration defined in this protocol
(PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE,
INVALIDATED) supersedes all other state enumerations in the project. Any
conflicting state values in other files (OPEN, READY_FOR_DECISION, RESOLVED,
SUPERSEDED) are deprecated and must not be used.
```

- [ ] **Step 3: Verify no RV- references remain**

Search both files for any remaining `RV-` text. If found, replace with `CR-`.

- [ ] **Step 4: Commit**

```
git add protocols/consolidation-protocol.md protocols/decision-protocol.md
git commit -m "feat: unify Finding ID prefix from RV- to CR- across protocols

- Replace all RV- references with CR- in consolidation-protocol.md
- Replace all RV- references with CR- in decision-protocol.md
- Add Finding Type field to Consolidated Finding Structure
- Add supersession note to decision-protocol.md

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Test Designer Role and Template Rewrite

**Rationale:** The Test Designer's AT/AC/BL three-section format is incompatible with the Consolidation Protocol. Unify to TD-001 + Finding Type before other files reference it.

**Files:**
- Modify: `roles/test-designer.md`
- Rewrite: `templates/test-review.md`

**Interfaces:**
- Consumes: Finding Type enum (ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT) from Task 1
- Produces: `TD-001` Finding format that is structurally compatible with PR/SC formats

- [ ] **Step 1: Update roles/test-designer.md — Finding ID and Format sections**

In `roles/test-designer.md`, make these specific changes:

1. **Finding ID section** (around line 689-703): Change the example from `TD-001 / TD-002 / TD-003` (keep this, it's already correct) and remove any mention of AT/AC/BL. The current file already uses TD-001, so this section needs no ID change, but add a note:

After the existing "Do not assign global Finding IDs." line, add:

```markdown
**Finding Type**: Every Test Designer Finding must include a Finding Type field:

- `ACCEPTANCE_TEST` — A concrete, objectively verifiable test scenario that exposes a verification gap or defines expected behavior
- `UNTESTABLE_REQUIREMENT` — A requirement that cannot currently be objectively verified due to missing acceptance criteria or ambiguous expected outcomes
- `BLIND_SPOT` — A high-risk production scenario that may silently fail and is difficult to detect through ordinary pre-release testing
```

2. **Required Finding Format section** (around line 710-815): Restructure the Finding format. Replace the current format with this unified structure that aligns with PR/SC while retaining test-specific fields:

```markdown
## TD-001 — <Short Descriptive Title>

### Severity

P0 / P1 / P2

### Evidence Class

CONFIRMED_GAP / MATERIAL_RISK

### Confidence

HIGH / MEDIUM / LOW

### Finding Type

ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT

### Location

Identify the relevant requirement, workflow, acceptance criterion, state
transition, data behavior, or operational behavior in the Solution Proposal.

### Verification Gap

State exactly what cannot currently be objectively verified.

For ACCEPTANCE_TEST: Describe the concrete scenario and what the expected
observable result should be.

For UNTESTABLE_REQUIREMENT: Describe the missing acceptance criterion or
ambiguous expected outcome.

For BLIND_SPOT: Describe the production scenario that may silently fail.

### Trigger Scenario

Describe a concrete scenario that exposes the verification gap.

1. Preconditions.
2. Action or event.
3. Expected behavior that should be determined.
4. The point at which the proposal becomes ambiguous or unobservable.

### Expected Verification

State what a tester should be able to verify if the behavior is correctly
defined. This may be a specific business state, API response, database
condition, event, audit record, log, metric, report, or user-visible result.

For BLIND_SPOT findings, describe what would need to be observable in
production to detect the failure.

### Verification Method

Describe exactly where and how the expected result can be verified.

If the proposal does not provide sufficient evidence:

```text
No objective verification method is currently defined.
```

### Consequence

Explain what can happen if the gap remains unresolved:

- incorrect behavior may pass testing;
- a regression may go undetected;
- a production failure may remain silent;
- data corruption may not be detected;
- different testers may reach different conclusions;
- release decisions may be based on subjective judgment.

### Evidence

Cite the relevant requirement or proposal behavior.

Distinguish explicit evidence from inference.

### Recommendation

Describe the minimum acceptance criterion, expected behavior, or observable
evidence that must be defined.

### Reviewer Notes

Optional. Use this only for important uncertainty or assumptions.
```

3. **Example Finding section** (around line 820-893): Replace the example with one using the new format. Keep the same scenario (timeout outcome verification) but restructure:

```markdown
## TD-001 — Timeout Outcome Cannot Be Objectively Verified

### Severity

P1

### Evidence Class

CONFIRMED_GAP

### Confidence

HIGH

### Finding Type

UNTESTABLE_REQUIREMENT

### Location

Proposal: External Operation Retry Behavior

### Verification Gap

The proposal defines that the system retries an operation after a timeout
but does not define how to determine whether the original operation completed
before the timeout. The expected final business state is therefore ambiguous.

### Trigger Scenario

1. The system sends an operation to an external dependency.
2. The request times out.
3. The external dependency may have completed the operation.
4. The system retries the operation.
5. The proposal does not define the expected result if the first operation
   succeeded and the retry is also processed.

### Expected Verification

A tester should be able to determine whether:
- the operation occurred exactly once;
- the operation may legitimately occur more than once;
- the retry is rejected;
- the original operation can be reconciled.

### Verification Method

No objective verification method is currently defined for distinguishing
Original Operation Succeeded from Original Operation Failed after the timeout.

### Consequence

A duplicate operation may pass testing as a valid retry result, or a valid
retry may be incorrectly classified as a failure. Different implementations
may produce different business outcomes while all appearing to satisfy the
proposal.

### Evidence

The proposal defines timeout retry behavior but does not define the expected
business outcome or observable evidence for an unknown completion state.

### Recommendation

Define the expected business outcome for timeout-unknown cases and specify
the observable evidence required to determine whether the operation completed.

### Reviewer Notes

The finding concerns verification ambiguity. The underlying retry architecture
is outside this review's scope.
```

- [ ] **Step 2: Rewrite templates/test-review.md**

Replace the entire file content. The new template uses TD-001 unified Finding format instead of AT/AC/BL three-section format. Key structural changes:
- Remove Section A (AT-001~005), Section B (AC-001~NNN), Section C (BL-001~NNN)
- Replace with a single "Findings" section using TD-001 format
- Each Finding has Finding Type field to preserve AT/AC/BL semantic distinction
- Retain Review Metadata, Review Scope, Testability Coverage table, Unresolved Verification Questions, Review Limitations, Machine-Readable Finding Index

Write the new template:

```markdown
# Test Review

## Review Metadata

### Review ID

<REVIEW_ID>

### Reviewer

yy-test-designer

### Review Type

TEST_REVIEW

### Specification

<PATH_TO_SPECIFICATION>

### Solution Proposal

<PATH_TO_SOLUTION_PROPOSAL>

### Review Date

<YYYY-MM-DD>

### Review Status

COMPLETED

---

## Review Scope

This review evaluates whether the Specification and Solution Proposal can be
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

The purpose of this review is to determine whether the proposal defines
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

<Specific document section, requirement ID, workflow step, or proposal section>

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
4. <The point at which the proposal becomes ambiguous or unobservable>

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

<Cite the relevant requirement or proposal behavior. Distinguish explicit
evidence from inference.>

#### Recommendation

<Minimum acceptance criterion, expected behavior, or observable evidence that
must be defined. Do not redesign the system.>

#### Source References

* <Document section>
* <Requirement ID>
* <Workflow step>
* <Proposal section>

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
answered from the Specification or Solution Proposal.

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
   absent from the Specification or Solution Proposal.

8. Do not redesign the system to make it easier to test.

9. Do not prescribe specific implementation technologies.

10. Do not convert uncertainty into fact.

11. Expected results must not rely on undefined subjective language.

12. The Machine-Readable Finding Index must accurately reflect the detailed
    review sections.

13. The Test Designer must not make final acceptance or rejection decisions.

14. The output must be directly consumable by the Consolidation Protocol.
```

- [ ] **Step 3: Commit**

```
git add roles/test-designer.md templates/test-review.md
git commit -m "feat: unify Test Designer to TD-001 format with Finding Type

- Replace AT/AC/BL three-section format with TD-001 unified Finding format
- Add Finding Type field (ACCEPTANCE_TEST/UNTESTABLE_REQUIREMENT/BLIND_SPOT)
- Align Finding structure with PR/SC formats
- Retain test-specific fields (Expected Verification, Verification Method)
- Update Machine-Readable Index to use TD-IDs

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Consolidated Review Template Updates

**Rationale:** The consolidated-review template must reflect the new CR-ID, unified decision states, new sections from review amendments (Coverage Gap, Consolidator Predispositions, Superpowers Instructions, severity change rationale), and TD-ID references.

**Files:**
- Modify: `templates/consolidated-review.md`

**Interfaces:**
- Consumes: CR-ID format from Task 1, TD-ID format from Task 2, decision states from Task 1
- Produces: Updated template with all new sections that SKILL.md (Task 5) will reference

- [ ] **Step 1: Update consolidated-review.md — ID prefixes and state values**

In `templates/consolidated-review.md`:

1. Replace all `RV-` with `CR-` throughout the file
2. Replace `OPEN` status with `PENDING_DECISION`
3. Replace `READY_FOR_DECISION` with `PENDING_DECISION`
4. Remove `RESOLVED` and `SUPERSEDED` from all status enumerations
5. Replace all `AT-ID / AC-ID / BL-ID` references with `TD-ID`
6. In the YAML index, replace `source_findings.test` AT/AC/BL entries with `td: ["TD-001"]` format

- [ ] **Step 2: Add new sections to consolidated-review.md**

After the `## Consolidation Principles` section and before `# Consolidated Findings`, add:

```markdown
## Consolidator Predispositions

<!--
Record the key judgments formed by the main agent during Phase 1 (Context
Acquisition) that may influence consolidation. This makes potential cognitive
bias auditable.

Example:
- "The proposal assumes synchronous external dependency responses — this
  assumption may bias consolidation toward confirming timeout-related findings."
- "The specification emphasizes data integrity over availability — this
  may affect severity assessment of availability-related findings."
-->

### Predisposition 1

<Description of key judgment and how it might influence consolidation>

---
```

After `# Consolidated Findings` and the CR-001 template structure, add these new required sub-sections within each Consolidated Finding:

After `### Consolidation Decision`, add:

```markdown
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
```

After the `# Cross-Reviewer Conflicts` section, add:

```markdown
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
```

Before the `# Decision Queue` section, add the `# Superpowers Instructions` section:

```markdown
# Superpowers Instructions

<!--
This section tells the reader (typically the proposal owner using superpowers)
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

**Decision options**: ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED

## Decision Template

For each finding, copy and fill in the following in the Decision Records
section below:

```markdown
## DR-<NNN> — CR-<NNN>

### Decision Status

ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

### Decision Owner

<your name or role>

### Decision Rationale

<Why this decision was made — must address the finding's validity, materiality,
and evidence>

### Required Action

<If ACCEPTED: what must change in the proposal>

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
```

- [ ] **Step 3: Update YAML index fields**

In the Machine-Readable YAML Index at the bottom of the file, add these fields:

```yaml
review:
  review_id: "<REVIEW_ID>"
  review_type: "CONSOLIDATED_REVIEW"
  status: "COMPLETED"
  specification: "<PATH_TO_SPECIFICATION>"
  solution_proposal: "<PATH_TO_SOLUTION_PROPOSAL>"
  round: 1
  proposal_stem: "<PROPOSAL_STEM>"
  final_review_state: null
```

Add `severity_escalation` field to each consolidated finding entry:

```yaml
consolidated_findings:
  - id: "CR-001"
    title: "<Short Descriptive Title>"
    severity: "P0|P1|P2"
    confidence: "HIGH|MEDIUM|LOW"
    status: "PENDING_DECISION"
    severity_escalation: false
    severity_change_rationale: null
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
    decision_status: "PENDING_DECISION"
```

- [ ] **Step 4: Commit**

```
git add templates/consolidated-review.md
git commit -m "feat: update consolidated-review template with CR-ID, new sections

- Replace RV- with CR- throughout
- Unify decision states (PENDING_DECISION replaces OPEN/READY_FOR_DECISION)
- Remove RESOLVED and SUPERSEDED status values
- Replace AT/AC/BL references with TD-ID
- Add Consolidator Predispositions section
- Add Coverage Gaps section for MISSING reviews
- Add Superpowers Instructions with decision template and hard rules
- Add Severity Change Rationale mandatory field
- Add round, proposal_stem, final_review_state, severity_escalation to YAML

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Review Orchestrator Protocol and Index Template

**Rationale:** These are the two new files that define how the skill orchestrates the entire review process and tracks cross-round statistics.

**Files:**
- Create: `protocols/review-orchestrator-protocol.md`
- Create: `templates/index.md`

**Interfaces:**
- Consumes: CR-ID format, decision states, MISSING hard rule, stem extraction algorithm, subagent prompt template requirements from all prior tasks
- Produces: Orchestration protocol that SKILL.md (Task 5) will reference; index template that SKILL.md will write to

- [ ] **Step 1: Create protocols/review-orchestrator-protocol.md**

Write the full file:

```markdown
# Review Orchestrator Protocol

## Purpose

This protocol defines the main agent's responsibilities for orchestrating the
proposal review workflow. The main agent (running SKILL.md) coordinates context
acquisition, subagent dispatch, result collection, consolidation, output
generation, and handoff to superpowers.

This protocol does not define how individual reviewers discover findings
(that belongs to the role definitions) or how findings are consolidated
(that belongs to the Consolidation Protocol).

---

## 1. Specification Location Algorithm

### Stem Extraction

Given a proposal filename, extract the stem:

```text
Input:  2026-07-19-customer-operation.md
Step 1: Remove .md extension → 2026-07-19-customer-operation
Step 2: Remove YYYY-MM-DD- prefix → customer-operation
Result: customer-operation
```

The algorithm: remove leading pattern matching `^\d{4}-\d{2}-\d{2}-` and
trailing `.md`.

### Specification Lookup

1. Extract the stem from the proposal filename
2. Search `docs/superpowers/specs/` for a file matching `*-<stem>.md` or
   `<stem>.md`
3. If found, use that path as the specification
4. If not found, check if the user provided an explicit specification path
5. If no specification is found, the review must proceed with
   `specification_status: MISSING` and the final review state must be
   INCOMPLETE

### Hard Rule

A review without a specification cannot produce a complete product review.
If the specification is MISSING:

- The Product Reviewer subagent must be informed that no specification exists
- The consolidated review must record this as a Coverage Gap
- The final review state must be INCOMPLETE

---

## 2. Subagent Prompt Construction

### Standardized Prompt Template

Every subagent prompt must follow this exact structure. The main agent must
NOT include any analytical descriptions, interpretations, or summaries of the
proposal content in the prompt. Only path information differs between prompts.

```markdown
You are the <ROLE_NAME>. Conduct an independent review.

## Your Role Definition

Read and follow: <ROLE_FILE_PATH>

## Input Documents

- Specification: <SPEC_PATH> (or "No specification file found — review
  based on the Solution Proposal alone")
- Solution Proposal: <PROPOSAL_PATH>

## Output Template

Follow the structure defined in: <TEMPLATE_FILE_PATH>

## Output Path

Write your complete review to: <OUTPUT_FILE_PATH>

## Critical Constraints

1. You must NOT read or reference any other reviewer's output
2. You must NOT read the main agent's analysis or internal model
3. You must form your own findings independently
4. You must write your output to the specified path
5. You must include the Machine-Readable Finding Index at the end
```

### What Must NOT Be Included in Subagent Prompts

- The main agent's summary or interpretation of the proposal
- The main agent's identified concerns or hypotheses
- Any hint about what findings might be expected
- References to the other reviewers or their roles
- The main agent's internal model of the problem

### Context Isolation

The Claude Code Agent tool provides context isolation: each subagent
dispatched via the Agent tool does NOT inherit the main agent's conversation
history. Each subagent starts with only the prompt provided to it.

---

## 3. Subagent Dispatch and Collection

### Parallel Dispatch

Dispatch all three subagents in a single response (3 Agent tool calls in one
message). This ensures parallel execution.

### Subagent Configuration

| Subagent | Role File | Template File | Output File |
|----------|-----------|---------------|-------------|
| Product Reviewer | roles/product-reviewer.md | templates/product-review.md | product-review.md |
| System Critic | roles/system-critic.md | templates/system-review.md | system-review.md |
| Test Designer | roles/test-designer.md | templates/test-review.md | test-review.md |

### Result Collection

After all subagents complete:

1. Check that each output file exists
2. Read each output file
3. Validate each output file (see Section 4)

---

## 4. Subagent Failure Handling

### Failure Criteria

A subagent is considered failed if any of:

1. The output file does not exist
2. The output file is empty
3. The output file is missing required fields:
   - Review Metadata section
   - At least one Finding (or explicit statement of no material findings)
   - Machine-Readable Finding Index

### Format Validation Checklist

For each review output, verify:

- [ ] Review ID is present
- [ ] Review Type is present and correct
- [ ] Specification path is present
- [ ] Solution Proposal path is present
- [ ] Review Date is present
- [ ] At least one Finding exists, or an explicit "no material findings" statement
- [ ] Each Finding has a unique ID (PR/SC/TD format)
- [ ] Each Finding has all required fields per its role definition
- [ ] Machine-Readable Index is present and parseable

### Retry Mechanism

If a subagent fails validation:

1. Allow one retry: dispatch the same subagent again with the same prompt
2. If the retry also fails, mark the review as MISSING
3. Do NOT retry more than once

### MISSING Hard Rule

If any review is MISSING:

- The consolidated review must include a Coverage Gap section
- The final review state must be INCOMPLETE
- The consolidation proceeds with available reviews only

### Partial Consolidation Strategy

When one or more reviews are MISSING:

1. Consolidate findings from available reviews
2. For each MISSING review, add a Coverage Gap entry identifying:
   - Which reviewer is missing
   - Which risk dimensions cannot be assessed
   - How this affects consolidation confidence
3. Do NOT speculate about findings the missing reviewer might have produced
4. The Consolidation Summary must reflect the reduced coverage

---

## 5. Source Finding Integrity Check

After consolidation, perform a mathematical consistency check:

```text
Total Source Findings (from all available reviews)
  = Consolidated Finding source references
  + Unmerged Finding count
  + Duplicate/Superseded Finding count
```

If the numbers do not match:

- The final review state must be INCOMPLETE
- The discrepancy must be recorded in the Consolidation Notes
- Possible causes: context window overflow during consolidation, Finding
  format parsing error, or a Finding was silently dropped

This check also serves as the primary defense against context window overflow
(CR-008): if the main agent's context overflowed during consolidation, some
source Findings would be missing from the consolidated output, and the math
would not add up.

---

## 6. Output Generation

### Directory Structure

```text
docs/superpowers/reviews/<proposal-stem>/
├── index.md
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

### Round Number Determination

1. Check if `docs/superpowers/reviews/<proposal-stem>/index.md` exists
2. If yes, read it and count existing rounds → next round number
3. If no, scan the directory for existing `*-review-NNN/` directories
4. If neither exists, this is round 1

### Duplicate Round Prevention

If a review round already exists for today's date, warn the user:

"The review directory already contains a round from today. Proceeding will
create a new round. Do you want to continue?"

---

## 7. Consolidator Predispositions

After Phase 1 (Context Acquisition), the main agent must record its key
judgments in the Consolidator Predispositions section of the consolidated
review. This makes potential cognitive bias auditable.

Record judgments such as:

- Core assumptions identified in the proposal
- Areas of particular concern noted during context acquisition
- Hypotheses about the proposal's strengths or weaknesses
- Any prior knowledge about the domain or system that may influence
  consolidation

Do NOT record specific findings expected from any reviewer.

---

## 8. Handoff to Superpowers

After all output files are written:

1. Report to the user:
   - File paths of all generated files
   - Summary of consolidated findings (count by severity, count by type)
   - Current review state
   - If INCOMPLETE, explain why

2. Point the user to the Superpowers Instructions section in the
   consolidated review for next steps.

3. The skill stops. It does NOT:
   - Make decisions on findings
   - Modify the Solution Proposal
   - Re-read the consolidated review after decisions are recorded
```

- [ ] **Step 2: Create templates/index.md**

Write the full file:

```markdown
# Review Index — <Proposal Name>

## Proposal

<PATH_TO_PROPOSAL>

## Specification

<PATH_TO_SPECIFICATION>

## Review Rounds

| Round | Date | P0 | P1 | P2 | Accepted | Rejected | Deferred | Status |
|-------|------|----|----|-----|----------|----------|----------|--------|
| 1 | YYYY-MM-DD | 0 | 0 | 0 | 0 | 0 | 0 | PENDING_DECISION |

<!--
Status values: PENDING_DECISION, BLOCKED, CHANGES_REQUIRED,
CONDITIONAL_APPROVAL, APPROVED, INCOMPLETE

Update this table after each review round and after decisions are recorded.
-->

## Finding Tracking

| CR-ID | Round | Severity | Title | Decision | Previous Round CR-ID | Source Reviewers | Status |
|-------|-------|----------|-------|----------|---------------------|-----------------|--------|
| CR-001 | 1 | P0 | <title> | PENDING_DECISION | — | PR, SC, TD | PENDING_DECISION |

<!--
Cross-round tracking:
- Previous Round CR-ID: Links to the same finding from a previous round.
  Use "—" for first-round findings.
- Status across rounds:
  - PENDING_DECISION: Awaiting decision
  - CARRIED_FORWARD: DEFERRED from a previous round, still open
  - RESOLVED: ACCEPTED and the required action has been implemented
  - STILL_OPEN: ACCEPTED but the required action has not yet been implemented
  - REJECTED: Not accepted
  - INVALIDATED: Factual basis disproven

"Substantively the same" test: Two findings describe the same fundamental
problem affecting the same component/area. If resolving one would resolve
the other, they are substantively the same.
-->

## Trend

<!--
Update after each round. Compare to the previous round.
-->

- Overall status: PENDING_DECISION
- Open findings: 0 P0, 0 P1, 0 P2
- First review round — no trend data yet.

---

## Machine-Readable Index

```yaml
proposal:
  path: "<PATH_TO_PROPOSAL>"
  stem: "<PROPOSAL_STEM>"

specification:
  path: "<PATH_TO_SPECIFICATION>"
  status: "AVAILABLE|MISSING"

rounds:
  - round: 1
    date: "YYYY-MM-DD"
    directory: "YYYY-MM-DD-review-001"
    findings:
      p0: 0
      p1: 0
      p2: 0
    decisions:
      accepted: 0
      rejected: 0
      deferred: 0
    status: "PENDING_DECISION"
    consolidated_file: "YYYY-MM-DD-review-001/consolidated-review.md"

findings:
  - id: "CR-001"
    round: 1
    severity: "P0|P1|P2"
    title: "<title>"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "SC"
      - "TD"
    status: "PENDING_DECISION"
```
```

- [ ] **Step 3: Commit**

```
git add protocols/review-orchestrator-protocol.md templates/index.md
git commit -m "feat: add review-orchestrator protocol and index template

- review-orchestrator-protocol: subagent dispatch, failure handling,
  integrity check, predispositions, handoff, spec location algorithm
- index.md template: cross-round summary, finding tracking with
  Previous Round CR-ID, trend analysis, machine-readable YAML index

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: SKILL.md Rewrite — Main Entry Point

**Rationale:** This is the core deliverable — the single entry point that orchestrates the entire review flow. All prior tasks have prepared the protocols, templates, and role definitions it references.

**Files:**
- Rewrite: `SKILL.md`

**Interfaces:**
- Consumes: All protocols (consolidation, decision, review-orchestrator), all role definitions, all templates, CR-ID format, decision states, output path convention

- [ ] **Step 1: Write the new SKILL.md**

```markdown
---
name: yy-proposal-review
description: >
  Review a Solution Proposal through three independent perspectives
  (Product, System, Test) in parallel, consolidate findings, and produce
  a structured review document for decision-making. Use when you need
  to review a proposal, or when the user says "review this proposal",
  "审核这个方案", or "run a proposal review".
---

# Proposal Review

## Purpose

Review a Solution Proposal generated from a Specification.

The review evaluates whether the proposed solution:

1. Solves the intended problem.
2. Is logically and technically coherent.
3. Defines behavior precisely enough to be validated.
4. Has sufficient handling for important edge cases and failure conditions.
5. Avoids unnecessary complexity and unjustified assumptions.

The review does not implement the solution.

The review does not modify the Solution Proposal.

The review produces structured findings for a later decision phase.

---

# Conceptual Model

```text
Specification
    ↓
Solution Proposal
    ↓
Independent Multi-Perspective Review (3 subagents in parallel)
    ↓
Finding Consolidation (main agent)
    ↓
Decision (by proposal owner via superpowers)
    ↓
Proposal Revision (outside this skill's scope)
```

---

# Inputs

The primary input is:

```text
docs/superpowers/plans/<proposal>.md
```

The proposal may be associated with:

```text
docs/superpowers/specs/<specification>.md
```

The specification is located using the stem extraction algorithm defined in
`protocols/review-orchestrator-protocol.md`.

If no specification is found, the review proceeds but the final review state
must be INCOMPLETE.

---

# Output

Each execution creates a new Review Round.

Never overwrite a previous Review Round.

Use:

```text
docs/superpowers/reviews/<proposal-stem>/
├── index.md
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

The `<proposal-stem>` is extracted from the proposal filename by removing
the leading `YYYY-MM-DD-` prefix and the `.md` suffix.

Example:

```text
Proposal: 2026-07-19-customer-operation.md
Stem:     customer-operation
Output:   docs/superpowers/reviews/customer-operation/2026-07-19-review-001/
```

---

# Review Phases

## Phase 1: Context Acquisition

1. Read the Solution Proposal path from user input
2. Locate the associated Specification using the stem extraction algorithm
   from `protocols/review-orchestrator-protocol.md`
3. If no specification is found, record `specification_status: MISSING`
4. Read the Specification (if available) and the complete Solution Proposal
5. Construct an internal model of the problem, desired outcome, boundaries,
   and assumptions
6. Record Consolidator Predispositions: key judgments that may influence
   consolidation, as defined in `protocols/review-orchestrator-protocol.md`
7. Determine the output directory and review round number by reading the
   existing `index.md` (if any)
8. If a review round already exists for today's date, warn the user

## Phase 2: Independent Reviews

Dispatch 3 subagents in parallel in a single response.

Follow the standardized prompt template from
`protocols/review-orchestrator-protocol.md` exactly.

Do NOT include any analytical descriptions from the main agent's internal
model in the subagent prompts. Only path information differs between prompts.

### Subagent Dispatch

| Subagent | Role Definition | Output Template | Output File |
|----------|----------------|-----------------|-------------|
| Product Reviewer | `roles/product-reviewer.md` | `templates/product-review.md` | `product-review.md` |
| System Critic | `roles/system-critic.md` | `templates/system-review.md` | `system-review.md` |
| Test Designer | `roles/test-designer.md` | `templates/test-review.md` | `test-review.md` |

### After Subagents Complete

1. Check that each output file exists
2. Validate each output file against the format validation checklist in
   `protocols/review-orchestrator-protocol.md`
3. If a subagent fails validation, allow one retry
4. If the retry also fails, mark the review as MISSING

### MISSING Review Handling

If any review is MISSING:

- The final review state must be INCOMPLETE
- The consolidated review must include a Coverage Gap section
- Consolidation proceeds with available reviews only

## Phase 3: Finding Consolidation

After all available reviews are collected:

1. Read all available review output files
2. Apply the Consolidation Protocol (`protocols/consolidation-protocol.md`):
   - Validate each finding against the Specification and Proposal
   - Normalize finding structure
   - Assign global CR-IDs
   - Preserve original reviewer IDs (PR/SC/TD)
   - Identify duplicate, related, and contradictory findings
   - Generate Conflict Records for contradictory findings
3. Perform the Source Finding Integrity Check:
   - Verify: total source Finding count = consolidated Finding references
     + unmerged Finding count + duplicate/superseded records
   - If mismatch, the final review state must be INCOMPLETE
4. Generate the consolidated review following
   `templates/consolidated-review.md`
5. Include Consolidator Predispositions
6. Include Coverage Gaps (if any review is MISSING)
7. Include Superpowers Instructions section

## Phase 4: Output and Handoff

1. Create the output directory: `YYYY-MM-DD-review-NNN/`
2. Write all 4 review files to the output directory
3. Create or update `index.md` with the new round's statistics
   following `templates/index.md`
4. Report completion to the user with:
   - File paths of all generated files
   - Summary of consolidated findings (count by severity)
   - Current review state
   - If INCOMPLETE, explain why
   - Reference to Superpowers Instructions for next steps

The skill stops here. It does not make decisions on findings, modify the
Solution Proposal, or re-read the consolidated review after decisions.

---

# Decision States

Decision states for consolidated findings are defined in
`protocols/decision-protocol.md`:

```text
PENDING_DECISION
ACCEPTED
REJECTED
DEFERRED
PARTIALLY_ACCEPTED
DUPLICATE
INVALIDATED
```

The decision-protocol enumeration supersedes all other state enumerations
in the project.

---

# Final Review States

```text
BLOCKED              — Unresolved P0 findings
CHANGES_REQUIRED     — Accepted P1/P2 changes outstanding
CONDITIONAL_APPROVAL — No blocking finding, conditions remain
APPROVED             — All required changes incorporated
INCOMPLETE           — Review records incomplete or MISSING reviews
```

---

# Reviewer Boundaries

## Product Reviewer

Evaluate whether the proposed solution solves the right problem.

## System Critic

Evaluate whether the proposed solution is technically and logically coherent.

## Test Designer

Evaluate whether the proposed solution is sufficiently precise and observable
to be validated.

---

# Finding Severity

## P0 — Must resolve before proceeding

Core requirement failure, data corruption, security breach, irrecoverable
system failure.

## P1 — Should normally resolve before implementation

Significant functional failure, major data inconsistency, serious risk.

## P2 — Requires explicit evaluation, may defer

Edge cases, maintainability, moderate risk, incomplete behavior definition.

---

# Completion Criteria

A Review Round is complete only when:

* The Specification has been read (or confirmed MISSING)
* The complete Solution Proposal has been read
* All three independent reviews are complete (or confirmed MISSING)
* All findings have stable CR-IDs
* Duplicate findings are identified
* Conflicting findings are identified
* Unverified assumptions are identified
* The Source Finding Integrity Check passes
* The Consolidated Review is generated
* No finding has been silently discarded
* The index.md is created or updated
```

- [ ] **Step 2: Verify SKILL.md references are consistent**

Check that all file paths referenced in SKILL.md exist or will exist after
all tasks are complete:
- `protocols/review-orchestrator-protocol.md` — created in Task 4 ✓
- `protocols/consolidation-protocol.md` — modified in Task 1 ✓
- `protocols/decision-protocol.md` — modified in Task 1 ✓
- `roles/product-reviewer.md` — unchanged ✓
- `roles/system-critic.md` — unchanged ✓
- `roles/test-designer.md` — modified in Task 2 ✓
- `templates/product-review.md` — unchanged ✓
- `templates/system-review.md` — unchanged ✓
- `templates/test-review.md` — rewritten in Task 2 ✓
- `templates/consolidated-review.md` — modified in Task 3 ✓
- `templates/index.md` — created in Task 4 ✓

- [ ] **Step 3: Commit**

```
git add SKILL.md
git commit -m "feat: rewrite SKILL.md as single entry point with subagent orchestration

- Add YAML frontmatter (name: yy-proposal-review)
- Define 4-phase execution flow with subagent parallel dispatch
- Specify standardized subagent prompt template (no analytical descriptions)
- Include Consolidator Predispositions for bias auditability
- Include Source Finding Integrity Check for overflow detection
- Include MISSING hard rule and Coverage Gap handling
- Include specification location algorithm
- Remove Phase 5 detailed description
- Reference review-orchestrator-protocol for orchestration details

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: CLAUDE.md Update

**Rationale:** Update the project documentation to reflect the new structure, resolved inconsistencies, and changed conventions.

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: All changes from Tasks 1-5

- [ ] **Step 1: Update CLAUDE.md**

In `CLAUDE.md`, make these specific changes:

1. **目录结构与关键文件** section — Update to reflect new/changed files:

Replace the existing directory structure with:

```markdown
## 目录结构与关键文件

```
SKILL.md                          # Skill 主定义（单一入口，4 Phase 流程，subagent 并行审核）
roles/
  product-reviewer.md             # 产品审核员角色（yy-product-reviewer）
  system-critic.md                # 系统批评员角色（yy-system-critic）
  test-designer.md                # 测试设计师角色（yy-test-designer，TD-001 + Finding Type）
protocols/
  finding-protocol.md             # 发现协议——单个 Finding 的结构与质量标准
  consolidation-protocol.md       # 合并协议——跨审核员 Finding 的去重/关联/合并规则（CR-ID）
  decision-protocol.md            # 决策协议——Finding 的最终处置（权威状态枚举来源，CR-ID）
  review-orchestrator-protocol.md # 编排协议——主 agent 的调度、失败处理、完整性校验、交接
templates/
  product-review.md               # 产品审核输出模板（PR-001 格式）
  system-review.md                # 系统审核输出模板（SC-001 格式）
  test-review.md                  # 测试审核输出模板（TD-001 统一格式 + Finding Type）
  consolidated-review.md          # 合并审核输出模板（CR-001 格式 + Superpowers Instructions）
  index.md                        # 跨轮次汇总模板（Review Rounds + Finding Tracking + Trend）
```
```

2. **审核流程** section — Update Phase descriptions:

Change the 5-Phase flow to 4-Phase:

```markdown
### 审核流程（4 个 Phase）

1. **Context Acquisition** — 读取 Specification + Proposal + 相关代码/测试/架构；记录 Consolidator Predispositions
2. **Independent Reviews** — 三个 subagent 并行审核，上下文隔离，互不阅读对方结论
3. **Finding Consolidation** — 合并三个审核的 Finding，去重/关联/识别冲突；执行 Source Finding 完整性校验
4. **Output + Handoff** — 写入审核文件 + 更新 index.md；生成 Superpowers Instructions，等待提案所有者做决策
```

3. **已知不一致** section — Update to reflect resolved issues:

Replace the existing "已知不一致" section with:

```markdown
## 已解决的不一致（v2 已修复）

1. ~~Finding ID 前缀冲突~~ → 统一为 CR-001，所有协议文件 RV→CR 已替换
2. ~~决策状态枚举冲突~~ → 统一为 decision-protocol.md 枚举，废弃 OPEN/READY_FOR_DECISION/RESOLVED/SUPERSEDED
3. ~~Test Designer 输出格式~~ → 统一为 TD-001 + Finding Type 字段，与 PR/SC 格式兼容
4. ~~SKILL.md 缺少 YAML frontmatter~~ → 已添加 name: yy-proposal-review
5. ~~Consolidator 角色文件缺失~~ → 主 agent 执行合并 + review-orchestrator-protocol.md 定义编排规则
6. ~~review-orchestrator 协议缺失~~ → 已创建 protocols/review-orchestrator-protocol.md

## 当前约束（修改时注意）

1. **CR-ID 是唯一的合并 Finding 标识** — 所有文件必须使用 CR-001 格式，不得使用 RV-001
2. **决策状态必须使用 decision-protocol 枚举** — PENDING_DECISION/ACCEPTED/REJECTED/DEFERRED/PARTIALLY_ACCEPTED/DUPLICATE/INVALIDATED
3. **Test Designer Finding 必须包含 Finding Type** — ACCEPTANCE_TEST/UNTESTABLE_REQUIREMENT/BLIND_SPOT
4. **MISSING 审核的硬性规则** — 任一审核 MISSING 时最终状态必须为 INCOMPLETE
5. **合并后必须执行完整性校验** — Source Finding 总数 = 合并引用 + 未合并 + 重复/取代记录
```

4. **审核输出路径** section — Update naming convention:

Replace the existing output path section with:

```markdown
## 审核输出路径

每次审核创建新的 Review Round，不覆盖之前的轮次：

```text
docs/superpowers/reviews/<proposal-stem>/
├── index.md                          # 跨轮次汇总（累积更新）
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

`<proposal-stem>` 从提案文件名提取：移除 `YYYY-MM-DD-` 前缀和 `.md` 后缀。

输入来自：`docs/superpowers/plans/<proposal>.md` 和 `docs/superpowers/specs/<specification>.md`
```

5. **修改原则** section — Add new principles:

After the existing principles, add:

```markdown
- **Subagent 提示词不得包含主代理的分析**——只传递路径信息，禁止注入理解或假设
- **合并后必须记录 Consolidator Predispositions**——使认知偏差可审计
- **完整性校验失败时最终状态必须为 INCOMPLETE**——防止不完整审核被当作完整审核使用
- **严重度变更理由为强制字段**——必须引用具体源 Finding 证据，不得使用泛化推理
```

- [ ] **Step 2: Commit**

```
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md to reflect v2 changes

- Update directory structure with new/changed files
- Update review flow from 5 to 4 phases
- Move resolved inconsistencies to '已解决' section
- Add current constraints section
- Update output path naming convention
- Add new modification principles

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 7: Final Consistency Verification

**Rationale:** After all files are changed, verify that cross-file references are consistent. This is the manual equivalent of a build/test step for a Markdown-only project.

**Files:**
- All modified files from Tasks 1-6

**Interfaces:**
- Consumes: All prior task outputs

- [ ] **Step 1: Verify CR-ID consistency across all files**

Search all `.md` files in the project for any remaining `RV-` text. If found, replace with `CR-`.

- [ ] **Step 2: Verify decision state consistency**

Search all `.md` files for these deprecated state values: `OPEN` (in finding status context), `READY_FOR_DECISION`, `RESOLVED` (as a finding status), `SUPERSEDED` (as a finding status). If found in finding-status context (not general English usage), replace with the correct value per decision-protocol.

- [ ] **Step 3: Verify AT/AC/BL references are updated to TD**

Search all `.md` files for `AT-001`, `AC-001`, `BL-001` pattern references. These should only exist in the consolidated-review.md's comment explaining the migration. If found as active references (not in migration notes), replace with TD-ID.

- [ ] **Step 4: Verify cross-file path references**

Check that every file path referenced in SKILL.md and review-orchestrator-protocol.md actually exists on disk.

- [ ] **Step 5: Commit any fixes**

```
git add -A
git commit -m "fix: final consistency verification — align cross-file references

Co-Authored-By: Claude <noreply@anthropic.com>"
```
