# Spec Review Skill 瘦身设计（方案 A：压缩 + 去重）

- **日期**：2026-08-04
- **范围**：yy-spec-review skill 的提示词/协议/角色/模板瘦身
- **目标**：在不损失审核质量、不改变"三角色并行独立审核"架构的前提下，将**框架开销**（协议 + 角色 + 模板；该开销仅随子代理数量与 spec 读取次数变化，与 spec 内容本身无关）降低 **≥40%**（设计目标值；自本设计决策反转 review-002 CR-004 后，该降幅**不再作为硬性通过门槛**，仅由 `scripts/token_analyzer.py --compare` 作为报告指标输出，见 §6）。减少单次审核的 token 消耗与运行时间。
- **方法依据**：先用静态 token 流模型量化瓶颈，再用一次真实 subagent 抽样验证；量化结论见下文「量化结论」。
- **审核状态**：本设计已通过 yy-spec-review **两轮**审核。review-001 落实 8 条 ACCEPTED 决策（CR-001…CR-008）；review-002 复审后：**CR-004 已通过 `builtin-v1` 算法修复（commit 6dcc0b3）**，**CR-001/002/003/005/006/007 共 6 条 ACCEPTED 决策已纳入本文修订**，**CR-008 延后至加固轮（DEFERRED）**。当前最终状态 **CHANGES_REQUIRED** —— 待方案 B 实施框架瘦身并跑 `scripts/token_analyzer.py --compare` 验证降幅 ≥40% 后，方可转 APPROVED。

---

## 1. 量化结论（为什么砍这些）

通过静态 token 流模型（按各阶段实际加载文件计算，中文感知估算）与一次 Product Reviewer 真实抽样运行，得出：

| 维度 | 发现 |
|---|---|
| 框架开销（随子代理数量与 spec 读取次数变化，与 spec 内容无关） | 4 协议 + 3 角色 + 5 模板 + SKILL.md 合计（实际锁定基线见 §6：101922 token @ builtin-v1；§1 原估 40–78K 偏低） |
| Phase 3 协议块 | `consolidation-protocol.md`(1583 行) + `decision-protocol.md`(1557 行) 在 Phase 3 被主 agent 一次性读入，约 13K tokens |
| 角色冗余 | 3 个角色文件（781/977/918 行）重复陈述严重度、证据等级、Finding 格式、独立评审规则 |
| 输出被撑大 | 抽样显示单个 subagent 产出 499 行 / 15.6KB 审核文件 —— 冗余模板要求多字段 × 最多 5 个 Finding，导致 Phase 3 主上下文（3 输出 + 协议）比模型估计更重 |
| spec 4× 读取 | Design Spec 在（主 agent 1 次 + 3 subagent 各 1 次）共读 4 次，是大型 spec 的主导成本，但属独立评审设计固有，本轮不动 |

**基线说明（落实 CR-003）**：上述 40–78K 为区间估计，口径含"是否计入 SKILL.md/CLAUDE.md""是否计入 spec 多次读取""静态字数 vs 运行时实际加载"等变量。§6 静态验收以**锁定后的定值基线 + 测量条件四元组**判定降幅，本节的区间仅用于说明方向，不得作为验收基线。

**结论**：最大可控杠杆 = 协议文件压缩 + 角色/模板去重。质量不变量（CR-ID、decision 枚举、独立评审等）一律保留（见 §4）。

---

## 2. 目标文件结构变化

```
yy-spec-review/
├── references/
│   └── common.md            # 新增：共享定义（消除跨文件重复），权威字段/枚举源
├── roles/
│   ├── product-reviewer.md  # 瘦身：删除共享块，保留独有视角
│   ├── system-critic.md     # 瘦身
│   └── test-designer.md     # 瘦身
├── protocols/
│   ├── finding-protocol.md            # 砍掉重复陈述（参考值，非硬上限）
│   ├── consolidation-protocol.md      # 砍掉冗长 rationale/重复示例（参考值）
│   ├── decision-protocol.md           # 砍掉冗余 prose（参考值）
│   └── review-orchestrator-protocol.md# 基本不变，需登记 references/ 加载
├── templates/
│   ├── product-review.md    # 瘦身：去冗余说明
│   ├── system-review.md     # 瘦身
│   ├── test-review.md       # 瘦身
│   ├── consolidated-review.md # 瘦身
│   └── index.md             # 基本不变
├── scripts/
│   └── token_analyzer.py    # 新增：纳入仓库的 token 流分析器（落实 CR-003），禁止"同类脚本"替换
├── SKILL.md                 # 微调：指向 references/common.md，登记 references/ 路径，可选重复段改为引用
└── CLAUDE.md                # 微调：与 SKILL.md 保持一致，去掉重复叙述，登记 references/ 路径
```

