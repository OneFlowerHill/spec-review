# v2 缺陷修复设计

> 日期：2026-07-19
> 依据：`docs/项目二期审查报告.md`（D-002 ~ D-010）
> 审核反馈：Consolidated Review（CR-001 ~ CR-008），采纳 7 项，部分采纳 3 项，不采纳 1 项
> 目标：修复所有残留/新引入缺陷，使 skill 达到"能稳定标记、能可靠统计"的状态

---

## 0. 审核反馈处置记录

| CR | 审核定级 | 最终判定 | 核心原因 |
|----|---------|---------|---------|
| CR-001 | P0 | **采纳，降为 P1** | 行号偏移是真实问题，但后果是定位不准而非数据损坏；改为内容锚点定位 |
| CR-002 | P0 | **采纳，降为 P1** | P3 移除范围确实不完整，必须全面清除；但非数据损坏 |
| CR-003 | P1 | **部分采纳** | COMPLETED 遗漏和验证主观性采纳；字段改名区分流程状态 |
| CR-004 | P1 | **部分采纳** | 全扫描和表述修正采纳；分类边界指导不采纳（consolidation-protocol 已有决策树） |
| CR-005 | P1 | **部分采纳** | 客观标准和迭代上限采纳；固定测试输入和覆盖率要求不采纳（过度设计） |
| CR-006 | P1 | **采纳** | Question/Finding 状态必须区分；保留 Question 的 OPEN |
| CR-007 | P1 | **采纳** | 更新计划文件中的陈旧值 |
| CR-008 | P2 | **不采纳** | YAGNI——防漂移机制解决的是未来可能的问题 |

**两个冲突的决策**：
1. **COMPLETED 状态** → YAML 中 `decision_status` 改名为 `processing_status`，值为 `PENDING_DECISION|DECIDED`，与 Finding 的 7 态解耦；Decision Records 骨架中的 `COMPLETED` 改为 `DECIDED`
2. **Question 状态** → 保留 Question 的 `OPEN`，不为 Question 定义独立生命周期枚举

---

## 1. 修复策略总览

所有 9 个缺陷归为 3 个批次，按依赖关系排序执行：

| 批次 | 缺陷 | 主题 | 原则 |
|------|------|------|------|
| 1 | D-002 / D-003 / D-004 / D-005 / D-006 | 契约层统一 | 每个枚举确定唯一权威源，下游全部对齐 |
| 2 | D-008 / D-009 | 格式清理 | 机械删除悬挂围栏 |
| 3 | D-007 / D-010 | 陈旧文档 + 实跑验证 | 更新过时文档，实跑验证 |

**核心原则**：
- 先修权威源（finding-protocol / decision-protocol / consolidation-protocol），再修下游模板和角色文件
- 所有修改定位使用**内容锚点**而非行号（CR-001 采纳）
- 同一文件的多个修改必须**严格串行**执行（CR-001 采纳）

---

## 2. 权威源定义（单点真相）

修复前，先明确每个枚举的唯一权威源：

| 枚举 | 权威源文件 | 权威值 |
|------|-----------|--------|
| 证据类 (Evidence Class) | `protocols/finding-protocol.md` | `CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE / CONFIRMED_GAP` |
| 严重度 (Severity) | `protocols/finding-protocol.md` | `P0 / P1 / P2`（移除 P3） |
| 关系分类 (Relationship) | `protocols/consolidation-protocol.md` | 7 类：`DUPLICATE / SAME_ROOT_CAUSE / RELATED / INDEPENDENT / CONTRADICTORY / SUBSET / CONSEQUENCE` |
| 决策状态 (Decision Status) | `protocols/decision-protocol.md` | 7 态：`PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED` |

所有非权威源文件中的同类枚举必须与权威源完全一致，不得自行定义、增减或重命名。

---

## 3. 批次 1：契约层统一（5 个 P1 缺陷）

### 3.1 D-003 · finding-protocol.md 补 CONFIRMED_GAP

**当前状态**：finding-protocol.md 定义 3 个证据类（CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE），test-designer.md 和 test-review.md 使用了第 4 个 `CONFIRMED_GAP` 但无合同出处。

**修复动作**：在 finding-protocol.md 的 `#### DESIGN_PREFERENCE` 段落之后、`---` 分隔线之前，新增：

```markdown
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
```

**影响范围**：
- `roles/test-designer.md` — 无需修改（CONFIRMED_GAP 已在使用，补上合同出处即闭环）
- `templates/test-review.md` — 无需修改（同上）
- `roles/product-reviewer.md` / `roles/system-critic.md` — 无需修改（这两个角色不使用 CONFIRMED_GAP）

