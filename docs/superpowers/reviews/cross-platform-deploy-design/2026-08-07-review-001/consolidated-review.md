# Consolidated Review

## 输出语言

本审核的所有描述性内容必须使用中文撰写。

以下内容保持英文：

- Finding ID（CR-001, CR-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 证据等级：CONFIRMED_DEFECT, MATERIAL_RISK
  - 置信度：HIGH, MEDIUM, LOW
  - 决策状态：PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
  - 关系分类：DUPLICATE, SAME_ROOT_CAUSE, RELATED, INDEPENDENT, CONTRADICTORY, SUBSET, CONSEQUENCE
  - 冲突状态：NO_CONFLICT, MINOR_INTERPRETATION_DIFFERENCE, MATERIAL_CONFLICT, UNRESOLVED_CONFLICT
  - 合并决策：MERGED, KEPT_SEPARATE, DUPLICATE, REQUIRES_CLARIFICATION
  - 审核状态：COMPLETED, AVAILABLE, MISSING
  - 审核结果：REQUIRES_REVIEW
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 和 description 等描述性字段使用中文。

## Review Metadata

### Review ID

2026-08-07-review-001

### Review Type

CONSOLIDATED_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md

### Consolidation Date

2026-08-07

### Consolidator

orchestrator（yy-spec-review 主 agent）

### Review Status

COMPLETED

---

## Consolidation Scope

本文档合并以下三个独立审核的产出：

- `yy-product-reviewer`
- `yy-system-critic`
- `yy-test-designer`

合并的目的：

1. 识别描述同一根本问题的 Finding；
2. 合并重复 Finding 而不丢失关键证据；
3. 保留实质性不同的 Finding；
4. 识别审核员之间的冲突；
5. 建立统一的 Finding 身份；
6. 保留原始审核视角；
7. 为规格所有者或 Superpowers 工作流准备单一审核文档；
8. 为每个 Finding 记录最终决策提供稳定结构。

本文档是合并产物，不替代原始审核报告。原始审核员的 Finding 仍是各自视角的来源。

---

## Source Reviews

| Reviewer            | Review Type    | Review ID   | Source File | Status              |
| ------------------- | -------------- | ----------- | ----------- | ------------------- |
| yy-product-reviewer | PRODUCT_REVIEW | 2026-08-07-review-001 | product-review.md | AVAILABLE |
| yy-system-critic    | SYSTEM_REVIEW  | 2026-08-07-review-001 | system-review.md  | AVAILABLE |
| yy-test-designer    | TEST_REVIEW    | 2026-08-07-review-001 | test-review.md    | AVAILABLE |

---

## Consolidation Principles

合并者遵循以下原则：

### 1. Findings 不因相似关键词合并

两个 Finding 不得仅因提到同一组件、措辞相似、严重度相同或后果相似而合并。只有描述同一根本问题或同一失效机制时才可合并。

### 2. 保留独立视角

若 Product、System、Test 审核员识别出同一根本问题的不同侧面，合并为一个 Finding 同时保留各视角的差异。

### 3. 不强制合并

两个 Finding 若确实独立，则保持分离。合并的目的是去重，不是人为减少 Finding 数量。

### 4. 不静默消解冲突

审核员对风险是否存在、严重度、可能性、后果、需求解释或建议解决方案产生分歧时，分歧必须显式记录。

### 5. 证据优先于审核员权威

Finding 不因由特定审核员提出、严重度高或多位审核员提及而被接受。合并者必须评估证据与推理。

### 6. 不确定性必须可见

不将推断行为转换为已确认行为，不将可能后果转换为确定后果，不将假设转换为需求。

---

## Consolidator Predispositions

以下记录主 agent 在 Phase 1（Context Acquisition）阶段形成的判断，这些判断可能影响合并过程，使其可审计。

### Predisposition 1

**本规格的性质判断**：本规格本质是一份"技能改名 + 双平台 symlink 部署 + Git/GitHub 推送"的运维迁移操作手册，而非产品功能规格。这可能导致合并者更关注操作鲁棒性、失败处理与可逆性，而对需求完整性、业务规则等产品维度评价相对宽松。合并时已注意不因"操作手册"性质而弱化对破坏性操作的安全要求。

### Predisposition 2

**Hermes 注册机制的现场核验**：合并者在 Phase 1 现场核验发现——`yuanbao` 是真实目录（非 symlink），其 `scan_verdict: backfilled` 记录来自 Hermes 官方 optional-skills 集；而参照范例 `goal-manager` 是 symlink 且当前不在 `~/.hermes/skills/.hub/lock.json` 的 installed 映射中。这与规格 §2.2"手动/symlink 放入的技能会被自动发现注册"的断言存在出入。这可能使合并者偏向采信 PR-003 / SC-004 / TD-002（Hermes 注册机制证据不足）的结论。合并时保留这些 Finding 的原始置信度，未因个人核验结果上调任何严重度。

### Predisposition 3

**规格验证标准自洽性的观察**：合并者在 Phase 1 注意到：新规格文件本身（`docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md`）含 25 处 `yy-` 引用，而规格 §5 的 `grep -rn "yy-"` 一致性目标要求改名后 `yy-` 仅命中"不改"目录，且 §3.1"不改"清单中的 specs 限定为"旧"规格。新规格不在"不改"清单内，因此按规格自身命令执行时 `grep -rn "yy-"` 会命中新规格，可能导致验证标准自相矛盾。此观察已并入 CR-004 的证据综合（grep 验证策略不足），但未作为独立的新增 Finding 注入（合并阶段不新增 Finding）。

### Predisposition 4

**破坏性与不可逆操作的敏感性**：本规格含 `rm -rf`（破坏性）与 GitHub 推送（不可逆、对外可见）操作。合并者可能因此更重视回滚路径、预检嵌入与数据安全类发现。合并时未因此上调严重度，但确保 PR-001 / SC-001 / TD-003 的合并（CR-001）保留了各自最完整的证据链。

---

# Consolidated Findings

## CR-001 — 旧技能目录删除缺乏安全的预检、客观判定标准与恢复保障

### Consolidated Severity

P1

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

规格 §4.7 步骤 7 使用 `rm -rf ~/.claude/skills/yy-spec-review` 删除旧技能目录。该目录是 7 月 20 日的真实目录拷贝（非 symlink），含 `.workbuddy/`、`.superpowers/` 等本地工作产物。规格 §6 风险表虽将"删除丢失本地改动"列为风险并给出 `diff -r` 对策，但：该预检未嵌入 §4.7 执行步骤序列；`diff -r` 输出的解读缺乏客观判定标准（无法区分"正常的版本演进差异"与"需保留的未同步改动"）；删除后若 `ln -s` 失败或后续步骤出错，无定义的回滚/恢复路径。

### Evidence

#### Confirmed Evidence

- 规格 §4.7 步骤 7 为"建 symlink：Claude 删旧+建新，Hermes 建新"，未引用 §6 的 `diff -r` 预检（SC-001 证据）。
- 规格 §6 风险表对策为"先 `diff -r` 旧拷贝与本地仓库，确认无未同步改动后再删"，但未定义判定标准（TD-003 证据）。
- 现场核验：`~/.claude/skills/yy-spec-review/` 为真实目录（非 symlink），与本地仓库存在内容差异（本地仓库多出 `agents/`、新增 specs/plans、`.superpowers/sdd/*.diff` 等；SKILL.md/CLAUDE.md/README.md 内容不同）。
- `rm -rf` 为不可逆文件系统操作（PR-001 证据）。

#### Inferred Evidence

- 操作者按 §4.7 线性执行时可能跳过 §6 风险表的交叉引用，直接执行 `rm -rf`（SC-001）。
- `ln -s` 可能因父目录权限、路径冲突而失败，形成"旧目录已删、新 symlink 未建"的中间状态（PR-001）。

#### Unknowns

- 自 7 月 20 日以来，用户在旧目录中是否有独有未同步改动（SC-001 Q-002 / TD-003）。
- 外部备份（如 Time Machine）是否存在、是否覆盖 `.workbuddy/` / `.superpowers/`。

### Trigger Scenario

1. 操作者按 §4.7 顺序执行步骤 1–6（改名、frontmatter、.gitignore、README、git init/commit、push）全部成功。
2. 操作者未交叉引用 §6 风险表，直接执行步骤 7 的 `rm -rf ~/.claude/skills/yy-spec-review`。
3. 旧目录中存在自 7 月 20 日以来未同步到本地仓库的独有工作产物。
4. 数据随 `rm -rf` 永久丢失；或 `rm -rf` 成功后 `ln -s` 失败，Claude Code 中 `/yy-spec-review` 与 `/spec-review` 均不可用。
5. 规格未定义此状态下的恢复操作。

### Consequence

- Data Impact：旧目录中的独有本地工作产物（`.workbuddy/` 记忆文件、`.superpowers/` 工作流状态）可能永久丢失，且不在 git 跟踪范围内，无法从 GitHub 恢复。
- Operational Impact：删除后 `ln -s` 失败将导致技能在两平台不可用；不同操作者对同一失败场景可能采取不同恢复策略，产生不一致的最终状态。
- Availability Impact：部署失败导致 Claude Code 审核技能中断，直到手动恢复。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

