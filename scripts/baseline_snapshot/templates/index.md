# Review Index — <Spec Name>

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

<PATH_TO_DESIGN_SPEC>

## Review Rounds

| 轮次 | 日期 | P0 | P1 | P2 | 已接受 | 已拒绝 | 已延迟 | 状态 |
|-------|------|----|----|-----|----------|----------|----------|--------|
| 1 | YYYY-MM-DD | 0 | 0 | 0 | 0 | 0 | 0 | PENDING_DECISION |

<!--
Status values: PENDING_DECISION, BLOCKED, CHANGES_REQUIRED,
CONDITIONAL_APPROVAL, APPROVED, INCOMPLETE

Update this table after each review round and after decisions are recorded.
-->

## Finding Tracking

| CR-ID | 轮次 | 严重度 | 标题 | 决策 | 前轮 CR-ID | 来源审核员 | 状态 |
|-------|-------|----------|-------|----------|---------------------|-----------------|--------|
| CR-001 | 1 | P0 | <title> | PENDING_DECISION | — | PR, SC, TD | PENDING_DECISION |

<!--
Cross-round tracking:
- Previous Round CR-ID: Links to the same finding from a previous round.
  Use "—" for first-round findings.
- Status across rounds:
  - PENDING_DECISION: Awaiting decision
  - CARRIED_FORWARD: DEFERRED from a previous round, still open
  - RESOLVED: ACCEPTED and the required action has been implemented
  - STILL_OPEN: ACCEPTED but the required action has not yet been implemented
  - REJECTED: Not accepted
  - INVALIDATED: Factual basis disproven

"Substantively the same" test: Two findings describe the same fundamental
problem affecting the same component/area. If resolving one would resolve
the other, they are substantively the same.
-->

## Trend

<!--
Update after each round. Compare to the previous round.
-->

- Overall status: PENDING_DECISION
- Open findings: 0 P0, 0 P1, 0 P2
- First review round — no trend data yet.

---

## Machine-Readable Index

```yaml
spec:
  path: "<PATH_TO_DESIGN_SPEC>"
  stem: "<SPEC_STEM>"

rounds:
  - round: 1
    date: "YYYY-MM-DD"
    directory: "YYYY-MM-DD-review-001"
    findings:
      p0: 0
      p1: 0
      p2: 0
    decisions:
      accepted: 0
      rejected: 0
      deferred: 0
    status: "PENDING_DECISION"
    consolidated_file: "YYYY-MM-DD-review-001/consolidated-review.md"

findings:
  - id: "CR-001"
    round: 1
    severity: "P0|P1|P2"
    title: "<title>"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "SC"
      - "TD"
    status: "PENDING_DECISION"
```
