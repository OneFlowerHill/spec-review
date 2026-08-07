# Design Spec: spec-review 跨平台部署（Claude Code + Hermes）与 GitHub 推送

- **日期**: 2026-08-07
- **状态**: DRAFT（待规格所有者决策）
- **技能当前名**: yy-spec-review → **目标名**: spec-review
- **目标仓库**: `https://github.com/OneFlowerHill/spec-review`（私有）

---

## 1. 背景与目标

`yy-spec-review` 是一套基于 Claude Code Skill 的设计规格多视角审核方法论框架。当前分发走用友内部 git（`git@git.yyrd.com:yyit/yy-spec-review.git`），仅面向 Claude Code。

本设计目标：

1. **兼容性**：确认并实现该技能同时支持 Claude Code 与 Hermes（Nous Research 自进化 agent，兼容 agentskills.io 开放标准）。
2. **symlink 安装**：Claude Code 与 Hermes 的技能目录通过 symlink 指向同一份本地仓库，两平台共用单一代码源。
3. **GitHub 推送**：在用户个人 GitHub 账号（`OneFlowerHill`）下创建私有仓库 `spec-review` 并推送。
4. **改名**：活技能源文件全面去除 `yy-` 前缀，统一为 `spec-review` / `product-reviewer` / `system-critic` / `test-designer`，与 goal-manager 范例对齐（仓库名 = 技能 name = 目录名，无命名空间前缀）。历史快照与瘦身工具链保留原命名，见 §3.1。

---

## 2. 现状调研结论（兼容性）

### 2.1 格式兼容

- Claude Code 与 Hermes 均以 `SKILL.md` + YAML frontmatter 为技能入口，目录结构（`SKILL.md` + `references/` + `templates/`）兼容。
- **同一份本地仓库可被两个平台同时通过 symlink 引用**，无需平台分支。

### 2.2 Hermes 技能机制

- 技能目录：`~/.hermes/skills/<category>/<skill-name>/`（按分类组织），与 Claude Code 的扁平 `~/.claude/skills/<name>/` 不同。
- frontmatter 可选增强字段：`platforms`、`metadata.hermes.tags`、`metadata.hermes.category`（用于 `/skills` 浏览分类与关联推荐）。缺少不影响功能，仅影响浏览体验。
- **技能发现机制（区分两类，CR-002 修正）**：
  - **目录技能**：Hermes 扫描 skills 目录，对未注册的真实目录技能自动 backfill 到 `~/.hermes/skills/.hub/lock.json`（`yuanbao` 即 `scan_verdict: backfilled` 证据，但它是根目录真实目录、来自官方 optional-skills，非 symlink）。
  - **symlink 技能**：参照范例 `goal-manager` 是 `productivity/` 分类子目录下的 symlink 且在 Hermes 中正常工作（`/skills` 可见、可触发），**证明分类子目录下的 symlink 技能可被发现**。但 `goal-manager` 不在 `lock.json` 的 installed 映射中——**symlink 技能可能通过实时扫描发现，未必持久化到 lock.json**。
- **结论**：不以 `lock.json` 作为 symlink 技能注册的可靠凭证；以 `/skills` 实际列出 + 功能可用为权威验证信号（见 §5）。回退方案见 §6。

### 2.3 参考范例：goal-manager

用户已用 goal-manager 技能完成同款跨平台部署，作为本设计的直接参照：

| 维度 | goal-manager 现状 |
|---|---|
| 本地仓库 | `/Users/yuezhenhua/yonyou/projects/0__AI/skills/goal-manager` |
| GitHub | `https://github.com/OneFlowerHill/goal-manager.git`（HTTPS） |
| Claude symlink | `~/.claude/skills/goal-manager -> 本地仓库` |
| Hermes symlink | `~/.hermes/skills/productivity/goal-manager -> 本地仓库` |
| frontmatter | `platforms: [macos,linux,windows]` + `metadata.hermes.{tags, category}` |
| .gitignore | `.DS_Store / __pycache__/ / *.pyc / .claude/ / .superpowers/` |

