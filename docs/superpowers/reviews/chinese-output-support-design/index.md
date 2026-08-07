# 审核索引 — 中文输出支持设计

## 设计规格

docs/superpowers/specs/2026-07-20-chinese-output-support-design.md

## 审核轮次

| 轮次 | 日期 | P0 | P1 | P2 | 已接受 | 已拒绝 | 已延迟 | 状态 |
|------|------|----|----|-----|--------|--------|--------|------|
| 1 | 2026-07-20 | 0 | 1 | 3 | 0 | 0 | 0 | PENDING_DECISION |

## 发现追踪

| CR-ID | 轮次 | 严重度 | 标题 | 决策 | 前轮 CR-ID | 来源审核员 | 状态 |
|-------|------|--------|------|------|-----------|-----------|------|
| CR-001 | 1 | P1 | 中文输出质量缺乏验证机制 | PENDING_DECISION | — | PR, SC, TD | PENDING_DECISION |
| CR-002 | 1 | P2 | 枚举值保持英文的范围不完整 | PENDING_DECISION | — | PR, TD | PENDING_DECISION |
| CR-003 | 1 | P2 | 三层中文约束的冗余性增加维护成本 | PENDING_DECISION | — | SC | PENDING_DECISION |
| CR-004 | 1 | P2 | index.md 表头中文化后与 YAML 索引对应关系未明确 | PENDING_DECISION | — | PR | PENDING_DECISION |

## 趋势

- 整体状态: PENDING_DECISION
- 未解决发现: 0 P0, 1 P1, 3 P2
- 首次审核轮次 — 无趋势数据。

---

## 机器可读索引

```yaml
spec:
  path: "docs/superpowers/specs/2026-07-20-chinese-output-support-design.md"
  stem: "chinese-output-support-design"

rounds:
  - round: 1
    date: "2026-07-20"
    directory: "2026-07-20-review-001"
    findings:
      p0: 0
      p1: 1
      p2: 3
    decisions:
      accepted: 0
      rejected: 0
      deferred: 0
    status: "PENDING_DECISION"
    consolidated_file: "2026-07-20-review-001/consolidated-review.md"

findings:
  - id: "CR-001"
    round: 1
    severity: "P1"
    title: "中文输出质量缺乏验证机制"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "SC"
      - "TD"
    status: "PENDING_DECISION"

  - id: "CR-002"
    round: 1
    severity: "P2"
    title: "枚举值保持英文的范围不完整"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
      - "TD"
    status: "PENDING_DECISION"

  - id: "CR-003"
    round: 1
    severity: "P2"
    title: "三层中文约束的冗余性增加维护成本"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "SC"
    status: "PENDING_DECISION"

  - id: "CR-004"
    round: 1
    severity: "P2"
    title: "index.md 表头中文化后与 YAML 索引对应关系未明确"
    decision: "PENDING_DECISION"
    previous_round_cr_id: null
    source_reviewers:
      - "PR"
    status: "PENDING_DECISION"
```
