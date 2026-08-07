# System Review

## Review Metadata

### Review ID

2026-08-07-review-001

### Reviewer

yy-system-critic

### Review Type

SYSTEM_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md

### Review Date

2026-08-07

### Review Status

COMPLETED

---

## Review Scope

This review evaluates the Design Spec from the perspective of system reliability, security, data integrity, operational resilience, architectural complexity, reversibility, and long-term maintainability.

This review does not:

* redesign the system;
* produce an implementation plan;
* review source-code style;
* optimize implementation details;
* make the final approval decision;
* replace detailed security testing or production validation.

The purpose of this review is to identify system-level risks that could cause data loss, security breaches, production outages, unrecoverable failures, excessive operational burden, or unnecessary architectural complexity.

The review assumes that the Design Spec will eventually be implemented and operated in production.

---

## Findings

### SC-001 — 安全预检仅列于风险表而未嵌入执行步骤，存在跳过检查导致数据丢失的风险

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

HIGH

#### Location

Design Spec 第 4.7 节"实施顺序"与第 6 节"风险与对策"

#### Risk

第 4.7 节第 7 步执行 `rm -rf ~/.claude/skills/yy-spec-review` 删除旧技能目录。该目录是一个真实目录拷贝（非 symlink），内含 `.workbuddy/` 和 `.superpowers/` 子目录。第 6 节风险表正确识别了"旧拷贝删除丢失本地改动"的风险，并将对策定义为"先 `diff -r` 旧拷贝与本地仓库，确认无未同步改动后再删"。然而，这个 `diff -r` 预检步骤并未出现在第 4.7 节的逐步执行计划中——第 7 步仅写了"建 symlink：Claude 删旧+建新，Hermes 建新"，未引用或嵌套该预检。

实际文件系统对比证实：当前本地仓库比旧拷贝多出 `agents/`、`docs/superpowers/plans/`、`docs/superpowers/reviews/`、新增 spec 文件、`.superpowers/sdd/*.diff`、`.workbuddy/memory/2026-08-04.md` 等内容；同时 SKILL.md、CLAUDE.md、README.md 在两处内容不同。这意味着两处已经存在实质性差异。按第 4.7 节逐字执行的操作者可能直接执行 `rm -rf` 而跳过 diff 确认。

#### Trigger Condition

1. 操作者按第 4.7 节逐步骤执行，未交叉引用第 6 节风险表。
2. 到达第 7 步时，操作者执行 `rm -rf ~/.claude/skills/yy-spec-review`，未先行 diff 对比。
3. 旧拷贝中存在自 7 月 20 日以来在旧目录中直接编辑但未同步到本地仓库的文件。
4. 数据随 `rm -rf` 永久丢失。

#### Consequence

本地工作产物（`.workbuddy/` 记忆文件、`.superpowers/` 工作流状态）如在旧拷贝中有独有更新，将随目录删除而永久丢失。由于删除发生在本部署流程的末尾步骤，此时 git 首提交已完成并可能已推送至 GitHub，恢复路径仅剩外部备份（如 Time Machine）——而该备份是否存在、是否包含这些文件，设计未做任何假设或验证。

#### Likelihood

MEDIUM

操作者按第 4.7 节线性执行的可能性高；跳过风险表交叉引用的可能性中等。但旧拷贝中实际存在独有未同步改动的概率取决于自 7 月 20 日以来操作者的使用模式——当前 diff 显示本地仓库是超集（repo 包含更多文件），但该状态在部署执行时可能已变化。

#### Reversibility

IRREVERSIBLE

`rm -rf` 删除的文件无法通过本设计的任何步骤恢复。外部备份是唯一的恢复路径，但不在设计范围内。

#### Recommendation

将 `diff -r` 预检作为独立步骤嵌入第 4.7 节的执行序列中，置于 symlink 创建步骤之前。例如，在第 6 步和第 7 步之间插入：

> 6.5. 对比旧拷贝与本地仓库：`diff -r ~/.claude/skills/yy-spec-review/ <本地仓库路径>`，确认无未同步改动；如有差异，先同步或备份后再继续。

同时建议在 `rm -rf` 之前先执行 `cp -r` 到临时备份目录，提供即时回滚能力。

#### Evidence

- 第 4.7 节第 7 步仅写"建 symlink：Claude 删旧+建新"，未提及 `diff -r` 预检。
- 第 6 节风险表将 `diff -r` 列为对策，但未说明该对策在第 4.7 节的哪一步执行。
- 文件系统对比证实两处 SKILL.md、CLAUDE.md、README.md 内容不同；本地仓库含多个旧拷贝不存在的文件。

#### Assumptions

- CONFIRMED：第 4.7 节与第 6 节之间存在结构性脱节——对策未嵌入执行计划。
- CONFIRMED：`~/.claude/skills/yy-spec-review/` 是真实目录而非 symlink，`rm -rf` 将物理删除其内容。
- INFERRED：操作者可能仅遵循第 4.7 节的线性步骤而忽略风险表。

#### Reversibility Analysis

`rm -rf` 删除在本地文件系统上不可逆。如删除前已推送至 GitHub，仓库内容可恢复，但 `.workbuddy/` 和 `.superpowers/` 中不在 git 跟踪范围内的本地独有文件无法从 GitHub 恢复。外部备份（如 Time Machine）是唯一恢复路径，但其覆盖范围和时效性未验证。