**验证**：`grep -r "CONFIRMED_GAP" --include="*.md"` — 所有命中均在 finding-protocol.md 有定义。

### 3.2 D-004 · 移除 P3 严重度（全范围清除）

**当前状态**：finding-protocol.md 定义 P0/P1/P2/P3，decision-protocol.md 对 P3 无决策分支。P3 在以下文件中存在引用，必须全部清除（CR-002 采纳）：

| 文件 | P3 内容 | 修复动作 |
|------|---------|---------|
| `protocols/finding-protocol.md` | `### P3` 段落 + 枚举汇总 `P0 / P1 / P2 / P3` | 删除 P3 段落；枚举汇总改为 `P0 / P1 / P2`；`Do not inflate P2 or P3 issues` 改为 `Do not inflate P2 issues` |
| `protocols/decision-protocol.md` | `4. P3 Findings.` | 删除该行 |
| `protocols/consolidation-protocol.md` | `P0 / P1 / P2 / P3` 枚举 + `4. P3 severity.` | 枚举改为 `P0 / P1 / P2`；删除 P3 severity 行 |
| `roles/product-reviewer.md` | `## P3` 段落 | 删除 P3 段落及其内容 |
| `roles/system-critic.md` | `## P3` 段落 | 删除 P3 段落及其内容 |
| `roles/test-designer.md` | `## P3` 段落 | 删除 P3 段落及其内容 |
| `SKILL.md` | `## P3 — May defer` 段落 | 删除 P3 段落及其内容 |
| `CLAUDE.md` | `**P3**：轻微歧义/文档——仅在协议支持时使用` | 删除该行 |
| `templates/consolidated-review.md` | "By Severity" 统计中 `* P3: <COUNT>` | 删除该行 |
| `templates/test-review.md` | `P2 and P3` | 改为 `P2` |
| `docs/superpowers/plans/2026-07-19-proposal-review-skill-v2.md` | `P0 / P1 / P2 / P3` + `P0 and P1 findings over P2 and P3` + `## P3 — May defer` | 枚举改为 `P0 / P1 / P2`；优先级改为 `P0 and P1 findings over P2`；删除 P3 段落 |

**验证**：`grep -rn "### P3\|## P3\|P0.*P1.*P2.*P3" --include="*.md"` → 零命中（可机械判定）。

### 3.3 D-005 · 关系分类统一为 7 类（全范围清除）

**当前状态**：consolidation-protocol.md 定义 7 类，consolidated-review.md 模板使用 4 类（SAME_PROBLEM / RELATED_PROBLEMS / ONE_CAUSES_ANOTHER / DIFFERENT_PROBLEMS）。v2 计划文件也有陈旧 4 类引用。

**修复动作**：

1. **templates/consolidated-review.md** — 全文扫描并替换所有旧分类引用：

   a. Relationship Classification 区域（`### Relationship Classification` 下的 4 类列表）——替换为 7 类：
   ```markdown
   * `DUPLICATE` — findings describe the same problem with substantially overlapping evidence;
   * `SAME_ROOT_CAUSE` — findings have different manifestations but share one root cause;
   * `RELATED` — findings are connected but independently actionable;
   * `INDEPENDENT` — findings should not be consolidated;
   * `CONTRADICTORY` — findings reach opposite conclusions about the same issue;
   * `SUBSET` — one finding's scope is entirely contained within another;
   * `CONSEQUENCE` — one finding is a direct causal consequence of another.
   ```

   b. 示例区域（`SAME_PROBLEM / RELATED_PROBLEMS / ONE_CAUSES_ANOTHER / DIFFERENT_PROBLEMS`）——替换为 7 类枚举

   c. YAML 区域（`relationship_classification: "SAME_PROBLEM|RELATED_PROBLEMS|ONE_CAUSES_ANOTHER|DIFFERENT_PROBLEMS"`）——替换为 `"DUPLICATE|SAME_ROOT_CAUSE|RELATED|INDEPENDENT|CONTRADICTORY|SUBSET|CONSEQUENCE"`

2. **docs/superpowers/plans/2026-07-19-proposal-review-skill-v2.md** — YAML 区域的 `relationship_classification: "SAME_PROBLEM|RELATED_PROBLEMS|ONE_CAUSES_ANOTHER|DIFFERENT_PROBLEMS"` 替换为 7 类（CR-007 采纳）

