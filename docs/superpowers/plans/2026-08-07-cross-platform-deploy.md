# spec-review 跨平台部署实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 yy-spec-review 技能改名为 spec-review，通过双 symlink 同时部署到 Claude Code 与 Hermes，并推送至 GitHub 私有仓库 OneFlowerHill/spec-review。

**Architecture:** 本地仓库 `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review` 保持原位；`~/.claude/skills/spec-review` 与 `~/.hermes/skills/software-development/spec-review` 两个 symlink 均指向该仓库。GitHub 远程 `https://github.com/OneFlowerHill/spec-review.git`（私有，HTTPS）。两平台共用同一份 `SKILL.md`（frontmatter 含 `platforms` + `metadata.hermes`）。

**Tech Stack:** Git、GitHub CLI（`gh`）、POSIX shell（`sed`/`grep`/`test`/`ln`/`mv`/`diff`）、macOS。无运行时代码（纯 Markdown 技能框架）。

## Global Constraints

- **仓库名**：`spec-review`（私有），GitHub 账号 `OneFlowerHill`，HTTPS。
- **技能 name**：`spec-review`；**角色 name**：`product-reviewer` / `system-critic` / `test-designer`（全部去 `yy-` 前缀）。
- **Finding ID 前缀不变**：`PR-` / `SC-` / `TD-` / `CR-` 是 Finding 标识，与技能命名解耦，**不改**。
- **不改目录**（锁定，禁止 sed 触及）：`scripts/baseline_snapshot/`、`scripts/prompt_scope.json`、`scripts/token_analyzer.py`、`docs/superpowers/reviews/`、`docs/superpowers/plans/`（旧）、`docs/superpowers/specs/`（旧设计）、`.workbuddy/`、`.superpowers/`。
- **.gitignore**：`.DS_Store` / `__pycache__/` / `*.pyc` / `.claude/`。其余（含 `docs/` 审查报告、`.workbuddy/`、`.superpowers/`）入仓。
- **首提交即干净目标状态**：所有改名/frontmatter/.gitignore/README 改动先于首个 commit（规格 §4.7）。
- **本地仓库路径**：`/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review`（原位不动）。
- **commit message 格式**：`type[scope]: <description>`，末尾附 `Co-Authored-By: Claude <noreply@anthropic.com>`。

---

## File Structure

| 文件 | 责任 | 操作 |
|---|---|---|
| `SKILL.md` | 技能入口（frontmatter + 4 Phase 流程） | 改名 + frontmatter 适配 |
| `CLAUDE.md` | 项目指导 | 改名 |
| `README.md` | 文档与安装说明 | 改名 + clone URL + 迁移指南 |
| `update.sh` | 自更新脚本 | 改名（注释/echo） |
| `roles/*.md`（3） | 角色定义 | 改名（frontmatter name） |
| `templates/*.md`（4） | 输出模板 | 改名（角色名引用） |
| `references/common.md` | 共享权威定义 | 改名（描述） |
| `agents/openai.yaml` | 多平台接口 | 改名（`$yy-spec-review`） |
| `.gitignore` | 忽略纯本地状态 | 创建 |

---

## Task 1: 前置条件验证 + git init + .gitignore

**Files:**
- Create: `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/.gitignore`
- Init: `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/.git`

**Interfaces:**
- Consumes: 规格§2.4 前置条件清单
- Produces: 已初始化的 git 仓库 + `.gitignore`

- [ ] **Step 1: 验证 7 项前置条件**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
gh auth status                                      # 1+2: 已认证 + repo scope
command -v hermes                                   # 3: hermes 已安装
ls -d ~/.hermes/skills/software-development/        # 4: 分类目录存在
test ! -e ~/.claude/skills/spec-review && echo "claude name free"      # 5
test ! -e ~/.hermes/skills/software-development/spec-review && echo "hermes name free"  # 6
git rev-parse --is-inside-work-tree 2>&1 | grep -q "not a git" && echo "not a repo"  # 7
```

Expected: 全部命令成功输出（条件 7 应输出 "not a repo"）。任一失败则先按规格§2.4"处理策略"处置。

- [ ] **Step 2: git init + 主分支命名**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git init
git branch -M main
```

