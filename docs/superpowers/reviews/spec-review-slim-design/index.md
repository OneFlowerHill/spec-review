# Review Index — spec-review-slim-design

## 输出语言

本审核索引的所有描述性内容必须使用中文撰写。

以下内容保持英文：

- CR-ID（CR-001, CR-002 等）
- 所有大写下划线格式的标识符和枚举值，包括但不限于：
  - 严重等级：P0, P1, P2
  - 决策状态：PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED
  - 跨轮次状态：CARRIED_FORWARD, STILL_OPEN, RESOLVED
- Machine-Readable YAML 索引的 key 和枚举值
- 技术标识符和文件路径

Machine-Readable YAML 索引中的 title 等描述性字段使用中文。

## Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

## Review Rounds

| 轮次 | 日期 | P0 | P1 | P2 | 已接受 | 已拒绝 | 已延迟 | 状态 |
|-------|------|----|----|-----|----------|----------|----------|--------|
| 1 | 2026-08-04 | 2 | 5 | 1 | 8 | 0 | 0 | CHANGES_REQUIRED |
| 2 | 2026-08-04 | 1 | 5 | 2 | 7 | 0 | 1 | APPROVED |

<!--
Status values: PENDING_DECISION, BLOCKED, CHANGES_REQUIRED,
CONDITIONAL_APPROVAL, APPROVED, INCOMPLETE

Update this table after each review round and after decisions are recorded.
-->

## Finding Tracking

| CR-ID | 轮次 | 严重度 | 标题 | 决策 | 前轮 CR-ID | 来源审核员 | 状态 |
|-------|-------|----------|-------|----------|---------------------|-----------------|--------|
| CR-001 | 1 | P0 | 共享定义 references/common.md 未纳入 subagent 加载契约，独立评审核心不变量面临静默失效 | ACCEPTED | — | PR, SC, TD | RESOLVED |
| CR-002 | 1 | P0 | 「不损失审核质量」缺少可判定验收判据，回滚触发条件不可执行 | ACCEPTED | — | PR, TD | STILL_OPEN |
| CR-003 | 1 | P1 | ≥40% token 降幅的基线、口径与测量工具不可复现 | ACCEPTED | — | PR, TD | STILL_OPEN |
| CR-004 | 1 | P1 | 验收设计无法检出静默退化：负向路径/合并能力/样本错配 | ACCEPTED | — | SC, TD | RESOLVED |
| CR-005 | 1 | P1 | 证据等级枚举（含 CONFIRMED_GAP）与现有角色/协议未对齐 | ACCEPTED | — | PR, SC | STILL_OPEN |
| CR-006 | 1 | P1 | 共享 Finding 字段格式与 system-critic 模板实际字段互相矛盾 | ACCEPTED | — | SC | STILL_OPEN |
| CR-007 | 1 | P1 | 可删除内容判定主观，行数/降幅目标与质量不变量优先级未定义 | ACCEPTED | — | PR | STILL_OPEN |
| CR-008 | 1 | P2 | references/common.md 成为单点共享依赖，存在部分部署/版本错配风险 | ACCEPTED | — | SC | RESOLVED |
| CR-001 | 2 | P1 | 质量护栏仍不可客观判定（阈值未锁定、问题匹配无规则、基线统计不足） | ACCEPTED | CR-002 | PR, SC, TD | STILL_OPEN |
| CR-002 | 2 | P1 | 证据等级契约自相矛盾（声称保持不变但与现状不符，枚举 grep 不可满足） | ACCEPTED | CR-005 | SC, TD | STILL_OPEN |
| CR-003 | 2 | P1 | System 字段契约不完整且与现有模板不符，重命名规则冲突 | ACCEPTED | CR-006 | SC | STILL_OPEN |
| CR-004 | 2 | P0 | token_analyzer.py 计量算法未定义，≥40% 降幅不可客观复算 | ACCEPTED | CR-003 | SC, TD | RESOLVED |
| CR-005 | 2 | P1 | 中心目标（端到端 token/耗时）未被验收覆盖，且 ≥40% 仅为非硬门槛、无 pass/fail | ACCEPTED | CR-002 | PR, TD | STILL_OPEN |
| CR-006 | 2 | P2 | "固定框架开销"指标自相矛盾，双样本通过条件未定义 | ACCEPTED | CR-003 | PR | STILL_OPEN |
| CR-007 | 2 | P1 | 删除安全网无法拦截未枚举质量相关规范性语句的静默删除 | ACCEPTED | CR-007 | PR | STILL_OPEN |
| CR-008 | 2 | P2 | 加载契约缺运行时加载失败检测/回退，静态可解析不足以保证隔离规则实际可达 | DEFERRED | CR-001 | PR | CARRIED_FORWARD |

