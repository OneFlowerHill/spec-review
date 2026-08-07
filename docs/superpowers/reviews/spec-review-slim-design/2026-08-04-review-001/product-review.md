# Product Review

## Review Metadata

### Review ID

2026-08-04-review-001

### Reviewer

yy-product-reviewer

### Review Type

PRODUCT_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Review Date

2026-08-04

### Review Status

COMPLETED

---

## Review Scope

本次审核从产品正确性、业务规则完整性、用户与执行者行为、工作流完整性、运维可操作性等角度评估该 Design Spec。

本次审核不评估：

* 实现质量；
* 源码质量；
* 详细系统架构；
* 技术选型；
* 基础设施设计；
* 性能优化；
* 测试实现细节。

本审核的目的是识别在实施前存在的、含义模糊、不完整、相互矛盾、不安全或定义不足的产品层需求。

需要说明的审核对象特点：该 Design Spec 的"产品"是一套供 AI agent 与人类维护者共同使用的审核流程规范，其"用户"包括触发审核的使用者、执行瘦身改造的执行者、以及作为运行主体的主 agent 与三个 subagent。本审核据此界定产品行为边界。

---

## Design Spec 完整性检查表

| 元素类别 | 状态 | 说明 |
| --- | --- | --- |
| Problem Definition | 覆盖 | §1 用静态 token 流模型与一次抽样量化了瓶颈，问题陈述清晰（固定框架开销大、协议与角色重复）。 |
| Desired Outcome | 部分覆盖 | 目标有量化值（固定框架开销 ≥40%）与质量约束（不损失审核质量），但后者缺乏可判定判据，前者的度量口径未定义 —— 见 PR-002、PR-003。 |
| Business Rules | 部分覆盖 | §4 给出 7 条质量不变量，但未声明该清单是否穷尽，也未定义与行数削减目标冲突时的优先级 —— 见 PR-005。 |
| Workflows | 部分覆盖 | §5 声明数据流向不变，但共享定义 `references/common.md` 的获取路径未纳入 subagent 读取链路 —— 见 PR-001。 |
| States and Transitions | 不适用 | 本方案不引入或修改实体状态机；decision 状态枚举被列为不可变更内容且不在本轮改动范围内。 |
| Boundary Conditions | 缺失 | 未定义大型 spec 场景下的预期收益边界、行数目标与保留内容冲突时的边界、验收结果的各种组合。 |
| Data Lifecycle | 缺失 | 未说明历史审核产出（旧模板生成）与跨版本审核轮次的处置 —— 见 Q-002。 |
| Assumption Declarations | 缺失 | 方案的根本假设"被删除的 rationale 与重复示例对 subagent 输出质量无实质贡献"未被显式声明，也未定义假设不成立时的处理方式 —— 相关风险见 PR-002、PR-005。 |

---

## Findings

### PR-001 — 共享定义 `references/common.md` 未纳入 subagent 读取链路，独立审核角色将失去严重度与证据等级的权威定义

#### Severity

P0

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

Design Spec §3.1「新增 `references/common.md`」（第 55–63 行）与 §5「数据流向（行为不变）」（第 102–106 行）之间的冲突。

#### The Gap

§3.1 规定：严重度定义、证据等级定义、Finding 必填字段格式、独立评审规则等内容从各角色文件中移出，集中到 `references/common.md`，各角色"以「见 `references/common.md`」引用，不再各自重述"。

§5 同时规定：subagent 提示词"仍指示「读 roles/X.md + templates/X.md + spec 路径」"。

Design Spec 因此把三类必备定义搬到了一个**不在 subagent 读取清单内**的文件中，却没有定义 subagent 如何获得这些定义。具体未定义的内容包括：

1. subagent 提示词的读取清单是否新增 `references/common.md`；
2. 若不新增，subagent 是否被要求跟随角色文件内的引用去自行读取该文件；
3. 若必须读取，哪些定义允许外链、哪些必须在角色文件内保留原文；
4. 若 subagent 需要额外读取 common.md，§5 声称的"每个 subagent 上下文更小"依据什么成立。

这不是实现细节缺失，而是产品工作流中一个必经环节（评审者获取判定标准）的行为未被定义。

#### Trigger Scenario

1. 执行者按 §3.1 将 P0/P1/P2 判据、CONFIRMED_DEFECT/MATERIAL_RISK 等证据等级定义、Finding 必填字段清单从 `roles/product-reviewer.md` 移入 `references/common.md`，角色文件中仅保留一行「见 `references/common.md`」。
2. 主 agent 按 §5 组装 Product Reviewer 的 subagent 提示词，读取清单仍为「roles/product-reviewer.md + templates/product-review.md + spec 路径」。
3. subagent 在隔离上下文中启动，读取瘦身后的角色文件，遇到指向 common.md 的引用。
4. Design Spec 未规定第 3 步之后的行为，出现两条均未定义的分支：
   * 分支 A：subagent 不读取 common.md —— 该评审者在缺少严重度判据与证据等级定义的情况下输出 Finding，severity 与 evidence_class 取值失去统一基准。
   * 分支 B：subagent 读取 common.md —— 其上下文为「瘦身后的角色文件 + common.md」，内容总量与瘦身前的单个角色文件基本相当，§5「每个 subagent 上下文更小」的收益结论不成立。
