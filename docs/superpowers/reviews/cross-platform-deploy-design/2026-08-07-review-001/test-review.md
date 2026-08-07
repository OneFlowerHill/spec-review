# Test Review

## 输出语言

本审核的所有描述性内容使用中文撰写。所有大写下划线格式的标识符和枚举值（如 P0、CONFIRMED_GAP、ACCEPTANCE_TEST 等）保持英文。Machine-Readable YAML 索引的 key 和枚举值保持英文。

## Review Metadata

### Review ID

2026-08-07-review-001

### Reviewer

yy-test-designer

### Review Type

TEST_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-07-cross-platform-deploy-design.md

### Review Date

2026-08-07

### Review Status

COMPLETED

---

## Review Scope

本审核评估：在实施开始前，Design Spec 定义的各项行为是否可以被客观验证。

审核聚焦于：

* 验收标准的完整性
* 不可测试的需求
* 未定义的预期结果
* 缺失的边界条件
* 失败恢复验证缺口
* 数据完整性验证缺口
* 状态迁移验证缺口
* 向后兼容性验证缺口
* 运维可观测性缺口
* 长期回归风险

本审核不涉及：

* 代码质量审查
* 系统架构重设计
* 实施技术选型
* 创建完整测试计划
* 替代安全测试、性能测试或生产验证
* 做出最终批准决策

本审核的目的：判断 Design Spec 是否足够清晰地定义了可观测行为，使得可以在实施后客观验证。

一个无法被客观验证的需求是不充分定义的。

---

## Findings

### TD-001 — 实施步骤中途失败后仓库状态无客观验证方法

#### Severity

P1

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

BLIND_SPOT

#### Location

Design Spec §4.5（Git / GitHub 操作）+ §4.7（实施顺序）

#### Verification Gap

Design Spec 定义了 8 步实施顺序（§4.7），且 §4.5 建议 `gh repo create --private --source=. --remote=origin --push` 一步完成仓库创建与推送。当此步骤失败时——例如网络中断导致 `gh repo create` 成功但 `--push` 失败——当前规格未定义如何客观验证本地仓库在重试前所处的状态是否正确。

具体缺口：

1. 步骤 5（git init + add + commit）成功后的本地仓库状态未被定义为可验证的检查点
2. 步骤 6 部分失败后（远程仓库已创建但推送未完成），本地仓库与远程仓库的关系未定义
3. 规格未说明步骤 6 失败后：本地仓库是否需要重置、origin 是否已设置但指向空仓库、重试是否幂等

#### Trigger Scenario

1. 前置条件：改名（步骤 1-2）已完成，.gitignore 已创建（步骤 3），README/update.sh 已更新（步骤 4）
2. 动作：执行步骤 5（`git init && git branch -M main && git add -A && git commit`），成功完成
3. 动作：执行步骤 6（`gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin --push`）
4. GitHub API 成功创建远程仓库并设置 origin，但推送阶段因网络超时失败
5. 此时本地仓库有 origin 指向已存在的远程仓库，但远程仓库可能为空或仅有部分数据
6. 规格未定义如何验证此时的重试安全性，也未定义期望的最终状态

#### Expected Verification

测试者应能确定：

- 本地仓库是否处于可安全重试步骤 6 的状态
- 远程仓库是否存在且为空（允许重新推送）还是已有部分数据（需要 force push 或删除重建）
- 是否需要回滚本地仓库的 origin 设置
- 是否有幂等路径可以安全恢复到已知正确状态

#### Verification Method

无客观验证方法被定义。规格仅提供主路径命令序列，未定义异常路径的验证步骤。

#### Consequence

一次性的跨平台部署操作可能因部分失败而产生不可恢复的中间状态。操作者可能采取错误的恢复动作（如重复 `git init` 或 force push），导致仓库历史损坏或远程仓库状态不一致。由于无验证中间状态的客观标准，不同操作者对同一失败场景可能采取不同恢复策略并得到不同最终结果。