Expected: `Initialized empty Git repository in .../spec-review/.git/`

- [ ] **Step 3: 创建 .gitignore**

```bash
cat > /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/.gitignore <<'EOF'
.DS_Store
__pycache__/
*.pyc
.claude/
EOF
```

- [ ] **Step 4: 验证 .gitignore 生效（.DS_Store 被忽略）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git status --short | grep -q "\.DS_Store" && echo "FAIL: .DS_Store tracked" || echo "OK: .DS_Store ignored"
git status --short | head -5
```

Expected: `OK: .DS_Store ignored`；`git status --short` 列出待 add 的源文件（不含 .DS_Store）。

（本任务不 commit——改名等改动先于首提交，见 Task 5。）

---

## Task 2: 改名（去 yy- 前缀）+ grep 验证门 1

**Files:**
- Modify: `SKILL.md`, `CLAUDE.md`, `README.md`, `update.sh`, `roles/{product-reviewer,system-critic,test-designer}.md`, `templates/{product,system,test,consolidated}-review.md`, `references/common.md`, `agents/openai.yaml`

**Interfaces:**
- Consumes: 规格§4.1 替换规则
- Produces: 活源文件中 `yy-` 前缀清零

- [ ] **Step 1: 写验证（改名前 grep 应非零命中）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -rn "yy-" SKILL.md CLAUDE.md README.md update.sh \
  roles/product-reviewer.md roles/system-critic.md roles/test-designer.md \
  templates/product-review.md templates/system-review.md templates/test-review.md templates/consolidated-review.md \
  references/common.md agents/openai.yaml
```

Expected: 多行命中（`yy-spec-review` / `yy-product-reviewer` 等）。这是"未满足"基线。

- [ ] **Step 2: sed 批处理替换（4 个映射，仅活文件）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
sed -i '' 's/yy-spec-review/spec-review/g; s/yy-product-reviewer/product-reviewer/g; s/yy-system-critic/system-critic/g; s/yy-test-designer/test-designer/g' \
  SKILL.md CLAUDE.md README.md update.sh \
  roles/product-reviewer.md roles/system-critic.md roles/test-designer.md \
  templates/product-review.md templates/system-review.md templates/test-review.md templates/consolidated-review.md \
  references/common.md agents/openai.yaml
```

Expected: 无输出（sed 成功）。**注意：sed 文件列表严格限定为活文件，不含 `scripts/`、`docs/superpowers/`、`.workbuddy/`、`.superpowers/`。**

- [ ] **Step 3: grep 验证门 1——活源文件 0 命中**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -rn "yy-" SKILL.md CLAUDE.md README.md update.sh \
  roles/product-reviewer.md roles/system-critic.md roles/test-designer.md \
  templates/product-review.md templates/system-review.md templates/test-review.md templates/consolidated-review.md \
  references/common.md agents/openai.yaml
```

Expected: 无输出（0 命中）。若有命中，定位遗漏处手动修正后重跑 Step 3。

- [ ] **Step 4: 正向一致性检查（frontmatter name 期望值）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
echo "SKILL.md:        $(grep -Po '^name: \K.*' SKILL.md)"
echo "product-reviewer: $(grep -Po '^name: \K.*' roles/product-reviewer.md)"
echo "system-critic:    $(grep -Po '^name: \K.*' roles/system-critic.md)"
echo "test-designer:    $(grep -Po '^name: \K.*' roles/test-designer.md)"
```

Expected:
```
SKILL.md:        spec-review
product-reviewer: product-reviewer
system-critic:    system-critic
test-designer:    test-designer
```
任一不符则该文件 frontmatter 残留，回 Step 2 检查 sed 是否漏该文件。

- [ ] **Step 5: 对"不改"目录专项检查——确认 sed 未误伤**

首次 commit 前无 git 基线可比（`git diff` 对未跟踪文件无输出），改用 grep 确认"不改"目录仍保留 `yy-`（若 sed 误伤，这些文件的 `yy-` 会被替换为 `spec-`）：

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
echo "baseline_snapshot/SKILL.md: $(grep -c 'yy-' scripts/baseline_snapshot/SKILL.md)"
echo "prompt_scope.json:          $(grep -c 'yy-' scripts/prompt_scope.json)"
echo "token_analyzer.py:          $(grep -c 'yy-' scripts/token_analyzer.py)"
echo "baseline_snapshot/roles:    $(grep -rl 'yy-' scripts/baseline_snapshot/roles/ | wc -l | tr -d ' ')"
echo "docs/superpowers/reviews:   $(grep -rl 'yy-' docs/superpowers/reviews/ | wc -l | tr -d ' ')"
```