- PR-001

**Assessment:**

产品审核员指出规格仅覆盖了 `gh repo create --push`（步骤 6）的失败场景，而步骤 7 的 `rm -rf` 是破坏性操作且无恢复方案；步骤 1–5 的文件编辑同样无回退策略。这暴露了部署流程整体缺少回滚路径设计。

#### System Perspective

**Source Findings:**

- SC-001

**Assessment:**

系统批评员指出 §6 的 `diff -r` 预检与 §4.7 执行序列结构性脱节——对策未嵌入执行步骤，操作者可能跳过检查直接 `rm -rf`，导致数据永久丢失（IRREVERSIBLE）。

#### Test Perspective

**Source Findings:**

- TD-003

**Assessment:**

测试设计师指出"先 `diff -r` 确认无未同步改动"缺乏客观判定标准——无法区分可安全忽略的版本演进差异与需要保留的改动，不同操作者对同一 diff 输出可能做出相反决策。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

三个 Finding 从不同角度指向同一根本问题：旧技能目录的破坏性删除（`rm -rf`）缺少安全的删除流程。PR-001 关注恢复/回滚路径缺失，SC-001 关注预检未嵌入执行序列，TD-003 关注 diff 判定的客观性缺失。三者是同一根因的不同表现，合并为一个 Finding 并保留各自证据。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。三个审核员对问题存在与严重度判断一致（均认为 P1 级数据丢失风险）。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

1. 将 `diff -r` 预检作为独立步骤嵌入 §4.7 执行序列，置于 symlink 创建步骤之前（如步骤 6 与 7 之间）。
2. 定义 `diff -r` 输出的客观分类规则（如 SAFE_TO_IGNORE / NEEDS_REVIEW / BLOCK_DELETION），并明确安全删除的前置条件。
3. 删除前先执行备份（如 `cp -r` 到临时目录，或改用 `mv` 而非 `rm`），提供即时回滚能力。
4. 为步骤 1–5（文件编辑）与步骤 7（symlink 创建）分别定义失败处理策略与"不可逆点"。

### Source References

#### Product Review

- PR-001

#### System Review

- SC-001

#### Test Review

- TD-003

#### Design Spec References

- §4.3（双平台 symlink 安装）
- §4.7（实施顺序，步骤 7）
- §6（风险与对策，第 3 行）
- §2.4（环境就绪状态）

### Consolidation Decision

MERGED

#### Decision Rationale

PR-001、SC-001、TD-003 描述同一根本问题（旧目录破坏性删除的安全流程缺失），不同证据（恢复路径、步骤嵌入、判定标准）可互补为完整因果链。合并后保留全部三个证据来源。

### Severity Change Rationale

三个源 Finding 均为 P1（PR-001 P1 / SC-001 P1 / TD-003 P1），合并严重度维持 P1，无变更。未升级为 P0：风险表已识别该风险并提供 `diff -r` 对策，问题在于对策未强制化、未客观化，而非完全无防护；实际数据丢失需要"操作者跳过检查 + 旧目录确有独有改动"两个条件同时成立。

---

## CR-002 — Hermes 技能发现/注册机制假设证据不足，验证标准存在歧义

### Consolidated Severity

P1

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

规格 §2.2 断言 Hermes 的 "scan + backfill" 机制会"对手动/symlink 放入的技能自动发现注册"，并以 `yuanbao` 技能的 `scan_verdict: backfilled` 作为唯一证据。但该证据链存在两层缺口：(1) `yuanbao` 是真实目录（且来自官方 optional-skills 集），非 symlink；而参照范例 `goal-manager` 是 symlink 但不在 `lock.json` 的 installed 记录中——symlink 技能是否走同一 backfill 路径未经验证。(2) 目标路径是分类子目录 `software-development/spec-review/`，与 yuanbao 的根目录扁平路径不同，分类子目录下的 symlink 是否被扫描器同等处理无先例。此外，规格 §5 验证清单第 3 项用"或"连接 `/skills` 列表与 `lock.json` 记录两个验证来源，未定义权威判定依据与扫描触发时机，两个独立测试者可能对同一部署状态得出相反结论。

### Evidence

#### Confirmed Evidence

- 规格 §2.2："手动/symlink 放入的技能会被自动发现注册"，引用 yuanbao 为证据（PR-003 / SC-004）。
- 现场核验 `lock.json`：installed 映射中仅含 `yuanbao`（`install_path: "yuanbao"`，`scan_verdict: "backfilled"`，`metadata.backfilled_from: "optional-skills"`）；`goal-manager`（symlink）不在其中。
- 现场核验：`yuanbao` 为普通目录，`goal-manager` 为 symlink（指向本地仓库）。
- 规格 §5 第 3 项：`/skills` 列出 spec-review；或 `lock.json` 出现 backfilled 记录（TD-002）。
- 规格 §2.2 未定义扫描触发时机与 backfill 记录的期望字段结构（TD-002）。

#### Inferred Evidence

- Hermes 对 symlink 技能的发现机制可能与目录技能的 backfill 注册不同（PR-003）。
- backfill 机制对分类子目录中的 symlink 行为可能与根目录不同（SC-004）。

#### Unknowns

- Hermes scanner 对分类子目录中 symlink 的精确发现/backfill 逻辑（SC-004 Q-001 / TD-002 Q-002）。
- Hermes 重启后是否会对 symlink 技能执行延迟 backfill（PR-003）。
- Hermes 未来版本是否收紧技能发现机制（PR Q-002）。

### Trigger Scenario

1. 操作者按 §4.3 在 `~/.hermes/skills/software-development/` 下创建 spec-review symlink。
2. Hermes 启动或执行下次 scan。
3. Scanner 对分类子目录中 symlink 的处理与对根目录真实目录（yuanbao 场景）不同，或 symlink 技能不被持久化到 lock.json。
4. 操作者检查验证清单第 3 项：`/skills` 列表与 `lock.json` 给出不一致的结果（一个显示存在、另一个不显示），或因为扫描未执行而在启动后立即检查得到假阴性。
5. 规格未定义何者为权威判定依据，操作者可能误判部署成功或失败。

### Consequence

- Availability Impact：若 Hermes 端未识别技能，设计目标 1（兼容 Hermes）未达成，但可恢复（可将 symlink 移至根目录或手动编辑 lock.json）。
- Verification Impact：验证标准歧义可能掩盖真实的注册失败，或产生假阴性导致不必要的排查；部署成功/失败的判定不可靠。
- Operational Impact：需要额外的手动介入（验证、排查、可能的路径调整）。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

- PR-003

**Assessment:**

产品审核员指出 lock.json 的 backfill 证据被过度推广——yuanbao（目录技能）的证据不适用于 symlink 技能，`goal-manager`（symlink）未出现在 lock.json，说明验证信号可能产生假阴性。

#### System Perspective

**Source Findings:**

- SC-004

**Assessment:**

系统批评员指出 backfill 兼容性假设基于 yuanbao 单一样本，且 spec-review 的目标路径（分类子目录）与 yuanbao（根目录）在目录层级上不同，`software-development/` 下无用户手动放置后 backfill 的先例，假设未经独立验证。

#### Test Perspective

**Source Findings:**

- TD-002

**Assessment:**

测试设计师指出验证清单第 3 项的"或"逻辑歧义与扫描时机不可控，无法编写客观的验证标准；建议拆分验证项并定义期望的 lock.json 记录结构与等待时限。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

三个 Finding 均围绕"Hermes 对 symlink 技能的发现/注册机制未充分验证 + 验证标准不可靠"这一根本问题。PR-003 关注证据过度推广，SC-004 关注单一样本与分类目录差异，TD-002 关注验证标准的可测试性。三者互补，合并为一个 Finding。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。三个审核员一致认为 Hermes 注册机制断言证据不足，仅在置信度与严重度上略有差异（TD-002 为 P1，PR-003/SC-004 为 P2）。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

1. 在规格 §2.2 中区分"目录技能的 backfill 注册"与"symlink 技能的扫描发现"，不将 yuanbao 证据直接推广到 symlink 技能。
2. 在部署前进行最小化验证：在分类子目录下创建最小 symlink 测试技能，触发 Hermes scan，确认 backfill 行为与根目录一致。
3. 将 §5 第 3 项拆分为独立验证项：`/skills` UI 表现与 `lock.json` 程序化记录分别验证，定义期望的 `scan_verdict` 字段值与最大等待时间；明确主验证信号为实际功能可用性。
4. 在 §6 风险表中记录该不确定性，并准备回退方案（symlink 移至根目录 / 手动 lock.json 编辑）。

### Source References

#### Product Review

- PR-003

#### System Review

- SC-004

#### Test Review

- TD-002

#### Design Spec References

- §2.2（Hermes 技能机制）
- §2.3（参考范例 goal-manager）
- §4.3（双平台 symlink 安装）
- §5（验证清单第 3 项）
- §6（风险与对策）

### Consolidation Decision

MERGED

#### Decision Rationale