#### Evidence

- Design Spec §4.5 定义主路径命令序列，未包含失败分支
- Design Spec §4.7 定义 8 步顺序执行，未定义每步的前置条件验证和失败恢复路径
- Design Spec §6 风险表提到 `gh repo create --push` 失败风险，对策仅为"退化为分步"，但未定义分步后的状态验证方法
- 经验证：当前仓库确实为非 git 仓库（`NOT_GIT_REPO`），步骤 5 将从零初始化，无历史状态可依赖

#### Recommendation

为每个不可逆或外部依赖步骤定义可验证的检查点：

1. 步骤 5 完成后：定义验证项——`git log --oneline` 应显示首提交存在；`git status` 应显示 clean
2. 步骤 6 的 `--push` 标志失败场景：定义分步验证——先验证 `gh repo create` 成功（通过 `gh repo view`），再验证 `git push` 成功（通过 `git ls-remote origin`）
3. 定义步骤 6 失败后的安全回滚路径或幂等重试条件

#### Source References

* Design Spec §4.5 "Git / GitHub 操作"
* Design Spec §4.7 "实施顺序"
* Design Spec §6 "风险与对策" 第 5 行

#### Reviewer Notes

本 Findings 关注验证缺口而非实施缺陷。分步执行本身是合理的降级策略，但规格需明确定义每一步成功/失败的可观测标准，使操作者可在重试前确认状态。

---

### TD-002 — Hermes 技能发现验证存在"或"逻辑歧义与时机不可控

#### Severity

P1

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

UNTESTABLE_REQUIREMENT

#### Location

Design Spec §5（验证清单）第 3 项 + §2.2（Hermes 技能机制）

#### Verification Gap

验证清单第 3 项的表述为：

> Hermes 启动后 `/skills` 列出 spec-review；或 `~/.hermes/skills/.hub/lock.json` 出现 spec-review 的 backfilled 记录

此验证条件存在两个不可测试的问题：

1. **"或"逻辑歧义**：两个验证路径（`/skills` UI 列表 vs. `lock.json` 文件记录）被"或"连接，但未定义哪个是权威判定依据。如果 `/skills` 列出来了但 `lock.json` 未出现记录（或反之），技能部署算成功还是失败？两个条件等价性的假设未经验证。

2. **时机不可控**：规格 §2.2 描述 backfill 机制为 "Hermes 扫描 skills 目录，对未注册技能自动 backfill"，但未定义扫描触发的确切时机（启动时立即执行？延迟执行？定时执行？）。测试者在 Hermes 启动后立即检查 `lock.json` 可能得到假阴性——不是因为部署失败，而是因为扫描尚未执行。

#### Trigger Scenario

1. 前置条件：Symlink 已按 §4.3 创建，指向正确的本地仓库
2. 动作：启动 Hermes
3. 测试者立即检查 `lock.json`——未发现 spec-review 记录
4. 测试者检查 `/skills` 列表——spec-review 出现（或未出现）
5. 两个验证路径给出不一致的结果
6. 规格未定义在此情况下哪个结果为权威判定

#### Expected Verification

测试者应能确定：

- 技能是否被 Hermes 成功发现和注册
- 验证的单一权威来源是什么（lock.json 文件内容 vs. `/skills` UI 表现 vs. 其他）
- 验证应在什么时机执行（Hermes 启动后多少秒/分钟）
- 什么具体字段组合表示"成功注册"（lock.json 中 backfill 记录的期望字段结构）

当前 `lock.json` 中 yuanbao 技能的 backfill 记录结构为：
```json
{
  "source": "official",
  "identifier": "official/yuanbao",
  "trust_level": "builtin",
  "scan_verdict": "backfilled",
  "metadata": { "backfilled_from": "optional-skills" }
}
```

symlink 部署的技能 backfill 记录是否具有相同字段结构，规格未定义。

#### Verification Method