3. **finding-protocol.md** — 不定义关系分类（由 consolidation-protocol.md 定义），无需修改。修正原方案表述：finding-protocol.md 不定义关系分类，关系分类的唯一权威源是 consolidation-protocol.md。

**验证**：`grep -ri "same.problem\|related.problem\|one.cause\|different.problem" --include="*.md"` → 零命中（不区分大小写，CR-004 采纳）。

### 3.4 D-002 · consolidated-review.md 决策词汇统一

**当前状态**：同一文件内决策状态有多套命名。精确差异如下：

| 位置（内容锚点） | 当前值 | 应统一为 |
|-----------------|--------|---------|
| `### Finding Status` 下的 Allowed values 列表 | 6 态（缺 PENDING_DECISION） | 补全为 7 态，PENDING_DECISION 放首位 |
| `**Decision options**:` 行 | 6 态（缺 PENDING_DECISION） | 7 态，补 PENDING_DECISION |
| `### Decision Status` 骨架（Decision Template 内） | 6 态（缺 PENDING_DECISION） | 7 态，补 PENDING_DECISION |
| `### Decision` 骨架（DR-001 示例内） | `ACCEPT / REJECT / DEFER / MODIFY / DUPLICATE / SUPERSEDE / RESOLVE` | `PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED` |
| `### By Status` 统计区域 | `Open / Ready for Decision / Accepted / Rejected / Deferred / Resolved / Duplicate / Represented Elsewhere` | 7 态计数：`PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED` |
| YAML `status` 字段（consolidated_findings） | 7 态 ✅ | 已正确，无需修改 |
| YAML `decision_status` 字段（consolidated_findings） | `PENDING_DECISION` ✅ | 已正确 |
| YAML `status` 字段（conflicts） | `REQUIRES_DECISION` | `PENDING_DECISION` |
| YAML `decision_status` 字段（decision_queue） | `PENDING` | `PENDING_DECISION` |
| YAML `decision_status` 字段（decisions） | `PENDING_DECISION\|COMPLETED` | 改字段名为 `processing_status`，值为 `PENDING_DECISION\|DECIDED`（CR-003 采纳：与 Finding 7 态解耦） |
| `### Decision Status`（DR-001 示例末尾） | `COMPLETED` | `DECIDED`（与 YAML 字段改名同步） |
| YAML `status` 字段（review 顶层） | `COMPLETED` | `COMPLETED` — 保留不变（这是审核流程状态，不是 Finding 决策状态，语义不同） |

**修复动作**：按上表逐一替换。所有修改定位使用内容锚点（如"在 `### Finding Status` 下的 Allowed values 列表中"），不使用行号。

**验证**（可机械判定，CR-003 采纳）：
- `grep -rn 'status:.*"OPEN"' --include="*.md" templates/` → 零命中
- `grep -rn 'REQUIRES_DECISION' --include="*.md"` → 零命中
- `grep -rn 'decision_status' --include="*.md" templates/` → 零命中（已改名为 processing_status）
- `grep -rn '"PENDING"' --include="*.md" templates/` → 零命中

### 3.5 D-006 · 各模板 status 枚举统一（区分 Finding 与 Question）

**当前状态**：模板中 `OPEN` 出现在两种不同语义的上下文中（CR-006 采纳）：

**Finding 状态的 OPEN → PENDING_DECISION**：

| 文件 | 位置（内容锚点） | 当前值 | 修改为 |
|------|-----------------|--------|--------|
| product-review.md | Finding Status 说明文字 | `OPEN` | `PENDING_DECISION` |
| product-review.md | YAML `status` 字段（3 处） | `"OPEN"` | `"PENDING_DECISION"` |
| system-review.md | Finding Status 说明文字（3 处） | `OPEN` | `PENDING_DECISION` |
| system-review.md | YAML `status` 字段（5 处） | `"OPEN"` | `"PENDING_DECISION"` |
| test-review.md | YAML `status` 字段（1 处） | `"OPEN"` | `"PENDING_DECISION"` |

**Question 状态的 OPEN → 保留 OPEN**：

| 文件 | 位置（内容锚点） | 当前值 | 修改为 |
|------|-----------------|--------|--------|
| product-review.md | Unresolved Product Questions 的 `#### Status` | `OPEN` | `OPEN`（保留，Question 不是 Finding） |
| test-review.md | Unresolved Verification Questions 的 `#### Status` | `OPEN` | `OPEN`（保留，Question 不是 Finding） |
| test-review.md | YAML `open_questions` 的 `status` | `"OPEN"` | `"OPEN"`（保留） |