Expected: 各项计数 > 0（这些"不改"文件/目录保留 `yy-` 前缀，证明 sed 未触及）。若某项为 0，说明 sed 误伤该目录，需从用友内部 git（`git@git.yyrd.com:yyit/yy-spec-review.git`）或备份恢复后重做 Step 2。

（本任务不 commit——累积到 Task 5 首提交。）

---

## Task 3: SKILL.md frontmatter 适配（platforms + metadata.hermes）

**Files:**
- Modify: `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/SKILL.md`（frontmatter 区块）

**Interfaces:**
- Consumes: 规格§4.2 frontmatter 模板
- Produces: SKILL.md frontmatter 含 `platforms` 与 `metadata.hermes.{tags,category}`

- [ ] **Step 1: 写验证（适配前 frontmatter 无 platforms/metadata.hermes）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
awk '/^---$/{c++; next} c==1' SKILL.md | grep -E "platforms|metadata:|hermes:" || echo "FAIL: not adapted yet"
```

Expected: `FAIL: not adapted yet`（当前 frontmatter 仅有 name + description）。

- [ ] **Step 2: 在 frontmatter 末尾追加 platforms + metadata.hermes**

用 Edit 工具，将 SKILL.md frontmatter 的结束 `---`（第一个）替换为含新字段的版本。当前 frontmatter 结束处：

```
  a review would be helpful. The agent never initiates this skill on its own.
---
```

改为：

```
  a review would be helpful. The agent never initiates this skill on its own.
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [review, spec, design, qa, multi-perspective, audit]
    category: software-development
---
```

- [ ] **Step 3: 验证 frontmatter 适配**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
awk '/^---$/{c++; next} c==1' SKILL.md | grep -E "platforms|category: software-development"
```

Expected:
```
platforms: [macos, linux, windows]
    category: software-development
```

（本任务不 commit——累积到 Task 5。）

---

## Task 4: README clone URL + 迁移指南 + update.sh / openai.yaml 确认

**Files:**
- Modify: `/Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/README.md`（安装段）
- Verify: `update.sh`、`agents/openai.yaml`（已被 Task 2 sed 改名）

**Interfaces:**
- Consumes: 规格§4.6
- Produces: README clone 指向 GitHub HTTPS + 迁移指南

- [ ] **Step 1: 写验证（README 仍含内部 git URL）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -n "git.yyrd.com" README.md
```

Expected: 命中 `git clone git@git.yyrd.com:yyit/spec-review.git`（Task 2 已把 yy-spec-review→spec-review，但 SSH 域名未改）。

- [ ] **Step 2: 用 Edit 替换 README 安装段 clone URL**

old_string（README 安装段）:
```
git clone git@git.yyrd.com:yyit/spec-review.git
```
new_string:
```
git clone https://github.com/OneFlowerHill/spec-review.git
```

- [ ] **Step 3: 用 Edit 在 README 安装段后追加"已有用户迁移指南"**

在 README 的"### 更新"小节末尾追加（Edit 插入）：

```
### 已有用户迁移指南

若你之前从用友内部 git（`git@git.yyrd.com`）clone 过本技能，部署迁移到 GitHub 后，在旧 clone 副本执行：