#### Operational Impact

- 部署前置条件增加一个验证步骤。
- 如 diff 发现差异，部署流程暂停等待操作者决策，可能延长部署窗口。
- 无持续运维影响——此为一次性部署风险。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

无长期维护影响。如在部署时按建议嵌入预检步骤，后续执行者始终可见完整的安全操作序列。

#### Source References

- Design Spec 第 4.7 节"实施顺序"
- Design Spec 第 6 节"风险与对策"
- Design Spec 第 2.4 节"环境就绪状态"（确认旧目录为非 symlink 的真实拷贝）

---

### SC-002 — 改名操作在 git init 之前执行，缺乏版本控制安全网

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

HIGH

#### Location

Design Spec 第 4.1 节"改名策略"与第 4.7 节"实施顺序"

#### Risk

改名操作（8 条替换规则覆盖 13 个文件）在第 4.7 节第 1 步执行，而 `git init` 在第 5 步。改名采用人工文本替换方式（设计未指定使用脚本化工具），涉及 frontmatter `name` 字段、文件内角色名引用、description 文本、路径引用等多种上下文。一旦某条规则被错误应用——例如替换范围过宽（误改了不应改的历史文件）或过窄（遗漏了某处引用）——在 `git init` 之前的任何错误都没有版本控制历史可供回滚。

更关键的是：第 4.7 节将 grep 验证放在第 8 步（最后），而非在改名完成后、git commit 之前立即执行。这意味着如果 grep 验证在第 8 步发现问题，此时 commit 已生成、GitHub 仓库已创建、可能已推送——修复需要 amend commit 或创建新 commit，且必须在 GitHub 上覆盖历史。

#### Trigger Condition

1. 操作者按第 4.1 节替换规则逐文件手动修改。
2. 某条规则被错误应用（如将 `yy-` 替换为 `spec-` 时误匹配了不应改的历史文档中的 `yy-` 前缀，或遗漏了某处 `yy-spec-review` 引用）。
3. 操作者继续执行步骤 2-5，将包含错误的文件 `git add -A` 并 commit。
4. 步骤 6 推送至 GitHub。
5. 步骤 8 grep 验证发现残留或误改。
6. 此时修复需要 amend commit 并 force push（或追加修正 commit），且 GitHub 上的首提交已包含错误历史。

#### Consequence

- 如错误在 push 前发现：需 amend commit，操作复杂但可接受。
- 如错误在 push 后发现：需 force push 覆盖 GitHub 历史，如有多人/多机协作则引入协调成本。
- 无论哪种情况，都破坏了"仓库首提交即为干净的目标状态"的设计意图（第 4.7 节末尾声明）。
- 最坏情况：误改扩散到 §3.1 声明"不改"的历史文件（如 `scripts/baseline_snapshot/` 内的角色名），破坏了基线快照与瘦身工具链的内部自洽性。

#### Likelihood

MEDIUM

13 个文件、8 条替换规则的组合产生约 30+ 个独立改动点。人工逐文件执行时遗漏或误匹配的概率不可忽略。虽然操作者可通过谨慎执行降低风险，但设计未提供任何减少人为错误的结构性保障（如脚本化替换、阶段性验证门）。

#### Reversibility

PARTIALLY_REVERSIBLE

在 git commit 之前，可通过手动逆向编辑恢复；commit 之后但 push 之前，可 amend；push 之后需 force push 或追加修正 commit。但 `scripts/baseline_snapshot/` 内的文件如被误改，恢复依赖外部备份（基线快照本身就是备份锚点，修改它将破坏其作为锚点的可靠性）。

#### Recommendation

（1）将 grep 验证拆分为两个阶段：第一阶段在改名完成后、`git add` 之前立即执行，作为通过门；第二阶段在全部步骤完成后作为终验。（2）考虑使用脚本化替换（如 `sed` 批处理）替代纯人工编辑，减少人为错误概率。（3）在 `git add` 之前对 §3.1 声明的"不改"目录执行专项 diff，确认无意外修改。

#### Evidence

- 第 4.1 节列出了 13 个文件中的约 30+ 改动点，但未指定替换工具或方法（人工 vs 脚本化）。
- 第 4.7 节第 1 步"改名"与第 5 步"git init + git add + git commit"之间无中间验证门。
- 第 5 节的 grep 验证（`grep -rn "yy-"`）被放在第 8 步，在 commit 和 push 之后。
- 第 4.7 节末尾声明"改名与 .gitignore 必须先于首个 commit，确保仓库首提交即为干净的目标状态"——此目标依赖改名的一次性正确执行，但缺乏程序化保障。

#### Assumptions

- CONFIRMED：改名操作（步骤 1）在 `git init`（步骤 5）之前执行。
- CONFIRMED：grep 验证（步骤 8）在所有 git 操作（步骤 5-6）之后执行。
- INFERRED：13 个文件的约 30+ 改动点以人工方式执行。
- INFERRED：操作者在多步操作中可能出现遗漏或误匹配。

#### Reversibility Analysis