5. 无论走哪条分支，Design Spec 都没有给出预期行为。

#### Consequence

* 确认后果：三个独立评审 subagent 获取判定标准的路径在 Design Spec 中未定义，这是核心工作流的缺口。
* 逻辑后果（分支 A）：三份独立审核的严重度与证据等级不再基于同一判据，彼此不可比。合并阶段的关系分类（DUPLICATE / SAME_ROOT_CAUSE / RELATED 等）与 §4 第 5 条的 Source Finding 完整性校验将建立在口径不一致的输入之上，随后 decision 阶段依据这些结果做取舍，错误会沿链路传导且难以在事后追溯。
* 逻辑后果（分支 B）：§1 的收益估算与 §6 的 ≥40% 静态验收失去意义，因为运行时实际加载量并未下降（另见 PR-003）。
* 可能后果：由于 §4 第 6 条要求 subagent 提示词不得包含主 agent 分析，主 agent 也不能简单地把共享定义内联进提示词来兜底，缺口无法在实施期被"顺手"补上。

#### Recommendation

至少明确以下三项产品规则：

1. subagent 的读取清单是否新增 `references/common.md`，并据此更新 §5 的数据流向描述；
2. 若选择不新增，明确列出**必须在角色文件内保留原文、禁止外链**的定义集合（至少包括严重度判据、证据等级、Finding 必填字段）；
3. 按最终选定的方案重新表述 §5「每个 subagent 上下文更小」这一收益结论，避免把未成立的收益写入验收依据。

#### Evidence

* §3.1 第 63 行（显式）："各角色与模板以「见 `references/common.md`」引用，不再各自重述。"
* §3.1 第 58–59 行（显式）：被集中的内容包含证据等级与 Finding 必填字段格式。
* §5 第 104 行（显式）："subagent 提示词仍指示「读 roles/X.md + templates/X.md + spec 路径」；角色变小后每个 subagent 上下文更小。"
* §4 第 6 条（显式）："独立评审：subagent 提示词不得含主 agent 分析，角色间互不参考。"
* 缺失规则（显式缺失）：全文未出现任何关于 subagent 读取 `references/common.md` 的指令或约束。

#### Assumptions

* CONFIRMED — §3.1 明确要求角色文件不再重述共享定义。
* CONFIRMED — §5 明确 subagent 提示词的读取清单保持不变。
* INFERRED — subagent 运行于隔离上下文，无法从主 agent 上下文继承 common.md 的内容。
* UNKNOWN — subagent 是否会在无明确指令的情况下自发跟随文档内的相对路径引用去读取该文件；本 Finding 的成立不依赖该行为，因为两条分支均未被 Design Spec 定义。

#### Source References

* Design Spec §3.1（第 55–63 行）
* Design Spec §4 第 6 条（第 97 行）
* Design Spec §5（第 102–106 行）
* Design Spec §2 目标文件结构（第 30–31 行，新增 references/common.md）

---

### PR-002 — 核心约束「不损失审核质量」没有可判定的验收判据，回滚触发条件因此无法执行

#### Severity

P0

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

Design Spec 目标陈述（第 5 行）与 §6「回滚与验收」的功能验收条目（第 113–120 行）。

#### The Gap

Design Spec 把"不损失审核质量"作为整个方案的前置约束，但 §6 给出的对应验收判据是"Finding 数量与严重度分布**基本一致**"。该判据不可判定，缺失内容包括：

1. "基本一致"没有量化阈值 —— 例如改动前 Product Reviewer 产出 4 个 Finding（1 个 P0 / 2 个 P1 / 1 个 P2），改动后产出 3 个（0 个 P0 / 2 个 P1 / 1 个 P2），Design Spec 无法判定这是通过还是失败；
2. 未定义判定责任人（由执行者自评还是由第三方判定）；
3. 未定义基线波动的测量方式 —— 本审核流程由 LLM subagent 执行，同一提示词重复运行本身就会产生不同的 Finding 集合，Design Spec 只安排"改动前后各跑一次"的单样本对比，无法把"瘦身导致的质量下降"与"固有运行波动"区分开；
4. 验收样本被固定为一个小 spec（`2026-07-20-chinese-output-support-design.md`），而 §1 明确指出瘦身收益与风险在大型 spec 上才显著，样本代表性未被论证。

由于质量判据不可判定，§6 的回滚规则"若功能验收质量下降，直接 `git revert` 到留底提交"也就没有可执行的触发条件。

#### Trigger Scenario