### 2.4 环境前置条件清单（CR-005）

部署前必须逐项验证，任一不满足则按"处理策略"处置后再继续：

| # | 前置条件 | 验证命令 | 不满足时处理 |
|---|---|---|---|
| 1 | GitHub CLI 已认证 | `gh auth status` | 报错终止，先 `gh auth login` |
| 2 | token 有 repo 权限 | `gh auth status`（scopes 含 `repo`） | 报错终止 |
| 3 | Hermes 已安装 | `command -v hermes` | 报错终止，先安装 Hermes |
| 4 | Hermes 分类目录存在 | `ls -d ~/.hermes/skills/software-development/` | `mkdir -p ~/.hermes/skills/software-development/` |
| 5 | Claude 目标名未占用 | `test ! -e ~/.claude/skills/spec-review` | 已存在则提示确认后删除/重命名 |
| 6 | Hermes 目标名未占用 | `test ! -e ~/.hermes/skills/software-development/spec-review` | 已存在则提示确认后删除/重命名 |
| 7 | 项目非 git 仓库（首推） | `git rev-parse --is-inside-work-tree`（应失败） | 若已是 git 仓库，按既有 remote 处理 |

补充事实：
- 已认证账号 `OneFlowerHill`，token scopes 含 `repo`。
- `~/.claude/skills/yy-spec-review/` 为 7 月 20 日旧真实目录拷贝（非 symlink），需替换（见 §4.7 步骤 8）。
- 敏感内容扫描：源文件中无真实 token/密钥（命中的 "secret"/"token" 均为审核维度与计量文字）。

---

## 3. 范围与边界

### 3.1 改名边界

**改（活技能源文件）**：技能运行时实际加载的文件，去除 `yy-` 前缀。

**不改（历史与锁定快照）**：改名即篡改历史或破坏基线语义，保留原样。

| 类别 | 路径 | 不改理由 |
|---|---|---|
| 瘦身工具链（锁定） | `scripts/**`（`baseline_snapshot/`、`prompt_scope.json`、`token_analyzer.py`） | 瘦身工程的基线锚点与计量工具，内部自洽引用 `yy-spec-review` 历史命名；改名会破坏基线-工具一致性 |
| 历史审核产物 | `docs/superpowers/reviews/**` | 历史审核记录，反映当时技能状态 |
| 历史计划/设计 | `docs/superpowers/plans/**`、`docs/superpowers/specs/*-design.md`（旧） | 过去的设计与计划文档，历史记录 |
| 工作记忆/产物 | `.workbuddy/`、`.superpowers/` | 工作日记与 sdd 工作流产物，历史快照 |

> 一致性目标：改名后 `grep -rn "yy-"` 仅命中上述"不改"目录。

### 3.2 推送内容边界

遵循规格所有者"全部推送（私有）"决策：

- **入仓**：全部技能源文件 + `docs/`（含内部审查报告）+ `.workbuddy/` + `.superpowers/`。
- **不入仓**（.gitignore）：纯本地状态——`.DS_Store`、`__pycache__/`、`*.pyc`、`.claude/`。
- **风险提示**：`docs/项目一期|二期审查报告.md`、`.superpowers/sdd/review-*.diff` 含用友内部审核与代码内容，将进入个人 GitHub 私有仓库。规格所有者已确认可接受。

---

## 4. 设计详述

### 4.1 改名策略

**替换规则**（活文件全局适用）：

| 原值 | 新值 |
|---|---|
| `yy-spec-review` | `spec-review` |
| `yy-product-reviewer` | `product-reviewer` |
| `yy-system-critic` | `system-critic` |
| `yy-test-designer` | `test-designer` |

**待改文件清单**（含命中点数）：