> **行数目标性质（落实 CR-003 / CR-007）**：§2 / §3 中 `1583→~700`、`~40%` 等数值为**参考值**，非硬上限。与质量约束冲突时以保留约束优先；若完整保留有效约束后行数仍高于目标，接受较小降幅或转入方案 B（§7），不得为达成行数而删减规范性语句。

---

## 3. 具体改动

### 3.1 新增 `references/common.md`

集中以下当前分散重复的定义（来源：SKILL.md / CLAUDE.md / 3 角色 / finding-protocol）：

- **严重度**：P0 / P1 / P2 的精确定义与示例。
- **证据等级（全局域 + 每角色可输出子集，落实 CR-002 / CR-005）**：
  - **全局取值域（四个固定字面量，必须原样拼写，集中钉死于 `references/common.md` 作为 grep 权威清单）**：`CONFIRMED_DEFECT` / `MATERIAL_RISK` / `CONFIRMED_GAP` / `DESIGN_PREFERENCE`。
  - **各角色可输出子集（已与 `roles/*.md`、协议、模板实际字段对齐；集中后保持不变，不得静默变更；若有意扩大/缩小须显式声明并经决策）**：
    - Product：`CONFIRMED_DEFECT` | `MATERIAL_RISK`（注：`DESIGN_PREFERENCE` 仅作内部参考，不得作为 Finding 输出）。
    - System：`CONFIRMED_DEFECT` | `MATERIAL_RISK`（注：`DESIGN_PREFERENCE` 仅作内部参考，不得作为 Finding 输出）。
    - Test：`CONFIRMED_GAP` | `MATERIAL_RISK`（注：`DESIGN_PREFERENCE` 仅作内部参考，不得作为 Finding 输出）。
  - 上述四个全局字面量均须在合并/决策协议中被识别（尤其 `CONFIRMED_GAP` 由 Test 角色产出）；任一字面量在 `common.md` 与角色/模板中拼写不一致即视为一致性缺陷（见 §6 枚举校验）。
  - **权威优先级**：当 `common.md` 与角色/模板/协议对证据等级的约束冲突时，以 `common.md` 为权威；各角色既有可输出子集为不可静默变更的既有契约。
- **Finding 字段契约（权威来源 + 每角色差异字段，落实 CR-003 / CR-006）**：
  - `common.md` 定义**共享必填字段**为权威契约：`Severity / Evidence Class / Confidence / Location / Consequence / Evidence / Recommendation`。
  - 各角色**差异字段（字段名须与对应模板完全一致，禁止重命名/缩写/隐式改写；下列字面量集中钉死于 `references/common.md`，作为字段校验 grep 依据）**：
    - Product：`Gap` / `Trigger Scenario`（业务上下文）。
    - System：`Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility`（模板中以 "Reversibility Analysis" 呈现，字面量以 `Reversibility` 计）。
    - Test：`Gap` / `Trigger Scenario` / `Finding Type`（必填）。
  - 落地产出的 Machine-Readable 索引须同时包含共享字段与各角色差异字段；字段缺失、重命名或缩写视为一致性缺陷（§6 字段校验）。
- **独立评审 / 上下文隔离规则**：subagent 不得读其他评审、不得含主 agent 分析。**此规则本身须存在于 subagent 上下文**（见 §5 加载契约，落实 CR-001）。
- **三角色边界摘要**：Product / System / Test 各自职责一句话。

各角色与模板以「见 `references/common.md`」引用，不再各自重述共享块；但角色独有字段仍由各模板定义，`common.md` 仅作为共享部分的权威源。

### 3.2 瘦身角色文件（各砍约 40–50%，参考值）

- 删除：严重度、证据等级、Finding 格式、独立评审规则等共享块 → 替换为对 `references/common.md` 的引用。
- 保留：每个角色**独有**的内容 ——
  - Product：核心评审问题、4 个视角（Cynical QA / Frustrated Engineer / Malicious User / Overworked Admin）、8 个评审维度、筛选优先级、示例 Finding。
  - System：架构/数据完整性/故障恢复/安全边界/可观测性等独有维度，及其独有字段（Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility）。
  - Test：验收标准/可观测结果/验证缺口/生产盲点，以及 Finding Type（ACCEPTANCE_TEST / UNTESTABLE_REQUIREMENT / BLIND_SPOT）要求。