无客观验证方法被定义。当前验证条件存在歧义且时机未指定，两个独立测试者可能对同一部署状态得出相反结论。

#### Consequence

如果验证依赖"或"条件中的任一条满足即认为成功，可能掩盖真实的注册失败。如果验证要求两条均满足，可能因时机问题产生假阴性。无论哪种情况，部署成功/失败的判定不可靠，导致部署后被误认为已就绪的技能实际上无法被 Hermes 调用。

#### Evidence

- Design Spec §5 验证清单第 3 项：使用"或"连接两个不同来源的验证条件
- Design Spec §2.2：描述 backfill 机制但未定义触发时机和期望的 lock.json 记录字段结构
- 实际 `lock.json` 文件内容：展示了 backfill 记录的实际结构（`scan_verdict`、`metadata.backfilled_from` 等字段），但规格未引用此结构定义验证标准

#### Recommendation

1. 将"或"条件拆分为两个独立验证项：一项验证 `lock.json` 中的程序化记录（定义期望字段和值），另一项验证 `/skills` UI 表现
2. 为 `lock.json` 验证定义最大等待时间（如"启动后 30 秒内"），超时视为失败
3. 定义 backfill 记录的期望字段结构：至少包含 `scan_verdict: "backfilled"`，以及技能对应的 `install_path` 和 `files` 列表

#### Source References

* Design Spec §5 验证清单第 3 项
* Design Spec §2.2 "Hermes 技能机制"

#### Reviewer Notes

yuanbao 技能的 lock.json 记录已在本次审核中实际读取，其结构可作为定义验证标准的参考。本 Findings 不要求 Hermes 改变其 backfill 行为，仅要求在规格层面定义可客观判断成功/失败的标准。

---

### TD-003 — 删除旧技能目录前的内容差异判定缺乏客观标准

#### Severity

P1

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

BLIND_SPOT

#### Location

Design Spec §6（风险与对策）第 3 行 + §4.3（双平台 symlink 安装）

#### Verification Gap

规格 §6 风险表第 3 行给出删除旧 `~/.claude/skills/yy-spec-review` 前的安全措施：

> 先 `diff -r` 旧拷贝与本地仓库，确认无未同步改动后再删

此指令存在以下验证缺口：

1. **"无未同步改动"未被客观定义**：`diff -r` 的输出可能包含数十甚至数百行差异——哪些差异是"可接受的历史差异"（如不同时间创建的产物文件），哪些是"需要保留的未同步改动"？规格未定义判定标准。
2. **无差异分类方法**：旧目录（7 月 20 日创建）与本地仓库（持续更新）之间必然存在差异（如新增的设计规格文件、修改的模板等），这些差异不一定是"需要保留的改动"——但没有客观标准区分。
3. **`diff -r` 的输出格式与解读规则未定义**：递归 diff 可能包含二进制文件、权限差异、时间戳差异等非内容差异，这些差异是否构成"未同步改动"未定义。
4. **验证通过/失败条件未定义**：`diff -r` 显示什么结果时可以安全删除？什么结果时需要暂停并人工介入？

#### Trigger Scenario

1. 前置条件：本地仓库已包含 7 月 20 日之后的多次修改（新增审核产物、修改 SKILL.md、新增设计规格等）
2. 动作：执行 `diff -r ~/.claude/skills/yy-spec-review /本地仓库路径`
3. 输出显示：47 个文件存在差异，包括新文件（本地仓库有旧目录无）、内容变更（如 SKILL.md 的 description 已更新）
4. 操作者无法从差异输出中判断：哪些差异是预期内的演进？哪些是需要先同步到旧目录的遗漏改动？
5. 两个不同操作者面对同一份 diff 输出可能做出不同决策（一个直接删除，一个尝试合并），无客观标准

#### Expected Verification

操作者应能确定：