**修复动作**：按上表区分修改。逐行确认每个 OPEN 的实体类型（Finding vs Question），仅替换 Finding 的 OPEN。

**验证**（可机械判定）：
- `grep -rn 'status:.*"OPEN"' --include="*.md" templates/` → 仅在 `open_questions` 上下文中命中
- `grep -rn 'Status\n\nOPEN' --include="*.md" templates/` → 仅在 Question 区域命中

---

## 4. 批次 2：格式清理（2 个 P2 缺陷）

### 4.1 D-008 · finding-protocol.md 末尾悬挂围栏

**当前状态**：文件末尾 `This protocol defines the Finding contract.` 段落之后有两个连续空围栏。

**修复动作**：删除文件末尾的两个空围栏行。

**验证**：文件以正文段落结尾，不以 ` ``` ` 结尾。

### 4.2 D-009 · system-critic.md 残留围栏

**当前状态**：在 `### Reviewer Notes` 段落的最后一个示例之后、`---` 分隔线之前，有一个带非法 id 属性的悬挂代码围栏 ` ```id="0p8u3h" `。

**修复动作**：删除该残留行。

**验证**：Reviewer Notes 内容与 `---` 分隔线之间无多余围栏。

---

## 5. 批次 3：陈旧文档 + 实跑验证（2 个 P2 缺陷）

### 5.1 D-007 · 陈旧文档清理

**当前状态**：

1. `docs/codebase/.codebase-scan.txt` — 记录旧文件结构，未反映 v2 新增文件
2. `docs/项目一期建设审查报告.md` — 记录已被 v2 修复的旧缺陷状态
3. `.superpowers/sdd/progress.md` — 7 个任务全标 pending，但实际已完成

**修复动作**：

1. **codebase-scan.txt**：删除此文件（其信息可由 `find` 命令随时获取，维护成本高于价值）
2. **项目一期建设审查报告.md**：在文件顶部添加历史标注：`> ⚠️ 本报告为 v1 审查记录，缺陷状态已过时。请参考 docs/项目二期审查报告.md 获取最新状态。`
3. **progress.md**：删除此文件（SDD 流程已结束，pending 状态已无意义）

### 5.2 D-010 · 实跑验证

**当前状态**：skill 从未在真实 spec 上完整跑过。

**修复动作**（在批次 1+2 修复完成后执行）：

1. 使用项目中现有的 spec/proposal 文件作为测试输入
2. 调用 `yy-review-orchestrator` skill 执行一次完整审核
3. 验证输出到 `docs/superpowers/reviews/<stem>/YYYY-MM-DD-review-001/`

**客观通过条件**（CR-005 采纳）：

| 检查项 | 通过标准 | 判定方式 |
|--------|---------|---------|
| 产物完整性 | 每个产物文件包含模板定义的所有一级章节标题 | `grep "^# "` 命题检查 |
| YAML 同步 | findings 数组长度 = 详细章节 ID 数量 | 人工比对 |
| 枚举合规 | 无陈旧枚举值残留 | `grep -rn '"OPEN"\|"P3"\|SAME_PROBLEM\|REQUIRES_DECISION' docs/superpowers/reviews/` → 零命中 |
| Integrity Check | source_findings 总数 = merged + unmerged + duplicate/superseded 记录 | 人工比对 |

**迭代控制**（CR-005 采纳）：
- 最大迭代次数：3 轮修复-验证
- 第 3 轮后仍有未解决问题：记录为新缺陷，验证阶段以 INCOMPLETE 状态退出

---

## 6. 修改文件清单