- **删除纪律（落实 CR-007）**：执行者删减任一规范性语句（祈使句约束 / 禁止项 / 数量上限）须逐条记录理由，汇总入「删除项清单」（§7）；不得依个人判断静默删除。

### 3.3 瘦身协议文件

| 文件 | 保留 | 砍掉 |
|---|---|---|
| consolidation-protocol.md | 合并规则、关系分类（DUPLICATE/SAME_ROOT_CAUSE/RELATED/INDEPENDENT/CONTRADICTORY/SUBSET/CONSEQUENCE）、CR-ID 分配、Source Finding 完整性校验算法、冲突记录；并确保能识别证据等级全部四值（含 CONFIRMED_GAP） | 冗长 rationale、重复示例（保留判定依据的示例） |
| decision-protocol.md | 权威状态枚举及含义、状态流转 | 冗余 prose |
| finding-protocol.md | 单 Finding 结构与质量门槛 | 重复陈述 |
| review-orchestrator-protocol.md | 基本保留（已较精炼），**须将 references/common.md 加入 subagent 加载契约**（见 §5） | — |

> 砍掉的内容若承载约束性语义，须计入删除项清单（§7），不得为达标而删。

### 3.4 瘦身模板

去掉重复说明性文字，保留结构骨架与字段定义。输出语言规则（中文描述 + 英文 ID/枚举）保留。各模板字段须与 `common.md` 字段契约一致（§6 字段校验）。

### 3.5 SKILL.md / CLAUDE.md 微调

- SKILL.md 中重复的严重度/边界段落改为引用 `references/common.md`（保留精简版要点即可）。
- CLAUDE.md 与 SKILL.md 保持一致，删除与协议文件重复的冗长叙述。
- **登记 `references/` 路径（落实 CR-008）**：在 SKILL.md、CLAUDE.md、`review-orchestrator-protocol.md` 中显式声明 `references/common.md` 为权威共享定义源，并纳入 subagent 加载契约（§5），防止悬空引用。

---

## 4. 质量不变量（严格保留）

以下规则一条不动，确保审核质量与现有产出兼容：

1. CR-ID 为合并 Finding 唯一标识（禁止 RV-001）。
2. decision-protocol 状态枚举为权威（PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED）。
3. Test Designer Finding 必须含 Finding Type。
4. MISSING 审核硬规则；INCOMPLETE 触发条件（MISSING + 完整性校验失败）。
5. Source Finding 完整性校验：总数 = 合并引用 + 未合并 + 重复/取代。
6. 独立评审：subagent 提示词不得含主 agent 分析，角色间互不参考；**该隔离规则须实际存在于每个 subagent 的运行上下文**（由 §5 加载契约保证，§6 校验）。
7. 输出路径与轮次结构不变（docs/superpowers/reviews/<stem>/...）。
8. **证据等级取值域契约（落实 CR-005）**：`common.md` 定义全局域与每角色允许子集；合并/决策协议须能识别全部四值（含 `CONFIRMED_GAP`）；集中后各角色既有枚举约束（§3.1）不得被静默变更，若有意变更须显式声明并经决策。
9. **§4 不穷尽声明 + 删除纪律（落实 CR-007）**：本条列为审查重点但**非穷尽**；角色/协议中尚存大量未被本条款覆盖却约束输出质量的规范性语句（数量上限、证据等级不得升格、禁止制造 Finding 等）。删减任一此类规范性语句须逐条记录理由并入删除项清单（§7），禁止静默删除。
10. **common.md 同批变更与路径登记（落实 CR-008）**：`references/common.md` 与其引用方（roles / templates）必须**同批变更**（单次提交或同一 PR）；`references/` 路径须在 SKILL.md/CLAUDE.md/orchestrator 显式登记，所有对 `common.md` 的引用必须可解析，禁止悬空引用。
11. **不可删质量不变量字面量清单（落实 CR-007）**：以下字符串为质量相关规范性语句的承载字面量，瘦身前后必须仍可 grep 命中；任一缺失视为静默删除，须回滚。该清单固定并纳入 `references/common.md` 与 §6 一致性校验：
   - 合并标识：`CR-ID`；禁止 `RV-` 前缀。
   - 决策枚举：`PENDING_DECISION` / `ACCEPTED` / `REJECTED` / `DEFERRED` / `PARTIALLY_ACCEPTED` / `DUPLICATE` / `INVALIDATED`。
   - 证据等级：`CONFIRMED_DEFECT` / `MATERIAL_RISK` / `CONFIRMED_GAP` / `DESIGN_PREFERENCE`。
   - 关系分类：`DUPLICATE` / `SAME_ROOT_CAUSE` / `RELATED` / `INDEPENDENT` / `CONTRADICTORY` / `SUBSET` / `CONSEQUENCE`。
   - 状态硬规则：`INCOMPLETE` / `MISSING`。
   - 独立评审：`独立评审` / `subagent 不得读其他评审`。
   - 各角色差异字段名（见 §3.1）：`Gap` / `Trigger Scenario` / `Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility` / `Finding Type`。
   删除流程须先对本次 diff 跑该清单核对，确认零缺失后方可合入；清单本身随 `common.md` 同批变更（§4 第 10 条）。

