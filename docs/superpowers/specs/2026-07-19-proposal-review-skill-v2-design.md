# Proposal Review Skill v2 Design

## Metadata

- **Date**: 2026-07-19
- **Status**: REVIEWED — CHANGES_REQUIRED
- **Scope**: Rewrite the proposal-review skill to support single-terminal execution, subagent parallel reviews, superpowers handoff, and cross-round statistics
- **Review Round**: 1 (2026-07-19)

---

## 1. Problem Statement

The current proposal-review skill has a solid methodological foundation (role definitions, finding protocols, consolidation rules, decision protocols) but fails on three engineering layers:

1. **Execution layer**: No single entry point. Users must open 4 terminal windows (3 reviewer roles + 1 orchestrator) and manually copy-paste results between them.
2. **Handoff layer**: No mechanism for the skill to hand off the consolidated review to superpowers, and no mechanism for superpowers to write decisions back.
3. **Statistics layer**: No cross-round tracking. Each review round is isolated; users cannot see which findings were accepted/rejected across iterations.

Additionally, the existing files contain internal inconsistencies (ID prefix conflicts, decision state enum conflicts, Test Designer format incompatibility) that prevent the skill from executing correctly.

---

## 2. Design Decisions

### 2.1 Single Entry Skill with Subagent Parallel Reviews

**Decision**: Rewrite `SKILL.md` as the sole entry point. The main agent orchestrates the entire flow: context acquisition, parallel subagent dispatch for three independent reviews, consolidation, and output generation.