- 旧目录中存在但本地仓库中不存在的文件清单（潜在丢失风险）
- 本地仓库中存在但旧目录中不存在的文件清单（预期差异，安全忽略）
- 两个位置均存在但内容不同的文件清单，以及差异是否属于"待保留的用户改动"还是"正常的版本演进"
- 一个明确的判定规则：满足什么条件时可以安全执行 `rm -rf`

#### Verification Method

无客观验证方法被定义。当前指令依赖操作者的主观判断。

#### Consequence

可能发生两种错误：
1. **假阴性（过度保守）**：操作者看到大量差异而不敢删除，旧 symlink 被替换后旧文件仍然占用磁盘，或两个 `spec-review` 入口同时存在导致 Claude Code 技能冲突
2. **假阳性（错误删除）**：操作者未识别出旧目录中有尚未提交到本地仓库的重要修改，删除后数据永久丢失

实际确认：当前旧目录（7 月 20 日创建）仍然存在（`ls` 确认），尺寸 352 字节，包含 `.superpowers/`、`.workbuddy/`、`docs/`、`SKILL.md` 等，与本地仓库的最新产品状态必然存在差异。此差异的判定风险是真实的。

#### Evidence

- Design Spec §6 风险表第 3 行：对策仅描述"先 `diff -r`"但未定义判定标准
- Design Spec §2.4：确认 "`~/.claude/skills/yy-spec-review/` 为 7 月 20 日的旧真实目录拷贝（非 symlink）"
- 实际环境验证：旧目录存在（实目录，非 symlink），本地仓库为非 git 仓库，两者内容必然有差异

#### Recommendation

1. 定义旧目录与本地仓库的差异分类规则，将差异分为三类：SAFE_TO_IGNORE（仅存在于本地仓库的新文件）、NEEDS_REVIEW（两处都存在但内容不同）、BLOCK_DELETION（仅存在于旧目录的文件）
2. 给出 `diff -r` 的具体命令和参数（建议 `diff -rq` 先列差异文件，再对可疑文件做内容 diff）
3. 定义明确的删除前置条件：NEEDS_REVIEW 和 BLOCK_DELETION 列表均为空时方可安全删除
4. 作为附加安全措施：建议在删除前先 `cp -r` 备份旧目录到 `/tmp`

#### Source References

* Design Spec §6 风险与对策表格第 3 行
* Design Spec §4.3 "双平台 symlink 安装"
* Design Spec §2.4 "环境就绪状态"

---

### TD-004 — Symlink 验证仅检查存在性而忽略目标可达性与内容完整性

#### Severity

P2

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

BLIND_SPOT

#### Location

Design Spec §5（验证清单）第 1-2 项

#### Verification Gap

验证清单第 1 项和第 2 项分别用 `ls -la ~/.claude/skills/spec-review` 和 `ls -la ~/.hermes/skills/software-development/spec-review` 验证 symlink。`ls -la` 命令在 symlink 目标不存在或不可访问时仍会成功显示 symlink 自身的信息（权限、链接目标路径、时间戳），并以颜色或箭头指示"断链"——但这种指示依赖终端颜色配置，不构成可程序化判定的客观验证。

此外，即使 symlink 目标路径存在，规格未验证：
1. 目标目录的内容完整性（如 `SKILL.md` 是否存在且可读）
2. 目标目录的权限是否允许技能系统读取
3. 两个平台的 symlink 是否确实指向同一份本地仓库（而非碰巧同名但内容不同的两个目录）

#### Trigger Scenario

1. 前置条件：Symlink 已按 §4.3 创建
2. 隐错条件：本地仓库路径被意外移动/删除/重命名，或路径中某级目录权限被收紧
3. 动作：执行 `ls -la ~/.claude/skills/spec-review`
4. 输出显示：`lrwxr-xr-x ... spec-review -> /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review`（断链指示器可能仅在彩色终端可见）
5. Claude Code 尝试加载技能时失败——但验证步骤已显示"通过"
6. 操作者在部署完成数天后才发现技能不可用

#### Expected Verification

测试者应能确定：