| 文件 | 改动点 |
|---|---|
| `SKILL.md` | frontmatter `name`；description 内 `/yy-spec-review` |
| `CLAUDE.md` | 角色名注释（3 处）；历史记录行 `name: yy-spec-review` |
| `README.md` | 标题、介绍、目录树角色名（3）、`git clone` 地址、更新触发词（共 8 处） |
| `update.sh` | 注释与 echo（3 处） |
| `roles/product-reviewer.md` | frontmatter `name` |
| `roles/system-critic.md` | frontmatter `name` |
| `roles/test-designer.md` | frontmatter `name` |
| `templates/product-review.md` | 角色名（2 处） |
| `templates/system-review.md` | 角色名（2 处） |
| `templates/test-review.md` | 角色名（2 处） |
| `templates/consolidated-review.md` | 角色名（9 处） |
| `references/common.md` | "yy-spec-review skill" 描述 |
| `agents/openai.yaml` | `default_prompt` 内 `$yy-spec-review` |

**不改清单**：见 §3.1 表格（含 `scripts/**` 瘦身工具链：`baseline_snapshot/`、`prompt_scope.json`、`token_analyzer.py`，整体保留 `yy-` 历史命名以维持基线-工具自洽）。

**Finding ID 前缀不变**：`PR-` / `SC-` / `TD-` / `CR-` 是 Finding 标识，与技能命名解耦，不受本次改名影响。

### 4.2 SKILL.md frontmatter 适配

两平台共用同一份 `SKILL.md`，新增 `platforms` 与 `metadata.hermes`：

```yaml
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
```

`metadata.hermes.category: software-development` 决定 Hermes 分类目录位置（与 hermes 自带的 `requesting-code-review`、`simplify-code` 同类）。

### 4.3 双平台 symlink 安装

本地仓库**保持原位**：`/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review`（与 goal-manager 同级，路径不变）。

```bash
# Claude Code：删旧拷贝，建 symlink
rm -rf ~/.claude/skills/yy-spec-review
ln -s /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review \
      ~/.claude/skills/spec-review

# Hermes：建 symlink（scan+backfill 自动注册）
ln -s /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review \
      ~/.hermes/skills/software-development/spec-review
```

两平台 symlink 均指向同一本地仓库，修改一处两平台同步生效。

### 4.4 .gitignore（新建）

仿 goal-manager，仅忽略纯本地状态；遵循"全部推送"意愿，保留 `.workbuddy/`、`.superpowers/`、`docs/` 入仓：

```
.DS_Store
__pycache__/
*.pyc
.claude/
```

### 4.5 Git / GitHub 操作（CR-003：拆分步骤 + 检查点）

`git init` 已在 §4.7 步骤 0 提前执行。此处为仓库创建与推送，拆分为可独立观察的步骤：

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
# 前置检查：目标仓库名未冲突
gh repo view OneFlowerHill/spec-review 2>/dev/null \
  && { echo "仓库已存在，需先删除或改名"; exit 1; } || echo "名称可用"
# 创建仓库（不含 --push，便于隔离失败）
gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin
# 推送
git push -u origin main
```

可验证检查点：
- `git log --oneline` 显示首提交、`git status` clean（commit 完成标志）
- `gh repo view OneFlowerHill/spec-review` 成功（仓库创建标志）
- `git remote -v` 显示 origin 指向 GitHub HTTPS
- `git ls-remote origin main` 返回提交 SHA（推送完成标志）

部分失败恢复（见 §6）：仓库已创建但推送失败 → `git push -u origin main` 重试；名称冲突 → `gh repo delete OneFlowerHill/spec-review --yes` 后重试或改名；remote 未设置 → `git remote add origin https://github.com/OneFlowerHill/spec-review.git`。

### 4.6 update.sh / README（CR-006：认证变更 + 迁移指南）