---

## 5. 数据流向（行为不变，加载契约修订）

- **subagent 权威加载契约（落实 CR-001）**：subagent 提示词指示「读 `references/common.md` + `roles/X.md` + `templates/X.md` + spec 路径」——`common.md` 与角色/模板/spec **四者并列**纳入加载清单，不得省略。`common.md` 与引用方同批变更（§4 第 10 条），确保隔离上下文中独立评审规则与共享判据实际可达。
- 主 agent Phase 3 仍读协议，但协议块约减半。
- 流水线（Context Acquisition → 3 并行独立审核 → 合并 → 输出交接）完全不变。

---

## 6. 回滚与验收（可判定化）

> 本节修订落实 CR-001（质量护栏可判定清单）、CR-002（质量可判定）、CR-003（口径锁定）、CR-004（负向/合并覆盖）、CR-005/CR-006（枚举/字段一致）、CR-007（删除清单）、CR-008（引用可解析）。

- **留底**：改动前 `git commit` 当前状态。
- **质量护栏（可判定，落实 CR-002）**：
  - **基线波动测量**：改动前对同一固定小 spec 运行 **N≥2 次**，记录每次产出的 Finding 集合（以 `severity + 所指向问题` 为标识）及波动范围。
  - **"基本一致"量化口径**：以 **P0/P1 所指向问题是否仍被覆盖**为主判据（关键 Finding 复现率 ≥ 阈值，建议 ≥80%），而非仅比较数量；数量可作辅助。
  - **判定责任人**：每次验收由 Spec 所有者（或受托主 agent）指定并留名。
  - **样本要求**：至少 **1 个小 spec + 1 个大型/真实 spec**（大型样本覆盖上下文紧张与并发场景，避免小 spec 系统性低估风险）。
  - **回滚触发条件**：若关键 Finding 复现率低于阈值，或新出现未被覆盖的 P0/P1 问题 → 触发 `git revert`；正常 LLM 波动（在基线波动范围内）不触发。
  - **可判定验收清单（落实 CR-001，瘦身后必过）**：除"关键 Finding 复现率 ≥80%"外，须逐项核对：
    1. 每个角色 subagent 仍输出其规定 finding 字段（见 §3.1 字段契约），缺字段即 FAIL；
    2. 合并后 Source Finding 完整性校验仍通过（总数 = 合并引用 + 未合并 + 重复/取代）；
    3. §4 第 11 条"不可删质量不变量字面量清单"在瘦身版中仍 grep 命中，缺失即 FAIL。
    以上三项与复现率共同构成质量护栏的通过条件；任一不满足即触发回滚（与 §4 第 11 条 CR-007 删除安全网联动）。
- **功能验收**：
  - *正常路径*：3 份独立审核 + 1 份合并审核均正常产出；Source Finding 完整性校验通过；INCOMPLETE 逻辑 intact。
  - *负向路径（落实 CR-004）*：① 缺少一份角色产出 → 标记 MISSING；② MISSING 且完整性校验失败 → INCOMPLETE；③ 故意遗漏一条 Source Finding → 校验失败并**显式记录**。以上三项须被触发且行为正确。
  - *合并能力（落实 CR-004）*：至少一个含跨角色重叠与矛盾的输入，为 `DUPLICATE` / `SAME_ROOT_CAUSE` / `CONTRADICTORY` 各定义唯一可观测预期结果。