改名本身是可逆的（反向替换即可），但逆转的难度随后续步骤的推进而增加。在 git init 之前：简单文件编辑回退。git init 之后但 push 之前：amend commit。push 之后：force push 或追加修正 commit。`scripts/baseline_snapshot/` 如被误改且无外部备份，回退到原始基线内容需要从 git 历史（如之前的内部 git 仓库 `git@git.yyrd.com:yyit/yy-spec-review.git`）恢复，但设计已声明当前项目非 git 仓库，基线内容仅存在于文件系统。

#### Operational Impact

- 部署窗口增加约 5-10 分钟（拆分验证门后额外检查时间）。
- 如第一阶段验证发现问题，部署暂停等待修正，然后重新验证。
- 无长期运维影响——此为一次性部署风险。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

如因改名遗漏导致文件中残留 `yy-` 引用，后续维护者将面临命名不一致的困惑——部分引用使用 `spec-review`，部分仍为 `yy-spec-review`。这可能持续到下一次全面改名或重构为止。

#### Source References

- Design Spec 第 4.1 节"改名策略"（替换规则与待改文件清单）
- Design Spec 第 4.7 节"实施顺序"（步骤 1 与步骤 5 的顺序关系）
- Design Spec 第 5 节"验证清单"（grep 验证位于全部步骤末尾）
- Design Spec 第 3.1 节"改名边界"（不改清单与一致性目标）

---

### SC-003 — 双平台 symlink 共享单文件源，并发访问的竞态窗口未定义

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 第 4.3 节"双平台 symlink 安装"

#### Risk

两个独立平台运行时（Claude Code 技能加载器、Hermes 技能扫描器与执行引擎）通过 symlink 共享同一份文件系统。在正常稳态下这是安全的——两者均为只读消费者。但在以下场景中存在竞态窗口：

- `update.sh` 执行 `git merge --ff-only` 修改文件时，Hermes 的 skill scanner（§2.2 描述的 scan 机制）正并发扫描同一目录树。
- Claude Code 正在加载并读取 SKILL.md 或角色定义文件时，`git merge` 更新了同一文件。
- Hermes 正在将 symlink 指向的技能 backfill 写入 `lock.json` 时，文件树发生变更。

文件系统级别的 `git merge --ff-only` 不具备原子目录更新语义——文件逐个变更，存在中间状态窗口。在极端情况下，平台加载器可能读取到部分旧版本文件与部分新版本文件的不一致组合。

#### Trigger Condition

1. 系统处于稳态——两个平台正常运行，symlink 均生效。
2. 操作者执行 `bash update.sh`（或等效的 `git pull`）以获取远程更新。
3. 在 `git merge --ff-only` 的文件更新窗口内（通常 <1 秒，但取决于文件数量和磁盘 I/O），Hermes scanner 或 Claude Code loader 恰好发起对 symlink 目标目录的读取。
4. 读取操作跨越了文件更新窗口，获取到不一致的文件快照。

#### Consequence

- Hermes scanner 可能在 `lock.json` 中记录不一致的 content_hash，导致后续的变更检测逻辑误判技能是否需要重新 backfill。
- Claude Code 可能在同一次加载中读取到新版 SKILL.md 但旧版角色定义（或反之），导致技能行为与设计预期短暂偏离。
- 实际影响受限于两个因素：（a）skill 文件总数约 20 个，更新窗口极短；（b）两个平台均为读密集型，写入仅发生在显式 `git pull` 时。因此，该风险的**概率低**，但缺乏任何形式的并发保护使得**一旦命中，诊断困难**。

#### Likelihood

LOW

触发条件要求操作者恰好在对技能目录执行 git pull 的同时，某个平台恰好发起扫描或加载。考虑到技能文件数量少（约 20 个关键文件），文件更新窗口在毫秒级别。但 Hermes 的 scan 机制可能被多种事件触发（启动、定时扫描、手动 `/skills` 刷新），增加了时间窗口的重叠概率。

#### Reversibility

REVERSIBLE

竞态窗口是瞬时的。下次扫描或重新加载将获取一致的文件快照。但如果 Hermes 的 `lock.json` 被写入不一致的 hash，可能需要手动清理或等待下次自动修正。

#### Recommendation

在 `update.sh` 或操作文档中增加一条约束：执行 `git pull` 更新前，建议在低使用时段操作；或者，接受本风险但记录为已知限制。另一个更结构化的方案是：在 `update.sh` 中通过锁定文件或检查 Hermes/Claude 进程活跃状态来降低并发概率。但对本技能的小文件集和低频更新场景，轻量方案（文档记录 + 推荐操作窗口）可能是合适的。

#### Evidence

- 第 4.3 节确认两平台 symlink 指向同一份本地仓库，"修改一处两平台同步生效"。
- 第 4.6 节确认 update.sh 执行 `git merge --ff-only`，直接修改工作目录文件。
- 第 2.2 节描述 Hermes scan 机制为自动后台行为，触发时机未被本设计控制。
- goal-manager 参考范例（第 2.3 节）使用相同的 symlink 架构，意味着此风险也存在于参考范例中。这是通过先例验证的设计模式，但不代表该模式没有并发风险。

#### Assumptions

- CONFIRMED：两平台通过 symlink 共享同一份文件系统。
- CONFIRMED：`update.sh` 的 `git merge --ff-only` 直接修改工作目录文件。
- CONFIRMED：Hermes scan 是自动后台行为，非操作者显式触发。
- INFERRED：Hermes scanner 在扫描时对每个文件单独 `open/read/close`，而非获取原子快照。
- INFERRED：`git merge --ff-only` 的文件更新窗口足够短，实际命中概率低。