- **update.sh**：逻辑不变（`git fetch origin` + `git merge --ff-only origin/<branch>`），仅改注释与 echo 内的 `yy-spec-review → spec-review`。
- **认证方式变更**：origin 从 SSH（`git@git.yyrd.com`）切换到 HTTPS（`github.com`）。部署后执行 `gh auth setup-git` 配置 git credential helper 使用 gh token，确保 `update.sh` 的 `git fetch` 在 HTTPS 下认证可用。
- **README.md**：
  - 安装段 `git clone git@git.yyrd.com:yyit/yy-spec-review.git` → `git clone https://github.com/OneFlowerHill/spec-review.git`
  - 更新触发词 `更新 yy-spec-review` → `更新 spec-review`
  - 新增"已有用户迁移指南"：旧 clone 副本执行 `git remote set-url origin https://github.com/OneFlowerHill/spec-review.git`
- **agents/openai.yaml**：保留（多平台接口文件，无理由删除），仅改 `$yy-spec-review → $spec-review`。

### 4.7 实施顺序（CR-001 + CR-004 修订）

0. **`git init` + `git branch -M main`**（提前，为改名提供版本控制安全网，可 `git diff`/`git checkout` 回退）
1. 改名（§4.1 活文件去 `yy-`，建议 `sed` 脚本化替换）
2. **grep 验证门 1**（CR-004）：`grep -rn "yy-"` 在活源文件中应为 0 命中（仅历史/快照目录命中）；正向一致性检查——`SKILL.md` 的 `name` = `spec-review`、`roles/*.md` 的 `name` = `product-reviewer`/`system-critic`/`test-designer`；对 §3.1"不改"目录专项 `git diff` 确认无意外修改。未通过则 `git checkout .` 回退改名后重做。
3. frontmatter 适配（§4.2）
4. 创建 `.gitignore`（§4.4）
5. 更新 README clone 地址、update.sh 注释、`gh auth setup-git` 提示（§4.6）
6. `git add -A` + `git commit`（检查点：`git log --oneline` 有首提交、`git status` clean）
7. `gh repo view` 前置检查名称冲突 → `gh repo create --private --source=. --remote=origin` → `git push -u origin main`（检查点：`gh repo view` 成功、`git ls-remote origin main` 返回 SHA）（§4.5）
8. **旧目录安全迁移（CR-001）**：
   - 8a. `diff -rq ~/.claude/skills/yy-spec-review/ <本地仓库>`，按 SAFE_TO_IGNORE（仅本地仓库新增）/ NEEDS_REVIEW（两处都有但内容不同）/ BLOCK_DELETION（仅旧目录有）分类；NEEDS_REVIEW 与 BLOCK_DELETION 均空方可继续，否则先合并/备份。
   - 8b. `mv ~/.claude/skills/yy-spec-review ~/.claude/skills/.yy-spec-review.bak.20260807`（以 `mv` 替代 `rm`，保留数据可回滚）
9. 建 symlink：`ln -s <本地仓库> ~/.claude/skills/spec-review` 与 `ln -s <本地仓库> ~/.hermes/skills/software-development/spec-review`（§4.3）。若 `ln -s` 失败，从 8b 备份 `mv` 回退。
10. **grep 验证门 2 + 完整验证（§5）**

改名与 .gitignore 必须先于首个 commit，确保仓库首提交即为干净的目标状态。步骤 0 提前 `git init` 使改名有 git 安全网。

---

## 5. 验证清单

**Symlink 验证（CR-008，可程序化判定）**：
- [ ] 存在性：`test -L ~/.claude/skills/spec-review` && `test -L ~/.hermes/skills/software-development/spec-review`
- [ ] 目标可达性：`test -d ~/.claude/skills/spec-review/` && `test -d ~/.hermes/skills/software-development/spec-review/`
- [ ] 关键内容完整性：`test -f ~/.claude/skills/spec-review/SKILL.md`（Hermes 侧同理）
- [ ] 双平台一致性：`[ "$(readlink ~/.claude/skills/spec-review)" = "$(readlink ~/.hermes/skills/software-development/spec-review)" ]`