1. 执行者按 §6 在改动前用指定小 spec 跑一次完整审核，记录基线：3 份独立审核 + 1 份合并审核，共 11 个 Finding，分布为 2 个 P0 / 6 个 P1 / 3 个 P2。
2. 执行者完成瘦身改造。
3. 改动后再跑一次，得到 9 个 Finding，分布为 1 个 P0 / 5 个 P1 / 3 个 P2；缺失的 P0 与基线中的某个 P0 并非同一问题。
4. 执行者对照 §6，判断"数量与严重度分布是否基本一致"—— Design Spec 没有阈值，也没有规定是否需要逐条比对 Finding 的实质内容（只提到"数量与严重度分布"）。
5. 执行者判定"基本一致"并放行；或另一位执行者判定"下降"并回滚。两种相反结论在 Design Spec 下都能自洽。
6. 后续无法确定该次放行是否掩盖了真实的质量回归。

#### Consequence

* 确认后果：方案的首要约束"不损失审核质量"在 §6 中没有对应的可判定验收项，验收流程无法证伪质量回归。
* 逻辑后果：质量回归可能被当作正常波动而放行，且由于瘦身直接改动的是判定标准与格式约束本身，回归表现为"Finding 变少、变浅、严重度评定漂移"，恰恰是最难被人工察觉的形式。
* 逻辑后果：反向误判同样可能 —— 正常波动被判定为回归而触发不必要的 `git revert`，使本轮工作被无依据地推翻。
* 可能后果：§7 规定方案 B "仅在方案 A 落地且验证有效后再评估"，该门槛依赖于同一套不可判定的验收结论，风险会向下一轮改造传导。

#### Recommendation

在 §6 中把质量约束转化为可判定判据，至少定义：

1. **基线波动的测量方式**：在改动前用同一版本对同一 spec 重复运行 N 次（N ≥ 2），记录 Finding 集合的波动范围，作为判定的对照基准；
2. **"基本一致"的量化定义**：明确以什么为比较单位（建议以 P0/P1 Finding 所指向的问题是否仍被覆盖为准，而非仅比较数量），并给出通过阈值；
3. **判定责任人**：明确由谁作出通过/不通过结论；
4. **样本要求**：验收样本至少包含一个大型 spec，或显式声明并接受"仅在小 spec 上验证"的局限；
5. **回滚触发条件**：与上述判据一一对应，使"质量下降"成为可判定事件。

#### Evidence

* 目标陈述第 5 行（显式）："在不损失审核质量、不改变'三角色并行独立审核'架构的前提下……"
* §6 第 115–117 行（显式）："Finding 数量与严重度分布基本一致"，无阈值、无判定人。
* §6 第 113 行（显式）：验收方式为"改动前后各跑一次完整审核"，即单样本对比。
* §6 第 120 行（显式）："若功能验收质量下降，直接 `git revert` 到留底提交。"
* §1 第 20 行（显式）：Design Spec 自身承认成本结构随 spec 大小变化，且大型 spec 的成本主导项不同，佐证小 spec 样本的代表性问题。
* 缺失规则（显式缺失）：全文未定义任何量化质量阈值或波动基线。

#### Assumptions

* CONFIRMED — §6 是本 Design Spec 中唯一定义质量验收方式的章节。
* INFERRED — 三个评审角色由 LLM subagent 执行，其输出存在固有的运行间波动；该推断由 §1 "抽样显示单个 subagent 产出 499 行 / 15.6KB 审核文件"这类以单次运行为观测样本的表述佐证。
* UNKNOWN — 该波动的实际幅度未被 Design Spec 测量，因此无法判断当前判据距离可用还差多少。

#### Source References

* Design Spec 目标陈述（第 5 行）
* Design Spec §1（第 19–20 行）
* Design Spec §6（第 110–120 行）
* Design Spec §7（第 128 行）

---

### PR-003 — 「固定框架开销降低 ≥40%」的度量口径未定义，静态验收可以通过而目标收益未必兑现

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

Design Spec 目标陈述（第 5 行）、§1 量化结论表（第 14–20 行）与 §6「静态验收」条目（第 118 行）。

#### The Gap

Design Spec 的目标是"将固定框架开销降低 ≥40%，**从而减少单次审核的 token 消耗与运行时间**"，而 §6 的静态验收只检查"固定框架 tokens 降幅 ≥40%"。这条因果链中的关键口径全部未定义：

1. **"固定框架"在新结构下包含哪些文件未定义**：新增的 `references/common.md` 是否计入未说明。
2. **按静态文件体积计还是按运行时实际加载量计未定义**：去重把三份重复内容合并为一份共享文件，静态文件总量必然下降；但运行时若三个 subagent 各读一次 common.md（PR-001 的分支 B），该内容在一次完整审核中仍被加载三次，实际 token 消耗与瘦身前基本持平。同一个"40%"在两种口径下结论相反。
3. **端到端目标缺失**：§1 自述"spec 4× 读取……是大型 spec 的主导成本，但……本轮不动"。既然主导成本不动，固定框架降 40% 对"单次审核 token 消耗"的实际改善幅度未被给出任何目标值或估算。
4. **"运行时间"完全没有验收项**：目标中列出的第二项收益在 §6 的四类验收中没有任何对应度量。
5. **基线不可复现**：§6 指定"重跑 token 分析器（`/tmp/yy_spec_token_analyzer.py` 同类脚本）"。该脚本位于临时目录、未纳入版本库，且措辞允许使用"同类脚本"，改动前后可能使用不同估算算法，两次数字不具可比性。

