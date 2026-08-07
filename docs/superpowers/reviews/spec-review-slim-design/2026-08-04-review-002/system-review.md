# System Review

## 输出语言

本审核的所有描述性内容使用中文撰写；所有大写下划线标识符、枚举值、文件路径保持英文（见模板规则）。

## Review Metadata

### Review ID

2026-08-04-review-002

### Reviewer

yy-system-critic

### Review Type

SYSTEM_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Review Date

2026-08-04

### Review Status

COMPLETED

---

## Review Scope

本审核以系统可靠性、契约一致性、可验收性（acceptability）、可回滚性、架构耦合与长期可维护性视角，评审该「瘦身设计」方案。

本审核不重做产品/测试的语义分析，不产出实现计划，不对最终接受/拒绝做决策。

本审核重点关注（按任务指令）：共享定义（references/common.md）在三个角色间是否一致定义；字段/评估契约是否连贯；修订后的验收/回滚准则是否内部自洽且可实现。

---

## Findings

### SC-001 — Product 与 Test 的证据等级子集被静默变更，违反「保持不变 / 不得静默变更」契约

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

§3.1 证据等级（全局域 + 每角色子集）、§4 第 8 条；对照现存 `roles/product-reviewer.md`、`roles/test-designer.md`

#### Risk

方案声称各角色的「允许子集（集中后保持不变，不得静默变更）」，但方案 §3.1 给出的子集与当前已落地的角色文件并不一致：

- 当前 `roles/product-reviewer.md`（第 154–162 行）的 Evidence Classification 含 `CONFIRMED_DEFECT` / `MATERIAL_RISK` / `DESIGN_PREFERENCE`，并说明「Do not normally report DESIGN_PREFERENCE」。而方案 §3.1 将 Product 子集限定为 `CONFIRMED_DEFECT | MATERIAL_RISK`，并额外要求「不得把 DESIGN_PREFERENCE 作为 Finding 输出」——即把 `DESIGN_PREFERENCE` 从 Product 中移除/禁止。
- 当前 `roles/test-designer.md`（第 160–192 行）的 Evidence Classification 仅含 `CONFIRMED_GAP` / `MATERIAL_RISK` / `DESIGN_PREFERENCE`（Required Finding Format 第 708–710 行亦仅列此三值），**不含 `CONFIRMED_DEFECT`**。而方案 §3.1 将 Test 子集扩展为 `CONFIRMED_DEFECT | MATERIAL_RISK | CONFIRMED_GAP | DESIGN_PREFERENCE`——即向 Test 新增了 `CONFIRMED_DEFECT`。

因此，两个角色的证据等级子集实际上都被变更（Product 收窄、Test 扩张），但方案正文却声明这些子集「保持不变」，且 §4 第 8 条要求「若有意扩大/缩小须显式声明并经决策」。方案中找不到对这两项变更的显式声明。

#### Trigger Condition

1. 评审者将 §3.1 的每角色子集与当前已提交的角色文件逐一比对。
2. 发现 Product 的 `DESIGN_PREFERENCE` 被移除、Test 的 `CONFIRMED_DEFECT` 被新增。
3. 方案正文却声明这些子集「保持不变」（§3.1）。
4. §4 第 8 条要求有意扩大/缩小须显式声明并经决策。
5. 方案中不存在对上述两项变更的显式声明。

#### Consequence

证据等级契约自相矛盾：要么「保持不变」的声明为假（属缺陷），要么发生了方案自身禁止的静默变更（违反 §4 第 8 条）。后果是 `common.md` 将成为一份与角色实际支持范围不一致的「权威」契约；合并/决策协议可能收到 Test 产出的、当前 Test 角色并未定义的 `CONFIRMED_DEFECT` 类，或错误地拒绝 Product 原本允许的 `DESIGN_PREFERENCE`。方案所承诺的「既有枚举约束不得静默变更」保证被自身打破。

#### Likelihood

HIGH —— 该不一致直接存在于当前已提交文件与方案 §3.1 文本之间，任何对照阅读即可确认。

#### Reversibility

REVERSIBLE —— 属方案阶段（尚未实施），可通过修订文本或 git revert 修正；但若已据此落地并影响下游工具，则修复成本上升。

