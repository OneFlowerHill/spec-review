# Spec Review Skill 框架瘦身（方案 B）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实施设计规格 `docs/superpowers/specs/2026-08-04-spec-review-slim-design.md` 中方案 A 的瘦身——新建 `references/common.md` 共享定义源、压缩 13 个框架文件（3 角色 + 4 协议 + 5 模板 + SKILL.md/CLAUDE.md），使框架 token 降幅 ≥40%（候选人 ≤ 61,153 token），同时零质量不变量丢失。

**Architecture:** 把分散在角色/协议/模板中的「严重度、证据等级、Finding 字段、独立评审规则」抽到单一权威文件 `references/common.md`，各文件改为引用它而非重述；协议/模板保留规则骨架与字段定义、砍掉重复示例与冗余 prose。所有改动由 `scripts/token_analyzer.py --compare` 的客观 ≥40% 闸门 + 一组 grep 一致性校验把关。

**Tech Stack:** 纯 Markdown 内容编辑；Python 3.9+（仅用于运行已有的 `scripts/token_analyzer.py`）；`grep`/`git` 用于一致性校验与提交。无新增依赖。

## Global Constraints

以下为规格的全局硬性要求，每条任务的实现须隐式遵守（逐条从规格原文摘录）：

- 计量算法 `builtin-v1@1.0.0`，仅依赖 Python 标准库，写死于 `scripts/token_analyzer.py`；任何口径修改须 bump 版本并经决策。
- 降幅硬门槛 **≥40.0%** 为 PASS（退出码 0），否则 FAIL（退出码 1）；基线 = **101,922 tokens**（13 框架文件，无 common.md）；候选上限 = **61,153 tokens**（13 瘦身文件 + `references/common.md`）。
- `scripts/prompt_scope.json` 锁定的文件清单**禁止编辑**（除非 scope  legitimately 变化，须同步 bump 算法/清单版本）。
- §2/§3 中的行数目标（如 `1583→~700`、`~40%`）仅为**参考值，非硬上限**；与质量约束冲突时以**保留约束优先**，不得为达标删规范性语句。
- `references/common.md` 与其引用方（roles/templates）必须**同批变更**（单次提交或同一 PR）；所有对 common.md 的引用必须可解析，**禁止悬空引用**。
- §4 质量不变量第 1–11 条**一条不动**（CR-ID 唯一、决策枚举权威、Test 必含 Finding Type、MISSING/INCOMPLETE 硬规则、Source Finding 完整性、独立评审隔离、输出路径结构、证据等级取值域、§4 不穷尽声明+删除纪律、common.md 同批变更、不可删不变量字面量清单）。
- 证据等级四字面量 `CONFIRMED_DEFECT`/`MATERIAL_RISK`/`CONFIRMED_GAP`/`DESIGN_PREFERENCE` 及各角色可输出子集（Product/System=`CONFIRMED_DEFECT|MATERIAL_RISK`；Test=`CONFIRMED_GAP|MATERIAL_RISK`；`DESIGN_PREFERENCE` 仅内部参考不得输出）**不得静默变更**。
- 任何删减须逐条记入「删除项清单」（规格 §7 格式）；标记为"影响质量约束"的项须经决策，不得静默合入。

---

## File Structure

**新建：**
- `references/common.md` — 共享权威定义源：严重度、证据等级（四字面量+角色子集）、Finding 字段契约（共享必填+角色差异）、独立评审/隔离规则、三角色边界摘要、不可删不变量字面量清单。被 roles/templates/protocols/SKILL.md/CLAUDE.md 引用。

**修改（原地瘦身，引用 common.md 替代重复块）：**
- `roles/product-reviewer.md` — 删 Independence Requirement / Evidence Classification / Severity Classification / Required Finding Format 四大共享块，改引用 common.md。
- `roles/system-critic.md` — 同上四类共享块。
- `roles/test-designer.md` — 同上四类共享块。
- `protocols/finding-protocol.md` — 删 Evidence Class/Severity/Confidence 的重复定义段，改引用 common.md；保留单 Finding 结构与质量门槛。
- `protocols/consolidation-protocol.md` — 保留合并规则、关系分类（7 类）、CR-ID、Source Finding 完整性校验、冲突记录；砍冗长 rationale 与重复示例。
- `protocols/decision-protocol.md` — 保留状态枚举及含义、状态流转；砍冗余 prose。
- `protocols/review-orchestrator-protocol.md` — 基本保留；§2 子代理提示构造中把 `references/common.md` 加入加载契约（与角色/模板/spec 四者并列）。
- `templates/product-review.md` / `system-review.md` / `test-review.md` — 砍字段说明性冗余 prose，保留结构骨架与字段定义；字段名与 common.md 逐字一致。
- `templates/consolidated-review.md` — 砍重复示例 prose，保留合并结构骨架。
- `templates/index.md` — 基本不变。
- `SKILL.md` / `CLAUDE.md` — 重复的严重度/边界段落改为引用 common.md；显式登记 `references/` 路径。

**辅助（实现期跟踪，随实现提交）：**
- `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md` — 删除项清单（规格 §7 格式），每删一段追加一行。

**验收（已有，不改）：**
- `scripts/token_analyzer.py` + `scripts/prompt_scope.json` — `--compare` 闸门。