#### Trigger Scenario

1. 执行者按 §3.1、§3.2 把三个角色文件中重复的严重度、证据等级、Finding 格式、独立评审规则搬入 `references/common.md`。
2. 执行者按 §6 重跑 token 分析器，统计对象取"协议 + 角色 + 模板 + SKILL.md"的静态文件体积；由于共享内容从三份变为一份，且 common.md 未被计入统计清单，降幅达到 45%，静态验收通过。
3. 实际运行一次完整审核：三个 subagent 分别读取各自的瘦身角色文件后再各读一次 common.md，共享内容在本次审核中仍被加载三次。
4. 单次审核的实际 token 消耗与改动前相比几乎没有变化；若叠加额外的文件读取轮次，运行时间可能反而上升。
5. §6 的所有验收项均判定通过，Design Spec 未提供任何能发现该结果的检查点。

#### Consequence

* 确认后果：验收指标（静态文件体积降幅）与目标收益（单次审核的 token 消耗与运行时间）之间没有被定义的换算关系，前者达标不能证明后者达成。
* 逻辑后果：改造可能在通过全部验收的同时不产生真实收益，投入的改造与回归成本无法回收。
* 逻辑后果：§7 规定方案 B "仅在方案 A 落地且验证有效后再评估"，若"有效"的判定基于失真的静态指标，会得出错误的后续决策。
* 可能后果：由于 `/tmp` 下的脚本随时可能丢失，改动前的基线数字可能在验收时已无法复算，验收退化为对一个孤立数字的信任。

#### Recommendation

在 §6 中把度量口径定义清楚，至少包括：

1. 明确度量对象为**单次完整审核实际加载的 token 总量**（包含各 subagent 对同一共享文件的重复读取），而非静态文件字数；若坚持使用静态口径，需显式声明其局限并降低对目标收益的承诺；
2. 给出新结构下"固定框架"的文件清单，明确 `references/common.md` 是否计入以及按几次加载计；
3. 将分析脚本纳入版本库并固定版本，改动前后使用同一脚本、同一参数；
4. 对目标中的"运行时间"给出度量方式，或从目标陈述中移除该项收益承诺；
5. 结合 §1 已承认的"spec 4× 读取为大型 spec 主导成本"，给出端到端节省的预期区间，使收益预期与验收指标对齐。

#### Evidence

* 目标陈述第 5 行（显式）："将固定框架开销（协议 + 角色 + 模板）降低 ≥40%，从而减少单次审核的 token 消耗与运行时间。"
* §6 第 118 行（显式）："静态验收：重跑 token 分析器（`/tmp/yy_spec_token_analyzer.py` 同类脚本），固定框架 tokens 降幅 ≥40%。"
* §1 第 20 行（显式）："spec 4× 读取……是大型 spec 的主导成本，但属独立评审设计固有，本轮不动。"
* §3.1 第 63 行（显式）：共享内容被集中到单一文件，由多个角色引用。
* 缺失规则（显式缺失）：全文未定义"固定框架"的文件清单、未定义共享文件的计数方式、未定义运行时间的度量方式。

#### Assumptions

* CONFIRMED — §6 的静态验收是本 Design Spec 中唯一的收益度量方式。
* INFERRED — 三个评审 subagent 运行在互相隔离的上下文中，因此同一共享文件在一次审核中会被重复加载；该推断由 §4 第 6 条的独立评审要求支持。
* UNKNOWN — `/tmp/yy_spec_token_analyzer.py` 当前是否仍存在、其统计口径为何；本 Finding 不依赖该脚本的具体实现，仅依赖 Design Spec 对其位置与可替换性的表述。

#### Source References

* Design Spec 目标陈述（第 5 行）
* Design Spec §1 量化结论表（第 14–20 行）
* Design Spec §6 静态验收（第 118 行）
* Design Spec §7（第 126–128 行）

---

### PR-004 — 集中后的证据等级取值域与现有角色/模板不一致，且未定义共享定义与各文件冲突时的权威优先级

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

MEDIUM

#### Location

Design Spec §3.1 证据等级条目（第 58 行）与 §4 质量不变量清单（第 89–98 行）。

#### The Gap

§3.1 规定 `references/common.md` 集中收录四个证据等级：CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE。