```bash
git remote set-url origin https://github.com/OneFlowerHill/spec-review.git
gh auth setup-git   # 配置 git credential helper 使用 gh token（HTTPS 认证）
```
```

- [ ] **Step 4: 验证 README URL 已改 + 迁移指南存在**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -q "github.com/OneFlowerHill/spec-review.git" README.md && echo "OK: clone URL" || echo "FAIL"
grep -q "已有用户迁移指南" README.md && echo "OK: migration guide" || echo "FAIL"
grep -q "git.yyrd.com" README.md && echo "FAIL: internal URL remains" || echo "OK: no internal URL"
```

Expected: 三行 `OK`。

- [ ] **Step 5: 确认 update.sh 与 agents/openai.yaml 已被 sed 正确改名**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -n "yy-" update.sh agents/openai.yaml && echo "FAIL: residual yy-" || echo "OK: no yy-"
grep -n "spec-review" update.sh | head -3
grep -n '\$spec-review' agents/openai.yaml
```

Expected: `OK: no yy-`；update.sh 含 `spec-review`；agents/openai.yaml 含 `$spec-review`。

（本任务不 commit——累积到 Task 5。）

---

## Task 5: 首次 commit（首提交即干净目标状态）

**Files:**
- Stage: 全部活源文件 + `.gitignore` + `docs/`（含审查报告）+ `.workbuddy/` + `.superpowers/`（按规格§3.2 全部入仓）

**Interfaces:**
- Consumes: Task 1–4 全部改动
- Produces: 仓库首提交（干净目标状态）

- [ ] **Step 1: git add -A**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git add -A
```

- [ ] **Step 2: 验证暂存区干净（.DS_Store 等被忽略；改名文件就绪）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git status --short | grep -E "\.DS_Store|\.claude/" && echo "FAIL: ignored files staged" || echo "OK: no ignored files"
git diff --cached --stat | tail -3
```

Expected: `OK: no ignored files`；`git diff --cached --stat` 显示大量文件 staged（含改名后的 SKILL.md 等）。

- [ ] **Step 3: 首次 commit**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git commit -m "chore: initial commit, cross-platform spec-review skill

Renamed from yy-spec-review to spec-review (removed yy- prefix from
skill name and role names). Added platforms + metadata.hermes frontmatter.
Dual symlink deploy to Claude Code + Hermes. GitHub remote.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Expected: `[main (root-commit) ...] chore: initial commit...`

- [ ] **Step 4: 验证首提交存在 + 工作区 clean**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git log --oneline
git status --short
```

Expected: `git log` 显示 1 条提交；`git status --short` 无输出（clean）。

---

## Task 6: GitHub 推送（拆分 create + push + 检查点）

**Files:**
- Remote: `https://github.com/OneFlowerHill/spec-review.git`（私有）

**Interfaces:**
- Consumes: 规格§4.5
- Produces: GitHub 私有仓库 + origin remote + 推送完成

- [ ] **Step 1: 配置 git HTTPS 认证（CR-006）**

```bash
gh auth setup-git
```

Expected: 无错误输出（配置 git credential helper 使用 gh token）。

- [ ] **Step 2: 前置检查——目标仓库名未冲突（CR-003）**

```bash
gh repo view OneFlowerHill/spec-review 2>/dev/null && echo "EXISTS: need to handle" || echo "AVAILABLE"
```

Expected: `AVAILABLE`。若 `EXISTS`：需用户决策删除旧仓库（`gh repo delete OneFlowerHill/spec-review --yes`）或改名后重试。

- [ ] **Step 3: 创建私有仓库 + 设置 origin（不含 --push）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
gh repo create OneFlowerHill/spec-review --private --source=. --remote=origin
```

Expected: `✓ Created repository OneFlowerHill/spec-review on github.com` + `✓ Added remote ...origin...`

- [ ] **Step 4: 验证仓库创建 + origin 设置（检查点）**

```bash
gh repo view OneFlowerHill/spec-review --json visibility,name -q '.name + " " + .visibility'
git remote -v
```

Expected: `spec-review PRIVATE`；`git remote -v` 显示 `origin https://github.com/OneFlowerHill/spec-review.git`。