- Symlink 目标路径真实存在且为目录（而非意外指向文件）
- 目标目录中包含最小的技能入口文件（至少 `SKILL.md` 存在且可读）
- 两个平台的 symlink 目标 inode 相同（证明指向同一目录）或至少内容一致
- 目标目录的权限允许运行用户读取

#### Verification Method

当前仅验证 symlink 存在性，未验证目标可达性和内容完整性。以下等价验证未被定义：

```bash
# 验证目标可达且为目录
test -d ~/.claude/skills/spec-review/ && echo "OK"

# 验证关键文件存在
test -f ~/.claude/skills/spec-review/SKILL.md && echo "OK"

# 验证两平台指向同一目标
[ "$(readlink ~/.claude/skills/spec-review)" = \
  "$(readlink ~/.hermes/skills/software-development/spec-review)" ] && echo "OK"
```

#### Consequence

一个断开的 symlink 可能在部署验证阶段被误判为成功。此问题在生产中表现为技能在 Claude Code 或 Hermes 中不可用（不会出现在技能列表或无法触发），但由于"部署验证已通过"，排查方向可能偏离 symlink 问题，延长故障定位时间。

#### Evidence

- Design Spec §5 验证清单第 1 项：`ls -la ~/.claude/skills/spec-review` → 仅检查元数据
- Design Spec §5 验证清单第 2 项：`ls -la ~/.hermes/skills/software-development/spec-review` → 同上
- Design Spec §4.3 的 symlink 命令仅定义创建，未定义验证
- `ls -la` 对断链的行为：不会返回非零退出码，需要额外解析输出或使用 `test -d` 方可客观判断

#### Recommendation

将验证清单第 1-2 项拆分为：

1. Symlink 存在性：`test -L ~/.claude/skills/spec-review`（返回码可程序化判定）
2. 目标可达性：`test -d ~/.claude/skills/spec-review/`（末尾斜杠强制 dereference）
3. 关键内容完整性：`test -f ~/.claude/skills/spec-review/SKILL.md`
4. 双平台一致性（可选）：验证两个 symlink 指向同一 inode 或同一规范路径

对 Hermes symlink 同理拆分为可独立判定的验证项。

#### Source References

* Design Spec §5 验证清单第 1-2 项
* Design Spec §4.3 "双平台 symlink 安装"

---

### TD-005 — 改名后模板/协议间角色名称交叉引用的完整性无自动验证方法

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Finding Type

UNTESTABLE_REQUIREMENT

#### Location

Design Spec §4.1（改名策略）+ §5（验证清单）第 5 项

#### Verification Gap

规格 §4.1 定义了 4 组精确的字符串替换规则（`yy-spec-review` → `spec-review` 等），并规定验证方法为 `grep -rn "yy-"` 仅命中"不改"目录（§5 第 5 项）。

此验证仅覆盖 **遗漏替换**（false negative：应替换但未替换）。它不覆盖 **错误替换**（false positive：替换了但替换为目标值之外的错误值）和 **交叉引用漂移**（文件 A 中的角色名已更名，但文件 B 中对文件 A 角色的引用未同步更新）。具体场景：

1. 模板文件 `templates/product-review.md` 引用了 `yy-product-reviewer` 角色名，替换后变为 `product-reviewer`。但如果替换脚本出错，将 `yy-product-reviewer` 替换为 `product-reviewr`（拼写错误），新字符串不含 `yy-`，grep 验证通过但引用已断裂。
2. `CLAUDE.md` 中角色注释行（如 `product-reviewer.md # 产品审核员角色（product-reviewer）`）在替换后注释内容正确，但如果有路径引用如 `roles/product-reviewer.md`，而 frontmatter 中 name 被误改为 `product-reviewer-old`——grep 验证认为改名完成，但技能运行时加载的角色定义名称与模板/协议中的引用不一致。
3. `references/common.md` §1-§6 中多处使用角色名简称（如"Product"、"System"、"Test"），这些不包含 `yy-`，grep 无法验证它们与改名后的全量一致。