---

### Task 1: 初始化工作区与基线确认

**Files:**
- Read: `scripts/prompt_scope.json`, `scripts/token_analyzer.py`
- Create: `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md`

**Interfaces:**
- Produces: 基线 token 数（供后续 Task 15 比对）、删除项清单文件（后续任务追加）。

- [ ] **Step 1: 确认在 main 分支且工作区干净**

```bash
git status --short
git branch --show-current
```
Expected: 无未提交改动；当前分支 `main`。如有未提交改动先 `git stash`。

- [ ] **Step 2: 运行基线，记录 101,922**

```bash
python3 scripts/token_analyzer.py --baseline
```
Expected: 输出 JSON 含 `"total_tokens": 101922`，`"missing_files": []`。

- [ ] **Step 3: 创建删除项清单文件（规格 §7 格式）**

```markdown
# 删除项清单（方案 B 实现跟踪）

| 文件 | 删除段落/语句 | 类型(约束/禁止/数量上限/说明) | 删除理由 | 是否影响质量约束 |
|---|---|---|---|---|
```

- [ ] **Step 4: 提交初始化**

```bash
git add docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "chore(B): init slim workspace, baseline 101922 tokens, deletion log"
```

---

### Task 2: 新建 references/common.md（共享权威定义源）

**Files:**
- Create: `references/common.md`

**Interfaces:**
- Produces: `references/common.md` 全文（后续所有角色/协议/模板/SKILL.md/CLAUDE.md 的引用目标）。
- Consumes: 规格 §3.1、§4 第 11 条不变量字面量清单。

- [ ] **Step 1: 写可判定校验脚本（验证 common.md 含全部不变量字面量）**

创建临时校验（或直接使用 Step 5 的 grep）：

```bash
grep -Eq "CONFIRMED_DEFECT|MATERIAL_RISK|CONFIRMED_GAP|DESIGN_PREFERENCE" references/common.md && echo "enum-ok"
grep -Eq "PENDING_DECISION|ACCEPTED|REJECTED|DEFERRED|PARTIALLY_ACCEPTED|DUPLICATE|INVALIDATED" references/common.md && echo "decision-ok"
grep -Eq "INCOMPLETE|MISSING|独立评审|CR-ID" references/common.md && echo "invariant-ok"
```
Expected（此时文件未建）: 命令报错/无输出（"test fails"）。

- [ ] **Step 2: 创建 references/common.md，内容如下（完整，逐字）**