- [ ] **Step 5: 推送**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git push -u origin main
```

Expected: `* [new branch] main -> main` + `Branch 'main' set up to track 'origin/main'`。

- [ ] **Step 6: 验证推送完成（检查点）**

```bash
git ls-remote origin main
```

Expected: 输出一个 SHA（与本地 `git rev-parse HEAD` 一致）。

---

## Task 7: 旧目录安全迁移 + symlink 创建

**Files:**
- Remove (rename): `~/.claude/skills/yy-spec-review/` → `~/.claude/skills/.yy-spec-review.bak.20260807/`
- Create (symlink): `~/.claude/skills/spec-review`, `~/.hermes/skills/software-development/spec-review`

**Interfaces:**
- Consumes: 规格§4.3 + §4.7 步骤 8（CR-001 mv 备份 + diff 预检）
- Produces: 双平台 symlink 指向本地仓库

- [ ] **Step 1: diff -rq 分类预检（CR-001）**

```bash
diff -rq ~/.claude/skills/yy-spec-review/ /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review/ 2>/dev/null | tee /tmp/spec-review-diff.txt
echo "--- 仅旧目录有的文件（BLOCK_DELETION 风险）---"
grep -E "^Only in.*yy-spec-review" /tmp/spec-review-diff.txt
echo "--- 两处都有但内容不同（NEEDS_REVIEW）---"
grep -E "^Files differ" /tmp/spec-review-diff.txt
```

Expected:
- `Only in .../spec-review/` 行（本地仓库新增，SAFE_TO_IGNORE）——安全。
- `Only in .../yy-spec-review/` 行（仅旧目录有，BLOCK_DELETION）——若有，先备份/合并这些文件再继续。
- `Files differ` 行（NEEDS_REVIEW）——这些通常是 SKILL.md/CLAUDE.md/README.md（本地仓库已改名，旧目录是 7 月 20 日版本，预期差异，安全）。

**判定规则**：BLOCK_DELETION 与 NEEDS_REVIEW 中非预期的独有改动均为空方可继续。若旧目录有独有本地产物（如 `.workbuddy/memory/` 独有日记），先 `cp` 到本地仓库或备份目录。

- [ ] **Step 2: 以 mv 替代 rm 备份旧目录（可回滚）**

```bash
mv ~/.claude/skills/yy-spec-review ~/.claude/skills/.yy-spec-review.bak.20260807
```

Expected: 无输出。旧目录移至备份名，`spec-review` 名字腾空。

- [ ] **Step 3: 创建 Claude Code symlink**

```bash
ln -s /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review ~/.claude/skills/spec-review
```

Expected: 无输出。若失败（如目标已存在），`ls -la ~/.claude/skills/spec-review` 检查，从 Step 2 备份回退。

- [ ] **Step 4: 创建 Hermes symlink**

```bash
ln -s /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review ~/.hermes/skills/software-development/spec-review
```

Expected: 无输出。

- [ ] **Step 5: symlink 验证（CR-008，可程序化判定）**

```bash
test -L ~/.claude/skills/spec-review && echo "claude: exists" || echo "claude: FAIL"
test -d ~/.claude/skills/spec-review/ && echo "claude: target reachable" || echo "claude: FAIL broken"
test -f ~/.claude/skills/spec-review/SKILL.md && echo "claude: SKILL.md present" || echo "claude: FAIL"
test -L ~/.hermes/skills/software-development/spec-review && echo "hermes: exists" || echo "hermes: FAIL"
test -d ~/.hermes/skills/software-development/spec-review/ && echo "hermes: target reachable" || echo "hermes: FAIL broken"
test -f ~/.hermes/skills/software-development/spec-review/SKILL.md && echo "hermes: SKILL.md present" || echo "hermes: FAIL"
[ "$(readlink ~/.claude/skills/spec-review)" = "$(readlink ~/.hermes/skills/software-development/spec-review)" ] && echo "dual: same target" || echo "dual: FAIL mismatch"
```

Expected: 7 行全部非 FAIL（`exists` / `target reachable` / `SKILL.md present` ×2 / `same target`）。

---

## Task 8: 最终验证（grep 门 2 + 双平台功能 + Git/GitHub + update.sh）

**Files:**
- Verify: 全仓库 + 双平台 + GitHub 远程

**Interfaces:**
- Consumes: 规格§5 验证清单
- Produces: 部署完成确认

- [ ] **Step 1: grep 验证门 2——活源文件 0 命中**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
grep -rn "yy-" SKILL.md CLAUDE.md README.md update.sh roles/ templates/ references/common.md agents/openai.yaml
echo "--- 历史产物命中（预期，不计失败）---"
grep -rln "yy-" scripts/baseline_snapshot/ docs/superpowers/reviews/ docs/superpowers/plans/ docs/superpowers/specs/ .workbuddy/ .superpowers/ | head -5
```