#### Trigger Scenario

1. 前置条件：按 §4.1 替换表在所有活文件中执行字符串替换
2. 隐错条件：某个替换因正则匹配过宽/过窄而产生错误的新值（如 `yy-product-reviewer` → `product-reviewr`），或某处引用（如 `CLAUDE.md` 中的路径注释）在替换后指向了不存在的角色名
3. 动作：执行 `grep -rn "yy-"` ——结果仅命中"不改"目录，验证判断为"通过"
4. 技能部署到 Claude Code / Hermes，尝试触发 `/spec-review`
5. 主 agent 尝试调度 subagent 时，发现角色定义文件中的 `name` 字段与期望的角色名不一致——调度失败
6. grep 验证无异常，问题被掩盖至首次实际使用

#### Expected Verification

测试者应能确定：

- 每个角色定义文件（`roles/product-reviewer.md`、`roles/system-critic.md`、`roles/test-designer.md`）的 frontmatter `name` 字段值与模板文件和 `CLAUDE.md` 中的引用是否一致
- `SKILL.md` frontmatter `name: spec-review` 与目录名（`spec-review`）、symlink 名（`spec-review`）是否一致
- 是否存在因搜索替换操作（如 sed 批量替换）产生的拼写错误或部分匹配错误

#### Verification Method

无自动验证方法被定义。以下验证未被规格包含：

1. 提取 `roles/*.md` frontmatter 中的 `name` 值，交叉比对 `CLAUDE.md` 和 `templates/*.md` 中的引用
2. 验证 `SKILL.md` 中 `name: spec-review` 与仓库目录名一致
3. 验证 `agents/openai.yaml` 中 `$spec-review`（替换后）不是空引用

#### Consequence

改名后的内部引用不一致可能在部署完成后才暴露。由于技能触发路径涉及多个文件的协同（SKILL.md name → 调度逻辑 → 角色定义 name → 模板引用），单点不一致即可能导致技能部分功能静默失败。最坏情况下，技能在 `/skills` 列表可见但触发后执行出错——用户感知为"技能有问题"而非"部署验证不完整"。

#### Evidence