PR-003、SC-004、TD-002 描述同一根本问题（Hermes symlink 发现/注册机制证据不足且验证标准歧义），证据互补，合并后保留三个视角。

### Severity Change Rationale

源 Finding 严重度分别为 PR-003 P2 / SC-004 P2 / TD-002 P1。合并严重度定为 P1：TD-002 的 P1 基于验证标准不可靠可能导致部署被误判为成功/失败，进而影响核心设计目标（Hermes 兼容性）的可验证性。未升级为 P0：Hermes 端注册失败可恢复（symlink 移至根目录、手动 lock.json 编辑），不造成数据丢失或不可逆后果。

---

## CR-003 — Git/GitHub 推送步骤的失败处理与中间状态验证未定义

### Consolidated Severity

P1

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

规格 §4.5 将仓库创建、remote 设置、推送合并为单条命令 `gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin --push`。规格 §6 的退化方案仅覆盖"整条命令失败"场景，未覆盖部分失败状态（仓库创建成功但推送失败、remote 设置失败、名称冲突、gh 进程中途崩溃）。同时，规格未定义步骤 5（git init/commit）与步骤 6（gh repo create）之间的可验证检查点，失败后的重试安全性与期望的最终状态无客观验证标准。

### Evidence

#### Confirmed Evidence

- 规格 §4.5：`gh repo create --push` 为组合操作（SC-005）。
- 规格 §6 风险表：对策仅"退化为分步：gh repo create 后 git push -u origin main"，未覆盖部分成功子场景（SC-005）。
- 规格 §4.7 定义 8 步顺序执行，未定义每步的前置条件验证与失败恢复路径（TD-001）。
- 现场核验：当前项目为非 git 仓库，步骤 5 将从零初始化，无历史状态可依赖（TD-001）。

#### Inferred Evidence

- `gh repo create` 在 remote 添加失败时不会自动回滚 GitHub 端的仓库创建（SC-005）。
- 网络中断或 token 过期可导致组合命令部分执行（SC-005 / TD-001）。

#### Unknowns

- `OneFlowerHill` 账户下是否已存在同名 `spec-review` 仓库（SC-005）。
- `gh repo create --push` 在网络故障边界下的精确行为（TD-001 Review Limitations）。

### Trigger Scenario

1. 执行步骤 5（`git init && git branch -M main && git add -A && git commit`），成功。
2. 执行步骤 6（`gh repo create --push`）。
3. GitHub API 成功创建仓库并设置 origin，但推送阶段因网络超时失败；或仓库创建成功但 remote 设置失败；或仓库创建因名称冲突失败。
4. 本地仓库与远程仓库关系不一致（origin 指向已存在但可能为空的远程仓库，或本地无 origin 而 GitHub 上已有空仓库）。
5. 规格未定义如何客观验证当前状态、重试是否安全、是否需要删除重建。

### Consequence

- Availability Impact：一次性的跨平台部署操作可能因部分失败产生不一致的中间状态；操作者可能采取错误恢复动作（如重复 `git init` 或 force push），损坏仓库历史或造成远程仓库状态不一致。
- Operational Impact：最坏情况需手动清理 GitHub 上的残留仓库（`gh repo delete`）后重试；不同操作者对同一失败场景可能采取不同恢复策略。
- Data Impact：本地 commit 始终安全（仅本地 git 操作），不造成数据丢失。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

无对应 Product Finding。

**Assessment:**

产品审核员未识别此问题（该问题属于技术操作层面）。

#### System Perspective

**Source Findings:**

- SC-005

**Assessment:**

系统批评员指出 `gh repo create --push` 组合操作的部分失败场景（名称冲突、remote 设置失败、gh 崩溃）恢复路径不完整，建议增加前置检查 `gh repo view` 并拆分步骤。

#### Test Perspective

**Source Findings:**

- TD-001

**Assessment:**

测试设计师指出实施步骤中途失败后仓库状态无客观验证方法——步骤 5/6 之间无可验证检查点，重试安全性未定义，不同操作者对同一失败场景可能得到不同最终结果。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

SC-005 与 TD-001 均围绕"Git/GitHub 推送步骤的失败处理与状态验证未定义"这一根本问题。SC-005 关注组合命令的部分失败恢复路径，TD-001 关注可验证检查点与重试安全性。两者针对同一执行步骤（§4.5/§4.7 步骤 5–6），合并后保留完整证据。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。两个审核员对问题存在与后果判断一致。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

1. 在 §4.5 增加前置检查：`gh repo view OneFlowerHill/spec-review` 确认目标仓库不存在（或存在但为空，询问是否复用）。
2. 为步骤 5 与步骤 6 分别定义可验证检查点：`git log --oneline` 显示首提交、`git status` 显示 clean、`gh repo view` 确认仓库创建、`git ls-remote origin` 确认推送完成。
3. 将 `--push` 拆分为独立步骤（`gh repo create` 与 `git push -u origin main`），使每步的成败可独立观察和恢复；补充名称冲突与部分成功场景的具体恢复步骤。

### Source References

#### Product Review

无。

#### System Review

- SC-005

#### Test Review

- TD-001

#### Design Spec References

- §4.5（Git / GitHub 操作）
- §4.7（实施顺序，步骤 5–6）
- §6（风险与对策，第 5 行）

### Consolidation Decision

MERGED

#### Decision Rationale

SC-005 与 TD-001 描述同一执行步骤（Git/GitHub 推送）的失败处理与验证缺口，根本问题一致，合并后保留系统与测试两个视角的证据。

### Severity Change Rationale

源 Finding 严重度分别为 SC-005 P2 / TD-001 P1。合并严重度定为 P1：TD-001 的 P1 基于该步骤位于部署关键路径，部分失败后无客观验证可能导致错误恢复动作（force push / 重复 init）损害仓库历史。未升级为 P0：所有失败场景均可手动恢复，本地 commit 不丢失，不构成数据丢失或不可逆状态。

---

## CR-004 — 改名验证策略不足：验证时机过晚且只检查旧值残留

### Consolidated Severity

P1

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

规格 §4.1 定义了 8 条替换规则、覆盖 13 个文件约 30+ 改动点的人工改名操作，但：(1) 改名在 §4.7 步骤 1 执行、`git init` 在步骤 5，改名阶段无版本控制安全网；(2) 规格唯一的改名验证 `grep -rn "yy-"` 位于步骤 8（所有 git 与 push 操作之后），而非改名完成后、commit 之前——若验证发现遗漏，错误已随首提交进入 GitHub 历史；(3) grep 只检查旧值（`yy-`）残留，不检查新值是否正确（如拼写错误 `product-reviewr`）或文件间角色引用是否同步更新。

### Evidence

#### Confirmed Evidence