但现有 Product 侧的规范只承认更小的取值域：`roles/product-reviewer.md` 只定义 CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE 三值，并明确要求不把 DESIGN_PREFERENCE 作为 Finding 输出；`templates/product-review.md` 的字段说明与 Machine-Readable 索引进一步把 evidence_class 限定为 CONFIRMED_DEFECT|MATERIAL_RISK 两值。

Design Spec 把四值统一集中，却没有定义：

1. 集中后各角色**允许使用的证据等级子集**是否发生变化；
2. 当 `references/common.md` 与角色文件、模板、协议文件对同一概念的规定不一致时，**以哪一份为准**（§4 只把 decision-protocol 的状态枚举列为权威，未对共享定义作同类规定）；
3. 各角色的 evidence_class 取值域是否属于必须保持不变的质量不变量 —— §4 的七条清单中没有这一项。

#### Trigger Scenario

1. 执行者按 §3.1 在 `references/common.md` 中写入四个证据等级的含义与用法。
2. 执行者按 §3.2 删除 `roles/product-reviewer.md` 中本地的证据等级定义，改为引用 common.md。
3. Product Reviewer 依据 common.md 判定某个 Finding 属于 CONFIRMED_GAP 并如实填写。
4. 同一份产出的 Machine-Readable 索引依据 `templates/product-review.md` 的约束，其 evidence_class 只允许 CONFIRMED_DEFECT 或 MATERIAL_RISK。
5. Design Spec 未定义此时以哪一份规定为准，也未定义合并阶段遇到超出模板取值域的 evidence_class 时的处理方式。
6. 三个角色可能各自收敛出不同的取值域，且这种偏差不会触发 §6 的任何验收项。

#### Consequence

* 确认后果：Design Spec 声明要集中的取值域与现有 Product 角色/模板的取值域不一致，且未给出收敛规则或优先级规则。
* 逻辑后果：Machine-Readable 索引的 evidence_class 取值可能超出模板声明的枚举范围，破坏该索引"可被合并协议直接消费"的用途。
* 逻辑后果：同等强度的证据在不同角色下被标注为不同等级，合并阶段的关系分类与去重判断随之失真，进而影响 decision 阶段的取舍。
* 可能后果：历史审核产出使用旧取值域，与新取值域并存后，跨轮次的统计与比较口径不一致。

#### Recommendation

在 Design Spec 中补充两条规则：

1. 定义证据等级的**全局取值域**以及**每个角色允许使用的子集**，并说明集中到 common.md 后各角色取值域是否发生变化（若发生变化，需说明这是有意的行为变更而非瘦身副作用）；
2. 定义 `references/common.md` 与角色文件、模板、协议文件冲突时的权威优先级；并明确"各角色 evidence_class 取值域保持不变"是否应加入 §4 质量不变量。

#### Evidence

* §3.1 第 58 行（显式）："**证据等级**：CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE 的含义与用法。"
* `roles/product-reviewer.md`（现状，显式）：Evidence Classification 章节仅定义 CONFIRMED_DEFECT、MATERIAL_RISK、DESIGN_PREFERENCE，并规定"Do not normally report DESIGN_PREFERENCE as a finding"。
* `templates/product-review.md`（现状，显式）：Finding 字段说明为 "CONFIRMED_DEFECT / MATERIAL_RISK"，Machine-Readable 索引为 `evidence_class: "CONFIRMED_DEFECT|MATERIAL_RISK"`。
* §4（显式缺失）：七条质量不变量中只有第 2 条把 decision 状态枚举列为权威，未涉及证据等级取值域，也未给出共享定义的优先级规则。

#### Assumptions

* CONFIRMED — §3.1 明确列出四个证据等级作为集中对象。
* CONFIRMED — 现行 Product 角色定义与 product-review 模板的取值域小于四值。
* UNKNOWN — CONFIRMED_GAP 当前是否为其他角色（如 Test Designer）专用取值；本次审核未查阅其他角色文件。若确为其他角色专用，则本 Finding 的本质是"集中后各角色取值域的收敛规则缺失"，结论不变。
* UNKNOWN — 合并与决策协议当前是否已能处理 CONFIRMED_GAP。

#### Source References

* Design Spec §3.1（第 58 行、第 63 行）
* Design Spec §4 第 2 条（第 93 行）
* `roles/product-reviewer.md` — Evidence Classification
* `templates/product-review.md` — Finding 字段定义与 Machine-Readable Finding Index

---

### PR-005 — 「可删除内容」的判定标准是主观描述，且行数削减目标与质量不变量的优先级未定义

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec §2 目标文件结构中的行数目标（第 37–40 行）、§3.2（第 65 行）、§3.3 的「砍掉」列（第 73–78 行）与 §4 质量不变量清单（第 89–98 行）。

#### The Gap

Design Spec 给出了硬性的削减目标（finding-protocol 864 → ~400 行、consolidation-protocol 1583 → ~700 行、decision-protocol 1557 → ~700 行、角色文件"各砍 ~40–50%"），但对"什么内容可以删"只给出主观描述："冗长 rationale、重复示例"、"冗余 prose"、"重复陈述"。由此产生三处未定义：