- Design Spec §4.1 定义 4 组精确替换规则，但验证仅反向检查旧值残留
- Design Spec §5 验证清单第 5 项：仅检查 `yy-` 字符串是否仍存在于不该存在的文件中
- Design Spec §4.1 末尾声明 "Finding ID 前缀不变"——这表明规格意识到并非所有引用都受影响，但未将这一差异识别路径扩展到角色名的前向验证
- 实际 grep 确认：当前仓库中 `yy-` 引用遍布 13 个活源文件（SKILL.md、CLAUDE.md、README.md、roles/*.md、templates/*.md、references/common.md、update.sh、agents/openai.yaml），替换规模较大，人工逐文件验证容易遗漏

#### Recommendation

在验证清单中增加以下验证项：

1. 正向一致性检查：提取 `roles/*.md` 的 frontmatter `name` 值（应为 `product-reviewer`、`system-critic`、`test-designer`），确认与替换表的期望值一致
2. 关键引用检查：确认 `CLAUDE.md` 中引用的角色名与 `roles/*.md` 中定义的 name 一致
3. 入口名一致性：确认 `SKILL.md` 的 `name: spec-review` 与仓库目录名的 basename 一致

建议用简单脚本实现而非依赖人工逐行审查：
```bash
# 验证角色定义 name 值
grep -Po '^name: \K.*' roles/product-reviewer.md  # 期望: product-reviewer
grep -Po '^name: \K.*' roles/system-critic.md      # 期望: system-critic
grep -Po '^name: \K.*' roles/test-designer.md      # 期望: test-designer
grep -Po '^name: \K.*' SKILL.md                    # 期望: spec-review
```

#### Source References

* Design Spec §4.1 "改名策略" 替换规则表
* Design Spec §5 验证清单第 5 项
* Design Spec §3.1 "改名边界"

#### Reviewer Notes

本 Findings 的风险等级设定为 P2 而非 P1，原因是：如果严格按替换表的四个精确字符串执行搜索替换（全字匹配），错误替换的概率较低。但考虑到涉及 13 个文件且分散在不同目录层级，人工执行或简单 sed 替换确实存在出错可能。正向验证的缺失使这一风险无法被客观排除。

---

## Testability Coverage

| Verification Dimension                 | Status      | Finding IDs |
| -------------------------------------- | ----------- | ----------- |
| Happy Path Verification                | REVIEWED    | —           |
| Boundary and Limit Verification        | REVIEWED    | TD-001      |
| Duplicate and Idempotency Verification | REVIEWED    | TD-001      |
| Invalid Input Verification             | NOT_APPLICABLE | —        |
| Failure and Timeout Verification       | REVIEWED    | TD-001, TD-002 |
| Partial Failure Verification           | REVIEWED    | TD-001      |
| Data Integrity Verification            | REVIEWED    | TD-005      |
| State Transition Verification          | REVIEWED    | TD-001, TD-003 |
| Permission Boundary Verification       | NOT_APPLICABLE | —        |
| Backward Compatibility Verification    | REVIEWED    | TD-003      |
| Temporal Verification                  | REVIEWED    | TD-002      |
| Migration Verification                 | REVIEWED    | TD-003, TD-005 |
| External Dependency Verification       | REVIEWED    | TD-001, TD-002 |
| Observability Verification             | REVIEWED    | TD-002, TD-004 |
| Recovery Verification                  | REVIEWED    | TD-001, TD-003 |

不适用维度说明：

* **Invalid Input Verification**：此规格定义的是部署操作流程，不涉及用户输入处理。命令参数均为确定值，无"无效输入"概念。
* **Permission Boundary Verification**：此规格的操作均在同一用户（yuezhenhua）下执行，不涉及权限边界变更。GitHub 仓库权限（private）为固定声明，不构成可变权限边界。

---

## Unresolved Verification Questions

### Q-001 — Hermes backfill 机制对 symlink 部署技能的期望 lock.json 记录结构是什么？

#### Question

当 symlink 部署的技能被 Hermes 扫描并 backfill 时，`lock.json` 中生成的记录是否有确定的字段结构？`source` 字段值是什么（目前仅见 `"official"`）？`scan_verdict` 是否始终为 `"backfilled"`？

#### Why It Matters

验证清单第 3 项依赖 `lock.json` 作为验证来源之一，但未定义期望的记录结构。没有结构定义就无法编写验证脚本，也不能区分"backfill 失败"与"记录结构符合预期但尚未生成"。

#### Required Clarification

需要规格所有者或 Hermes 文档提供：symlink 部署技能的 backfill 记录结构定义，包括期望的字段名和值。

#### Status

OPEN

---

### Q-002 — Hermes skills 分类目录 `software-development` 是否已作为有效分类被 Hermes 识别？

#### Question

规格 §4.2 定义 `metadata.hermes.category: software-development`，§4.3 将 symlink 放入 `~/.hermes/skills/software-development/spec-review`。Hermes 是否已将 `software-development` 识别为有效分类目录？

#### Why It Matters

实际检查显示 `~/.hermes/skills/software-development/` 存在且包含 11 个其他技能（如 `requesting-code-review`、`systematic-debugging` 等），但没有直接证据表明 Hermes 的扫描器会识别新放入此目录的技能——现有技能可能是通过 Hermes 内置安装器而非 symlink 放入的。如果 Hermes 不识别新分类目录，symlink 放入后可能不会被扫描。

#### Required Clarification

Hermes 技能扫描器的目录发现机制：是否扫描所有 `~/.hermes/skills/<category>/` 下的子目录，还是仅跟踪已知分类？新创建的分类目录是否需要额外注册？

#### Status

OPEN

---

## Review Limitations

1. **Hermes 行为来源于规格自述而非独立验证**：本审核中关于 Hermes backfill 机制的结论依赖于规格 §2.2 的描述和 `lock.json` 中 yuanbao 技能的记录。未独立启动 Hermes 并观察 symlink 技能的发现过程。如果规格对 Hermes 机制的描述不完整或不准确，TD-002 的严重度可能需要上调为 P0。

2. **GitHub API 行为假设**：TD-001 中关于 `gh repo create --push` 可能部分失败的场景基于 GitHub API 的一般行为模式（创建仓库和推送是两个独立 API 调用）。未实际测试 `gh repo create` 在网络故障边界下的行为。

3. **改名文件数量基于 grep 快照**：TD-005 中的文件统计基于审核时的 `grep -rn "yy-"` 结果。如果在审核后到改名执行前有新增文件，改名范围可能扩大。

---

## Reviewer Conclusion

### Critical Testability Finding Count

* P0: 0
* P1: 3
* P2: 2

### Finding Type Breakdown

* Acceptance Tests: 0
* Untestable Requirements: 2
* Blind Spots: 3

### Review Result

REQUIRES_REVIEW

本审核识别出 3 个 P1 级验证缺口和 2 个 P2 级风险项。主要缺口集中在：(1) 实施步骤部分失败后的状态验证、(2) Hermes 技能发现的客观验证标准、(3) 旧目录清理前的安全判定标准。这些缺口在规格当前状态下无客观验证方法，均属于部署操作的关键路径，应在实施前予以解决。

测试设计师不确定 Findings 最终是被接受、拒绝、延迟还是以其他方式解决。

最终处置由 Decision Protocol 确定。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-07-review-001"
  reviewer: "yy-test-designer"
  review_type: "TEST_REVIEW"
  status: "COMPLETED"

findings:
  - id: "TD-001"
    severity: "P1"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "BLIND_SPOT"
    title: "实施步骤中途失败后仓库状态无客观验证方法"
    source_references:
      - "Design Spec §4.5 Git / GitHub 操作"
      - "Design Spec §4.7 实施顺序"
      - "Design Spec §6 风险与对策第5行"
    status: "PENDING_DECISION"

  - id: "TD-002"
    severity: "P1"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "UNTESTABLE_REQUIREMENT"
    title: "Hermes 技能发现验证存在'或'逻辑歧义与时机不可控"
    source_references:
      - "Design Spec §5 验证清单第3项"
      - "Design Spec §2.2 Hermes 技能机制"
    status: "PENDING_DECISION"

  - id: "TD-003"
    severity: "P1"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "BLIND_SPOT"
    title: "删除旧技能目录前的内容差异判定缺乏客观标准"
    source_references:
      - "Design Spec §6 风险与对策表格第3行"
      - "Design Spec §4.3 双平台 symlink 安装"
      - "Design Spec §2.4 环境就绪状态"
    status: "PENDING_DECISION"

  - id: "TD-004"
    severity: "P2"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "BLIND_SPOT"
    title: "Symlink 验证仅检查存在性而忽略目标可达性与内容完整性"
    source_references:
      - "Design Spec §5 验证清单第1-2项"
      - "Design Spec §4.3 双平台 symlink 安装"
    status: "PENDING_DECISION"

  - id: "TD-005"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    finding_type: "UNTESTABLE_REQUIREMENT"
    title: "改名后模板/协议间角色名称交叉引用的完整性无自动验证方法"
    source_references:
      - "Design Spec §4.1 改名策略替换规则表"
      - "Design Spec §5 验证清单第5项"
      - "Design Spec §3.1 改名边界"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "Hermes backfill 机制对 symlink 部署技能的期望 lock.json 记录结构是什么？"

  - id: "Q-002"
    status: "OPEN"
    question: "Hermes skills 分类目录 software-development 是否已作为有效分类被 Hermes 识别？"
```
