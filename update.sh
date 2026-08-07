#!/usr/bin/env bash
#
# spec-review 自更新脚本
# 从 origin 拉取最新版本（仅快进合并）。
# 安全保证：不产生 merge commit、不丢失本地改动、不在 detached HEAD 上乱动。
#
# 用法：
#   bash update.sh
#
# 智能体调用：当用户说“更新这个技能 / update this skill / 更新 spec-review”时，
# 在本技能根目录执行本脚本（等价于 git pull --ff-only）。
#
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> 更新 spec-review：$SKILL_DIR"

if [ ! -d "$SKILL_DIR/.git" ]; then
  echo "错误：$SKILL_DIR 不是一个 git 仓库。" >&2
  echo "本技能需通过 'git clone' 安装才能支持自动更新。" >&2
  exit 1
fi

cd "$SKILL_DIR"

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  echo "错误：当前处于 detached HEAD，无法自动更新。" >&2
  exit 1
fi

# 存在本地改动时提前失败，绝不覆盖用户工作。
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "错误：$SKILL_DIR 存在未提交的本地改动。" >&2
  echo "请先提交或 stash，再重新运行本脚本。当前改动：" >&2
  git status --short >&2
  exit 1
fi

echo "==> 拉取 origin..."
git fetch origin

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse "origin/$BRANCH")"

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "==> 已是最新版本（${LOCAL}）。"
  exit 0
fi

echo "==> 更新 ${BRANCH}：${LOCAL:0:8} -> ${REMOTE:0:8}"
git merge --ff-only "origin/$BRANCH"

echo "==> 已更新到 $(git rev-parse --short HEAD)。"
echo "==> 最近变更："
git log --oneline -5