#### Reversibility Analysis

竞态导致的瞬时不一致状态会在下一次文件读取时自动修复。如果 Hermes `lock.json` 被污染（content_hash 不匹配），Hermes 的下次 scan 应自动检测到不匹配并重新 backfill（如果 Hermes 的 backfill 逻辑使用 content_hash 作为变更检测依据）。不需要人工恢复操作。

#### Operational Impact

- 建议在文档中标注推荐的更新窗口（低使用时段）。
- 如果未来技能文件数量大幅增长，更新窗口变长，需重新评估本风险的严重度。
- 当前无实际运维告警需求。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

长期来看，如果 Hermes 或 Claude Code 的 skill 加载器未来增加了写入行为（如缓存、状态文件），本风险的严重度将上升。当前两个平台对 skill 源文件均为只读消费者，维护影响有限。

#### Source References

- Design Spec 第 4.3 节"双平台 symlink 安装"
- Design Spec 第 4.6 节"update.sh / README"
- Design Spec 第 2.2 节"Hermes 技能机制"
- Design Spec 第 2.3 节"参考范例：goal-manager"

---

### SC-004 — Hermes backfill 对分类目录下 symlink 的兼容性假设基于单一样本

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 第 2.2 节"Hermes 技能机制"与第 4.3 节"双平台 symlink 安装"

#### Risk

第 2.2 节断言 Hermes 的 scan + backfill 注册机制使"手动/symlink 放入的技能会被自动发现注册"，并引用 `yuanbao` 技能的 `scan_verdict: backfilled` 作为唯一证据。

但 yuanbao 的安装路径为 `yuanbao/`（技能目录根下的扁平路径），而 spec-review 的目标路径为 `software-development/spec-review/`（分类子目录下）。两者在目录层级上不同。

检查 Hermes lock.json 证实：当前仅 yuanbao 一个 backfilled 记录；`software-development/` 目录下现有的 10 个技能均为 Hermes 内置技能（dogfood、requesting-code-review 等），通过 bundling 机制安装而非 backfill。目前 Hermes 环境中不存在任何"用户在分类子目录下手动放置 symlink 后被成功 backfill"的先例。

这意味着设计对 backfill 行为在分类目录 symlink 场景下的兼容性假设未经独立验证。

#### Trigger Condition

1. 操作者按第 4.3 节在 `~/.hermes/skills/software-development/` 下创建 spec-review symlink。
2. Hermes 启动或执行下次 scan。
3. Scanner 的行为在处理分类子目录中的 symlink 时与处理根目录下的 symlink（yuanbao 场景）不同——例如，scanner 可能跳过分类目录中来源非内置的技能、对 symlink 的目标路径解析行为不同、或 backfill 逻辑假定技能在根目录下。
4. spec-review 未被自动 backfill，在 Hermes 中不可用，或 `/skills` 列表中不显示。

#### Consequence

- 技能在 Hermes 中不可见或不可用，第 5 节验证清单的第 3 项（"Hermes 启动后 /skills 列出 spec-review"）失败。
- 需要人工介入：可能需手动编辑 lock.json、在 Hermes 配置中显式注册、或将 symlink 移至根目录。
- 不影响 Claude Code 端——symlink 在 Claude Code 的扁平 `~/.claude/skills/` 下正常工作（已有 goal-manager 先例证实）。

#### Likelihood

LOW

yuanbao 的 backfill 证明了 Hermes scanner 确实能发现非内置安装的技能。分类目录与根目录的差异可能仅是路径组织方式，不影响 scanner 的核心发现逻辑。但缺乏直接先例使得该断言存在不确定性。

#### Reversibility

REVERSIBLE

如 backfill 失败，可通过以下方式恢复：（a）将 symlink 移动到 `~/.hermes/skills/` 根目录；（b）手动编辑 `lock.json` 添加条目；（c）向 Hermes 提交 issue/反馈。均不涉及数据丢失。

#### Recommendation

（1）在部署前进行最小化验证：在 `~/.hermes/skills/software-development/` 下创建一个最小 symlink 测试技能（仅含 SKILL.md 和 frontmatter），重启 Hermes 或触发 scan，确认 backfill 行为与 flat 目录一致。（2）在第 5 节验证清单第 3 项中增加具体观察点：不仅检查 `/skills` 列表，还应直接检查 `lock.json` 中新条目的 `scan_verdict` 字段值。（3）在第 6 节风险表中记录该不确定性，并准备回退方案（如必要时将 symlink 放至根目录并调整 `metadata.hermes.category` 来控制分类展示）。

#### Evidence

- 第 2.2 节："手动/symlink 放入的技能会被自动发现注册"——基于 yuanbao 单一样本。
- lock.json 证实：yuanbao 安装路径为 `"install_path": "yuanbao"`（根目录），`"scan_verdict": "backfilled"`。
- `software-development/` 目录下现有 10 个技能均为内置技能，无任何用户手动放置后 backfill 的先例。
- 第 2.3 节 goal-manager 参考范例中 Hermes symlink 在 `productivity/goal-manager`（分类子目录），但 goal-manager 的 backfill 状态未在设计中被引用或验证。

#### Assumptions