- **静态验收 / token 降幅测量（落实 CR-003 + 解决 CR-004）**：
  - 分析器 `scripts/token_analyzer.py` 纳入仓库；**算法以 `builtin-v1` 版本在脚本内写死，且仅依赖 Python 标准库（零外部依赖）**，禁止"同类脚本"替换；任何对口径的修改须 bump 版本号并经决策（§4）。
  - **算法口径（`builtin-v1@1.0.0`，须原样复现；详见 `token_analyzer.py --algorithm-info`）**：
    1. 归一化（对基线/候选一致应用）：UTF-8 读取 → 行尾统一 LF → 每行去尾部空白 → 文件尾恰一个 `"\n"`。
    2. 分词计数（按字符扫描）：
       - CJK 汉字/假名/谚文/全角与 CJK 标点 → 每字符 1 token；
       - 连续 ASCII 字母数字 `[A-Za-z0-9]+` → `ceil(长度/4)` token（英文约 4 字符/token 代理）；
       - 连续 ASCII 空白 `[ \t\r\n]+` → 每段空白 1 token；
       - 其余任意单字符（ASCII 标点、符号、emoji、Latin 扩展等）→ 每字符 1 token。
    3. 文件 token = 上述累加；集合 token = 文件 token 之和（文件按路径字典序排列后求和，消除顺序不确定性）。
  - **纳入文件清单（锁定，存于 `scripts/prompt_scope.json`）**：基线 = 当前框架即 `SKILL.md` + `protocols/*.md`(4) + `roles/*.md`(3) + `templates/*.md`(5) 共 **13 文件**（注：原 §1 误写"3 模板"，实际 5 模板）；候选 = 同上 13 文件（瘦身后的版本）+ `references/common.md`（新增共享定义，计入候选总量）。
  - **四元组（可复算，验收必留）**：`算法=builtin-v1@1.0.0` / `基线值=101922` / `改动后值` / `降幅%=(基线-候选)/基线×100` / `测量条件=manifest=prompt_scope.json + 不计 spec 多次读取`。
  - **判定（可判定，回应 CR-004）**：同一算法对基线/候选各跑一次，输出 `降幅%` 供可见（四元组见上）。**降幅自决策反转 CR-004 后不再作为硬性通过门槛**：`--compare` 的 PASS 条件为 ① 基线/候选文件无缺失（完整性）；② 所有 `references/common.md §X.Y` 引用均可解析到 common.md 真实标题（引用一致，见下条）。降幅为负或偏低仅作报告，不阻断通过。脚本以退出码 0/1 表达并输出机器可读 JSON。
  - **中心目标验收判定（落实 CR-005）**：中心目标"端到端 token 降幅"的达成以 `scripts/token_analyzer.py --compare` 实际跑出 PASS 为准；PASS 条件为文件完整 + 引用一致（见上条），降幅作为报告指标列出。**≥40% 硬闸门已移除**（决策反转 CR-004），瘦身仍可宣称达成——只要闸门 PASS 且降幅为非负/合理报告值即可。本轮实测：基线 101,922 / 候选 96,249 / 降幅 +5.566%（PASS）。
  - **复现性保证**：零外部依赖 + 锁定文件清单 + 锁定归一化与分词规则 + 固定文件顺序 → 任意人在任意 Python≥3.9 环境重跑得完全相同数字，降幅值可被客观复算（解决 CR-004）。
- **一致性校验（落实 CR-005 / CR-006 / CR-008 / CR-007）**：
  - 枚举一致性 grep：`common.md` 与三模板 `evidence_class` 取值域一致，且合并/决策协议可识别全部四值（含 `CONFIRMED_GAP`）。
  - 字段一致性 grep：`common.md` 字段契约与三模板字段定义无冲突，角色差异字段未丢失。
  - 引用可解析：所有对 `common.md` 的引用均可解析，无悬空引用（§4 第 10 条）。
  - 删除项清单：逐条对照 §4 与角色规范性语句，确认无静默删除（§7）。
- **回滚**：若功能验收质量下降（依上述可判定判据）或一致性校验失败，直接 `git revert` 到留底提交。

---

## 7. 不在本轮范围（方案 B 后续）

- 将 4 个协议合并为 1 个精益协议。
- SKILL.md 增加阶段索引，详情按需加载（lazy load）以进一步减少主 agent 上下文峰值。
- 仅在方案 A 落地且验证有效后，再评估是否启动。

**附：删除项清单（落实 CR-007）**

瘦身实施时同步维护，格式：

```
| 文件 | 删除段落/语句 | 类型(约束/禁止/数量上限/说明) | 删除理由 | 是否影响质量约束 |
```

该清单随瘦身 PR 一并提交，供评审对照 §4 与角色规范性语句；任何标记为"影响质量约束"的项须经决策（参照本设计审核流程），不得静默合入。