**Hermes 发现验证（CR-002，主信号 = 功能可用）**：
- [ ] 主信号：Hermes 启动后 `/skills` 列出 spec-review，且 `/spec-review` 可触发
- [ ] 辅助信号（可选）：`~/.hermes/skills/.hub/lock.json` 出现 spec-review 记录（symlink 技能可能不写入，缺此记录不判失败）

**Claude Code 验证**：
- [ ] `/spec-review` 可触发识别

**改名一致性验证（CR-004）**：
- [ ] `grep -rn "yy-"` 仅命中"不改"目录（`scripts/baseline_snapshot/`、`scripts/prompt_scope.json`、`scripts/token_analyzer.py`、`docs/superpowers/{reviews,plans,specs(旧)}`、`.workbuddy/`、`.superpowers/`）；**新规格设计文档（本文件）含 `yy-` 引用属预期**（描述改名），不计为失败
- [ ] 正向一致性：`grep -Po '^name: \K.*' SKILL.md` = `spec-review`；`roles/*.md` 的 name = `product-reviewer`/`system-critic`/`test-designer`

**Git/GitHub 验证（CR-003）**：
- [ ] `git log --oneline` 显示首提交，`git status` clean
- [ ] `gh repo view OneFlowerHill/spec-review` 显示 private、含 main 分支
- [ ] `git remote -v` → origin 为 `https://github.com/OneFlowerHill/spec-review.git`
- [ ] `git ls-remote origin main` 返回提交 SHA

**update.sh 验证（CR-006）**：
- [ ] `gh auth setup-git` 已执行（git credential helper 配置）
- [ ] `bash update.sh` 在已是最新时输出"已是最新版本"（验证 HTTPS 认证可达）

---

## 6. 风险与对策

| 风险 | 对策 |
|---|---|
| 改名遗漏/误改导致 name 与目录/symlink 不一致（CR-004） | 步骤 2 grep 验证门 1 + 正向一致性检查（frontmatter name 交叉比对）；`sed` 脚本化替换；对"不改"目录专项 diff |
| Hermes 不识别分类子目录下 symlink 技能（CR-002） | goal-manager 已是分类子目录 symlink 先例（可发现）；不以 lock.json 为凭证，以 `/skills`+功能可用为主信号；回退：symlink 移至 `~/.hermes/skills/` 根目录，或手动编辑 lock.json |
| 旧目录删除丢失本地独有改动（CR-001） | 步骤 8a `diff -rq` 分类判定（BLOCK_DELETION/NEEDS_REVIEW 均空方可继续）；步骤 8b 以 `mv` 替代 `rm` 移至备份目录，可回滚 |
| `gh repo create` 部分失败/名称冲突（CR-003） | 步骤 7 前置 `gh repo view` 检查冲突；拆分 create 与 push，每步检查点；恢复：`gh repo delete` 后重试，或 `git remote add origin <url>` + `git push -u origin main` |
| update.sh HTTPS 认证失败（CR-006） | `gh auth setup-git` 配置 credential helper；旧 clone 副本用 `git remote set-url` 迁移 |
| 内部内容进入个人 GitHub | 仓库私有；规格所有者已确认；.gitignore 排除纯本地状态 |
| 并发读取竞态（CR-007，已知限制） | update.sh 的 `git merge` 与平台扫描器存在极低概率并发读取窗口；建议低使用时段执行 `git pull`；文件规模显著增长时重新评估。不引入锁定机制（避免过度工程） |

---

## 7. 不在范围内

- 不修改技能的审核方法论、协议、角色边界、模板结构（仅改名与 frontmatter 适配）。
- 不处理 `scripts/baseline_snapshot/` 与历史审核/设计产物（保留原样）。
- 不为 openai.yaml 适配新的平台接口（仅改名保留）。
- 不设置 GitHub Actions、CI、release 等仓库自动化（YAGNI）。
- 不迁移 issue/历史（首次推送，无历史可迁）。