1. **判定标准与判定人未定义**：谁、依据什么标准判断某段文字属于"冗长 rationale"而非有效约束。
2. **§4 是否为穷尽清单未声明**：§4 前言称"以下规则一条不动"，但未说明"未被列入的规则"是可自由删除、还是同样需要保留。现行角色文件中存在大量未出现在 §4 中的规范性语句（例如"输出不超过 5 个 Finding"、"不得把 MATERIAL_RISK 呈现为 CONFIRMED_DEFECT"、"不得为凑数制造 Finding"、"不得把个人偏好当作产品缺陷"等），这些语句直接约束输出质量。
3. **冲突时的优先级未定义**：当保留全部有效约束后行数仍高于目标、或静态降幅达不到 ≥40% 时，Design Spec 未规定是以行数/降幅目标为准还是以保留质量约束为准。

#### Trigger Scenario

1. 执行者按 §2 的行数目标改写 `consolidation-protocol.md`（1583 → ~700 行）。
2. 删到 ~850 行时，剩余内容中已无明显重复，但仍高于目标。
3. 执行者面对一段既像"冗长 rationale"、又实际承载判定约束的文字（例如说明为何某类 Finding 不应被合并的推理段落），Design Spec 未提供判定标准。
4. 执行者查阅 §4，该规则不在七条不变量之列，且 Design Spec 未声明清单是否穷尽。
5. 执行者为达成行数目标删除该段。
6. §6 的功能验收因 PR-002 所述原因无法发现由此产生的质量变化，删除结果被固化。

#### Consequence

* 确认后果：Design Spec 没有定义可删除内容的判定标准，也没有定义行数目标与质量约束冲突时的优先级。
* 逻辑后果：删除决策依赖执行者个人判断，而该判断被一个硬性行数指标反向驱动 —— 指标压力指向"多删"，而唯一的质量护栏（§4 七条）覆盖面明显小于现有规范性语句的总量。
* 可能后果：承载质量的约束被静默移除，且由于 Design Spec 未要求记录删除项，后续维护者无法区分某条规则是被有意删除还是被误删，也无法定向回滚（§6 的回滚是整体 `git revert`，粒度为整次改动）。

#### Recommendation

补充三条最小规则：

1. 声明 §4 是否为穷尽清单；若不穷尽，明确"删除任一规范性语句（含祈使句形式的约束、禁止项、数量上限）需逐条记录理由"；
2. 明确行数目标与 ≥40% 降幅为**参考值**，当其与保留质量约束冲突时以保留约束优先，并规定此时的处理方式（接受较小降幅还是转入方案 B）；
3. 要求瘦身产出附一份"删除项清单"，使删除决策可被复核、可被定向恢复。

#### Evidence

* §2 第 37–40 行（显式）：给出各协议文件的目标行数。
* §3.2 第 65 行（显式）："瘦身角色文件（各砍 ~40–50%）"。
* §3.3 第 75–77 行（显式）：「砍掉」列内容为"冗长 rationale、重复示例"、"冗余 prose"、"重复陈述"。
* §4 第 91 行（显式）："以下规则一条不动"，随后列出七条；全文未说明该清单是否穷尽。
* `roles/product-reviewer.md`（现状，显式）：存在多条未被 §4 覆盖的规范性约束（Finding 数量上限、证据等级不得升格、禁止制造 Finding 等）。
* §6（显式缺失）：验收项中没有任何针对"规范性语句是否被完整保留"的检查（"一致性校验"仅 grep CR-ID、decision 枚举、Finding Type 三项）。

#### Assumptions

* CONFIRMED — §2、§3.2 给出的是数值化削减目标。
* CONFIRMED — §4 未声明其清单的穷尽性。
* INFERRED — 现有角色与协议文件中存在大量未被 §4 覆盖、但对输出质量有实质约束作用的语句；本推断基于对 `roles/product-reviewer.md` 与 `templates/product-review.md` 现状的直接查阅。
* UNKNOWN — 协议文件中"冗长 rationale"的实际占比，即在完整保留所有约束的前提下能否达成行数目标；本次审核未查阅协议文件正文。

#### Source References

* Design Spec §2（第 37–40 行）
* Design Spec §3.2（第 65–70 行）
* Design Spec §3.3（第 73–78 行）
* Design Spec §4（第 89–98 行）
* Design Spec §6 一致性校验（第 119 行）

---

## Finding Summary