**Rationale**: Subagent parallel execution is the only technical solution that satisfies both "single terminal window" and "reviewer independence" (the core methodological requirement that reviewers must not read each other's outputs). Sequential role-switching in a single context would violate independence.

**Trade-off**: Higher token consumption (3 subagents running in parallel) vs. guaranteed reviewer independence. The trade-off is acceptable because the review quality depends on independence.

### 2.2 Manual Decision Write-back

**Decision**: The skill stops after generating the consolidated review. Users make decisions in superpowers and manually write them back to the Decision Records section of `consolidated-review.md`.

**Rationale**: The review skill identifies and organizes problems. The proposal owner decides what to do about them. Automating the decision step would violate the separation of concerns defined in the Decision Protocol. The skill's job is to make the decision process easy, not to make the decisions.

**Support**: Add a `Superpowers Instructions` section to the consolidated review template that explicitly tells the reader what to decide, where to record decisions, and how to determine the final review state.

### 2.3 Main Agent as Consolidator

**Decision**: The main agent (the one running SKILL.md) performs consolidation. No separate consolidator role file is needed.

**Rationale**: Consolidation requires reading all three review outputs, which the main agent already has access to after collecting subagent results. The consolidation rules are defined in `protocols/consolidation-protocol.md`. A separate role file would add complexity without value.

**Support**: Add `protocols/review-orchestrator-protocol.md` to define the main agent's orchestration responsibilities (subagent construction, result collection, consolidation execution, file output, handoff).

**Review Amendment (CR-002)**: The main agent's dual role (context builder + consolidator) introduces theoretical cognitive bias. Mitigate with:

1. **Standardized subagent prompt template**: Input description must be identical across all three subagents (only path information differs). No analytical descriptions from the main agent's internal model.
2. **Consolidator Predispositions**: After Phase 1, the main agent explicitly records its key judgments as "Consolidator Predispositions" in the consolidated review, making bias auditable.
3. **Source Finding integrity check**: After consolidation, verify: Source Finding total count = Consolidated Finding references + Unmerged Finding count + Duplicate/Superseded records (mathematical consistency check).
4. **Context isolation confirmation**: Document that Claude Code Agent tool provides context isolation between subagents — each subagent does not inherit the main agent's conversation history.

### 2.4 Finding ID and State Enum Unification

**Decision**:

- **Consolidated Finding IDs**: Use `CR-001` (Consolidated Review), aligning with the consolidated-review template.
- **Test Designer Finding IDs**: Use `TD-001` with a `Finding Type` field (ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT), replacing the AT/AC/BL three-section format.
- **Decision States**: Use the `decision-protocol.md` enumeration as the authoritative source: PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED.
- **Removed States**: OPEN (use PENDING_DECISION), READY_FOR_DECISION (use PENDING_DECISION), RESOLVED (covered by ACCEPTED + Required Action), SUPERSEDED (use DUPLICATE).
- **Final Review States**: BLOCKED, CHANGES_REQUIRED, CONDITIONAL_APPROVAL, APPROVED, INCOMPLETE.

**Rationale**: Three conflicting enumerations cannot coexist. The decision-protocol enumeration is the most complete and well-reasoned. The Test Designer's AT/AC/BL format creates a structural incompatibility with the Consolidation Protocol, which expects a uniform Finding structure.

### 2.5 Output Path Naming Convention

**Decision**: Use `YYYY-MM-DD-review-NNN/` directories under `docs/superpowers/reviews/<proposal-stem>/`, aligning with superpowers' date-prefix convention.

**Rationale**: The current `review-NNN/` naming does not align with superpowers conventions (which use date prefixes for specs and plans). The `<proposal-stem>` is extracted from the proposal filename by removing the date prefix and `.md` extension.

### 2.6 Phase 5 Scope Reduction

**Decision**: Remove the detailed Phase 5 (Proposal Revision) description from SKILL.md. Replace with a one-line note that proposal revision is the owner's responsibility, outside the skill's scope.

**Rationale**: The skill's purpose statement explicitly says "The review does not modify the Solution Proposal." Phase 5's detailed revision rules contradict this purpose and create role confusion.

### 2.7 Cross-Round Statistics via index.md

**Decision**: Add an `index.md` file at `docs/superpowers/reviews/<proposal-stem>/index.md` that accumulates statistics across all review rounds. Each round's completion updates this file.

**Rationale**: Users need to track which findings were accepted/rejected across iterations. The index.md provides a human-readable summary table plus a machine-readable structure that can be parsed for further analysis.

---

## 3. File Changes

### 3.1 Files to Rewrite

#### `SKILL.md`

- Add YAML frontmatter: `name: yy-proposal-review`, description, trigger conditions
- Define execution entry point and input parameters
- Define 4-phase execution flow (Context Acquisition, Parallel Reviews, Consolidation, Output + Handoff)
- Specify subagent parallel dispatch mechanism (3 subagents, each with role definition + template + input paths)
- Specify consolidation by main agent following consolidation-protocol
- Specify output file generation (4 review files + index.md update)
- Specify handoff to superpowers
- Remove Phase 5 detailed description, add one-line note

#### `templates/test-review.md`

- Rewrite from AT/AC/BL three-section format to unified TD-001 Finding format
- Each Finding has: Severity, Evidence Class, Confidence, Finding Type (ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT), Location, Verification Gap / Problem, Trigger Scenario, Expected Verification, Verification Method, Consequence, Evidence, Recommendation, Reviewer Notes
- Retain the semantic richness of the current three sections through the Finding Type field
- Retain Machine-Readable Finding Index with TD-ID format

#### `roles/test-designer.md`

- Change Finding ID from implicit AT/AC/BL to explicit `TD-001`
- Add Finding Type field to the Required Finding Format
- Align Finding structure with PR/SC format while preserving test-specific fields (Expected Verification, Verification Method)
- Update example finding to use TD-001 format

### 3.2 Files to Modify

#### `templates/consolidated-review.md`

- Change all `RV-` references to `CR-`
- Align Finding Status values with decision-protocol enumeration (PENDING_DECISION instead of OPEN/READY_FOR_DECISION)
- Remove RESOLVED and SUPERSEDED from status values
- Change Test perspective source references from AT/AC/BL to TD-ID
- Add `Superpowers Instructions` section before Decision Queue
- Add `round` and `proposal_stem` fields to Machine-Readable YAML Index
- Add `final_review_state` field to YAML index
- Update Decision Records DR status values to match decision-protocol enumeration

#### `protocols/consolidation-protocol.md`

- Change all `RV-` references to `CR-` in examples and structure definitions
- Confirm decision state references align with decision-protocol

#### `protocols/decision-protocol.md`

- No substantive changes. Confirm as the authoritative source for decision states.
- Minor: add note that this protocol's state enumeration supersedes all others in the project.

#### `CLAUDE.md`

- Update directory structure to reflect new files (review-orchestrator-protocol.md, index.md template)
- Update naming convention from `review-NNN/` to `YYYY-MM-DD-review-NNN/`
- Update "Known Inconsistencies" section to reflect which issues are resolved
- Update output path documentation

### 3.3 Files to Add

#### `protocols/review-orchestrator-protocol.md`

Defines the main agent's orchestration responsibilities:

1. How to construct subagent prompts (role definition reference, input paths, output paths, independence constraints)
2. How to dispatch subagents in parallel (3 Agent calls in one response)
3. How to collect and validate subagent results
4. How to handle subagent failures (mark as MISSING, continue with available reviews)
5. How to execute consolidation (read 3 reviews, apply consolidation-protocol, generate consolidated-review.md)
6. How to generate output files (write 4 review files, update index.md)
7. How to determine review round number (read existing index.md, increment)
8. How to handle the superpowers handoff (generate Superpowers Instructions, stop)

#### `templates/index.md`

Cross-round summary template containing:

1. Proposal and Specification paths
2. Review Rounds table (Round, Date, P0/P1/P2 counts, Accepted/Rejected/Deferred counts, Status)
3. Finding Tracking table (CR-ID, Round, Severity, Title, Decision, Source Reviewers)
4. Trend section (changes between rounds, open findings count, overall status)

### 3.4 Files Unchanged

- `roles/product-reviewer.md` - PR-001 format is correct
- `roles/system-critic.md` - SC-001 format is correct
- `protocols/finding-protocol.md` - Base protocol, no changes needed
- `templates/product-review.md` - PR format is correct
- `templates/system-review.md` - SC format is correct

---

## 4. Execution Flow

### Phase 1: Context Acquisition

1. Main agent reads the Solution Proposal path from user input
2. Main agent locates the associated Specification (same stem in specs/ directory)
3. Main agent reads both documents
4. Main agent constructs an internal model of the problem, desired outcome, boundaries, and assumptions
5. Main agent determines the output directory and review round number by reading existing index.md (if any)

### Phase 2: Independent Reviews

1. Main agent dispatches 3 subagents in parallel in a single response:

   - **Subagent 1 (Product Reviewer)**: Receives spec path, proposal path, role definition reference (roles/product-reviewer.md), template reference (templates/product-review.md), output path. Must produce product-review.md independently.
   - **Subagent 2 (System Critic)**: Same structure, using roles/system-critic.md and templates/system-review.md.
   - **Subagent 3 (Test Designer)**: Same structure, using roles/test-designer.md and templates/test-review.md.

2. Each subagent:
   - Reads the Specification and Solution Proposal independently
   - Follows its role definition to produce findings
   - Writes output to the specified path
   - Does NOT read other subagents' outputs

3. Main agent waits for all 3 subagents to complete

4. If a subagent fails, mark its review as MISSING in the consolidated review and continue

**Review Amendment (CR-001)**: Subagent failure handling semantics:

1. **Failure criteria**: Timeout (configurable, default 10 minutes), output file not generated, output file fails format validation (missing required fields)
2. **Retry**: Allow one retry per subagent. If retry also fails, mark as MISSING
3. **MISSING hard rule**: If any review is MISSING, the final review state must be INCOMPLETE
4. **Partial consolidation**: When a review is MISSING, consolidation proceeds with available reviews. The consolidated review must include a Coverage Gap section listing the risk dimensions that cannot be assessed without the MISSING review
5. **Format validation checklist**: Each review output must contain Review Metadata, at least one Finding, and Machine-Readable Index

### Phase 3: Finding Consolidation

1. Main agent reads all 3 review output files
2. Main agent applies the Consolidation Protocol:
   - Validate each finding against the Specification and Proposal
   - Normalize finding structure
   - Assign global CR-IDs
   - Preserve original reviewer IDs (PR/SC/TD)
   - Identify duplicate, related, and contradictory findings
   - Generate Conflict Records for contradictory findings
3. Main agent performs **Source Finding integrity check** (CR-002, CR-008): verify that total source Finding count = consolidated references + unmerged + duplicate/superseded records. If mismatch, final review state must be INCOMPLETE
4. Main agent records **Consolidator Predispositions** (CR-002): key judgments formed during Phase 1 that may influence consolidation, written explicitly in the consolidated review
5. Main agent generates consolidated-review.md following the template
6. Main agent generates Superpowers Instructions section

### Phase 4: Output and Handoff

1. Main agent writes all 4 review files to the output directory
2. Main agent creates or updates index.md with the new round's statistics
3. Main agent reports completion to the user with:
   - File paths of all generated files
   - Summary of consolidated findings (count by severity)
   - Instructions for the next step (review in superpowers, record decisions)

---

## 5. Defect Resolution Mapping

| # | Defect | Resolution |
|---|--------|-----------|
| 1 | Missing execution entry point | SKILL.md rewrite with frontmatter and execution steps |
| 2 | Missing superpowers handoff | Superpowers Instructions section in consolidated-review.md |
| 3 | Missing consolidator role | Main agent as consolidator + review-orchestrator-protocol.md |
| 4 | Three conflicting decision state enums | Unified to decision-protocol.md enumeration |
| 5 | Consolidated Finding ID inconsistency | Unified to CR-001 |
| 6 | Test Designer format incompatibility | TD-001 unified format + Finding Type field |
| 7 | Reviewer independence vs. single terminal | Subagent parallel execution |
| 8 | SKILL.md missing frontmatter | Added in rewrite |
| 9 | Missing cross-round statistics | index.md + enhanced YAML index |
| 10 | Unclear input/output path naming | YYYY-MM-DD-review-NNN/ convention |
| 11 | Phase 5 exceeds skill boundary | Removed detailed description, one-line note |
| 12 | Missing review-orchestrator protocol | New review-orchestrator-protocol.md |

---

## 6. Out of Scope

The following are explicitly out of scope for this design:

- **Automated decision-making**: The skill will not automatically accept or reject findings. This is the proposal owner's responsibility.
- **Proposal modification**: The skill will not modify the Solution Proposal, even after decisions are recorded.
- **HTML dashboard**: Statistics are provided through markdown tables and YAML indexes. A visual dashboard could be added later but is not part of this design.
- **Cross-proposal statistics**: The index.md tracks rounds within a single proposal. Aggregating statistics across different proposals is not supported.
- **CI/CD integration**: The skill runs within Claude Code sessions. Automated pipeline integration is not part of this design.

---

## 7. Review Decisions (Round 1)

Review conducted 2026-07-19 by Product Reviewer, System Critic, and Test Designer. 23 source findings consolidated into 9 CR findings.

### Decision Records

#### DR-001 — CR-001 Subagent Failure Handling

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Real design gap. MISSING reviews without defined consequences could lead to incomplete audits being treated as complete.
- **Required Action**: Define failure criteria, retry mechanism, MISSING hard rule, partial consolidation strategy, and format validation checklist in review-orchestrator-protocol.md
- **Scope Adjustment**: Retry mechanism simplified to one retry (no exponential backoff needed)

#### DR-002 — CR-002 Consolidator Independence

- **Decision**: PARTIALLY_ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: The theoretical bias risk is real but the severity is overstated — no evidence of actual biased consolidation. The root-cause solution (4th subagent as consolidator) is over-engineered and creates its own context overflow problems. The minimum-cost solution makes bias auditable without eliminating the main agent's consolidation role.
- **Accepted Scope**: Standardized subagent prompt template, Consolidator Predispositions recording, Source Finding integrity check, context isolation documentation
- **Rejected Scope**: Fourth subagent as consolidator (over-engineered, creates new context overflow risk), Finding overlap rate thresholds (introduces new subjective judgment)
- **Conflict Resolution**: Chose Suggestion B (minimum-cost mitigation) over Suggestion A (4th subagent)

#### DR-003 — CR-003 Cross-Round Finding ID Stability

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Cross-round tracking is unreliable without stable ID semantics. Each round independently numbering with Previous Round CR-ID linkage is pragmatic.
- **Required Action**: Define cross-round CR-ID rules, add Previous Round CR-ID to index.md Finding Tracking table, define Finding state transition rules across rounds (CARRIED_FORWARD / RESOLVED / STILL_OPEN)

#### DR-004 — CR-004 Superpowers Instructions Decision Closure

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Current Superpowers Instructions is guidance without structure. Users need concrete templates and validation rules.
- **Required Action**: Define required structure for Superpowers Instructions, provide copy-paste Markdown decision template, define PENDING_DECISION hard rule, define final_review_state consistency check
- **Deferred Scope**: Lightweight decision verification step (skill re-reads consolidated-review.md) — adds complexity, defer to later iteration

#### DR-005 — CR-005 Finding ID Prefix Migration

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: RV→CR migration must be complete across all files including decision-protocol.md. AT/AC/BL→TD migration target corrected (consolidated-review.md template, not test-designer.md which already uses TD-001).
- **Required Action**: Include decision-protocol.md in modification scope (RV→CR global replacement), add Finding Type field to consolidation-protocol's Consolidated Finding Structure, correct AT/AC/BL→TD modification target list
- **Deferred Scope**: AT/AC/BL→TD ID mapping rules for cross-version tracking — no current cross-version scenario

#### DR-006 — CR-006 Specification File Auto-Location

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: "Same stem" extraction rule is undefined. Missing specification silently degrades review quality.
- **Required Action**: Define stem extraction algorithm (remove YYYY-MM-DD- prefix and .md suffix), define hard rule (INCOMPLETE if specification not found), support explicit specification path as alternative input

#### DR-007 — CR-007 index.md Concurrent Write Control

- **Decision**: REJECTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Concurrent writes to index.md do not occur in practice. Reviews are low-frequency operations (once per week at most) and Claude Code is a single-session tool. Atomic write transactions for Markdown files is over-engineering.
- **Alternative Action**: Add simple duplicate-prevention rule in review-orchestrator-protocol.md: if a review round already exists for today's date, warn user and confirm before proceeding
- **Rejection Ground**: INAPPLICABLE_SCENARIO — concurrent writes cannot occur in the actual usage model

#### DR-008 — CR-008 Context Window Overflow

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Context overflow is silent and dangerous — user gets a partial consolidation without knowing. Source Finding integrity check is low-cost high-value protection.
- **Required Action**: Implement Source Finding integrity check (already captured in Phase 3), define overflow detection (integrity check failure → INCOMPLETE), define degradation strategy
- **Deferred Scope**: Multi-step consolidation (split into partial operations) — adds complexity, defer until overflow actually occurs

#### DR-009 — CR-009 Severity Escalation Traceability

- **Decision**: ACCEPTED
- **Decision Owner**: Proposal Owner
- **Rationale**: Severity escalation/demotion rationale should be mandatory and reference specific source Finding evidence, not generalized reasoning.
- **Required Action**: Make severity change rationale a mandatory field in consolidated-review template, require reference to specific source Finding evidence, add severity_escalation field to Machine-Readable YAML Index

### Conflict Decisions

#### Conflict 1: Consolidator Role

- **Decision**: Suggestion B — Main agent continues as Consolidator with minimum-cost mitigation
- **Rationale**: Fourth subagent approach is over-engineered. Bias is made auditable through Predispositions recording, standardized prompts, and integrity checks.

#### Conflict 2: Finding ID Prefix

- **Decision**: Suggestion A — Unified to CR-
- **Rationale**: CR-001 aligns with consolidated-review template. decision-protocol.md must be included in modification scope. One-time global replacement cost is worth eliminating dual ID systems.

### Final Review State

**CHANGES_REQUIRED** → After implementing CR-001, CR-002 (partial), CR-003, CR-004, CR-005, CR-006, CR-008, CR-009 → CONDITIONAL_APPROVAL

### Design Amendments Summary

Amendments incorporated into the design document above:

1. **Section 2.3** — Added Consolidator Predispositions, standardized prompt template, integrity check, context isolation documentation (CR-002)
2. **Phase 2** — Added subagent failure handling semantics: failure criteria, retry, MISSING hard rule, partial consolidation, format validation (CR-001)
3. **Phase 3** — Added Source Finding integrity check, Consolidator Predispositions recording (CR-002, CR-008)
4. **Section 3.2 decision-protocol.md** — Changed from "no substantive changes" to "included in RV→CR modification scope" (CR-005)
5. **Section 3.3 review-orchestrator-protocol.md** — Expanded scope: standardized prompt template, failure handling, format validation, integrity check, duplicate-prevention rule (CR-001, CR-002, CR-006, CR-007 alternative, CR-008)
6. **Section 3.3 index.md template** — Added Previous Round CR-ID column, Finding state transition tracking (CR-003)
7. **Section 3.2 consolidated-review.md** — Added Coverage Gap section, Consolidator Predispositions section, severity change rationale as mandatory field, Superpowers Instructions structure definition, copy-paste decision template (CR-001, CR-002, CR-004, CR-009)
8. **Phase 1** — Added stem extraction algorithm, specification-not-found hard rule, explicit specification path support (CR-006)