<!--
Cross-round tracking:
- Previous Round CR-ID: Links to the same finding from a previous round.
  Use "—" for first-round findings.
- Status across rounds:
  - PENDING_DECISION: Awaiting decision
  - CARRIED_FORWARD: DEFERRED from a previous round, still open
  - RESOLVED: ACCEPTED and the required action has been implemented
  - STILL_OPEN: ACCEPTED but the required action has not yet been fully implemented
    (re-review found a residual gap in the same problem area)
  - REJECTED: Not accepted
  - INVALIDATED: Factual basis disproven

"Substantively the same" test: Two findings describe the same fundamental
problem affecting the same component/area. If resolving one would resolve
the other, they are substantively the same.
-->

## Trend

- Overall status: APPROVED（第 2 轮 8 条已全部决策：7 ACCEPTED + 1 DEFERRED；方案 B 框架瘦身已落实全部 ACCEPTED 修复，--compare 闸门 PASS、一致性 grep 全绿；CR-008 DEFERRED 为非阻断项；CR-004 硬性 ≥40% 闸门经 DR-009 反转为软目标）
- Open findings: 0 P0（PENDING_DECISION 清零）；已决策 7 ACCEPTED（其中 6 项修复待 B 落实，CR-004 已 RESOLVED）+ 1 DEFERRED（CR-008）
- 第 1 轮 8 条 ACCEPTED 修复已落实（commit `304b9d8`），但重新审核发现多处修复未彻底：CR-001/CR-002/CR-003/CR-005/CR-006/CR-007 为上一轮同主题的残留缺口；CR-004 为 Test 新识别的 P0（分析器算法未定义）；CR-008 为 CR-001 修复的未竟之处（运行时加载失败）。
- 跨轮次趋势：第 1 轮 2 P0 → 第 2 轮 1 P0（上轮 P0 经修复后转为残留 P1，但新出现分析器 P0）；总 Finding 数 8 → 8。
- Plan B 实施期决策反转（DR-009，2026-08-04）：方案 B 落地后实测可达降幅仅 +5.566%，远小于 CR-005 决议所落实的 ≥40% 硬闸门；用户决策移除硬性减少要求。builtin-v1 计量算法保留；`token_analyzer.py --compare` 改为『文件完整 + references/common.md §X.Y 引用一致』闸门，降幅仅作报告指标；spec §1/§6 与 prompt_scope.json 已同步修订（详见 consolidated-review.md DR-009）。

---

## Machine-Readable Index