| Finding ID | Severity | Evidence Class | Confidence | Short Description |
| ---------- | -------- | -------------- | ---------- | ----------------- |
| PR-001 | P0 | CONFIRMED_DEFECT | HIGH | 共享定义 `references/common.md` 未纳入 subagent 读取链路，评审角色获取判定标准的路径未定义 |
| PR-002 | P0 | CONFIRMED_DEFECT | HIGH | 「不损失审核质量」缺乏可判定验收判据（"基本一致"无阈值、单样本对比未处理运行波动），回滚触发条件不可执行 |
| PR-003 | P1 | CONFIRMED_DEFECT | HIGH | ≥40% 降幅的度量口径与基线不可复现，静态指标达标不能证明目标收益兑现，运行时间无度量 |
| PR-004 | P1 | CONFIRMED_DEFECT | MEDIUM | 集中后的证据等级取值域与现有角色/模板不一致，共享定义与各文件冲突时的权威优先级未定义 |
| PR-005 | P1 | MATERIAL_RISK | MEDIUM | 「可删除内容」判定标准主观，§4 不变量清单穷尽性未声明，行数目标与质量约束的优先级未定义 |

---

## Product Risk Coverage

| Risk Dimension | Status | Finding IDs |
| -------------- | ------ | ----------- |
| State Machine Vulnerabilities | NOT_APPLICABLE | — |
| Hard Boundaries and Limits | REVIEWED | PR-003, PR-005 |
| Data Lifecycle | REVIEWED | Q-002 |
| Backward Compatibility | REVIEWED | PR-004, Q-002 |
| Implicit Assumptions | REVIEWED | PR-002, PR-005 |
| Business Rule Conflicts | REVIEWED | PR-004, PR-005 |
| Temporal Consistency | REVIEWED | Q-002 |
| User Workflow Integrity | REVIEWED | PR-001 |
| Administrative Operability | REVIEWED | PR-002, PR-003, PR-005 |
| Abuse and Misuse Scenarios | REVIEWED | PR-003 |

`NOT_APPLICABLE` 说明：

* **State Machine Vulnerabilities** —— 本方案不引入也不修改任何实体状态机；唯一涉及的状态枚举（decision 状态）被 §4 第 2 条列为不可变更内容且明确不在本轮改动范围内，因此不存在状态迁移层面的产品风险。证据等级取值域的冲突属于取值域一致性问题，已在 Business Rule Conflicts 维度下以 PR-004 记录。

**Abuse and Misuse Scenarios 说明**：本维度在此处不指外部用户攻击，而是指验收指标可被形式满足（指标达标而目标未达成）这类"对规则的无意识规避"，对应 PR-003。

---

## Unresolved Product Questions

### Q-001 — 验收结果的组合情形未穷尽，"方案 A 验证有效"的判定标准缺失

#### Question

§6 只定义了一种处置分支："若功能验收质量下降，直接 `git revert`"。质量与降幅两个维度共有四种组合，其余三种的处置规则未定义，尤其是"质量未下降但静态降幅低于 40%"应当接受、重做还是转入方案 B。同时 §7 规定方案 B "仅在方案 A 落地且验证有效后，再评估是否启动"，但"验证有效"未被定义。

#### Why It Matters

改造完成后大概率落入未定义分支（部分达标是最常见结果），此时缺少处置规则会导致由执行者临时裁量，且会直接影响后续是否启动方案 B 的判断。该问题与 PR-002、PR-003 同源（判据缺失），但其独立缺口是"结果组合的处置规则"，未被上述 Finding 覆盖。

#### Required Clarification

补充四种验收结果组合各自的处置规则，并给出"方案 A 验证有效"的判定条件。

#### Status

OPEN

---

### Q-002 — 瘦身落地后历史审核产出与跨版本审核轮次的处置未定义

#### Question

已有的历史审核产出由旧模板与旧取值域生成。瘦身改动模板字段说明与共享定义后：历史产出是否仍需按新规范可解释、可比较？若一次审核轮次的三份独立审核在改动前生成、合并阶段在改动后执行（改造期间发起审核即会出现），是否允许，如何处理？

#### Why It Matters

§4 第 7 条只保证输出路径与轮次结构不变，未涉及内容口径的跨版本一致性。若历史产出与新规范的取值域或字段口径不一致，跨轮次的统计与回溯比较会失去共同基准；混版轮次则可能使合并阶段的完整性校验建立在两套口径之上。

#### Required Clarification

明确 (a) 历史产出是否需要迁移或仅需保持"按生成时版本解读"；(b) 是否禁止跨版本审核轮次，或给出跨版本时的处理规则。

#### Status

OPEN

---

## Review Limitations

以下信息限制对本次审核的判断有实质影响：

