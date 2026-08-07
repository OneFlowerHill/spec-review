---
name: spec-review
description: >
  Review a Design Spec through three independent perspectives
  (Product, System, Test) in parallel, consolidate findings, and produce
  a structured review document for decision-making. USER-TRIGGERED ONLY:
  invoke ONLY when the user explicitly requests a spec review — e.g.
  "review this spec", "审核这个规格", "run a spec review", or the
  /spec-review command. Do NOT auto-invoke just because a design spec
  file is present, because you are reading a spec, or because you judge
  a review would be helpful. The agent never initiates this skill on its own.
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [review, spec, design, qa, multi-perspective, audit]
    category: software-development
---

# Spec Review

## Purpose

Review a Design Spec for quality and completeness.

The review evaluates whether the Design Spec:

1. Defines sufficiently complete and coherent product behavior.
2. Is logically and technically coherent.
3. Defines behavior precisely enough to be validated.
4. Has sufficient handling for important edge cases and failure conditions.
5. Avoids unnecessary complexity and unjustified assumptions.

The review does not implement the solution.

The review does not modify the Design Spec.

The review produces structured findings for a later decision phase.

---

# Conceptual Model

```text
Design Spec
    ↓
Independent Multi-Perspective Review (3 subagents in parallel)
    ↓
Finding Consolidation (main agent)
    ↓
Decision (by spec owner via superpowers)
    ↓
Spec Revision (outside this skill's scope)
```

---

# Inputs

The primary input is:

```text
docs/superpowers/specs/<spec>.md
```

If the Design Spec file does not exist or cannot be read, the skill must
report an error and stop. There is no fallback.

---

# Output

Each execution creates a new Review Round.

Never overwrite a previous Review Round.

Use:

```text
docs/superpowers/reviews/<spec-stem>/
├── index.md
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

The `<spec-stem>` is extracted from the spec filename by removing
the leading `YYYY-MM-DD-` prefix and the `.md` suffix.

### Stem Extraction Algorithm

Given a spec filename, extract the stem:

```text
Input:  2026-07-19-customer-operation.md
Step 1: Remove .md extension → 2026-07-19-customer-operation
Step 2: Remove YYYY-MM-DD- prefix → customer-operation
Result: customer-operation
```

The algorithm: remove leading pattern matching `^\d{4}-\d{2}-\d{2}-` and
trailing `.md`.

Example:

```text
Spec:    2026-07-19-customer-operation.md
Stem:    customer-operation
Output:  docs/superpowers/reviews/customer-operation/2026-07-19-review-001/
```

---

# Review Phases

## Phase 1: Context Acquisition

1. Read the Design Spec path from user input
2. If the Design Spec file does not exist or cannot be read, report error
   and stop
3. Read the complete Design Spec
4. Construct an internal model of the problem, desired outcome, boundaries,
   and assumptions
5. Record Consolidator Predispositions: key judgments that may influence
   consolidation, as defined in `protocols/review-orchestrator-protocol.md`
6. Determine the output directory and review round number by reading the
   existing `index.md` (if any)
7. If a review round already exists for today's date, warn the user

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

### Output Language

All review output files must be written in Chinese (中文).
Follow the detailed output language rules defined in the output templates.

The following must remain in English:

- Finding IDs (PR-001, SC-001, TD-001, CR-001)
- All UPPERCASE_WITH_UNDERSCORE identifiers (enumerated values, status codes, etc.)
- Machine-Readable YAML keys and enum values
- Technical identifiers and file paths

All descriptive content — titles, problem descriptions, scenarios, consequences, recommendations, evidence, and narrative sections — must be written in Chinese.

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
   - Validate each finding against the Design Spec
   - Normalize finding structure
   - Assign global CR-IDs
   - Preserve original reviewer IDs (PR/SC/TD)
   - Identify duplicate, related, and contradictory findings
   - Generate Conflict Records for contradictory findings
3. Perform the Source Finding Integrity Check:
   - Verify: total source Finding count = consolidated Finding references
     + unmerged Finding count + duplicate/represented elsewhere records
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
Design Spec, or re-read the consolidated review after decisions.

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

INCOMPLETE is triggered when:
- Any subagent review output is MISSING
- The Source Finding Integrity Check fails

---

# Reviewer Boundaries

## Product Reviewer

Evaluate whether the Design Spec defines sufficiently complete and coherent
product behavior.

## System Critic

Evaluate whether the Design Spec is technically and logically coherent.

## Test Designer

Evaluate whether the Design Spec is sufficiently precise and observable
to be validated.

三角色边界的完整契约（含审查维度清单）见 `references/common.md` §5。

---

# 共享定义

严重度（P0/P1/P2）、证据等级（四字面量）、Finding 字段契约、独立评审/上下文隔离规则等共享定义统一位于 `references/common.md`（权威源）：

- 严重度定义见 `references/common.md` §1
- 证据等级定义见 `references/common.md` §2
- Finding 字段契约见 `references/common.md` §3
- 独立评审/上下文隔离规则见 `references/common.md` §4

各角色/模板/协议须引用该文件，不得各自重述；修改须同批变更（设计规格 §4 第 10、11 条）。

---

# Completion Criteria

A Review Round is complete only when:

* The complete Design Spec has been read
* All three independent reviews are complete (or confirmed MISSING)
* All findings have stable CR-IDs
* Duplicate findings are identified
* Conflicting findings are identified
* Unverified assumptions are identified
* The Source Finding Integrity Check passes
* The Consolidated Review is generated
* No finding has been silently discarded
* The index.md is created or updated