- CONFIRMED：yuanbao 在根目录下被成功 backfill。
- CONFIRMED：spec-review 的目标路径在分类子目录 `software-development/` 下。
- INFERRED：backfill 机制对分类子目录中的 symlink 行为与根目录相同。
- UNKNOWN：Hermes scanner 处理分类子目录中 symlink 的精确逻辑。

#### Reversibility Analysis

完全可逆。backfill 失败不造成数据丢失。将 symlink 从分类目录移至根目录即可绕过问题。或手动编辑 lock.json。恢复不需要外部系统或备份。

#### Operational Impact

- 部署前增加一个轻量验证步骤（约需 5 分钟）。
- 如验证发现不兼容，需调整 symlink 目标路径——对实施顺序无结构性影响。
- 如部署后发现问题（跳过验证），需要事后变更 symlink 路径，并可能触发 Hermes 重新 scan。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

如果 Hermes 未来版本修改了 scanner 的发现逻辑（如仅扫描内置 skill、停止支持 backfill），symlink 方式可能完全失效。建议在 update.sh 或文档中标注该依赖，以便维护者了解 symlink 方式对 Hermes scan 行为的依赖关系。

#### Source References

- Design Spec 第 2.2 节"Hermes 技能机制"
- Design Spec 第 4.3 节"双平台 symlink 安装"
- Design Spec 第 2.3 节"参考范例：goal-manager"
- Hermes lock.json（`~/.hermes/skills/.hub/lock.json`）：yuanbao backfill 记录
- Hermes `software-development/` 目录：现有 10 个内置技能

---

### SC-005 — `gh repo create --push` 组合操作部分失败时的中间状态恢复路径不完整

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 第 4.5 节"Git / GitHub 操作"与第 6 节"风险与对策"

#### Risk

`gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin --push` 在第 4.5 节定义为单条命令完成三个操作：创建仓库、设置 remote、推送。这是一个复合操作，使用 GitHub CLI 封装了多次 GitHub API 调用和一次 git push。

第 6 节风险表识别了"gh repo create --push 失败（网络/权限）"风险，对策为"退化为分步：gh repo create 后 git push -u origin main"。

该对策仅覆盖了"整条命令失败"的场景，未覆盖以下部分失败场景：

- **场景 A**：仓库创建成功，remote 设置成功，push 失败（如网络断开）。此时 origin 已设置为 `https://github.com/OneFlowerHill/spec-review.git`，本地 commit 就绪，仅差推送。退化方案（分步 git push）适用。
- **场景 B**：仓库创建成功，remote 设置失败。`--source=. --remote=origin` 的组合行为在 remote 添加失败时是否回滚 remote 设置不确定。此时 `git remote -v` 可能不显示 origin，而 GitHub 上已存在空仓库。
- **场景 C**：仓库创建失败（如名称冲突——账户下已存在同名仓库）。此场景为硬失败，退化方案不适用（需先删除或重命名已有仓库，或选择不同仓库名）。第 4.5 节和第 6 节均未提及名称冲突的处理方式。
- **场景 D**：仓库在 GitHub 上创建成功，但 `gh` CLI 本地进程在设置 remote 前崩溃（如 OOM、kill 信号）。此时 GitHub 上有空仓库，本地无 origin remote，操作者可能不知道仓库已创建。

场景 C 和 D 尤其值得关注：它们导致 GitHub 上存在一个空仓库（或残留仓库），操作者需要额外的恢复步骤来关联或清理。

#### Trigger Condition

1. 按第 4.5 节执行 `gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin --push`。
2. GitHub API 调用中途失败（网络抖动、token 过期、名称冲突、rate limit），部分操作已完成。
3. 操作者根据错误信息判断当前状态，可能需要手动检查 GitHub 上仓库是否存在、本地 remote 是否已设置、本地是否有未推送的 commit。
4. 如果操作者误判状态（如认为仓库未创建而重试，导致名称冲突），恢复步骤变得更复杂。

#### Consequence

- 最坏情况：GitHub 上残留空仓库或半初始化仓库，与本地状态不一致。操作者需要手动清理（`gh repo delete` 或通过 GitHub Web UI 删除），然后重试。
- 中等情况：需要分步手动完成剩余操作，与设计预期的"一步完成"体验有差距，但不造成数据丢失。
- 无论哪种情况，本地 commit 始终安全（仅本地 git 操作，不受 GitHub API 失败影响）。

#### Likelihood

LOW

GitHub API 可用性高，`gh` CLI 稳定。但网络中断和 token 过期是真实场景。名称冲突的概率取决于 `OneFlowerHill` 账户下是否已有 `spec-review` 仓库——设计未对此做先行检查（如 `gh repo view OneFlowerHill/spec-review` 预检）。

#### Reversibility

REVERSIBLE

所有部分失败场景均可手动恢复，不造成数据丢失。最坏情况需手动删除 GitHub 上的残留仓库并重试。

#### Recommendation

（1）在第 4.5 节增加一条前置检查：`gh repo view OneFlowerHill/spec-review` 确认目标仓库不存在（或存在但为空，询问操作者是否复用/覆盖）。（2）在第 6 节风险表中补充"名称冲突"和"部分成功"的具体恢复步骤。（3）考虑将 `--push` 分离为独立步骤，使每个操作的成败可独立观察和恢复。按第 4.5 节的三条命令版本（git init、git commit、gh repo create、git push）虽然多一步，但每步的失败隔离和恢复路径更清晰。

