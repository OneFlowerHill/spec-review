# Review Orchestrator Protocol

## Purpose

This protocol defines the main agent's responsibilities for orchestrating the
Design Spec review workflow. The main agent (running SKILL.md) coordinates context
acquisition, subagent dispatch, result collection, consolidation, output
generation, and handoff to superpowers.

This protocol does not define how individual reviewers discover findings
(that belongs to the role definitions) or how findings are consolidated
(that belongs to the Consolidation Protocol).

---

## 1. Output Path Determination

### Stem Extraction

Given a spec filename, extract the stem:

```text
Input:  2026-07-19-customer-operation.md
Step 1: Remove .md extension → 2026-07-19-customer-operation
Step 2: Remove YYYY-MM-DD- prefix → customer-operation
Result: customer-operation
```

The algorithm: remove leading pattern matching `^\d{4}-\d{2}-\d{2}-` and
trailing `.md`.

### Output Directory

The output directory is determined by the spec stem:

```text
docs/superpowers/reviews/<spec-stem>/
```

---

## 2. Subagent Prompt Construction

### Standardized Prompt Template

Every subagent prompt must follow this exact structure. The main agent must
NOT include any analytical descriptions, interpretations, or summaries of the
Design Spec content in the prompt. Only path information differs between prompts.

```markdown
You are the <ROLE_NAME>. Conduct an independent review.

你的加载清单（四者并列，不得省略）：
1. `references/common.md`（共享权威定义：严重度/证据等级/Finding 字段/独立评审规则）
2. `roles/<你的角色>.md`
3. `templates/<你的模板>.md`
4. 被审 spec 路径

## Shared Definitions

Read first: references/common.md

## Your Role Definition

Read and follow: <ROLE_FILE_PATH>

## Input Document

- Design Spec: <SPEC_PATH>

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
6. You must follow the output language rules defined in the
   output template. All descriptive content must be written
   in Chinese (中文). All UPPERCASE_WITH_UNDERSCORE identifiers
   must remain in English.
```

### What Must NOT Be Included in Subagent Prompts

- The main agent's summary or interpretation of the Design Spec
- The main agent's identified concerns or hypotheses
- Any hint about what findings might be expected
- References to the other reviewers or their roles
- The main agent's internal model of the problem

### Context Isolation

> 独立评审/上下文隔离规则见 `references/common.md` §4；subagent 提示词不得含主 agent 分析或其他角色评审。

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
- [ ] Design Spec path is present
- [ ] Review Date is present
- [ ] At least one Finding exists, or an explicit "no material findings" statement
- [ ] Each Finding has a unique ID (PR/SC/TD format)
- [ ] Each Finding has all required fields per its role definition
- [ ] Machine-Readable Index is present and parseable
- [ ] Descriptive content is written in Chinese (Finding titles, problem descriptions, scenarios, consequences, recommendations, evidence, etc.)
- [ ] YAML index enum values match protocol-defined allowed values (UPPERCASE_WITH_UNDERSCORE format)
- [ ] YAML index descriptive fields (title, description, etc.) are written in Chinese

### Retry Mechanism

If a subagent fails validation:

1. Allow one retry: dispatch the same subagent again with the same prompt
2. If the retry also fails, mark the review as MISSING
3. Do NOT retry more than once

### Language Validation Failure

If format validation finds language issues:

1. Allow one retry: dispatch the same subagent again with the same prompt
2. If the retry also fails language validation, proceed with the output
3. Record the language quality issue in the review output's Review Limitations section
4. Language quality issues do NOT trigger INCOMPLETE status

### MISSING Hard Rule

If any review is MISSING:

- The consolidated review must include a Coverage Gap section
- The final review state must be INCOMPLETE
- The consolidation proceeds with available reviews only

INCOMPLETE is triggered when:
- Any subagent review output is MISSING
- The Source Finding Integrity Check fails

If the Design Spec file itself does not exist or cannot be read, the skill
must report an error and stop (not INCOMPLETE — there is nothing to review).

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
  + Duplicate/Represented Elsewhere Finding count
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
docs/superpowers/reviews/<spec-stem>/
├── index.md
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

### Round Number Determination

1. Check if `docs/superpowers/reviews/<spec-stem>/index.md` exists
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

- Core assumptions identified in the Design Spec
- Areas of particular concern noted during context acquisition
- Hypotheses about the Design Spec's strengths or weaknesses
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
   - Modify the Design Spec
   - Re-read the consolidated review after decisions are recorded