#### Recommendation

对每一角色证据子集的**实际当前值**逐条列出并核对；若确有意为 Product 移除 `DESIGN_PREFERENCE`、为 Test 新增 `CONFIRMED_DEFECT`，须按 §4 第 8 条**显式声明为有意变更并记录决策**，不得再以「保持不变」表述。建议将「保持不变」改为「以如下显式声明的子集为准」。

#### Evidence

- §3.1：Product = `CONFIRMED_DEFECT | MATERIAL_RISK`（且不得把 `DESIGN_PREFERENCE` 作为 Finding 输出）；Test = `CONFIRMED_DEFECT | MATERIAL_RISK | CONFIRMED_GAP | DESIGN_PREFERENCE`。
- §3.1：「各角色允许子集（集中后**保持不变**，不得静默变更；若有意扩大/缩小须显式声明）」。
- §4 第 8 条：「集中后各角色既有枚举约束（§3.1）不得被静默变更，若有意变更须显式声明并经决策。」
- `roles/product-reviewer.md` 第 154–162 行定义 `DESIGN_PREFERENCE`。
- `roles/test-designer.md` 第 160–192 行仅定义 `CONFIRMED_GAP` / `MATERIAL_RISK` / `DESIGN_PREFERENCE`，无 `CONFIRMED_DEFECT`。

#### Assumptions

- CONFIRMED：上述文件内容与方案 §3.1 文本均经直接读取核实。

#### Reversibility Analysis

可经修订文档或 git revert 回退；一旦 `common.md` 落地并被下游协议/脚本依赖，回退需同步修订多处引用，成本中等。

#### Operational Impact

NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

将一份与现状不符的「权威」契约固化为单一来源，会放大后续维护成本：任何角色文件与 `common.md` 的漂移都需跨文件协调；且静默变更未被记录，未来维护者无从得知 `DESIGN_PREFERENCE`/`CONFIRMED_DEFECT` 的取舍是有意还是遗漏。

#### Source References

* §3.1 证据等级（全局域 + 每角色子集）
* §4 第 8 条
* `roles/product-reviewer.md`
* `roles/test-designer.md`

---

### SC-002 — §6 枚举一致性 grep「取值域一致」在全局域(4 值)与每角色子集(2/3/4 值)间不可同时满足

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

§6 一致性校验（枚举一致性 grep）、§3.1 全局域与每角色子集

#### Risk

方案 §6 要求一次 grep 证明 `common.md` 与三个模板的 `evidence_class` 取值域「一致」，同时要求合并/决策协议能识别全部四值。但方案自己的数据模型是：全局域 = 4 值（`CONFIRMED_DEFECT` / `MATERIAL_RISK` / `CONFIRMED_GAP` / `DESIGN_PREFERENCE`），而每角色子集是其严格子集（Product 2 值、System 3 值、Test 4 值）。

若「取值域一致」按**集合相等**理解，则该 grep 对 Product、System 必然失败（子集 ≠ 全集）；若按「无矛盾定义」理解，则这是无法用 grep 机械判定的模糊语义。因此该验收门在其自身定义的数据模型下**不可被确定性地满足**。

#### Trigger Condition

1. 实施者按 §3.1 写入 `common.md`，全局域为 4 值。
2. 实施每角色模板，子集分别为 Product 2 值 / System 3 值 / Test 4 值。
3. 运行 §6 要求的「取值域一致」grep。
4. 在集合相等语义下，Product、System 模板与 `common.md` 不一致 → 门失败。
5. 验收门（CR-005）无法机械通过，或被临时放宽。

#### Consequence

一致性验收准则（CR-005）按字面不可实现：要么正确的变更被误判为失败而阻断，要么该检查被临时弱化 → 方案所承诺的「枚举一致性可机械校验」保证落空。

#### Likelihood

HIGH —— 直接由方案自身的定义推导得出，无需运行环境即可确认。

#### Reversibility

REVERSIBLE

#### Recommendation

精确定义该 grep 的语义，例如：「每个模板的 `evidence_class` 取值域 ⊆ `common.md` 全局域，且不得引入 `common.md` 之外的取值」；明确将「全局域」排除在对每个模板的相等性要求之外。给出确切的正则/模式与期望通过条件，使检查可机械判定。