#### Evidence

- 第 4.5 节将仓库创建、remote 设置、推送合并为单条命令。
- 第 6 节风险表的退化方案仅覆盖"整条命令失败"场景，不包括部分成功场景。
- 设计未对 `OneFlowerHill/spec-review` 是否已存在于 GitHub 做前置检查。

#### Assumptions

- CONFIRMED：`gh repo create --push` 是组合操作，包含多个 API 调用。
- CONFIRMED：第 6 节退化方案描述的是整条命令失败后的完整重试，未区分部分成功子场景。
- INFERRED：`gh repo create` 在 remote 添加失败时不会自动回滚 GitHub 端的仓库创建。
- UNKNOWN：`OneFlowerHill` 账户下是否已存在同名仓库。

#### Reversibility Analysis

所有部分失败状态均可恢复。最坏情况（GitHub 上有空仓库，本地无 remote）：手动 `gh repo delete OneFlowerHill/spec-review --yes` 后重试。或手动 `git remote add origin <url>` 后 `git push -u origin main`。本地 commit 不会丢失。

#### Operational Impact

- 部署前置检查增加约 10 秒（执行 `gh repo view` 确认仓库状态）。
- 如发现名称冲突，需额外决策步骤（删除旧仓库、改名、或使用其他仓库名）。
- 无长期运维影响。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

无长期维护影响。本 Finding 仅涉及一次性部署操作的鲁棒性。

#### Source References

- Design Spec 第 4.5 节"Git / GitHub 操作"
- Design Spec 第 6 节"风险与对策"

---

## Finding Summary

| Finding ID | Severity | Evidence Class | Confidence | Likelihood | Reversibility | Short Description |
| ---------- | -------- | -------------- | ---------- | ---------- | ------------- | ----------------- |
| SC-001     | P1       | MATERIAL_RISK  | HIGH       | MEDIUM     | IRREVERSIBLE  | 安全预检（diff -r）仅列于风险表而未嵌入执行步骤，存在跳过检查导致数据丢失的风险 |
| SC-002     | P1       | MATERIAL_RISK  | HIGH       | MEDIUM     | PARTIALLY_REVERSIBLE | 改名操作在 git init 之前执行，缺乏版本控制安全网；grep 验证在 push 之后而非 commit 之前 |
| SC-003     | P2       | MATERIAL_RISK  | MEDIUM     | LOW        | REVERSIBLE    | 双平台 symlink 共享单文件源，git merge 与平台扫描器之间存在并发读取竞态窗口 |
| SC-004     | P2       | MATERIAL_RISK  | MEDIUM     | LOW        | REVERSIBLE    | Hermes backfill 对分类目录下 symlink 的兼容性假设基于 yuanbao 单一样本，缺乏分类目录直接先例 |
| SC-005     | P2       | MATERIAL_RISK  | MEDIUM     | LOW        | REVERSIBLE    | gh repo create --push 组合操作部分失败（名称冲突、部分成功）时的中间状态恢复路径不完整 |

---

## System Risk Coverage

| Risk Dimension | Status | Finding IDs |
| -------------------------------- | -------- | ----------- |
| Data Integrity and Consistency | REVIEWED | SC-001, SC-002 |
| Security Boundaries | REVIEWED | — |
| Authentication and Authorization | NOT_APPLICABLE | 本设计不涉及认证授权变更 |
| Availability and Resilience | REVIEWED | SC-003 |
| Failure Recovery | REVIEWED | SC-001, SC-005 |
| External Dependencies | REVIEWED | SC-004, SC-005 |
| Concurrency and Race Conditions | REVIEWED | SC-003 |
| Data Lifecycle and Migration | REVIEWED | SC-001 |
| Backward Compatibility | NOT_APPLICABLE | 本设计不涉及向后兼容（新仓库首次推送） |
| Operational Complexity | REVIEWED | SC-001, SC-002 |
| Maintenance Burden | REVIEWED | SC-003, SC-004 |
| Irreversible Decisions | REVIEWED | ID-001, ID-002 |
| Over-Engineering | NOT_APPLICABLE | 设计范围精当，未发现过度工程 |
| Observability and Diagnosis | REVIEWED | SC-005 |

---

## Irreversible Decisions

### ID-001 — 将内部审查与开发产物推送至 GitHub 私有仓库

#### Decision

第 3.2 节决定将 `docs/项目一期|二期审查报告.md`、`.superpowers/sdd/review-*.diff`、`.workbuddy/` 等含用友内部审核与代码内容的文件推送至个人 GitHub 私有仓库。

#### Why It Is Difficult to Reverse

一旦数据离开本地文件系统进入 GitHub 的服务器，即受 GitHub 的数据留存策略约束。即使后续 force push 覆盖历史或删除仓库，GitHub 的内部备份、缓存和第三方索引（如搜索引擎缓存、archive.org）可能保留副本。私有仓库降低了公开暴露的概率，但无法消除以下泄露路径：账户被盗、访问权限误配、GitHub 内部安全事件、仓库可见性被意外改为 public。

#### Reversal Cost

HIGH

无法保证从 GitHub 及其生态中完全清除数据。删除仓库可阻止新的访问，但已存在的克隆、fork 或缓存副本不受控制。

#### Risk