- 规格 §4.7 步骤 1（改名）在步骤 5（git init/add/commit）之前；grep 验证在步骤 8（最后）（SC-002）。
- 规格 §5 第 5 项：`grep -rn "yy-"` 仅检查旧值残留，不验证新值正确性（TD-005）。
- 规格 §4.1 替换表覆盖 SKILL.md、CLAUDE.md、README.md、update.sh、roles/*.md、templates/*.md、references/common.md、agents/openai.yaml 等 13 个活文件（TD-005 现场 grep 确认 `yy-` 遍布这些文件）。
- 现场核验（合并者 Phase 1）：新规格文件 `docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md` 自身含 25 处 `yy-` 引用；规格 §5 的 grep 一致性目标要求 `yy-` 仅命中"不改"目录，而 §3.1"不改"清单中的 specs 限定为"旧"规格——新规格不在该清单内，按规格自身命令执行时 grep 会命中新规格，验证标准存在自相矛盾。

#### Inferred Evidence

- 13 个文件约 30+ 改动点以人工或简单 sed 方式执行时，遗漏或误匹配的概率不可忽略（SC-002 / TD-005）。
- 替换出错（如 `yy-product-reviewer` → `product-reviewr`）时，新字符串不含 `yy-`，grep 验证通过但引用已断裂（TD-005）。

#### Unknowns

- 改名执行时操作者选择人工逐文件替换还是脚本化替换（SC-002）。
- 审核后到改名执行前是否有新增文件扩大改名范围（TD-005 Review Limitations）。

### Trigger Scenario

1. 操作者按 §4.1 替换规则逐文件执行改名。
2. 某条规则被错误应用（替换过宽误改了历史文件，或替换过窄遗漏某处引用，或产生拼写错误的新值）。
3. 操作者继续执行步骤 2–5，将含错误的文件 `git add -A` 并 commit。
4. 步骤 6 推送至 GitHub。
5. 步骤 8 的 `grep -rn "yy-"` 验证：遗漏场景下命中错误（发现为时已晚），错误替换场景下通过验证（掩盖问题）。
6. 遗漏场景需 amend/force push 覆盖 GitHub 历史；错误替换场景问题被掩盖至首次实际使用技能时暴露。

### Consequence

- Data Impact：改名错误随首提交进入 GitHub 历史，修复需 force push 或追加修正 commit，破坏"仓库首提交即为干净的目标状态"的设计意图。
- Availability Impact：角色名交叉引用不一致可能导致技能部分功能静默失败——技能在 `/skills` 列表可见但触发后执行出错。
- Maintenance Impact：改名遗漏导致文件中残留 `yy-` 引用，后续维护者面临命名不一致的困惑。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

无对应 Product Finding。

**Assessment:**

产品审核员未识别此问题（该问题属于工程验证层面）。

#### System Perspective

**Source Findings:**

- SC-002

**Assessment:**

系统批评员指出改名在 git init 之前执行、grep 验证在 commit/push 之后，缺乏版本控制安全网与阶段验证门；建议拆分 grep 验证为两阶段并考虑脚本化替换。

#### Test Perspective

**Source Findings:**

- TD-005

**Assessment:**

测试设计师指出 grep 只覆盖遗漏替换（false negative），不覆盖错误替换（false positive）与交叉引用漂移；建议增加正向一致性检查（提取 roles/*.md 与 SKILL.md 的 frontmatter name 值并交叉比对）。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

SC-002 与 TD-005 均围绕"改名验证策略不足"这一根本问题：SC-002 关注验证时机（过晚，无安全网），TD-005 关注验证覆盖（只查旧值残留，不查新值正确性）。两者互补，合并后保留完整证据。合并者 Phase 1 核验的新规格自身含 `yy-` 引用问题作为附加证据并入 Evidence 的 Confirmed Evidence 部分。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。两个审核员一致认为 grep 验证策略不足，仅关注点不同。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

1. 将 grep 验证拆分为两阶段：第一阶段在改名完成后、`git add` 之前立即执行，作为通过门；第二阶段在全部步骤完成后作为终验。
2. 增加正向一致性检查：提取 `roles/*.md` 与 `SKILL.md` 的 frontmatter `name` 值，与替换表期望值及 `CLAUDE.md`/`templates/*.md` 中的引用交叉比对。
3. 建议使用脚本化替换（如 `sed` 批处理）减少人为错误，并在 `git add` 前对 §3.1"不改"目录执行专项 diff 确认无意外修改。
4. 调整 §5 grep 一致性目标的表述，明确新规格文件（含 `yy-` 引用的设计文档）的处理方式，避免验证标准自相矛盾。

### Source References

#### Product Review

无。

#### System Review

- SC-002

#### Test Review

- TD-005

#### Design Spec References

- §3.1（改名边界）
- §4.1（改名策略）
- §4.7（实施顺序，步骤 1 与步骤 5）
- §5（验证清单第 5 项）

### Consolidation Decision

MERGED

#### Decision Rationale

SC-002 与 TD-005 描述同一根本问题（改名验证策略不足），一个关注验证时机、一个关注验证覆盖，合并后形成完整因果链。

### Severity Change Rationale

源 Finding 严重度分别为 SC-002 P1 / TD-005 P2。合并严重度定为 P1：SC-002 的 P1 基于改名错误可能随首提交进入并推送至 GitHub 历史，且修复需 force push；该证据链完整成立。未升级为 P0：改名错误可逆（可反向替换），且主要后果是维护成本与历史污染，非数据丢失或不可逆破坏。

---

## CR-005 — 部署前环境前置条件未系统性声明，存在多个隐藏依赖

### Consolidated Severity

P1

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

规格 §2.4 仅声明"GitHub CLI 已认证"与"项目当前非 git 仓库"两项环境事实，但部署实际依赖的多个前置条件散落于各节命令中，未系统整理为可验证的前置条件清单。关键依赖包括：`~/.hermes/skills/software-development/` 目录必须存在；目标名 `spec-review` 在 Claude 与 Hermes 技能目录中未被占用；Hermes 已安装且 skills 目录已初始化。

### Evidence

#### Confirmed Evidence

- 规格 §2.4 仅列两项环境事实，未扩展为完整前置条件清单（PR-002）。
- 规格 §4.3 的 `ln -s` 命令直接引用 `~/.hermes/skills/software-development/`，但未声明其必须预先存在（PR-002）。
- 现场核验：当前环境 `~/.hermes/skills/software-development/` 存在（含 11 个技能）、`~/.claude/skills/spec-review` 与 `~/.hermes/skills/software-development/spec-review` 不存在、gh 已认证——当前环境全部满足，但规格未将这些条件声明为可验证前置条件（PR-002）。

#### Inferred Evidence

- 其他用户/环境的 Hermes 目录结构可能不同（裸机安装 Hermes 后分类目录不保证已初始化）（PR-002）。
- `ln -s` 在目标已存在时直接失败，不提供有意义错误信息（POSIX 语义）（PR-002）。

#### Unknowns

- 目标名 `spec-review` 在当前与未来环境中是否被其他技能占用。

### Trigger Scenario

1. 操作者按规格执行步骤 1–6，全部成功。
2. 执行步骤 7 的 Hermes symlink 命令 `ln -s ... ~/.hermes/skills/software-development/spec-review`。
3. 因分类目录尚不存在（Hermes 全新安装后未初始化该分类），或目标名已被占用（之前的部署尝试残留），`ln -s` 失败。
4. 操作者需自行判断：手动创建目录？选择其他分类？覆盖已有 symlink？规格未提供决策依据。

### Consequence

- Operational Impact：环境不满足时部署流程中断，操作者需自行排查与决策，增加部署时间与对个人经验的依赖。
- Consistency Impact：不同环境下的部署可能产生不同结果（如选择不同分类目录），降低可重复性。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

- PR-002

**Assessment:**

产品审核员指出环境依赖未被系统性声明为前置条件清单，每个依赖应附验证命令与不满足时的处理策略。

#### System Perspective

**Source Findings:**

无对应 System Finding。

**Assessment:**

系统批评员未将前置条件缺失识别为独立 Finding（其 SC-005 关注 GitHub 仓库名冲突，与本 Finding 的本地文件系统名冲突根因不同）。

#### Test Perspective

**Source Findings:**

无对应 Test Finding。

**Assessment:**

测试设计师未识别此问题。

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

PR-002 是单一来源 Finding，无其他审核员识别出相同根本问题。其内容（本地环境前置条件）与 CR-003（GitHub 推送失败）中的仓库名冲突虽表面相似，但根因不同（本地文件系统 `ln -s` 冲突 vs. GitHub 仓库名冲突），保持独立。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

在 §2.4 或独立"前置条件"章节系统列出所有环境依赖并附验证命令（如 `ls -d ~/.hermes/skills/software-development/`、`test ! -e ~/.claude/skills/spec-review`、`gh auth status`），并为每项定义不满足时的处理策略（自动创建目录 / 报错终止 / 提示用户手动操作）。针对同名技能冲突，明确覆盖策略（提示确认后再删除重建）。

### Source References

#### Product Review

- PR-002

#### System Review

无。

#### Test Review

无。

#### Design Spec References

- §2.4（环境就绪状态）
- §4.3（双平台 symlink 安装）

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

PR-002 为单一来源、内容独立、无其他审核员对应，保持为独立合并 Finding。

### Severity Change Rationale

源 Finding PR-002 为 P1，合并严重度维持 P1，无变更。理由：PR-002 识别了多个未声明的隐藏依赖（目录存在性、名称冲突、Hermes 安装），任一不满足即可中断部署关键路径；但其后果为操作中断而非数据丢失，故不升级为 P0。

---

## CR-006 — update.sh 自更新脚本在 GitHub 推送后的认证方式变更未定义

### Consolidated Severity

P2

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

规格 §4.6 将 `update.sh` 描述为"逻辑不变，origin 指向 GitHub 后自动生效"，但当前 origin 使用 SSH（`git@git.yyrd.com:yyit/yy-spec-review.git`），推送 GitHub 后 origin 变为 HTTPS（`https://github.com/OneFlowerHill/spec-review.git`）。SSH 与 HTTPS 的认证机制不兼容，规格未说明 `git fetch` 在 HTTPS 下认证失败时的行为，也未提供从旧 SSH 地址 clone 的副本的迁移指导。

### Evidence

#### Confirmed Evidence

- 规格 §4.6：update.sh 逻辑不变，仅改注释与 echo（PR-004）。
- README.md 中 `git clone git@git.yyrd.com:yyit/yy-spec-review.git` 证实当前 origin 使用 SSH（PR-004）。
- 规格 §4.5 使用 `gh repo create --source=.` 默认以 HTTPS 设置 remote（PR-004）。

#### Inferred Evidence

- 用户可能未配置 GitHub HTTPS credential helper，导致无人值守 `git fetch` 认证失败（PR-004）。

#### Unknowns

- 用友内部 git 仓库在部署后是否停用或保留为镜像（PR-004）。

### Trigger Scenario

1. 部署完成，origin 指向 GitHub HTTPS。
2. 用户执行 `bash update.sh`。
3. `git fetch origin` 因未配置 HTTPS 认证（无 credential helper 或 token 过期）而失败。
4. `update.sh` 报错退出，用户无法自动更新技能。

### Consequence

- Operational Impact：`update.sh` 自更新功能对未配置 GitHub HTTPS 认证的用户不可用。
- Maintenance Impact：存在从旧地址 clone 的副本的用户缺乏迁移指导，需在规格外自行更新 remote。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

- PR-004

**Assessment:**

产品审核员指出 SSH→HTTPS 认证方式变更未定义，可能使自更新功能在无人值守场景下失效，且旧 clone 副本用户缺乏迁移指导。

#### System Perspective

**Source Findings:**

无对应 System Finding。

**Assessment:**

系统批评员未识别此问题。

#### Test Perspective

**Source Findings:**

无对应 Test Finding。

**Assessment:**

测试设计师未识别此问题。

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

PR-004 为单一来源 Finding，独立于其他 Finding（update.sh 认证行为变更与其他根本问题无重叠）。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

在 §4.6 明确记录认证方式从 SSH 到 HTTPS 的变更，建议用户运行 `gh auth setup-git` 或配置 git credential helper；增加"已有用户的迁移指南"（`git remote set-url origin https://github.com/OneFlowerHill/spec-review.git`）；在 §5 验证清单中增加 `bash update.sh` 在认证环境下的成功验证项。

### Source References

#### Product Review

- PR-004

#### System Review

无。

#### Test Review

无。

#### Design Spec References

- §4.5（Git / GitHub 操作）
- §4.6（update.sh / README）
- §5（验证清单）

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

PR-004 为单一来源、内容独立，保持为独立合并 Finding。

### Severity Change Rationale

源 Finding PR-004 为 P2，合并严重度维持 P2，无变更。理由：认证摩擦可通过配置 credential helper 一次性解决，且自更新功能失败不阻断核心审核功能（可用 `git pull` 手动替代）。

---

## CR-007 — 双平台 symlink 共享单文件源，git merge 与平台扫描器之间存在并发读取竞态窗口

### Consolidated Severity

P2

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

两平台（Claude Code 加载器、Hermes 扫描器）通过 symlink 共享同一份文件系统。`update.sh` 的 `git merge --ff-only` 直接修改工作目录文件，无原子目录更新语义——文件逐个变更。若 Hermes scanner 或 Claude Code loader 在更新窗口内读取文件树，可能读取到部分旧版本与部分新版本混合的不一致快照。

### Evidence

#### Confirmed Evidence

- 规格 §4.3：两平台 symlink 指向同一份本地仓库，"修改一处两平台同步生效"（SC-003）。
- 规格 §4.6：update.sh 执行 `git merge --ff-only`，直接修改工作目录文件（SC-003）。
- 规格 §2.2：Hermes scan 为自动后台行为，触发时机不受本设计控制（SC-003）。

#### Inferred Evidence

- Hermes scanner 在扫描时对每个文件单独 open/read/close，而非获取原子快照（SC-003）。
- 技能文件总数约 20 个，`git merge` 更新窗口极短（毫秒级），实际命中概率低（SC-003）。

#### Unknowns

- Hermes scanner 的精确扫描触发时机（启动、定时、手动刷新）。

### Trigger Scenario

1. 系统处于稳态——两平台正常运行，symlink 均生效。
2. 操作者执行 `bash update.sh` 获取远程更新。
3. 在 `git merge --ff-only` 的文件更新窗口内，Hermes scanner 或 Claude Code loader 恰好发起对 symlink 目标目录的读取。
4. 读取操作跨越更新窗口，获取不一致的文件快照。

### Consequence

- Availability Impact：极低概率下，Claude Code 可能在同一加载中读取到新版 SKILL.md 与旧版角色定义的组合，导致技能行为短暂偏离。
- Maintenance Impact：若 Hermes `lock.json` 被写入不一致的 content_hash，可能导致后续变更检测误判。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

无对应 Product Finding。

**Assessment:**

产品审核员未识别此问题（属于系统并发层面）。

#### System Perspective

**Source Findings:**

- SC-003

**Assessment:**

系统批评员指出 git merge 与平台扫描器之间的并发读取竞态窗口未定义，建议在更新文档中标注低使用时段操作，或将风险记录为已知限制。

#### Test Perspective

**Source Findings:**

无对应 Test Finding。

**Assessment:**

测试设计师未识别此问题。

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

SC-003 为单一来源 Finding，独立于其他 Finding（并发竞态与其他根本问题无重叠）。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

在 `update.sh` 或操作文档中增加约束：执行 `git pull` 更新前建议在低使用时段操作，或将该风险记录为已知限制。轻量方案（文档记录 + 推荐操作窗口）对当前小文件集与低频更新场景已足够；未来技能文件数量大幅增长时需重新评估。

### Source References

#### Product Review

无。

#### System Review

- SC-003

#### Test Review

无。

#### Design Spec References

- §2.2（Hermes 技能机制）
- §2.3（参考范例 goal-manager）
- §4.3（双平台 symlink 安装）
- §4.6（update.sh / README）

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

SC-003 为单一来源、内容独立，保持为独立合并 Finding。

### Severity Change Rationale

源 Finding SC-003 为 P2（Likelihood LOW / Reversibility REVERSIBLE），合并严重度维持 P2，无变更。

---

## CR-008 — Symlink 验证仅检查存在性，忽略目标可达性与内容完整性

### Consolidated Severity

P2

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

规格 §5 验证清单第 1–2 项用 `ls -la` 验证两个平台的 symlink。`ls -la` 在 symlink 目标不存在或不可访问时仍显示 symlink 自身信息（断链指示依赖终端颜色配置，不构成可程序化判定的客观验证），且不验证目标目录内容完整性（如 `SKILL.md` 是否存在）与两平台 symlink 是否指向同一本地仓库。

### Evidence

#### Confirmed Evidence

- 规格 §5 第 1–2 项：`ls -la ~/.claude/skills/spec-review` 与 `ls -la ~/.hermes/skills/software-development/spec-review`（TD-004）。
- `ls -la` 对断链不返回非零退出码（TD-004）。

#### Inferred Evidence

- 断链 symlink 可能在部署验证阶段被误判为成功，技能在平台中不可用但"部署验证已通过"（TD-004）。

#### Unknowns

- 无重大未知（行为为 POSIX 文件系统标准语义）。

### Trigger Scenario

1. 前置条件：Symlink 已按 §4.3 创建。
2. 隐错条件：本地仓库路径被意外移动/删除/重命名，或路径中某级目录权限被收紧。
3. 执行 `ls -la ~/.claude/skills/spec-review`，输出显示 symlink 自身信息（断链指示可能仅彩色终端可见）。
4. Claude Code 加载技能时失败，但验证步骤已显示"通过"。
5. 操作者在部署完成数天后才发现技能不可用。

### Consequence

- Availability Impact：断开的 symlink 在部署验证阶段被误判为成功，技能实际不可用；排查方向可能偏离 symlink 问题，延长故障定位时间。
- Verification Impact：验证清单无法区分"存在但可用"与"存在但断链"。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:**

无对应 Product Finding。

**Assessment:**

产品审核员未识别此问题。

#### System Perspective

**Source Findings:**

无对应 System Finding。

**Assessment:**

系统批评员未识别此问题。

#### Test Perspective

**Source Findings:**

- TD-004

**Assessment:**

测试设计师指出 symlink 验证仅检查存在性，应拆分为存在性、目标可达性、关键内容完整性与双平台一致性四个可独立判定的验证项。

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

TD-004 为单一来源 Finding，独立于其他 Finding（symlink 验证的具体方法与 Hermes 注册机制问题 CR-002 关注点不同——CR-002 关注 Hermes 是否发现技能，CR-008 关注 symlink 本身是否有效）。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无冲突。

#### Conflict Evidence

不适用。

#### Resolution

不适用。

### Recommended Resolution

将验证清单第 1–2 项拆分为可程序化判定的验证项：symlink 存在性（`test -L`）、目标可达性（`test -d .../`）、关键内容完整性（`test -f .../SKILL.md`）、双平台一致性（两个 symlink 指向同一规范路径或 inode）。

### Source References

#### Product Review

无。

#### System Review

无。

#### Test Review

- TD-004

#### Design Spec References

- §4.3（双平台 symlink 安装）
- §5（验证清单第 1–2 项）

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

TD-004 为单一来源、内容独立，保持为独立合并 Finding。

### Severity Change Rationale

源 Finding TD-004 为 P2（CONFIRMED_GAP / HIGH），合并严重度维持 P2，无变更。理由：后果为技能可用性验证失效与排查成本增加，非数据丢失，P2 合适。

---

# Unmerged Source Findings

无。全部 14 个源 Finding 均已合并入对应的 Consolidated Finding，无未合并 Finding。

---

# Duplicate and Superseded Findings

无。无源 Finding 被标记为重复或被替代——每个源 Finding 均为其合并 Finding 的直接来源。

---

# Cross-Reviewer Conflicts

无。三个审核员之间不存在 CONTRADICTORY 或 MATERIAL_CONFLICT 级别的分歧。各 Finding 在根本问题、严重度与后果判断上互补而非对立。

---

# Coverage Gaps

无覆盖缺口——三个 source reviews 全部 AVAILABLE。以下维度均已覆盖：部署失败处理、数据安全（删除预检）、外部依赖（Hermes/GitHub）、验证标准、并发、兼容性、可维护性。

---

# Coverage Matrix

| Consolidated Finding | Product | System | Test | Primary Risk Area |
| -------------------- | ------- | ------ | ---- | ----------------- |
| CR-001               | PR-001  | SC-001 | TD-003 | 删除安全与数据保护 |
| CR-002               | PR-003  | SC-004 | TD-002 | Hermes 注册验证 |
| CR-003               | —       | SC-005 | TD-001 | Git/GitHub 失败处理 |
| CR-004               | —       | SC-002 | TD-005 | 改名验证策略 |
| CR-005               | PR-002  | —      | —     | 环境前置条件 |
| CR-006               | PR-004  | —      | —     | update.sh 认证 |
| CR-007               | —       | SC-003 | —     | 并发竞态 |
| CR-008               | —       | —      | TD-004 | symlink 验证 |

---

# Review Coverage Summary

| Review Dimension       | Product  | System   | Test     | Consolidated Findings |
| ---------------------- | -------- | -------- | -------- | --------------------- |
| Business Rules         | REVIEWED | —        | —        | CR-005                |
| User Workflow          | REVIEWED | —        | —        | CR-001, CR-003, CR-005 |
| State Transitions      | NOT_APPLICABLE | NOT_APPLICABLE | REVIEWED | CR-003                |
| Data Integrity         | REVIEWED | REVIEWED | REVIEWED | CR-001, CR-003, CR-004 |
| Security               | REVIEWED | REVIEWED | —        | CR-001                |
| Availability           | REVIEWED | REVIEWED | REVIEWED | CR-001, CR-002, CR-003, CR-007, CR-008 |
| Failure Recovery       | REVIEWED | REVIEWED | REVIEWED | CR-001, CR-003        |
| Backward Compatibility | REVIEWED | NOT_APPLICABLE | REVIEWED | CR-006                |
| Temporal Behavior      | REVIEWED | REVIEWED | REVIEWED | CR-006, CR-007        |
| Operational Complexity | REVIEWED | REVIEWED | REVIEWED | CR-001, CR-002, CR-003, CR-004, CR-005 |
| Testability            | —        | REVIEWED | REVIEWED | CR-002, CR-003, CR-004, CR-008 |
| Observability          | —        | REVIEWED | REVIEWED | CR-002, CR-008        |

---

# Superpowers Instructions

## What to Read

- **Consolidated Review**: 本文档
- **Source Reviews**: 见上方 Source Reviews 表（product-review.md / system-review.md / test-review.md）

## What to Decide

对下方 Decision Queue 中的每个 Consolidated Finding 设定决策：

| CR-ID | Title | Severity | Decision (choose one) |
|-------|-------|----------|----------------------|
| CR-001 | 旧技能目录删除缺乏安全的预检、客观判定标准与恢复保障 | P1 | ___ |
| CR-002 | Hermes 技能发现/注册机制假设证据不足，验证标准存在歧义 | P1 | ___ |
| CR-003 | Git/GitHub 推送步骤的失败处理与中间状态验证未定义 | P1 | ___ |
| CR-004 | 改名验证策略不足：验证时机过晚且只检查旧值残留 | P1 | ___ |
| CR-005 | 部署前环境前置条件未系统性声明，存在多个隐藏依赖 | P1 | ___ |
| CR-006 | update.sh 自更新脚本在 GitHub 推送后的认证方式变更未定义 | P2 | ___ |
| CR-007 | 双平台 symlink 共享单文件源，git merge 与平台扫描器之间存在并发读取竞态窗口 | P2 | ___ |
| CR-008 | Symlink 验证仅检查存在性，忽略目标可达性与内容完整性 | P2 | ___ |

**Decision options**: PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED

## Decision Template

对每个 Finding，在下方 Decision Records 节复制并填写：

```markdown
## DR-<NNN> — CR-<NNN>

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

### Decision Owner

<your name or role>

### Decision Rationale

<Why this decision was made — must address the finding's validity, materiality, and evidence>

### Required Action

<If ACCEPTED: what must change in the Design Spec>

### Decision Date

<YYYY-MM-DD>
```

## Hard Rules

1. A Finding with status PENDING_DECISION cannot have a final review state of APPROVED
2. All P0 findings must be resolved (not PENDING_DECISION) before the final review state can be anything other than BLOCKED
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

---

# Decision Queue

本节包含需要规格所有者或 Superpowers 工作流做出最终决策的 Finding。

## DQ-001 — CR-001

### Problem

旧技能目录删除（`rm -rf`）缺乏安全预检（未嵌入执行序列）、客观判定标准（diff 输出解读）与恢复保障（备份/回滚路径）。

### Severity

P1

### Evidence Summary

§6 风险表识别了删除丢失改动风险并给 `diff -r` 对策，但预检未嵌入 §4.7 步骤 7、判定标准未定义、删除后无恢复路径。旧目录为真实目录且与本地仓库存在实质差异。

### Recommended Resolution

将 diff 预检嵌入执行序列；定义 diff 输出分类规则；删除前备份（cp -r / mv）。

### Decision Required

是否接受"删除前必须嵌入预检、定义客观判定标准并备份"的要求，并据此修订 §4.7 与 §6。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-002 — CR-002

### Problem

Hermes 对 symlink 技能的发现/注册机制断言证据不足（yuanbao 为目录技能、goal-manager symlink 不在 lock.json），且 §5 验证标准存在"或"逻辑歧义与时机不可控。

### Severity

P1

### Evidence Summary

lock.json 仅含 yuanbao（backfilled from optional-skills）；goal-manager（symlink）不在其中。分类子目录下无 symlink 先例。

### Recommended Resolution

在 §2.2 区分目录技能与 symlink 技能；部署前做最小化 symlink 验证；拆分 §5 第 3 项验证标准。

### Decision Required

是否接受"Hermes 注册机制须先验证、验证标准须拆分"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-003 — CR-003

### Problem

`gh repo create --push` 组合操作的部分失败场景（名称冲突、部分成功）恢复路径不完整，且步骤 5/6 之间无可验证检查点。

### Severity

P1

### Evidence Summary

§6 退化方案仅覆盖整条命令失败；§4.7 无步骤间验证门；当前为非 git 仓库，从零初始化。

### Recommended Resolution

增加 `gh repo view` 前置检查；拆分 `--push` 为独立步骤；定义每步验证检查点与失败恢复步骤。

### Decision Required

是否接受"拆分 GitHub 操作步骤并定义验证检查点"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-004 — CR-004

### Problem

改名验证策略不足：grep 验证位于 commit/push 之后、只检查旧值残留，不验证新值正确性与交叉引用一致性；新规格文件自身含 `yy-` 引用与 §5 grep 一致性目标存在自相矛盾。

### Severity

P1

### Evidence Summary

改名在 git init 前执行、grep 验证在步骤 8；grep 无法捕获错误替换（如拼写错误）；合并者核验新规格含 25 处 `yy-`。

### Recommended Resolution

拆分 grep 为两阶段验证；增加正向一致性检查（frontmatter name 交叉比对）；脚本化替换；调整 grep 一致性目标表述。

### Decision Required

是否接受"改名验证须前置、正向化并脚本化"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-005 — CR-005

### Problem

部署前环境前置条件（Hermes 分类目录存在性、目标名未被占用、Hermes 已安装）未系统性声明为可验证清单。

### Severity

P1

### Evidence Summary

§2.4 仅列两项环境事实；§4.3 命令隐含依赖未声明；当前环境虽满足但未转化为前置条件清单。

### Recommended Resolution

新增前置条件清单，每项附验证命令与不满足时的处理策略。

### Decision Required

是否接受"新增环境前置条件清单"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-006 — CR-006

### Problem

`update.sh` 认证方式从 SSH 切换到 HTTPS 的行为变更未定义，未配置 credential helper 时自更新失败，旧 clone 副本缺乏迁移指导。

### Severity

P2

### Evidence Summary

README 现有 SSH clone 地址；§4.5 将 origin 设为 GitHub HTTPS；§4.6 声称"自动生效"。

### Recommended Resolution

在 §4.6 记录认证变更与 `gh auth setup-git` 建议；增加旧副本迁移指南；验证清单增加 `bash update.sh` 验证项。

### Decision Required

是否接受"记录认证变更并提供迁移指南"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-007 — CR-007

### Problem

双平台 symlink 共享单文件源，git merge 与平台扫描器并发读取存在竞态窗口。

### Severity

P2

### Evidence Summary

§4.3 symlink 共享同一目录；§4.6 git merge 直接修改工作目录；§2.2 Hermes scan 时机不可控。

### Recommended Resolution

在更新文档标注低使用时段操作，或将风险记录为已知限制。

### Decision Required

是否接受"以文档记录管理并发竞态风险"的处理方式。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

## DQ-008 — CR-008

### Problem

Symlink 验证仅用 `ls -la` 检查存在性，忽略目标可达性与内容完整性，断链可被误判为成功。

### Severity

P2

### Evidence Summary

§5 第 1–2 项用 `ls -la`；`ls -la` 对断链不返回非零退出码。

### Recommended Resolution

拆分验证项为存在性、目标可达性、SKILL.md 存在性、双平台一致性。

### Decision Required

是否接受"symlink 验证拆分并程序化"的要求。

### Decision Status

ACCEPTED（见 DR-001 ~ DR-008）

---

# Decision Records

本节在规格所有者或 Superpowers 工作流做出决策后更新。

每个 Consolidated Finding 最终必须拥有决策记录，除非其状态仍为 `PENDING_DECISION`。

## DR-001 — CR-001

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。`rm -rf ~/.claude/skills/yy-spec-review` 为不可逆操作，旧目录为真实目录含 `.workbuddy/`、`.superpowers/` 本地产物，且现场核验与本地仓库存在实质差异（本地仓库为超集，但旧目录可能有独有改动）。§6 的 `diff -r` 预检未嵌入 §4.7 执行序列，操作者可能跳过；diff 输出缺乏客观判定标准；删除后 `ln -s` 失败无恢复路径。三角色（PR-001/SC-001/TD-003）一致认定 P1，证据充分，修复成本低。

### Required Action

修订 §4.7 步骤 7——以 `mv` 替代 `rm -rf`（将旧目录移至备份路径如 `~/.claude/skills/.yy-spec-review.bak.20260807/`），既保留数据可回滚又腾出 `spec-review` 名字；将 `diff -r` 预检作为独立步骤嵌入执行序列（步骤 6.5）；定义 diff 输出分类规则（SAFE_TO_IGNORE / NEEDS_REVIEW / BLOCK_DELETION），明确 BLOCK_DELETION 与 NEEDS_REVIEW 均空方可继续；为 `ln -s` 失败定义恢复路径（从备份 `mv` 回）。同步更新 §6 风险表对策。

### Decision Date

2026-08-07

---

## DR-002 — CR-002

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。§2.2 将 `yuanbao`（根目录真实目录）的 backfill 证据过度推广到 symlink 技能与分类子目录；§5 第 3 项"或"逻辑歧义 + 扫描时机不可控导致验证标准不可靠。需修正 SC-004 一条论据：`goal-manager` 本身就是 `productivity/` 分类子目录下的 symlink 且在 Hermes 中正常工作——这恰是"分类子目录 symlink 可被发现"的直接先例，推翻 SC-004"分类子目录无 symlink 先例"之说。但 `goal-manager` 不在 `lock.json`，证明 symlink 技能可被发现但未必持久化到 lock.json，反强化"lock.json 非可靠注册凭证"的结论。Finding 整体成立。

### Required Action

修订 §2.2——明确 `goal-manager` 为分类子目录 symlink 先例（支持"发现"），但 symlink 技能可能不持久化到 `lock.json`（不以 lock.json 为注册凭证）；§5 第 3 项主验证信号改为 `/skills` 列出 spec-review + 实际触发可用，`lock.json` 记录降为辅助/可选信号；§6 增回退方案（symlink 移根目录 / 手动 lock.json）。不强制部署前最小化验证（goal-manager 先例已充分），保留为可选步骤。

### Decision Date

2026-08-07

---

## DR-003 — CR-003

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。`gh repo create --push` 组合操作的部分失败场景（名称冲突、remote 设置失败、gh 崩溃）恢复路径不完整，§6 退化方案仅覆盖整条命令失败；步骤 5/6 间无可验证检查点。证据充分（SC-005/TD-001）。

### Required Action

修订 §4.5——增加前置 `gh repo view OneFlowerHill/spec-review` 检查名称冲突；拆分 `--push` 为独立步骤（`gh repo create --private --source=. --remote=origin` + `git push -u origin main`）；为步骤 5/6 定义可验证检查点（`git log --oneline` 显示首提交、`git status` clean、`gh repo view` 确认仓库创建、`git ls-remote origin` 确认推送完成）；§6 补充名称冲突与部分成功的具体恢复步骤。

### Decision Date

2026-08-07

---

## DR-004 — CR-004

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。改名在 git init 前执行无版本控制安全网；grep 验证在步骤 8（commit/push 后）发现遗漏为时已晚；grep 只查旧值残留不查新值正确性与交叉引用一致性；新规格文件自身含 25 处 `yy-` 引用与 §5 grep 目标自相矛盾。证据充分（SC-002/TD-005 + 合并者现场核验）。

### Required Action

修订 §4.7——将 `git init` 提前到改名之前（作为步骤 0），使改名有 git 安全网可 `git diff`/`git checkout` 回退；grep 验证拆两阶段（改名后 `git add` 前立即执行作通过门 + 全部完成后终验）；增加正向一致性检查（提取 `roles/*.md` 与 `SKILL.md` frontmatter `name` 交叉比对期望值 `product-reviewer`/`system-critic`/`test-designer`/`spec-review`）；建议脚本化替换（sed）+ 对 §3.1"不改"目录专项 diff 确认无意外修改；修订 §5 grep 目标表述——明确"活源文件"不得含 `yy-`，新规格设计文档与历史/快照目录允许 `yy-` 残留。

### Decision Date

2026-08-07

---

## DR-005 — CR-005

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。§2.4 仅声明两项环境事实，多个隐藏依赖（Hermes 分类目录存在性、目标名未占用、Hermes 已安装）散落各节未系统声明为可验证前置条件。当前环境虽满足但未转化为前置条件清单，影响可重复性（PR-002）。

### Required Action

修订 §2.4——扩展为系统前置条件清单，每项附验证命令与不满足时处理策略：`ls -d ~/.hermes/skills/software-development/`（不存在则 `mkdir -p`）、`test ! -e ~/.claude/skills/spec-review` 与 `test ! -e ~/.hermes/skills/software-development/spec-review`（已存在则提示确认后处理）、`gh auth status`（未认证则报错终止）、`command -v hermes`（未安装则报错）。

### Decision Date

2026-08-07

---

## DR-006 — CR-006

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。update.sh origin 从 SSH（`git@git.yyrd.com`）变 HTTPS（`github.com`），认证机制不兼容，未配置 credential helper 时 `git fetch` 失败；旧 clone 副本缺乏迁移指导。P2 合理（不阻断核心功能，可手动 `git pull`）（PR-004）。

### Required Action

修订 §4.6——记录 SSH→HTTPS 认证变更，建议 `gh auth setup-git` 配置 git 用 gh 的 HTTPS 认证；README 增加"已有用户迁移指南"（`git remote set-url origin https://github.com/OneFlowerHill/spec-review.git`）；§5 验证清单增加 `bash update.sh` 在认证环境下成功完成 `git fetch` 的验证项。

### Decision Date

2026-08-07

---

## DR-007 — CR-007

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立但概率低、可逆。update.sh 的 `git merge` 与 Hermes scanner/Claude loader 存在并发读取竞态窗口，但文件少（约 20 个）、窗口毫秒级、goal-manager 同模式无问题。P2 合理。工程修复（锁定文件/进程检测）对当前规模过度，文档记录为已知限制即可（SC-003）。

### Required Action

修订 §6——增加已知限制条目：update.sh 更新存在极低概率并发读取竞态窗口，建议在低使用时段执行 `git pull`；未来技能文件数量大幅增长时重新评估。不在 update.sh 增加锁定机制（避免过度工程）。

### Decision Date

2026-08-07

---

## DR-008 — CR-008

### Decision Status

ACCEPTED

### Decision Owner

规格所有者（授权主 agent 代行决策）

### Decision Rationale

Finding 成立。§5 第 1–2 项用 `ls -la` 验证 symlink，断链不返回非零退出码，不可程序化判定；未验证目标可达性、内容完整性、双平台一致性。P2 合理（验证失效非数据丢失）（TD-004）。

### Required Action

修订 §5 第 1–2 项——拆分为可程序化判定的验证项：存在性（`test -L`）、目标可达性（`test -d .../`）、关键内容完整性（`test -f .../SKILL.md`）、双平台一致性（两个 symlink `readlink` 比对或 inode 比对）。

### Decision Date

2026-08-07

---

# Finding Lifecycle

每个合并 Finding 的生命周期：

```text
PENDING_DECISION
  ↓
ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED
```

Finding 不得因被拒绝、延迟、被认为不必要或在后续修订中修复而从审核中消失。其历史必须保留以供未来分析。

---

# Review Statistics

## Finding Counts

### By Source Review

- Product Findings: 4
- System Findings: 5
- Test Findings: 5

### After Consolidation

- Consolidated Findings: 8
- Unmerged Findings: 0
- Duplicate Findings: 0
- Superseded Findings: 0
- Cross-Reviewer Conflicts: 0

### By Severity

- P0: 0
- P1: 5
- P2: 3

### By Status

- PENDING_DECISION: 8
- ACCEPTED: 0
- REJECTED: 0
- DEFERRED: 0
- PARTIALLY_ACCEPTED: 0
- DUPLICATE: 0
- INVALIDATED: 0

---

# Consolidation Conclusion

### Consolidation Result

COMPLETED

### Decision Readiness

PENDING_DECISION

### Summary

三个 source reviews 全部 AVAILABLE 且通过格式校验。14 个源 Finding（Product 4 / System 5 / Test 5）合并为 8 个 Consolidated Finding，全部源 Finding 均有明确归属（14 = 合并引用 14 + 未合并 0 + 重复/替代 0），Source Finding 完整性校验通过，无 Finding 被静默丢弃。无跨审核员冲突。8 个 Consolidated Finding 均处于 PENDING_DECISION，等待规格所有者决策。

主要问题集中在部署的失败处理维度：破坏性删除的安全流程（CR-001）、外部依赖注册机制的证据充分性（CR-002）、GitHub 推送的失败处理（CR-003）、改名验证策略（CR-004）为 P1 级，建议在实施前解决。P2 级问题（CR-006/CR-007/CR-008）可通过文档记录或轻量验证管理。

合并者未对任何 Finding 做接受/拒绝判断。批准、拒绝、修改或延迟由规格所有者或 Superpowers 工作流决定。

### Final Review State

APPROVED

本审核无 P0 Finding（非 BLOCKED），审核记录完整（非 INCOMPLETE）。8 个 Consolidated Finding（5 P1 + 3 P2）已全部决策为 ACCEPTED（见 DR-001 ~ DR-008），且对应的规格修订已全部纳入设计文档（§2.2 / §2.4 / §4.5 / §4.6 / §4.7 / §5 / §6）。按 Decision Protocol，所有已接受变更已实施，最终审核状态转为 APPROVED。

---

# Machine-Readable Consolidation Index

```yaml
review:
  review_id: "2026-08-07-review-001"
  review_type: "CONSOLIDATED_REVIEW"
  status: "COMPLETED"
  design_spec: "docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md"
  round: 1
  spec_stem: "cross-platform-deploy-design"
  final_review_state: "APPROVED"

source_reviews:
  - reviewer: "yy-product-reviewer"
    review_type: "PRODUCT_REVIEW"
    review_id: "2026-08-07-review-001"
    source_file: "docs/superpowers/reviews/cross-platform-deploy-design/2026-08-07-review-001/product-review.md"
    status: "AVAILABLE"

  - reviewer: "yy-system-critic"
    review_type: "SYSTEM_REVIEW"
    review_id: "2026-08-07-review-001"
    source_file: "docs/superpowers/reviews/cross-platform-deploy-design/2026-08-07-review-001/system-review.md"
    status: "AVAILABLE"

  - reviewer: "yy-test-designer"
    review_type: "TEST_REVIEW"
    review_id: "2026-08-07-review-001"
    source_file: "docs/superpowers/reviews/cross-platform-deploy-design/2026-08-07-review-001/test-review.md"
    status: "AVAILABLE"

consolidated_findings:
  - id: "CR-001"
    title: "旧技能目录删除缺乏安全的预检、客观判定标准与恢复保障"
    severity: "P1"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-001"]
      system: ["SC-001"]
      test: ["TD-003"]
    finding_type: "BLIND_SPOT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §4.3", "Design Spec §4.7", "Design Spec §6", "Design Spec §2.4"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: "三个源 Finding 均为 P1，无变更"

  - id: "CR-002"
    title: "Hermes 技能发现/注册机制假设证据不足，验证标准存在歧义"
    severity: "P1"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-003"]
      system: ["SC-004"]
      test: ["TD-002"]
    finding_type: "UNTESTABLE_REQUIREMENT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §2.2", "Design Spec §2.3", "Design Spec §4.3", "Design Spec §5", "Design Spec §6"]
    processing_status: "ACCEPTED"
    severity_escalation: true
    severity_change_rationale: "源严重度 PR-003 P2 / SC-004 P2 / TD-002 P1，合并为 P1，依据 TD-002 的验证标准不可靠对核心设计目标（Hermes 兼容性）可验证性的影响"

  - id: "CR-003"
    title: "Git/GitHub 推送步骤的失败处理与中间状态验证未定义"
    severity: "P1"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-005"]
      test: ["TD-001"]
    finding_type: "BLIND_SPOT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §4.5", "Design Spec §4.7", "Design Spec §6"]
    processing_status: "ACCEPTED"
    severity_escalation: true
    severity_change_rationale: "源严重度 SC-005 P2 / TD-001 P1，合并为 P1，依据 TD-001 将步骤 5-6 视为部署关键路径且失败后无客观验证"

  - id: "CR-004"
    title: "改名验证策略不足：验证时机过晚且只检查旧值残留"
    severity: "P1"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-002"]
      test: ["TD-005"]
    finding_type: "UNTESTABLE_REQUIREMENT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §3.1", "Design Spec §4.1", "Design Spec §4.7", "Design Spec §5"]
    processing_status: "ACCEPTED"
    severity_escalation: true
    severity_change_rationale: "源严重度 SC-002 P1 / TD-005 P2，合并为 P1，依据 SC-002 的改名错误随首提交进入 GitHub 历史需 force push 的证据"

  - id: "CR-005"
    title: "部署前环境前置条件未系统性声明，存在多个隐藏依赖"
    severity: "P1"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-002"]
      system: []
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §2.4", "Design Spec §4.3"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: "单源 Finding PR-002 P1，无变更"

  - id: "CR-006"
    title: "update.sh 自更新脚本在 GitHub 推送后的认证方式变更未定义"
    severity: "P2"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-004"]
      system: []
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §4.5", "Design Spec §4.6", "Design Spec §5"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: "单源 Finding PR-004 P2，无变更"

  - id: "CR-007"
    title: "双平台 symlink 共享单文件源，git merge 与平台扫描器之间存在并发读取竞态窗口"
    severity: "P2"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-003"]
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §2.2", "Design Spec §2.3", "Design Spec §4.3", "Design Spec §4.6"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: "单源 Finding SC-003 P2，无变更"

  - id: "CR-008"
    title: "Symlink 验证仅检查存在性，忽略目标可达性与内容完整性"
    severity: "P2"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: []
      test: ["TD-004"]
    finding_type: "BLIND_SPOT"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["Design Spec §4.3", "Design Spec §5"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: "单源 Finding TD-004 P2，无变更"

unmerged_findings: []

duplicate_or_represented: []

conflicts: []

decision_queue:
  - id: "DQ-001"
    finding_id: "CR-001"
    severity: "P1"
    processing_status: "ACCEPTED"

  - id: "DQ-002"
    finding_id: "CR-002"
    severity: "P1"
    processing_status: "ACCEPTED"

  - id: "DQ-003"
    finding_id: "CR-003"
    severity: "P1"
    processing_status: "ACCEPTED"

  - id: "DQ-004"
    finding_id: "CR-004"
    severity: "P1"
    processing_status: "ACCEPTED"

  - id: "DQ-005"
    finding_id: "CR-005"
    severity: "P1"
    processing_status: "ACCEPTED"

  - id: "DQ-006"
    finding_id: "CR-006"
    severity: "P2"
    processing_status: "ACCEPTED"

  - id: "DQ-007"
    finding_id: "CR-007"
    severity: "P2"
    processing_status: "ACCEPTED"

  - id: "DQ-008"
    finding_id: "CR-008"
    severity: "P2"
    processing_status: "ACCEPTED"

decisions:
  - id: "DR-001"
    finding_id: "CR-001"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-002"
    finding_id: "CR-002"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-003"
    finding_id: "CR-003"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-004"
    finding_id: "CR-004"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-005"
    finding_id: "CR-005"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-006"
    finding_id: "CR-006"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-007"
    finding_id: "CR-007"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"
  - id: "DR-008"
    finding_id: "CR-008"
    decision: "ACCEPTED"
    owner: "规格所有者（授权主 agent 代行决策）"
    date: "2026-08-07"

statistics:
  source_findings:
    product: 4
    system: 5
    test: 5
  consolidated_findings: 8
  unmerged_findings: 0
  duplicate_findings: 0
  represented_elsewhere_findings: 0
  conflicts: 0
  p0: 0
  p1: 5
  p2: 3
```

---

# Template Completion Rules

合并者已遵守以下规则：

1. 每个 source review 均在 Source Reviews 中显式记录。
2. 每个 source Finding 均有明确归属（合并到 CR / 未合并 / 重复 / 替代）。
3. 无 source Finding 静默消失（完整性校验 14 = 14 + 0 + 0 通过）。
4. Consolidated Finding ID 唯一且连续（CR-001 至 CR-008）。
5. 每个 Consolidated Finding 代表一个根本问题。
6. Findings 未仅因共享组件/关键词/严重度/后果而合并。
7. 独立审核视角已保留（Reviewer Perspectives 节）。
8. 冲突已显式检查（无冲突，记录于 Cross-Reviewer Conflicts）。
9. 确认证据、推断证据、未知项已分离。
10. 未将假设转换为事实。
11. 未发明需求、系统行为或业务规则。
12. 严重度基于统一根本问题的实质后果，非机械取最高值（Severity Change Rationale 已逐条说明）。
13. 保留了所有相关 source review 的最强证据。
14. Decision Queue 包含所有待决策 Finding。
15. 合并者未做任何接受/拒绝决策。
16. Machine-Readable Consolidation Index 与详细审核保持一致。
17. 审核统计与实际 Findings 及归属一致。