```markdown
# Shared Definitions (references/common.md)

> 本文件是 yy-spec-review skill 的**共享权威定义源**，由 SKILL.md / CLAUDE.md / 角色 / 模板 / 协议引用。
> 修改本文件须与所有引用方**同批变更**（单次提交或同一 PR），且不得引入悬空引用（见设计规格 §4 第 10、11 条）。
> 本文件被纳入 token 降幅验收（prompt_scope.json candidate 含本文件）。

## 1. 严重度（Severity）

- **P0**：阻断性缺陷——审核流程无法继续、核心契约被破坏、或遗漏将导致严重质量/安全隐患。必须修复后方可 APPROVED。
- **P1**：重要缺陷——显著影响审核质量或正确性，但不阻断流程；须在进入 APPROVED 前解决。
- **P2**：次要问题——可读性、一致性或低成本改进；可延后，但须记录。

## 2. 证据等级（Evidence Class）

全局取值域（四个固定字面量，必须原样拼写；合并/决策协议须识别全部四值）：

| 字面量 | 含义 | 主要产出角色 |
|---|---|---|
| `CONFIRMED_DEFECT` | 已确认的设计缺陷 | Product / System |
| `MATERIAL_RISK` | 重大风险（非已确认缺陷） | Product / System / Test |
| `CONFIRMED_GAP` | 已确认的验证/覆盖缺口 | Test |
| `DESIGN_PREFERENCE` | 设计偏好（仅作内部参考，**不得**作为 Finding 输出） | — |

各角色**可输出**子集（与 `roles/*.md` 实际字段一致，不得静默变更）：

- Product：`CONFIRMED_DEFECT` | `MATERIAL_RISK`
- System：`CONFIRMED_DEFECT` | `MATERIAL_RISK`
- Test：`CONFIRMED_GAP` | `MATERIAL_RISK`

> `DESIGN_PREFERENCE` 在三个角色中均"仅作内部参考，不得作为 Finding 输出"。

## 3. Finding 字段契约

**共享必填字段**（每个 Finding 必须包含）：

`Severity` / `Evidence Class` / `Confidence` / `Location` / `Consequence` / `Evidence` / `Recommendation`

**各角色差异字段**（字段名须与对应模板逐字一致，禁止重命名/缩写）：

- Product：`Gap` / `Trigger Scenario`
- System：`Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility`
- Test：`Gap` / `Trigger Scenario` / `Finding Type`（必填）

> 落地产出的 Machine-Readable 索引须同时包含共享字段与各角色差异字段；字段缺失、重命名或缩写视为一致性缺陷（设计规格 §6 字段校验）。

## 4. 独立评审 / 上下文隔离规则

- 每个 subagent **只能读**：`references/common.md` + 自己的 `roles/X.md` + 自己的 `templates/X.md` + 被审 spec 路径。
- subagent 提示词**不得包含**主 agent 的分析、结论或其他角色的评审内容。
- 角色之间**互不参考**；合并阶段才汇总。
- 该隔离规则本身须存在于每个 subagent 的运行上下文中（由 orchestrator 加载契约保证，§6 校验）。

## 5. 三角色边界摘要

- **Product Reviewer**：从业务/需求完整性角度审查（需求完整性、业务规则、工作流、状态迁移、边界、数据生命周期、时间一致性、隐藏假设）。
- **System Critic**：从系统/架构/可靠性角度审查（数据完整性、故障恢复、并发、外部依赖、状态生命周期、可扩展性、安全边界、可观测性、部署兼容、不可逆决策、复杂度）。
- **Test Designer**：从可验证性角度审查（验收标准、可观测结果、状态迁移验证、边界验证、失败验证、数据完整性验证、时间验证、向后兼容、运维验证、生产盲点）。

## 6. 不可删质量不变量字面量清单（见设计规格 §4 第 11 条）

以下字面量在任何瘦身/重构后必须仍可 grep 命中（删除安全网）：

- 合并标识：`CR-ID`（禁止 `RV-` 前缀）
- 决策枚举：`PENDING_DECISION` / `ACCEPTED` / `REJECTED` / `DEFERRED` / `PARTIALLY_ACCEPTED` / `DUPLICATE` / `INVALIDATED`
- 证据等级：`CONFIRMED_DEFECT` / `MATERIAL_RISK` / `CONFIRMED_GAP` / `DESIGN_PREFERENCE`
- 关系分类：`DUPLICATE` / `SAME_ROOT_CAUSE` / `RELATED` / `INDEPENDENT` / `CONTRADICTORY` / `SUBSET` / `CONSEQUENCE`
- 状态硬规则：`INCOMPLETE` / `MISSING`
- 独立评审：`独立评审` / `subagent 不得读其他评审`
- 差异字段名：`Gap` / `Trigger Scenario` / `Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility` / `Finding Type`
```

- [ ] **Step 3: 运行 Step 1 的 grep 校验，确认三行均输出 ok**

Expected:
```
enum-ok
decision-ok
invariant-ok
```

- [ ] **Step 4: 提交**

```bash
git add references/common.md
git commit -m "feat(B): add references/common.md shared authoritative defs"
```

---

### Task 3: 瘦身 roles/product-reviewer.md

**Files:**
- Modify: `roles/product-reviewer.md`
- Read: `references/common.md` (Task 2)
- Modify: `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md`

**Interfaces:**
- Consumes: common.md 的四大共享块内容（作为替换目标）。
- Produces: 瘦身后的 product-reviewer.md（含对 common.md 的引用，保留独有内容）。

- [ ] **Step 1: 确认当前含待删共享块（pre-state）**

```bash
grep -cE "^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$" roles/product-reviewer.md
```
Expected: 输出 `4`（四个块均存在）。

- [ ] **Step 2: 删除以下 4 个顶层 `#` 区段（含其子标题与正文），逐段记录到删除项清单**
  - `# Independence Requirement`（含 `##` 子标题与正文）
  - `# Evidence Classification`（含 `## CONFIRMED_DEFECT`/`## MATERIAL_RISK`/`## DESIGN_PREFERENCE`）
  - `# Severity Classification`（含 `## P0`/`## P1`/`## P2`）
  - `# Required Finding Format`（含 `### Severity`/`### Evidence Class`/…/`### Reviewer Notes`；**保留**紧随其后的 `# Example Finding` 与 `# What This Role Must Not Do` / `# Completion Criteria`）

  每删一段，在删除项清单追加一行，例如：
  `| roles/product-reviewer.md | # Severity Classification (P0/P1/P2 定义) | 说明 | 抽至 references/common.md §1 | 否 |`

- [ ] **Step 3: 在每个被删块的原位置插入一行引用（四选一，语义对应）**

```markdown
> 严重度定义见 `references/common.md` §1。
> 证据等级定义见 `references/common.md` §2（Product 可输出 `CONFIRMED_DEFECT`/`MATERIAL_RISK`）。
> 独立评审/上下文隔离规则见 `references/common.md` §4。
> Finding 字段契约见 `references/common.md` §3（Product 差异字段：`Gap`/`Trigger Scenario`）。
```

- [ ] **Step 4: 校验——共享块已删、引用已加、独有内容保留**

```bash
echo "shared-blocks-remaining: $(grep -cE '^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$' roles/product-reviewer.md)"
echo "common-refs: $(grep -c 'references/common.md' roles/product-reviewer.md)"
echo "unique-kept: $(grep -cE '^# (Core Review Question|Review Perspectives|Review Dimensions|Example Finding|What This Role Must Not Do|Completion Criteria)$' roles/product-reviewer.md)"
```
Expected: `shared-blocks-remaining: 0`、`common-refs: ≥4`、`unique-kept: 6`（独有块全部保留）。

- [ ] **Step 5: 提交**

```bash
git add roles/product-reviewer.md docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "refactor(B): slim roles/product-reviewer.md, reference common.md"
```

---

### Task 4: 瘦身 roles/system-critic.md

**Files:**
- Modify: `roles/system-critic.md`
- Read: `references/common.md`
- Modify: `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md`

**Interfaces:**
- Produces: 瘦身后的 system-critic.md（System 差异字段 `Risk`/`Trigger Condition`/`Causal Chain`/`Likelihood`/`Reversibility` 须在引用中显式点名）。

- [ ] **Step 1: 确认当前含 4 个待删块**

```bash
grep -cE "^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$" roles/system-critic.md
```
Expected: `4`。

- [ ] **Step 2: 删除 4 个顶层 `#` 区段（同 Task 3 的块名），逐段记入删除项清单；保留 `# Example Finding` 及之后独有内容（`# Irreversible Decisions`/`# Complexity and Over-Engineering`/`# Risk Causal Chain` 等系统独有维度保留）**

- [ ] **Step 3: 在对应位置插入引用，System 字段引用须点名差异字段**

```markdown
> 严重度定义见 `references/common.md` §1。
> 证据等级定义见 `references/common.md` §2（System 可输出 `CONFIRMED_DEFECT`/`MATERIAL_RISK`）。
> 独立评审/上下文隔离规则见 `references/common.md` §4。
> Finding 字段契约见 `references/common.md` §3（System 差异字段：`Risk`/`Trigger Condition`/`Causal Chain`/`Likelihood`/`Reversibility`）。
```

- [ ] **Step 4: 校验**

```bash
echo "shared-remaining: $(grep -cE '^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$' roles/system-critic.md)"
echo "common-refs: $(grep -c 'references/common.md' roles/system-critic.md)"
```
Expected: `shared-remaining: 0`、`common-refs: ≥4`。

- [ ] **Step 5: 提交**

```bash
git add roles/system-critic.md docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "refactor(B): slim roles/system-critic.md, reference common.md"
```

---

### Task 5: 瘦身 roles/test-designer.md

**Files:**
- Modify: `roles/test-designer.md`
- Read: `references/common.md`
- Modify: `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md`

**Interfaces:**
- Produces: 瘦身后的 test-designer.md（须强调 `Finding Type` 必填，对应 common.md §3 Test 差异字段）。

- [ ] **Step 1: 确认当前含 4 个待删块**

```bash
grep -cE "^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$" roles/test-designer.md
```
Expected: `4`。

- [ ] **Step 2: 删除 4 个顶层 `#` 区段，逐段记入删除项清单；保留 `# Example Finding` 及之后独有内容（`# High-Value Verification Scenario` 等保留）**

- [ ] **Step 3: 插入引用，Test 字段引用须点名 `Finding Type` 必填**

```markdown
> 严重度定义见 `references/common.md` §1。
> 证据等级定义见 `references/common.md` §2（Test 可输出 `CONFIRMED_GAP`/`MATERIAL_RISK`）。
> 独立评审/上下文隔离规则见 `references/common.md` §4。
> Finding 字段契约见 `references/common.md` §3（Test 差异字段：`Gap`/`Trigger Scenario`/`Finding Type` **必填**）。
```

- [ ] **Step 4: 校验**

```bash
echo "shared-remaining: $(grep -cE '^# (Independence Requirement|Evidence Classification|Severity Classification|Required Finding Format)$' roles/test-designer.md)"
echo "common-refs: $(grep -c 'references/common.md' roles/test-designer.md)"
```
Expected: `shared-remaining: 0`、`common-refs: ≥4`。

- [ ] **Step 5: 提交**

```bash
git add roles/test-designer.md docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "refactor(B): slim roles/test-designer.md, reference common.md"
```

---

### Task 6: 瘦身 protocols/finding-protocol.md

**Files:**
- Modify: `protocols/finding-protocol.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 finding-protocol.md（保留单 Finding 结构 §7 与质量门槛 §2/§17，去掉与 common.md 重复的 Evidence/Severity/Confidence 定义）。

- [ ] **Step 1: 确认待删共享定义段存在**

```bash
grep -nE "^(### Evidence Class|## 4\. Finding Severity|## 5\. Confidence)$" protocols/finding-protocol.md
```
Expected: 输出三个匹配行号（如 123、176、233）。

- [ ] **Step 2: 将 `### Evidence Class`（§3 内，106 起）、`## 4. Finding Severity`（含 `### P0/P1/P2`）、`## 5. Confidence`（含 `### HIGH/MEDIUM/LOW`）三段的正文替换为对 common.md 的引用，保留段落标题作为锚点**

```markdown
## 3. Evidence Requirement

证据等级的四个字面量与各角色可输出子集见 `references/common.md` §2（合并/决策协议须识别全部四值，含 `CONFIRMED_GAP`）。

## 4. Finding Severity

严重度 P0/P1/P2 的精确定义与示例见 `references/common.md` §1。

## 5. Confidence

置信度 HIGH/MEDIUM/LOW 的语义见 `references/common.md`（如有定义）；本协议的置信度使用规则如下：置信度须与证据强度匹配（见 §16）。
```

- [ ] **Step 3: 保留并核对 §7 Required Finding Structure、§2 Quality Standard、§17 Quality Gate 未被触碰**

```bash
grep -cE "^(## 2\. Finding Quality Standard|## 7\. Required Finding Structure|## 17\. Finding Quality Gate)$" protocols/finding-protocol.md
```
Expected: `3`。

- [ ] **Step 4: 提交**

```bash
git add protocols/finding-protocol.md
git commit -m "refactor(B): slim finding-protocol.md shared defs to common.md"
```

---

### Task 7: 瘦身 protocols/consolidation-protocol.md

**Files:**
- Modify: `protocols/consolidation-protocol.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 consolidation-protocol.md（必须保留：§4 CR-ID、§5 Source Finding 完整性校验、§6 关系分类 7 类、§8 决策树、§9 合并规则、§14 冲突处理）。

- [ ] **Step 1: 列出必须保留的锚点（pre-state 校验）**

```bash
grep -cE "^(## 4\. Consolidated Finding Identity|## 5\. Source Finding Preservation|## 6\. Finding Relationship Classification|## 8\. Consolidation Decision Tree|## 9\. Consolidation Rules|## 14\. Contradiction Handling)$" protocols/consolidation-protocol.md
```
Expected: `6`。

- [ ] **Step 2: 对每个 `## N.` 区段，删除其中的"冗长 rationale 段落"与"重复示例"（保留规则陈述句与至少一个 worked example）。具体：§6 七类关系（`### DUPLICATE`/`### SAME_ROOT_CAUSE`/`### RELATED`/`### INDEPENDENT`/`### CONTRADICTORY`/`### SUBSET`/`### CONSEQUENCE`）全部保留，仅压缩每类内的解释性散文；§14 保留 `### Conflict C-001` 一个示例，删其余重复示例。**

逐段记入删除项清单（类型：说明/重复示例）。

- [ ] **Step 3: 在 §6 开头加一句引用，确认合并协议识别全部四证据值**

```markdown
> 证据等级四值见 `references/common.md` §2；合并协议须能识别全部四值（含 `CONFIRMED_GAP`），否则视为一致性缺陷。
```

- [ ] **Step 4: 校验 7 类关系与关键锚点仍在**

```bash
echo "rels: $(grep -cE '^### (DUPLICATE|SAME_ROOT_CAUSE|RELATED|INDEPENDENT|CONTRADICTORY|SUBSET|CONSEQUENCE)$' protocols/consolidation-protocol.md)"
echo "anchors: $(grep -cE '^(## 4\. Consolidated Finding Identity|## 5\. Source Finding Preservation|## 8\. Consolidation Decision Tree|## 9\. Consolidation Rules)$' protocols/consolidation-protocol.md)"
```
Expected: `rels: 7`、`anchors: 4`。

- [ ] **Step 5: 提交**

```bash
git add protocols/consolidation-protocol.md docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "refactor(B): slim consolidation-protocol.md, keep merge rules + 7 relations"
```

---

### Task 8: 瘦身 protocols/decision-protocol.md

**Files:**
- Modify: `protocols/decision-protocol.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 decision-protocol.md（保留 §2 状态枚举及含义、§4 状态流转、§5 Required Decision Structure）。

- [ ] **Step 1: 列出必须保留锚点**

```bash
grep -cE "^(## 2\. Decision States|## 4\. Decision Status Lifecycle|## 5\. Required Decision Structure)$" protocols/decision-protocol.md
```
Expected: `3`。

- [ ] **Step 2: 压缩 §1/§3/§6–§20 中的冗余 prose（保留每条规则的陈述句与状态含义）。决策枚举 7 个（`### ACCEPTED`/`### REJECTED`/`### DEFERRED`/`### PARTIALLY_ACCEPTED`/`### DUPLICATE`/`### INVALIDATED` 及生命周期）全部保留。**

逐段记入删除项清单。

- [ ] **Step 3: 在 §2 开头加引用**

```markdown
> 决策状态枚举的权威定义与流转见 `references/common.md` §4 及本文件 §4；状态枚举为全局权威（设计规格 §4 第 2 条）。
```

- [ ] **Step 4: 校验 7 状态枚举仍在**

```bash
echo "states: $(grep -cE '^### (ACCEPTED|REJECTED|DEFERRED|PARTIALLY_ACCEPTED|DUPLICATE|INVALIDATED)$' protocols/decision-protocol.md)"
```
Expected: `states: 6`（注：PENDING_DECISION 为初始态，可能在 §4 生命周期中定义；若不在该集合则额外确认其存在：`grep -c "PENDING_DECISION" protocols/decision-protocol.md` ≥ 1）。

- [ ] **Step 5: 提交**

```bash
git add protocols/decision-protocol.md docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
git commit -m "refactor(B): slim decision-protocol.md, keep state enum + lifecycle"
```

---

### Task 9: 更新 protocols/review-orchestrator-protocol.md 加载契约

**Files:**
- Modify: `protocols/review-orchestrator-protocol.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: orchestrator 的 subagent 提示构造把 `references/common.md` 加入加载清单（与角色/模板/spec 四者并列）。

- [ ] **Step 1: 定位 §2 Subagent Prompt Construction 的加载清单**

```bash
grep -nE "^(## 2\. Subagent Prompt Construction|### Standardized Prompt Template|### What Must NOT Be Included in Subagent Prompts|### Context Isolation)$" protocols/review-orchestrator-protocol.md
```
Expected: 输出对应行号。

- [ ] **Step 2: 在 §2 的标准化提示模板中明确四者并列加载**

找到提示模板中列角色/模板/spec 的位置，加入 `references/common.md`：

```markdown
你的加载清单（四者并列，不得省略）：
1. `references/common.md`（共享权威定义：严重度/证据等级/Finding 字段/独立评审规则）
2. `roles/<你的角色>.md`
3. `templates/<你的模板>.md`
4. 被审 spec 路径
```

- [ ] **Step 3: 在 `### Context Isolation`（§2 内）补一句引用**

```markdown
> 独立评审/上下文隔离规则见 `references/common.md` §4；subagent 提示词不得含主 agent 分析或其他角色评审。
```

- [ ] **Step 4: 校验引用已加、scope 未变**

```bash
echo "common-ref: $(grep -c 'references/common.md' protocols/review-orchestrator-protocol.md)"
```
Expected: `common-ref: ≥2`。

- [ ] **Step 5: 提交**

```bash
git add protocols/review-orchestrator-protocol.md
git commit -m "feat(B): orchestrator loads references/common.md in subagent contract"
```

---

### Task 10: 瘦身 templates/product-review.md

**Files:**
- Modify: `templates/product-review.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 product-review.md（字段名 `Gap`/`Trigger Scenario` 与 common.md §3 逐字一致）。

- [ ] **Step 1: 列出必须保留锚点**

```bash
grep -cE "^(## Review Metadata|## Findings|## Finding Summary|## Machine-Readable Finding Index|## Template Completion Rules)$" templates/product-review.md
```
Expected: `5`。

- [ ] **Step 2: 压缩每个 Finding 字段（如 `### PR-001` 下 `### Severity`/`### Evidence Class`/…）的说明性散文为 ≤2 行，保留字段名与必填标记；字段定义与 common.md §3 对齐（不得重命名）。在模板顶部 `## 输出语言` 后加一句引用：**

```markdown
> Finding 字段契约（共享必填 + Product 差异字段 `Gap`/`Trigger Scenario`）见 `references/common.md` §3。
```

- [ ] **Step 3: 校验字段名未变、引用已加**

```bash
echo "common-ref: $(grep -c 'references/common.md' templates/product-review.md)"
echo "gap-field: $(grep -c '^### Gap$' templates/product-review.md)"
echo "trigger-field: $(grep -c '^### Trigger Scenario$' templates/product-review.md)"
```
Expected: `common-ref: ≥1`、`gap-field: ≥1`、`trigger-field: ≥1`。

- [ ] **Step 4: 提交**

```bash
git add templates/product-review.md
git commit -m "refactor(B): slim templates/product-review.md prose"
```

---

### Task 11: 瘦身 templates/system-review.md

**Files:**
- Modify: `templates/system-review.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 system-review.md（差异字段 `Risk`/`Trigger Condition`/`Causal Chain`/`Likelihood`/`Reversibility` 与 common.md §3 逐字一致）。

- [ ] **Step 1: 列出必须保留锚点**

```bash
grep -cE "^(## Review Metadata|## Findings|## Finding Summary|## System Risk Coverage|## Machine-Readable Finding Index|## Template Completion Rules)$" templates/system-review.md
```
Expected: `6`。

- [ ] **Step 2: 压缩 Finding 字段说明散文为 ≤2 行，保留字段名；模板顶部加引用：**

```markdown
> Finding 字段契约（共享必填 + System 差异字段 `Risk`/`Trigger Condition`/`Causal Chain`/`Likelihood`/`Reversibility`）见 `references/common.md` §3。
```

- [ ] **Step 3: 校验字段名未变**

```bash
echo "common-ref: $(grep -c 'references/common.md' templates/system-review.md)"
for f in Risk "Trigger Condition" "Causal Chain" Likelihood Reversibility; do echo "$f: $(grep -c "^### $f\$" templates/system-review.md)"; done
```
Expected: `common-ref: ≥1`，五个字段名各 ≥1。

- [ ] **Step 4: 提交**

```bash
git add templates/system-review.md
git commit -m "refactor(B): slim templates/system-review.md prose"
```

---

### Task 12: 瘦身 templates/test-review.md

**Files:**
- Modify: `templates/test-review.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 test-review.md（`Finding Type` 必填，与 common.md §3 Test 差异字段一致）。

- [ ] **Step 1: 列出必须保留锚点**

```bash
grep -cE "^(## Review Metadata|## Findings|## Testability Coverage|## Machine-Readable Finding Index|## Template Completion Rules)$" templates/test-review.md
```
Expected: `5`。

- [ ] **Step 2: 压缩 Finding 字段说明散文为 ≤2 行，保留 `### Finding Type`（必填）；模板顶部加引用：**

```markdown
> Finding 字段契约（共享必填 + Test 差异字段 `Gap`/`Trigger Scenario`/`Finding Type` **必填**）见 `references/common.md` §3。
```

- [ ] **Step 3: 校验**

```bash
echo "common-ref: $(grep -c 'references/common.md' templates/test-review.md)"
echo "finding-type: $(grep -c '^### Finding Type$' templates/test-review.md)"
```
Expected: `common-ref: ≥1`、`finding-type: ≥1`。

- [ ] **Step 4: 提交**

```bash
git add templates/test-review.md
git commit -m "refactor(B): slim templates/test-review.md prose"
```

---

### Task 13: 瘦身 templates/consolidated-review.md

**Files:**
- Modify: `templates/consolidated-review.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: 瘦身后的 consolidated-review.md（保留 CR-XXX 结构骨架与合并原则）。

- [ ] **Step 1: 列出必须保留锚点**

```bash
grep -cE "^(## Consolidation Principles|## Consolidated Findings|## Unmerged Source Findings|## Duplicate and Superseded Findings)$" templates/consolidated-review.md
```
Expected: `4`。

- [ ] **Step 2: 压缩 `### Consolidation Principles` 的 6 条解释散文为每条 ≤1 行；压缩 `## CR-001`/`## CR-002` 示例中的重复叙述，保留字段骨架（`### Consolidated Severity`/`### Evidence Class`/…）；模板顶部加引用：**

```markdown
> 合并原则与字段契约见 `references/common.md` §3 与 §4（独立评审）；关系分类 7 类见 consolidation-protocol.md §6。
```

- [ ] **Step 3: 校验合并原则 6 条与 CR 结构仍在**

```bash
echo "common-ref: $(grep -c 'references/common.md' templates/consolidated-review.md)"
echo "principles: $(grep -cE '^### [0-9]\. ' templates/consolidated-review.md)"
```
Expected: `common-ref: ≥1`、`principles: ≥6`。

- [ ] **Step 4: 提交**

```bash
git add templates/consolidated-review.md
git commit -m "refactor(B): slim templates/consolidated-review.md prose"
```

---

### Task 14: 更新 SKILL.md 与 CLAUDE.md

**Files:**
- Modify: `SKILL.md`, `CLAUDE.md`
- Read: `references/common.md`

**Interfaces:**
- Produces: SKILL.md/CLAUDE.md 重复的严重度/边界段落改为引用 common.md，并显式登记 `references/` 路径。

- [ ] **Step 1: 在 SKILL.md 中定位重复的严重度/边界段落**

```bash
grep -nE "严重度|证据等级|独立评审|references/" SKILL.md | head
```
Expected: 输出相关行号。

- [ ] **Step 2: 将 SKILL.md 中"严重度定义/边界摘要/独立评审"的重复陈述替换为引用，并新增路径登记段**

```markdown
## 共享定义

- 严重度、证据等级、Finding 字段契约、独立评审/隔离规则等共享定义统一位于 `references/common.md`（权威源）。
- 各角色/模板/协议须引用该文件，不得各自重述；修改须同批变更（设计规格 §4 第 10、11 条）。
```

- [ ] **Step 3: 对 CLAUDE.md 执行相同替换（保持与 SKILL.md 一致）**

- [ ] **Step 4: 校验两文件均引用且登记路径**

```bash
echo "SKILL refs: $(grep -c 'references/common.md' SKILL.md)"
echo "CLAUDE refs: $(grep -c 'references/common.md' CLAUDE.md)"
```
Expected: 两值均 ≥1。

- [ ] **Step 5: 提交**

```bash
git add SKILL.md CLAUDE.md
git commit -m "refactor(B): SKILL.md/CLAUDE.md reference common.md, register path"
```

---

### Task 15: 运行 --compare 验证降幅 ≥40%

**Files:**
- Read: `scripts/token_analyzer.py`, `scripts/prompt_scope.json`
- Read: 全部 14 个框架/共享文件（Task 2–14 产出）

**Interfaces:**
- Produces: `--compare` 的 PASS/FAIL 结果与 reduction_pct；决定是否达到候选 ≤ 61,153 token。

- [ ] **Step 1: 运行对比（此时 common.md 已建、13 文件已瘦身）**

```bash
python3 scripts/token_analyzer.py --compare
```
Expected（PASS）: 退出码 0，JSON 含 `"pass": true`、`"reduction_pct": <≥40.0>`、`"candidate_tokens": <≤61153>`、`"candidate_missing": []`。

- [ ] **Step 2: 若 FAIL（reduction_pct < 40 或 candidate_missing 非空），回到 Task 3–14 进一步压缩，优先砍协议/模板中的剩余示例 prose，直至 PASS**

- [ ] **Step 3: PASS 后提交一次总闸确认**

```bash
git add -A
git commit -m "verify(B): token_analyzer --compare PASS (reduction >=40%, candidate <=61153)" || echo "nothing-to-commit"
```

---

### Task 16: 一致性 grep 校验（枚举/字段/不变量/引用可解析）

**Files:**
- Read: `references/common.md` + 全部 roles/templates/protocols

**Interfaces:**
- Produces: 一组 grep 校验全绿，确认无静默删除、无悬空引用。

- [ ] **Step 1: 枚举一致性——四字面量在 common.md 与各角色可输出子集 grep 可达**

```bash
echo "common-enum: $(grep -cE 'CONFIRMED_DEFECT|MATERIAL_RISK|CONFIRMED_GAP|DESIGN_PREFERENCE' references/common.md)"
echo "role-enum: $(grep -cE 'CONFIRMED_DEFECT|MATERIAL_RISK|CONFIRMED_GAP' roles/*.md)"
```
Expected: `common-enum: ≥4`、`role-enum: ≥3`（三角色文件各含其可输出子集）。

- [ ] **Step 2: 字段一致性——差异字段名在 common.md 与各模板 grep 可达**

```bash
for f in Gap "Trigger Scenario" Risk "Trigger Condition" "Causal Chain" Likelihood Reversibility "Finding Type"; do echo "$f: common=$(grep -c "^| .*$f" references/common.md || grep -c "$f" references/common.md) tmpl=$(grep -rl "$f" templates/*.md | wc -l)"; done
```
Expected: 每个字段在 common.md ≥1、在 templates 中 ≥1 个文件命中。

- [ ] **Step 3: 不变量字面量清单——§4 第 11 条清单在瘦身后框架仍可 grep 命中（抽样）**

```bash
echo "CR-ID: $(grep -rl 'CR-ID' roles templates protocols | wc -l)"
echo "INCOMPLETE: $(grep -rl 'INCOMPLETE' protocols templates | wc -l)"
echo "独立评审: $(grep -rl '独立评审' references/common.md roles templates protocols | wc -l)"
```
Expected: 各 ≥1（字面量未被静默删除）。

- [ ] **Step 4: 引用可解析——所有对 common.md 的引用均指向真实存在的文件**

```bash
test -f references/common.md && echo "common.md exists: OK" || echo "common.md MISSING"
grep -rn 'references/common.md' roles templates protocols SKILL.md CLAUDE.md | wc -l
```
Expected: `common.md exists: OK`，引用计数 ≥ 任务累计。

- [ ] **Step 5: 提交校验脚本（如需留存）或直接结束**

```bash
git add -A
git commit -m "verify(B): consistency grep checks green (enum/field/invariant/reference)" || echo "nothing-to-commit"
```

---

### Task 17: 收尾——删除项清单定稿与 review-002 状态更新

**Files:**
- Modify: `docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md`
- Read: `docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-002/consolidated-review.md`
- Read: `docs/superpowers/reviews/spec-review-slim-design/index.md`

**Interfaces:**
- Produces: 删除项清单完整、review-002 最终状态由 CHANGES_REQUIRED 推进（实现完成）。

- [ ] **Step 1: 通读删除项清单，确认无"影响质量约束=是"的未决策项**

```bash
grep -c "是" docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md
```
Expected: `0`（若有，须先走决策流程，不得静默合入）。

- [ ] **Step 2: 在 review-002 consolidated-review.md 顶部"Final Review State"处将 CHANGES_REQUIRED 更新为 APPROVED，并补一句：方案 B 已实施，--compare PASS，一致性校验全绿**

- [ ] **Step 3: 在 index.md 的 round-2 行与趋势段同步最终状态为 APPROVED**

- [ ] **Step 4: 提交收尾**

```bash
git add docs/superpowers/specs/2026-08-04-spec-review-slim-design.deletions.md docs/superpowers/reviews/spec-review-slim-design/
git commit -m "chore(B): finalize deletion log, mark review-002 APPROVED after B implementation"
```

---

## Self-Review（写作者自查）

**1. Spec coverage 对照：**
- §3.1 common.md 内容 → Task 2 完整覆盖（严重度/证据/字段/隔离/边界/不变量清单）。
- §3.2 角色瘦身（删四共享块、保留独有）→ Task 3/4/5 覆盖，含独有块保留校验。
- §3.3 协议瘦身 → Task 6/7/8/9 覆盖；合并规则/关系分类/CR-ID/完整性/状态枚举均设保留锚点。
- §3.4 模板瘦身 → Task 10/11/12/13 覆盖，字段名与 common.md 逐字一致校验。
- §3.5 SKILL.md/CLAUDE.md → Task 14 覆盖。
- §4 不变量 → Task 2 落 common.md §6、Task 16 grep 校验、Task 17 删除清单定稿。
- §5 加载契约 → Task 9 orchestrator 四者并列加载。
- §6 验收 → Task 15 `--compare`、Task 16 一致性 grep、Task 2/16 不变量字面量。
- §7 删除项清单 → Task 1 建、各任务追加、Task 17 定稿。
- CR-001 质量护栏可判定清单 → Task 15/16 即其落地。
- CR-002 证据枚举对齐 → Task 2 + Task 16 枚举 grep。
- CR-003 System 字段契约 → Task 2 + Task 11 字段校验。
- CR-005 中心目标链接 → Task 15 `--compare` PASS 即达成（spec §6 已写明）。
- CR-006 固定框架开销措辞 → 已在 spec (`53abe05`) 修订，实现不涉及。
- CR-007 删除安全网 → Task 1/17 删除清单 + Task 16 不变量 grep。
- CR-004 算法 → 已修（`6dcc0b3`），本计划仅消费。
- CR-008 运行时加载失败检测 → DEFERRED，本计划不处理。

**2. Placeholder 扫描：** 无 TBD/TODO/"implement later"/"similar to Task N"。每个代码/命令步骤均含实际内容或精确文件/段名。common.md 提供完整逐字内容。

**3. Type/名称一致性：** 引用路径统一为 `references/common.md`；章节锚点统一为 `§1`/`§2`/`§3`/`§4`/`§6`；字段名与差异字段清单（Gap/Trigger Scenario/Risk/Trigger Condition/Causal Chain/Likelihood/Reversibility/Finding Type）在 Task 2 定义、Task 3–14 与 Task 16 一致使用。证据等级四字面量全程一致。