长期来看，用友内部审核意见和代码变更细节（diff 内容）存储在第三方平台，超出用友的信息安全管控边界。如果未来用友信息安全策略收紧——禁止内部评审内容存储于非授权第三方平台——这些数据已经无法真正撤回。

#### Recommendation

（1）在推送前，对 `docs/项目一期|二期审查报告.md` 和 `.superpowers/sdd/review-*.diff` 内容进行脱敏审查，移除或泛化内部项目名称、人员信息、系统架构细节。（2）在 README.md 或 CLAUDE.md 中明确记录"本仓库包含用友内部评审产物"的警示，使未来的贡献者了解数据的敏感性。（3）确认第 3.2 节中的"规格所有者已确认可接受"是显式的、有记录的决策（而非口头确认）。

#### Status

OPEN

---

### ID-002 — 技能 name 从 `yy-spec-review` 改为 `spec-review`

#### Decision

第 4.1 节将 SKILL.md frontmatter 的 `name` 字段从 `yy-spec-review` 改为 `spec-review`，同时所有活文件中的引用同步变更。

#### Why It Is Difficult to Reverse

`name` 字段是技能在两个平台中的身份标识。一旦改名并部署到两平台，回退需要：（a）反向替换所有文件中的引用；（b）重新推送至 GitHub；（c）更新两平台的 symlink 路径。更重要的是——如果改名后产生了新的 Review Round 产物（包含 `spec-review` 引用）、外部用户克隆了仓库、或第三方文档引用了新名称，回退会引入历史命名不一致。

#### Reversal Cost

MEDIUM

纯文件和 symlink 层面的回退是直接的（反向替换 + 重建 symlink），但 Git 历史中会保留改名和回退的完整轨迹。外部引用（如有）不受控制。

#### Risk

如果改名后发现与 Hermes agentskills.io 生态中的其他 `spec-review` 技能冲突（虽然当前可能性低，该技能为原创方法论），回退将比较痛苦。当前风险较低，因为 `spec-review` 是描述性名称，命名空间冲突概率低，且私有仓库不参与生态索引。

#### Recommendation

无需特殊处理——改名是设计的核心目标之一，且已有 goal-manager 命名先例验证该模式的有效性。记录为不可逆决策即可，确保决策是显式的。

#### Status

OPEN

---

## Over-Engineering and Complexity Risks

无。本设计的范围精当、步骤清晰、复杂度合理。symlink 方案是满足"两平台共用单一代码源"需求的最简方案；改名策略明确区分了活文件与历史快照的边界；GitHub 推送使用 `gh` CLI 一步完成而非自行编排多步 API 调用。未发现与此设计需求不成比例的架构复杂度。

---

## Unresolved System Questions

### Q-001 — Hermes scanner 如何处理分类子目录中的 symlink？

#### Question

Hermes 的 scan + backfill 机制在发现 `software-development/spec-review` 分类子目录中的 symlink 时，其行为是否与发现根目录 `yuanbao/` 中的真实目录或 symlink 完全一致？

#### Why It Matters

如果 scanner 对分类子目录中的 symlink 有不同处理逻辑（如跳过来源非内置的技能、不触发 backfill、需要不同的文件结构），symlink 方式可能失败，技能在 Hermes 中不可见。

#### Required Clarification

（1）Hermes scanner 的发现逻辑是否对分类子目录和根目录一视同仁？（2）backfill 机制是否依赖技能目录中存在特定文件（如 `.hermesrc`）？（3）分类子目录中的技能是否受 `.bundled_manifest` 或 `.curator_state` 影响？

#### Status

OPEN

---

### Q-002 — 旧 `~/.claude/skills/yy-spec-review/` 中的 `.workbuddy/` 和 `.superpowers/` 是否有本地独有数据？

#### Question

自 7 月 20 日旧拷贝创建以来，用户是否在 `~/.claude/skills/yy-spec-review/` 目录中直接编辑过文件或产生了新的工作产物？如果有，这些改动是否已同步到本地仓库 `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/`？

#### Why It Matters

SC-001 的严重度取决于旧拷贝中是否存在未同步的独有数据。当前 diff 显示本地仓库是超集（repo 包含更多文件），但这只代表当前状态。在部署执行时，操作者可能已对旧拷贝产生了新的修改。

#### Required Clarification

执行 `diff -r ~/.claude/skills/yy-spec-review/ /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/` 并确认所有差异均为预期差异（repo 有更多文件，旧拷贝无独有修改），或对差异文件执行备份与合并。

#### Status

OPEN

---

## Review Limitations

1. **Hermes scanner 内部机制未验证**：本审核基于 Hermes lock.json、目录结构和 yuanbao 先例进行推理，但未阅读 Hermes scanner 源代码。SC-004 的置信度因此标记为 MEDIUM 而非 HIGH。
2. **GitHub 账户状态未实时验证**：`OneFlowerHill` 账户下是否已存在 `spec-review` 仓库未在审核时检查（仅 `gh repo view` 可确认）。SC-005 中的名称冲突场景取决于该信息。
3. **用户对旧技能目录的使用模式未知**：无法确定自 7 月 20 日以来用户在 `~/.claude/skills/yy-spec-review/` 中是否有编辑行为。SC-001 的后果评估基于一般性推理而非用户行为证据。

---

## Reviewer Conclusion

### Critical Finding Count