| 文件 | 修改类型 | 涉及缺陷 | 审核反馈 |
|------|---------|---------|---------|
| `protocols/finding-protocol.md` | 补 CONFIRMED_GAP；删 P3 段落+枚举；删末尾悬挂围栏 | D-003, D-004, D-008 | CR-002, CR-004 |
| `protocols/decision-protocol.md` | 删 P3 引用 | D-004 | CR-002 |
| `protocols/consolidation-protocol.md` | 删 P3 枚举+引用 | D-004 | CR-002 |
| `templates/consolidated-review.md` | 决策词汇统一 7 态；关系分类统一 7 类；COMPLETED→DECIDED；decision_status→processing_status | D-002, D-005 | CR-001, CR-003, CR-004 |
| `templates/product-review.md` | Finding OPEN→PENDING_DECISION；Question OPEN 保留 | D-006 | CR-006 |
| `templates/system-review.md` | OPEN→PENDING_DECISION | D-006 | |
| `templates/test-review.md` | Finding OPEN→PENDING_DECISION；Question OPEN 保留；P2 and P3→P2 | D-004, D-006 | CR-002, CR-006 |
| `roles/product-reviewer.md` | 删 P3 段落 | D-004 | CR-002 |
| `roles/system-critic.md` | 删 P3 段落；删悬挂围栏 | D-004, D-009 | CR-002 |
| `roles/test-designer.md` | 删 P3 段落 | D-004 | CR-002 |
| `SKILL.md` | 删 P3 段落 | D-004 | CR-002 |
| `CLAUDE.md` | 删 P3 行 | D-004 | CR-002 |
| `docs/superpowers/plans/2026-07-19-proposal-review-skill-v2.md` | P3→删除；4 类→7 类 | D-004, D-005 | CR-007 |
| `docs/codebase/.codebase-scan.txt` | 删除 | D-007 | |
| `docs/项目一期建设审查报告.md` | 添加历史标注 | D-007 | |
| `.superpowers/sdd/progress.md` | 删除 | D-007 | |

---

## 7. 执行顺序与依赖

同一文件的多个修改必须严格串行执行（CR-001 采纳）。所有修改定位使用内容锚点，不使用行号。

```
批次 1（契约层统一）— 严格串行：

  Step 1: finding-protocol.md（补 CONFIRMED_GAP + 删 P3 + 删悬挂围栏）
          ↓
  Step 2: decision-protocol.md（删 P3）
          ↓
  Step 3: consolidation-protocol.md（删 P3）
          ↓
  Step 4: consolidated-review.md（关系分类 7 类 → 决策词汇统一 → COMPLETED/processing_status）
          ↓  （同文件串行，按此顺序执行）
  Step 5: 三个角色文件（删 P3 段落）
          ↓  （不同文件，可并行）
  Step 6: SKILL.md + CLAUDE.md（删 P3）
          ↓  （不同文件，可并行）
  Step 7: 三个模板文件（Finding OPEN→PENDING_DECISION；Question OPEN 保留；test-review P2 and P3→P2）
          ↓  （不同文件，可并行）
  Step 8: v2 计划文件（P3 删除 + 4 类→7 类）

批次 2（格式清理）— 与批次 1 Step 1 合并执行：
  system-critic.md 删悬挂围栏（与 Step 5 的 P3 删除合并为同一次修改）

批次 3（收尾）— 依赖批次 1+2 完成：
  Step 9: 陈旧文档清理（删 codebase-scan.txt + 标注一期报告 + 删 progress.md）
  Step 10: 实跑验证
```

---

## 8. 验证检查清单

批次 1+2 完成后，执行以下全仓检查（全部可机械判定）：

- [ ] `grep -rn "### P3\|## P3\|P0.*P1.*P2.*P3" --include="*.md"` → 零命中
- [ ] `grep -ri "same.problem\|related.problem\|one.cause\|different.problem" --include="*.md"` → 零命中
- [ ] `grep -rn 'status:.*"OPEN"' --include="*.md" templates/` → 仅在 `open_questions` 上下文命中
- [ ] `grep -rn 'REQUIRES_DECISION' --include="*.md"` → 零命中
- [ ] `grep -rn 'decision_status' --include="*.md" templates/` → 零命中（已改名为 processing_status）
- [ ] `grep -rn '"PENDING"' --include="*.md" templates/` → 零命中
- [ ] `grep -rn 'CONFIRMED_GAP' --include="*.md"` → 所有命中在 finding-protocol.md 有定义
- [ ] 代码围栏配平检查：`grep -c '```' <file>` 对所有修改文件为偶数
- [ ] YAML 索引与详细内容一致性（人工抽检）

---

## 9. 风险与回退

| 风险 | 影响 | 缓解 |
|------|------|------|
| P3 移除后，Test Designer 的低严重度发现无处安放 | P2 严重度范围变宽，可能稀释高优先级信号 | P2 定义已包含"边界情况/可维护性"，语义足够覆盖原 P3 场景 |
| 关系分类从 4 类扩到 7 类，subagent 可能用错 | 合并阶段分类不一致 | consolidation-protocol.md 已有完整决策树（第 193-428 行），模板列出选项即可 |
| 实跑可能暴露新问题 | 需要额外修复轮次 | 预期之内，3 轮迭代上限控制范围 |
| processing_status 与 decision_status 拆分可能造成理解混淆 | 两个"状态"字段语义需区分 | processing_status 是流程状态（是否已处理），decision 是 Finding 决策（接受/拒绝等），字段名已显式区分 |