1. 本次审核未查阅 `roles/system-critic.md`、`roles/test-designer.md` 以及四个协议文件的正文，因此：PR-004 中 CONFIRMED_GAP 的现有归属标记为 UNKNOWN；PR-005 中"协议文件里可删冗余的实际占比"标记为 UNKNOWN。这两项不确定性不影响相应 Finding 的核心结论（缺少收敛规则、缺少删除判定标准），但降低了 PR-004 与 PR-005 的置信度至 MEDIUM。
2. §1 引用的量化数据（固定框架 40–78K tokens、Phase 3 协议块约 13K tokens、抽样产出 499 行 / 15.6KB）来自 Design Spec 自述，其原始测量数据与脚本未随 Design Spec 提供，本次审核未独立复核。PR-003 的结论不依赖这些数字的准确性，仅依赖口径定义的缺失。
3. §6 指定的验收样本 `docs/superpowers/specs/2026-07-20-chinese-output-support-design.md` 的实际规模未在本次审核中核实；PR-002 关于样本代表性的论述基于 Design Spec 自身对该样本"小 spec"的描述。
4. Design Spec 未提供瘦身后 `references/common.md` 的草稿内容，因此 PR-001 与 PR-004 只能基于 §3.1 声明的收录范围进行判断。

以上限制不构成对分析深度的免责，相关 Finding 的证据均取自 Design Spec 显式文本或本次审核实际查阅过的现行角色/模板文件。

---

## Reviewer Conclusion

### Critical Finding Count

* P0: 2
* P1: 3
* P2: 0

### Review Result

REQUIRES_REVIEW

本次审核识别出的产品层缺口需由 Consolidation 阶段纳入考量。

整体判断：该 Design Spec 对"要改什么"描述清晰，但对"改完如何证明没改坏"与"共享化之后行为如何运转"定义不足。两个 P0 分别指向工作流缺口（评审者获取判定标准的路径）与验收缺口（质量约束不可判定），二者叠加会形成一个危险组合 —— 最可能出问题的环节，恰好也是现有验收最看不见的环节。

Product Reviewer 不决定这些 Finding 最终被接受、拒绝、延后或以其他方式处置，最终处置由 Decision Protocol 确定。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-04-review-001"
  reviewer: "yy-product-reviewer"
  review_type: "PRODUCT_REVIEW"
  status: "COMPLETED"

findings:
  - id: "PR-001"
    severity: "P0"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "共享定义 references/common.md 未纳入 subagent 读取链路，评审角色获取判定标准的路径未定义"
    location: "Design Spec §3.1 与 §5"
    source_references:
      - "Design Spec §3.1（第 55-63 行）"
      - "Design Spec §4 第 6 条（第 97 行）"
      - "Design Spec §5（第 102-106 行）"
    risk_dimensions:
      - "User Workflow Integrity"
      - "Implicit Assumptions"
    status: "PENDING_DECISION"

  - id: "PR-002"
    severity: "P0"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "核心约束「不损失审核质量」没有可判定的验收判据，回滚触发条件无法执行"
    location: "Design Spec 目标陈述（第 5 行）与 §6 功能验收"
    source_references:
      - "Design Spec 目标陈述（第 5 行）"
      - "Design Spec §6（第 110-120 行）"
      - "Design Spec §1（第 19-20 行）"
    risk_dimensions:
      - "Implicit Assumptions"
      - "Administrative Operability"
    status: "PENDING_DECISION"

  - id: "PR-003"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "≥40% 降幅的度量口径未定义且基线不可复现，静态验收通过不能证明目标收益兑现"
    location: "Design Spec 目标陈述、§1 量化结论、§6 静态验收"
    source_references:
      - "Design Spec 目标陈述（第 5 行）"
      - "Design Spec §1（第 14-20 行）"
      - "Design Spec §6（第 118 行）"
    risk_dimensions:
      - "Hard Boundaries and Limits"
      - "Abuse and Misuse Scenarios"
      - "Administrative Operability"
    status: "PENDING_DECISION"

  - id: "PR-004"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "MEDIUM"
    title: "集中后的证据等级取值域与现有角色/模板不一致，共享定义的权威优先级未定义"
    location: "Design Spec §3.1 证据等级条目与 §4 质量不变量清单"
    source_references:
      - "Design Spec §3.1（第 58 行）"
      - "Design Spec §4 第 2 条（第 93 行）"
      - "roles/product-reviewer.md — Evidence Classification"
      - "templates/product-review.md — Machine-Readable Finding Index"
    risk_dimensions:
      - "Business Rule Conflicts"
      - "Backward Compatibility"
    status: "PENDING_DECISION"

  - id: "PR-005"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "可删除内容的判定标准主观，行数削减目标与质量不变量的优先级未定义"
    location: "Design Spec §2 行数目标、§3.2、§3.3 砍掉列、§4 质量不变量"
    source_references:
      - "Design Spec §2（第 37-40 行）"
      - "Design Spec §3.2（第 65-70 行）"
      - "Design Spec §3.3（第 73-78 行）"
      - "Design Spec §4（第 89-98 行）"
    risk_dimensions:
      - "Business Rule Conflicts"
      - "Hard Boundaries and Limits"
      - "Implicit Assumptions"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "验收结果的四种组合中只有一种定义了处置规则，且「方案 A 验证有效」的判定标准缺失"
  - id: "Q-002"
    status: "OPEN"
    question: "瘦身落地后历史审核产出的可解释性与跨版本审核轮次的处置规则未定义"
```