#### Evidence

- §6：「枚举一致性 grep：`common.md` 与三模板 `evidence_class` 取值域一致，且合并/决策协议可识别全部四值（含 `CONFIRMED_GAP`）。」
- §3.1 全局域 = 4 值；Product = 2 值、System = 3 值、Test = 4 值。

#### Assumptions

- CONFIRMED：§3.1 与 §6 文本经直接读取核实。

#### Reversibility Analysis

纯文档/校验规则修正，git revert 即可；不影响已产出数据。

#### Operational Impact

NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

验收门不可机械判定，会使 CI/验收脚本难以稳定落地，后续维护者需反复解释「一致」的口径，增加维护负担。

#### Source References

* §6 一致性校验
* §3.1 全局域与每角色子集

---

### SC-003 — Finding 字段契约不完整且与现有 System 模板字段不匹配；「重命名视为缺陷」会与有意对齐冲突

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

§3.1 Finding 字段契约（共享必填 + 每角色差异字段）、§3.4、§6 字段一致性 grep；对照 `templates/system-review.md`

#### Risk

§3.1 声明的 System「权威字段契约」= 共享必填 7 项（`Severity` / `Evidence Class` / `Confidence` / `Location` / `Consequence` / `Evidence` / `Recommendation`）+ System 差异 5 项（`Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility`）= 12 项。

但当前 `templates/system-review.md` 实际定义的字段中，有 5 项是该契约**未包含**的：`Assumptions`、`Operational Impact`、`Security Impact`、`Maintenance Impact`、`Source References`；且其可逆性字段命名为 `Reversibility Analysis`（非 `Reversibility`）。方案从未说明这 5 个字段是被删除、保留还是重命名：

- 若删除，则违反 §3.4「保留结构骨架与字段定义」与 §6「角色差异字段未丢失」；
- 若保留，则它们不在权威契约内，§6 字段一致性检查因缺少 System 的完整字段集而**无法校验**「未丢失」。