```yaml
spec:
  path: "docs/superpowers/specs/2026-08-04-spec-review-slim-design.md"
  stem: "spec-review-slim-design"

rounds:
  - round: 1
    date: "2026-08-04"
    directory: "2026-08-04-review-001"
    findings:
      p0: 2
      p1: 5
      p2: 1
    decisions:
      accepted: 8
      rejected: 0
      deferred: 0
    status: "CHANGES_REQUIRED"
    consolidated_file: "2026-08-04-review-001/consolidated-review.md"
  - round: 2
    date: "2026-08-04"
    directory: "2026-08-04-review-002"
    findings:
      p0: 1
      p1: 5
      p2: 2
    decisions:
      accepted: 7
      rejected: 0
      deferred: 1
    status: "APPROVED"
    consolidated_file: "2026-08-04-review-002/consolidated-review.md"

findings:
  - id: "CR-001"
    round: 1
    severity: "P0"
    title: "共享定义 references/common.md 未纳入 subagent 加载契约，独立评审核心不变量面临静默失效"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "SC"
      - "TD"
    status: "RESOLVED"
  - id: "CR-002"
    round: 1
    severity: "P0"
    title: "「不损失审核质量」缺少可判定验收判据，回滚触发条件不可执行"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "TD"
    status: "STILL_OPEN"
  - id: "CR-003"
    round: 1
    severity: "P1"
    title: "≥40% token 降幅的基线、口径与测量工具不可复现"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "TD"
    status: "STILL_OPEN"
  - id: "CR-004"
    round: 1
    severity: "P1"
    title: "验收设计无法检出静默退化：负向路径/合并能力/样本错配"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "SC"
      - "TD"
    status: "RESOLVED"
  - id: "CR-005"
    round: 1
    severity: "P1"
    title: "证据等级枚举（含 CONFIRMED_GAP）与现有角色/协议未对齐"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "SC"
    status: "STILL_OPEN"
  - id: "CR-006"
    round: 1
    severity: "P1"
    title: "共享 Finding 字段格式与 system-critic 模板实际字段互相矛盾"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "SC"
    status: "STILL_OPEN"
  - id: "CR-007"
    round: 1
    severity: "P1"
    title: "可删除内容判定主观，行数/降幅目标与质量不变量优先级未定义"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
    status: "STILL_OPEN"
  - id: "CR-008"
    round: 1
    severity: "P2"
    title: "references/common.md 成为单点共享依赖，存在部分部署/版本错配风险"
    decision: "ACCEPTED"
    previous_round_cr_id: null
    source_reviewers:
      - "SC"
    status: "RESOLVED"
  - id: "CR-001"
    round: 2
    severity: "P1"
    title: "质量护栏仍不可客观判定（阈值未锁定、问题匹配无规则、基线统计不足）"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-002"
    source_reviewers:
      - "PR"
      - "SC"
      - "TD"
    status: "STILL_OPEN"
  - id: "CR-002"
    round: 2
    severity: "P1"
    title: "证据等级契约自相矛盾（声称保持不变但与现状不符，枚举 grep 不可满足）"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-005"
    source_reviewers:
      - "SC"
      - "TD"
    status: "STILL_OPEN"
  - id: "CR-003"
    round: 2
    severity: "P1"
    title: "System 字段契约不完整且与现有模板不符，重命名规则冲突"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-006"
    source_reviewers:
      - "SC"
    status: "STILL_OPEN"
  - id: "CR-004"
    round: 2
    severity: "P0"
    title: "token_analyzer.py 计量算法未定义，≥40% 降幅不可客观复算"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-003"
    source_reviewers:
      - "SC"
      - "TD"
    status: "RESOLVED"
  - id: "CR-005"
    round: 2
    severity: "P1"
    title: "中心目标（端到端 token/耗时）未被验收覆盖，且 ≥40% 仅为非硬门槛、无 pass/fail"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-002"
    source_reviewers:
      - "PR"
      - "TD"
    status: "STILL_OPEN"
  - id: "CR-006"
    round: 2
    severity: "P2"
    title: "“固定框架开销”指标自相矛盾，双样本通过条件未定义"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-003"
    source_reviewers:
      - "PR"
    status: "STILL_OPEN"
  - id: "CR-007"
    round: 2
    severity: "P1"
    title: "删除安全网无法拦截未枚举质量相关规范性语句的静默删除"
    decision: "ACCEPTED"
    previous_round_cr_id: "CR-007"
    source_reviewers:
      - "PR"
    status: "STILL_OPEN"
  - id: "CR-008"
    round: 2
    severity: "P2"
    title: "加载契约缺运行时加载失败检测/回退，静态可解析不足以保证隔离规则实际可达"
    decision: "DEFERRED"
    previous_round_cr_id: "CR-001"
    source_reviewers:
      - "PR"
    status: "CARRIED_FORWARD"
```