Expected: 第一条命令无输出（活源文件 0 命中）；第二条命令列出历史文件（预期）。

- [ ] **Step 2: Hermes 发现验证（主信号 = 功能可用，CR-002）**

需用户启动/重启 Hermes 后：

```bash
# 在 Hermes 中执行（用户操作或 hermes CLI 触发）：
# /skills        → 列表中应出现 spec-review
# /spec-review    → 应能触发技能
# 辅助信号（可选，symlink 技能可能不写入）：
grep -l "spec-review" ~/.hermes/skills/.hub/lock.json 2>/dev/null && echo "hermes: lock.json has record (optional)" || echo "hermes: no lock.json record (acceptable for symlink)"
```

Expected: `/skills` 列出 spec-review；`/spec-review` 可触发。lock.json 无记录可接受（symlink 技能可能不持久化，见规格§2.2）。

- [ ] **Step 3: Claude Code 验证**

在 Claude Code 中执行 `/spec-review`，确认技能可触发识别。

Expected: Claude Code 识别 `/spec-review` 命令。

- [ ] **Step 4: Git/GitHub 验证（CR-003）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
git log --oneline | head -1                    # 首提交存在
git status --short                             # clean（无输出）
gh repo view OneFlowerHill/spec-review --json visibility -q '.visibility'   # PRIVATE
git remote -v | head -1                        # origin = github HTTPS
git ls-remote origin main                      # 返回 SHA
```

Expected: 首提交 SHA；clean；`PRIVATE`；`origin https://github.com/OneFlowerHill/spec-review.git`；远程 SHA。

- [ ] **Step 5: update.sh 验证（CR-006）**

```bash
cd /Users/yuezhenhua/yonyou/projects/0__AI/skills/spec-review
bash update.sh
```

Expected: `==> 已是最新版本（<SHA>）。`（验证 HTTPS 认证可达，`git fetch origin` 成功）。若认证失败，确认 `gh auth setup-git` 已执行。

---

## Self-Review

**1. Spec coverage**：
- §2.2 Hermes 机制 → Task 3（frontmatter）+ Task 8 Step 2（功能验证）
- §2.4 前置条件 → Task 1 Step 1
- §4.1 改名 → Task 2
- §4.2 frontmatter → Task 3
- §4.3 symlink → Task 7
- §4.4 .gitignore → Task 1 Step 3
- §4.5 Git/GitHub → Task 6
- §4.6 update.sh/README → Task 4
- §4.7 实施顺序 → Task 1–8 对应步骤 0–10
- §5 验证清单 → Task 7 Step 5（symlink）+ Task 8（全部）
- §6 风险对策 → Task 2 Step 5（不改目录 diff）+ Task 6 Step 2（名称冲突）+ Task 7（mv 备份/diff 预检）

**2. Placeholder scan**：无 TBD/TODO/"add error handling"/"similar to Task N"。每步含完整命令与期望输出。

**3. 一致性**：
- `spec-review`（技能名）在 Task 2/3/4/6/7/8 一致使用。
- `product-reviewer`/`system-critic`/`test-designer` 在 Task 2 Step 4 与 sed 命令一致。
- `OneFlowerHill/spec-review` 在 Task 4/6 一致。
- 本地仓库路径 `…/0__AI/skills/spec-review` 全程一致。

无遗留问题。