此外，§6 规定「字段缺失/**重命名**视为一致性缺陷」，而方案契约本身要求把 `Reversibility Analysis` 改名为 `Reversibility`（对齐契约）——该**有意重命名会被同一检查误判为缺陷**，产生假阳性。

#### Trigger Condition

1. 瘦身按 §3.1 的 12 字段契约实施，并将 `Reversibility Analysis` 重命名为 `Reversibility`。
2. 模板中既有的 `Assumptions` / `Operational Impact` / `Security Impact` / `Maintenance Impact` / `Source References` 要么被删（与 §3.4/§6 冲突），要么保留但游离于权威契约之外。
3. 运行 §6 字段一致性 grep：因契约未列全字段，「未丢失」无法核验；且有意重命名触发「重命名视为缺陷」假阳性。

#### Consequence

字段契约不可被验证；System 专属的诊断字段（`Operational Impact` / `Security Impact` / `Maintenance Impact`）存在被无意丢弃的风险，从而削弱审核质量；或一致性检查对该丢弃/重命名产生误报，干扰验收。

#### Likelihood

HIGH —— 由契约与现有模板的字段差异直接可得。

#### Reversibility

REVERSIBLE

#### Recommendation

完整枚举每个角色的权威字段集，纳入当前模板实际存在的全部字段（将 `Assumptions` / `Operational Impact` / `Security Impact` / `Maintenance Impact` / `Source References` 显式列入 System 契约，或明确声明删除并同步修订 §3.4/§6）；明确「为对齐权威契约而进行的重命名不视为一致性缺陷」，并将 §6 grep 的范围限定为检测**无意**的字段漂移。

#### Evidence

- §3.1 Finding 字段契约（共享 7 + System 差异 5）。
- `templates/system-review.md` 含 `Assumptions` / `Operational Impact` / `Security Impact` / `Maintenance Impact` / `Source References` 及 `Reversibility Analysis`。
- §3.4：「去掉重复说明性文字，保留结构骨架与字段定义。」
- §6：「字段一致性 grep：...角色差异字段未丢失」「字段缺失/重命名视为一致性缺陷」。

#### Assumptions

- CONFIRMED：字段差异经直接读取 `templates/system-review.md` 核实。

#### Reversibility Analysis

文档/模板修正，git revert 即可；无数据影响。

#### Operational Impact

NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

不完整的字段契约会成为长期维护隐患：未来任何角色模板字段调整都无法对照一份完整权威清单，易产生隐性字段丢失。

#### Source References

* §3.1 Finding 字段契约
* §3.4 模板瘦身
* §6 字段一致性 grep
* `templates/system-review.md`

---

### SC-004 — 质量护栏的复现率阈值未固化，「可判定」目标与回滚触发依赖未定义阈值相矛盾；N≥2 基线波动估计统计不足

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

§6 质量护栏（基线波动测量、「关键 Finding 复现率 ≥ 阈值，建议 ≥80%」、回滚触发「低于阈值」）

#### Risk

质量护栏声称「可判定」（落实 CR-002），但其通过/回滚的**阈值从未被固定**，仅以「建议 ≥80%」表述；而回滚触发条件写的是「若关键 Finding 复现率**低于阈值**」。此处「阈值」无定义值。此外，基线波动仅以「改动前对同一固定小 spec 运行 **N≥2 次**」估计——2 次采样无法可靠刻画 LLM 输出的方差，其「波动范围」只是 2 个样本的最值，极不稳定。

#### Trigger Condition

1. 实施者在瘦身后运行质量护栏。
2. 关键 Finding 复现率为例如 75%。
3. 无固定的阈值可判定通过/回滚；「建议 ≥80%」不具约束力。
4. 回滚触发条件「低于阈值」因阈值未定义而无法确定性触发。
5. 2 次运行的基线范围可能过宽或过窄，使「正常波动不触发」不可靠。

#### Causal Chain

验收门依赖未定义阈值 + 统计上欠驱动的基线 → 护栏无法确定性地决定接受/回滚 → 要么主观接受（质量退化可能漏过），要么任意回滚（正确变更被撤） → 瘦身项目的核心安全门实际上并非「可判定」。

#### Consequence

防止审核质量退化的首要保护机制无法被客观执行；验收结果依赖评审者主观判断；存在将「已悄然降低审核质量」的瘦身版本合入的风险。

#### Likelihood

HIGH —— 该歧义内置于方案文本，每次验收运行都会遇到。

#### Reversibility

REVERSIBLE

#### Recommendation

显式固化阈值（例如将「关键 Finding 复现率 ≥80%」定为硬门，或定义每次验收前确定阈值的成文决策流程）；将基线运行次数提升到统计上有意义的样本量（如 N≥5），并定义基线范围的算法（如均值 ± 容差）而非 2 样本最值。

#### Evidence

- §6：「关键 Finding 复现率 ≥ 阈值，建议 ≥80%」
- §6：「回滚触发条件：若关键 Finding 复现率低于阈值，或新出现未被覆盖的 P0/P1 问题 → 触发 `git revert`」
- §6：「改动前对同一固定小 spec 运行 N≥2 次，记录每次产出的 Finding 集合...及波动范围」
- §6 目标：「质量护栏（可判定，落实 CR-002）」

#### Assumptions

- CONFIRMED：上述条款经直接读取核实。

#### Reversibility Analysis

阈值/采样方法的修正属文档层面，git revert 即可；不影响已产出审核文件。

#### Operational Impact

验收成为人工主观判断，增加每次瘦身迭代的运维与争议成本；在阈值缺失时，回滚动作可能不触发或误触发。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

缺乏可复现的验收判定，会使方案 A 的后续维护与方案 B 的启动决策失去客观依据。

#### Source References

* §6 质量护栏
* CR-002（质量可判定）

---

### SC-005 — 静态降幅测量的可复算性依赖未规格化的脚本内部「中文感知」规则，且禁止同类脚本替换形成单点依据

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

§6 静态验收（`scripts/token_analyzer.py`「估算规则在其内写死（中文感知口径固定）」、「禁止同类脚本替换」、四元组可复算）

#### Risk

≥40% 的静态降幅验收依赖单一脚本 `scripts/token_analyzer.py`，其 token 估算方法（「中文感知」）被「写死」但**未在方案中规格化**。方案声称测量「可复算」依托四元组，但可复算性实际取决于该脚本未公开的**内部**规则；且「禁止同类脚本替换」使该脚本成为唯一权威度量，若其启发式对某一 spec 语言混合估计失真，既无交叉校验，也无法替换。

#### Trigger Condition

1. 某 spec 的中英文混合比例使脚本「中文感知」启发式估计失真。
2. 测得降幅与独立计数不一致。
3. 因脚本为固定权威且禁止替换，争议数值无法被交叉核对。
4. ≥40% 门的通过/失败建立在可能脆弱的内部逻辑之上。

#### Causal Chain

验收依赖不透明、单一来源的脚本逻辑 + 禁止替换 → 测量可能不准确却被当作权威 → ≥40% 门可能因启发式假象而非真实 token 节省而通过/失败。

#### Consequence

静态验收可能被估计器误差误导；方案头条「≥40%」主张的可审计性受限。

#### Likelihood

MEDIUM —— 取决于 spec 语言混合；启发式看似合理但未规格化，失真概率非空。

#### Reversibility

REVERSIBLE

#### Recommendation

在方案或脚本头部文档化 token 估算规则（或所用确切 tokenizer/算法），使四元组可被独立复算；允许独立重测（或定义交叉校验方法），而非一律禁止替代脚本。

#### Evidence

- §6：「分析器 `scripts/token_analyzer.py` 纳入仓库，禁止『同类脚本』替换；估算规则在其内写死（中文感知口径固定）」
- §6：「验收以四元组留存可复算：基线值 / 改动后值 / 降幅 / 测量条件（所用 spec、纳入文件清单、是否计入 spec 多次读取）」
- 现状：`scripts/token_analyzer.py` 尚不存在（属新增文件），其内部规则未在任何可读文档中定义。

#### Assumptions

- INFERRED：方案将 `token_analyzer.py` 作为静态验收的唯一度量来源（由「禁止同类脚本替换」推导）。
- UNKNOWN：脚本内部「中文感知」算法未被文档化，无法评估其对当前 spec 语言混合的精度。

#### Reversibility Analysis

脚本规则属代码层，可修订/替换；但一旦被设为权威且禁止替代，回退需先解除该约束。

#### Operational Impact

NO_MATERIAL_OPERATIONAL_IMPACT_IDENTIFIED

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

单一、未规格化的度量脚本成为验收硬依赖，增加长期维护耦合；其启发式若随 spec 语言演变而失真，需专人理解内部逻辑才能修正。

#### Source References

* §6 静态验收
* CR-003（口径锁定）

---

## Finding Summary

| Finding ID | Severity | Evidence Class                 | Confidence | Likelihood | Reversibility | Short Description |
| ---------- | -------- | ------------------------------ | ---------- | ---------- | ------------- | ----------------- |
| SC-001     | P1       | CONFIRMED_DEFECT               | HIGH       | HIGH       | REVERSIBLE    | Product/Test 证据子集被静默变更，违反「保持不变」契约 |
| SC-002     | P1       | CONFIRMED_DEFECT               | HIGH       | HIGH       | REVERSIBLE    | §6 枚举 grep「取值域一致」在全局域与子集间不可满足 |
| SC-003     | P1       | CONFIRMED_DEFECT               | HIGH       | HIGH       | REVERSIBLE    | System 字段契约不完整且与现有模板不符，重命名规则冲突 |
| SC-004     | P1       | CONFIRMED_DEFECT               | HIGH       | HIGH       | REVERSIBLE    | 质量护栏阈值未固化且 N≥2 基线统计不足，可判定目标落空 |
| SC-005     | P2       | MATERIAL_RISK                  | MEDIUM     | MEDIUM     | REVERSIBLE    | 静态降幅测量依赖未规格化脚本且禁止替换 |

---

## System Risk Coverage

| Risk Dimension                   | Status                    | Finding IDs |
| -------------------------------- | ------------------------- | ----------- |
| Data Integrity and Consistency   | NOT_APPLICABLE            | —           |
| Security Boundaries              | NOT_APPLICABLE            | —           |
| Authentication and Authorization | NOT_APPLICABLE            | —           |
| Availability and Resilience      | NOT_APPLICABLE            | —           |
| Failure Recovery                 | NOT_APPLICABLE            | —           |
| External Dependencies            | NOT_APPLICABLE            | —           |
| Concurrency and Race Conditions  | NOT_APPLICABLE            | —           |
| Data Lifecycle and Migration     | NOT_APPLICABLE            | —           |
| Backward Compatibility           | REVIEWED                  | SC-001, SC-003 |
| Operational Complexity           | REVIEWED                  | SC-004, SC-005 |
| Maintenance Burden               | REVIEWED                  | SC-001, SC-003, SC-005 |
| Irreversible Decisions           | REVIEWED                  | ID-001      |
| Over-Engineering                 | NOT_APPLICABLE            | —           |
| Observability and Diagnosis      | NOT_APPLICABLE            | —           |

> 说明：本方案为提示词/协议瘦身，无运行时数据存储、无鉴权边界、无并发/外部依赖/故障恢复等运行时风险；上述 `NOT_APPLICABLE` 维度与本方案范围无关。风险集中于**定义契约一致性**与**验收/回滚准则的可实现性**（见 SC-001…SC-005）。`Over-Engineering` 不适用：`references/common.md` 提取是去重所必需，未引入不成比例的抽象。

---

## Irreversible Decisions

### ID-001 — 将 `references/common.md` 设为证据等级/字段契约的权威单一来源（新增架构耦合）

#### Decision

建立 `references/common.md` 作为证据等级与字段契约的权威单一来源，被所有角色、模板、`SKILL.md`、`CLAUDE.md`、orchestrator 引用。

#### Why It Is Difficult to Reverse

一旦下游工具（合并/决策协议、`token_analyzer.py`）与所有审核产出依赖该文件，修改其结构需跨多文件协调编辑；它成为承载全局契约的共享依赖。

#### Reversal Cost

MEDIUM —— git revert 可行，但将分散定义重新耦合回各文件需较大工作量。

#### Risk

若 `common.md` 的契约本身有误或不完整（如 SC-001、SC-003 所示），错误会一次性传播到所有引用方。

#### Recommendation

在将其固化为权威源之前，先用 SC-001/SC-003 的方法对照所有当前角色/模板文件校验契约的完整性。

#### Status

OPEN

---

## Over-Engineering and Complexity Risks

未发现不成比例的架构复杂度。`references/common.md` 的提取用于消除跨文件重复，属方案核心机制，非过度设计。

---

## Unresolved System Questions

### Q-001 — 合并/决策协议当前是否已能识别全部四值（尤其 `CONFIRMED_GAP` 与新增的 Test `CONFIRMED_DEFECT`）？

#### Question

方案 §3.1/§4 第 8 条要求合并/决策协议「能识别全部四值（含 `CONFIRMED_GAP`）」，但 SC-001 指出现有 Test 子集并不含 `CONFIRMED_DEFECT`，方案却拟将其加入 Test。需确认现有 `consolidation-protocol.md` / `decision-protocol.md` 对来自 Test 的 `CONFIRMED_DEFECT` 与既有 `CONFIRMED_GAP` 的处理路径是否完备。

#### Why It Matters

若协议未预期 Test 产出 `CONFIRMED_DEFECT`，合并阶段可能错误处理该类 Finding，使 SC-001 的契约变更产生实际缺陷。

#### Required Clarification

核对 `consolidation-protocol.md` / `decision-protocol.md` 对四值（尤其是 `CONFIRMED_GAP` 与 Test `CONFIRMED_DEFECT`）的枚举覆盖；若不足，须在方案中补充。

#### Status

OPEN

### Q-002 — 瘦身后的实际 token 降幅能否达到 ≥40%，以及「中文感知」估算对当前 spec 语言混合的精度？

#### Question

静态降幅的 ≥40% 门依赖 `token_analyzer.py` 内部「中文感知」启发式（SC-005）。该启发式对中文/英文混合 spec 的估算精度未经验证。

#### Why It Matters

若估算失真，≥40% 头条目标可能建立在启发式假象上，使方案 A 的「成功」结论不可靠，并影响方案 B 的启动决策。

#### Required Clarification

提供估算规则的文档化定义，或对代表性 spec 做一次独立人工/工具计数交叉校验。

#### Status

OPEN

---

## Review Limitations

- 未逐行通读 `consolidation-protocol.md` / `decision-protocol.md` / `finding-protocol.md` 以验证「识别全部四值」与「Source Finding 完整性校验」的当前实现（仅确认其引用了证据等级枚举）。Q-001 因此保持开放。
- 未运行 `scripts/token_analyzer.py`（该文件尚不存在，属方案新增），对其内部「中文感知」算法无从直接验证（见 SC-005、Q-002）。
- 本审核仅评估方案文本的契约一致性与验收可实现性，不评估瘦身实施后的实际审核质量（那属于 §6 质量护栏的运行时职责）。

---

## Reviewer Conclusion

### Critical Finding Count

* P0: 0
* P1: 4
* P2: 1

### Risk Summary

* Security risks: 0
* Data integrity risks: 0
* Availability and resilience risks: 0
* Operational risks: 2（SC-004, SC-005）
* Maintenance risks: 3（SC-001, SC-003, SC-005）
* Irreversible decisions: 1（ID-001）
* Over-engineering risks: 0

### Review Result

REQUIRES_REVIEW

本审核识别出 4 项 P1 级契约/验收一致性缺陷与 1 项 P2 风险，均须在实施前澄清或修正。核心问题集中在三点：(1) 证据等级子集声明「保持不变」但与现状不符且未显式声明变更（SC-001）；(2) §6 枚举/字段一致性检查在其自身数据模型下不可机械满足（SC-002、SC-003）；(3) 质量护栏的「可判定」目标因阈值未固化、基线采样不足而未真正实现（SC-004），静态测量又依赖未规格化脚本（SC-005）。

System Critic 不决定上述发现最终是否被接受、拒绝、延期或另行处置；最终处置由 Decision Protocol 决定。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-04-review-002"
  reviewer: "yy-system-critic"
  review_type: "SYSTEM_REVIEW"
  status: "COMPLETED"

findings:
  - id: "SC-001"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "Product 与 Test 的证据等级子集被静默变更，违反保持不变契约"
    location: "§3.1 证据等级、§4 第8条；roles/product-reviewer.md、roles/test-designer.md"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§3.1 证据等级（全局域 + 每角色子集）"
      - "§4 第8条"
      - "roles/product-reviewer.md"
      - "roles/test-designer.md"
    risk_dimensions:
      - "Backward Compatibility"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-002"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "§6 枚举一致性 grep 取值域一致在全局域与子集间不可满足"
    location: "§6 一致性校验、§3.1 全局域与每角色子集"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§6 一致性校验"
      - "§3.1 全局域与每角色子集"
    risk_dimensions:
      - "Operational Complexity"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-003"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "System 字段契约不完整且与现有模板不符，重命名规则冲突"
    location: "§3.1 Finding 字段契约、§3.4、§6；templates/system-review.md"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§3.1 Finding 字段契约"
      - "§3.4 模板瘦身"
      - "§6 字段一致性 grep"
      - "templates/system-review.md"
    risk_dimensions:
      - "Backward Compatibility"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-004"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "质量护栏复现率阈值未固化且 N≥2 基线统计不足，可判定目标落空"
    location: "§6 质量护栏"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§6 质量护栏"
      - "CR-002"
    risk_dimensions:
      - "Operational Complexity"
    status: "PENDING_DECISION"

  - id: "SC-005"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "静态降幅测量依赖未规格化脚本且禁止同类脚本替换"
    location: "§6 静态验收；scripts/token_analyzer.py"
    likelihood: "MEDIUM"
    reversibility: "REVERSIBLE"
    source_references:
      - "§6 静态验收"
      - "CR-003"
    risk_dimensions:
      - "Operational Complexity"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

irreversible_decisions:
  - id: "ID-001"
    status: "OPEN"
    title: "将 references/common.md 设为证据等级/字段契约的权威单一来源"

complexity_risks:
  - id: "OC-001"
    status: "NOT_APPLICABLE"
    title: "未发现不成比例的架构复杂度"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "合并/决策协议是否完备识别全部四值（含 CONFIRMED_GAP 与新增的 Test CONFIRMED_DEFECT）？"
  - id: "Q-002"
    status: "OPEN"
    question: "瘦身实际 token 降幅能否达 ≥40%，中文感知估算精度是否可靠？"
```