* P0: 0
* P1: 2
* P2: 3

### Risk Summary

* Security risks: 0
* Data integrity risks: 2 (SC-001, SC-002)
* Availability and resilience risks: 1 (SC-003)
* Operational risks: 3 (SC-001, SC-002, SC-005)
* Maintenance risks: 1 (SC-004)
* Irreversible decisions: 2 (ID-001, ID-002)
* Over-engineering risks: 0

### Review Result

REQUIRES_REVIEW

This review identifies system-level risks that must be considered by the Consolidation phase.

SC-001 和 SC-002（均为 P1）应优先关注：前者涉及部署过程中的结构性安全缺陷（安全预检未嵌入执行计划），后者涉及改名操作的验证门位置不当。两者的修复成本低（调整步骤顺序、增加中间验证），但在当前设计状态下如被忽略，可能导致数据丢失或仓库历史污染。

SC-003 至 SC-005（均为 P2）是低频低影响的边界风险，建议在部署前通过增加文档说明或轻量验证来管理，不阻止部署推进。

ID-001（内部内容推送至 GitHub）是一次性不可逆决策，虽已获规格所有者确认，但建议在推送前执行内容脱敏审查。

The System Critic does not determine whether the Findings are ultimately accepted, rejected, deferred, or otherwise resolved.

Final disposition is determined by the Decision Protocol.

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-07-review-001"
  reviewer: "yy-system-critic"
  review_type: "SYSTEM_REVIEW"
  status: "COMPLETED"

findings:
  - id: "SC-001"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "安全预检（diff -r）仅列于风险表而未嵌入执行步骤，存在跳过检查导致数据丢失的风险"
    location: "Design Spec 第 4.7 节与第 6 节"
    likelihood: "MEDIUM"
    reversibility: "IRREVERSIBLE"
    source_references:
      - "Design Spec 第 4.7 节实施顺序"
      - "Design Spec 第 6 节风险与对策"
      - "Design Spec 第 2.4 节环境就绪状态"
    risk_dimensions:
      - "Data Integrity and Consistency"
      - "Failure Recovery"
      - "Operational Complexity"
    status: "PENDING_DECISION"

  - id: "SC-002"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "改名操作在 git init 之前执行，缺乏版本控制安全网；grep 验证在 push 之后而非 commit 之前"
    location: "Design Spec 第 4.1 节与第 4.7 节"
    likelihood: "MEDIUM"
    reversibility: "PARTIALLY_REVERSIBLE"
    source_references:
      - "Design Spec 第 4.1 节改名策略"
      - "Design Spec 第 4.7 节实施顺序"
      - "Design Spec 第 5 节验证清单"
      - "Design Spec 第 3.1 节改名边界"
    risk_dimensions:
      - "Data Integrity and Consistency"
      - "Operational Complexity"
    status: "PENDING_DECISION"

  - id: "SC-003"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "双平台 symlink 共享单文件源，git merge 与平台扫描器之间存在并发读取竞态窗口"
    location: "Design Spec 第 4.3 节"
    likelihood: "LOW"
    reversibility: "REVERSIBLE"
    source_references:
      - "Design Spec 第 4.3 节双平台 symlink 安装"
      - "Design Spec 第 4.6 节 update.sh / README"
      - "Design Spec 第 2.2 节 Hermes 技能机制"
      - "Design Spec 第 2.3 节参考范例 goal-manager"
    risk_dimensions:
      - "Availability and Resilience"
      - "Concurrency and Race Conditions"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-004"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "Hermes backfill 对分类目录下 symlink 的兼容性假设基于 yuanbao 单一样本，缺乏分类目录直接先例"
    location: "Design Spec 第 2.2 节与第 4.3 节"
    likelihood: "LOW"
    reversibility: "REVERSIBLE"
    source_references:
      - "Design Spec 第 2.2 节 Hermes 技能机制"
      - "Design Spec 第 4.3 节双平台 symlink 安装"
      - "Design Spec 第 2.3 节参考范例 goal-manager"
      - "Hermes lock.json yuanbao backfill 记录"
    risk_dimensions:
      - "External Dependencies"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-005"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "gh repo create --push 组合操作部分失败（名称冲突、部分成功）时的中间状态恢复路径不完整"
    location: "Design Spec 第 4.5 节与第 6 节"
    likelihood: "LOW"
    reversibility: "REVERSIBLE"
    source_references:
      - "Design Spec 第 4.5 节 Git / GitHub 操作"
      - "Design Spec 第 6 节风险与对策"
    risk_dimensions:
      - "Failure Recovery"
      - "External Dependencies"
    status: "PENDING_DECISION"

irreversible_decisions:
  - id: "ID-001"
    status: "OPEN"
    title: "将内部审查与开发产物推送至 GitHub 私有仓库——数据脱离本地管控边界后无法真正撤回"
  - id: "ID-002"
    status: "OPEN"
    title: "技能 name 从 yy-spec-review 改为 spec-review——一旦部署并产生外部引用，回退引入命名历史不一致"

complexity_risks: []

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "Hermes scanner 如何处理分类子目录（software-development/）中的 symlink？其行为是否与根目录中一致？"
  - id: "Q-002"
    status: "OPEN"
    question: "旧技能目录 ~/.claude/skills/yy-spec-review/ 中是否存在未同步到本地仓库的独有数据？"
```
