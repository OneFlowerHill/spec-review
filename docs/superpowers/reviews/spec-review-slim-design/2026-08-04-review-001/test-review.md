# Test Review

## Review Metadata

### Review ID

2026-08-04-review-001

### Reviewer

yy-test-designer

### Review Type

TEST_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Review Date

2026-08-04

### Review Status

COMPLETED

---

## Review Scope

本审核评估该 Design Spec 在实现前是否可被客观验证。

审核聚焦于：

* 缺失的验收标准；
* 不可测试的需求；
* 未定义的预期结果；
* 缺失的边界条件；
* 失败恢复缺口；
* 数据完整性验证缺口；
* 状态流转验证缺口；
* 向后兼容验证缺口；
* 运维可观测性缺口；
* 长期回归风险。

本审核不做：代码质量评审、架构重设计、技术选型、完整测试计划、安全/性能测试替代，也不做最终批准决定。

本次被审核的 Design Spec 是一次「提示词/协议/角色/模板」重构提案，其"生产运行时"是 skill 的实际审核流水线，其"数据"是协议与角色文件中承载的规则定义，其"输出"是三份独立审核与一份合并审核。本审核据此判断：该重构的成功与失败是否可被客观区分。

---

## Findings

### TD-001 — 核心目标「不损失审核质量」缺少可判定的验收阈值，且单次前后对比无法区分质量回归与模型波动

#### Severity

P0

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

UNTESTABLE_REQUIREMENT

#### Location

Design Spec 第 0 节「目标」；第 6 节「回滚与验收 → 功能验收」第 2 条「Finding 数量与严重度分布基本一致」；第 6 节「回滚」条「若功能验收质量下降，直接 git revert」。

#### Verification Gap

Spec 的首要约束是「在不损失审核质量的前提下」完成瘦身，但唯一对应的验收判据是「Finding 数量与严重度分布**基本一致**」。缺失的验收标准有两层：

1. **阈值未定义**：「基本一致」没有给出可判定口径。Finding 数量差多少算一致（±1？±2？完全相等？）？严重度分布如何比较（P0 数量必须相同？P0+P1 合计？分布差异容忍度？）？三个角色分别比较还是合计比较？两名测试者用同一组前后产出，完全可能一个判「通过」、一个判「质量下降」。
2. **比较基准不成立**：本流水线的三份独立审核由 LLM subagent 生成，同一份 spec 重复运行本身就会产生不同的 Finding 集合与不同的严重度判定。Spec 只要求「改动前后各跑一次」，即单次对单次。这种设计无法把「瘦身导致的质量回归」与「同一提示词下的正常输出波动」区分开：数量不同不能证明退化，数量相同也不能证明没退化（内容可能已明显变浅）。

同一缺口直接传导到回滚判据：「质量下降」未定义，回滚触发条件同样不可判定。

#### Trigger Scenario

1. 前置条件：按 Spec 第 3 节完成角色/协议/模板瘦身，并已按第 6 节「留底」提交基线。
2. 动作：对 `docs/superpowers/specs/2026-07-20-chinese-output-support-design.md` 在改动前跑一次完整审核（得到 3 份独立审核 + 1 份合并审核），改动后再跑一次。
3. 应被判定的行为：判断瘦身是否损失了审核质量，并据此决定放行或 `git revert`。
4. 变得不可判定的点：改动前产出 12 个 Finding（P0×2 / P1×6 / P2×4），改动后产出 9 个 Finding（P0×1 / P1×5 / P2×3）。这是「质量下降必须回滚」，还是「正常波动可以放行」？Spec 未给出任何判定规则，也未要求重复运行以估计波动区间。结论只能由执行者主观裁量。

#### Expected Verification

测试者应当能够依据明确规则得出唯一结论，至少包括：

- 一个可计算的通过条件，例如：改动后每个角色的 Finding 数量不低于基线的某个下限；基线中的 P0/P1 Finding 必须有语义对应项被再次发现（可按问题主题人工对照并记录对应表）；
- 一个明确的比较对象与样本量，例如：同一 spec 至少运行 N 次以给出波动范围，或以「基线关键 Finding 复现率」而非「数量近似」作为主判据；
- 一个与之对应的、同样可判定的回滚触发条件。

#### Verification Method

当前未定义客观验证方法。Spec 仅给出「基本一致」「质量下降」这类主观表述，既没有量化阈值，也没有指定用于消除运行波动的比较协议。

#### Consequence

- 明显的质量退化可能通过验收：只要数量看起来接近，评审深度变浅（例如共享定义丢失后严重度普遍下调）不会被判为失败；
- 正常波动可能被误判为退化，触发不必要的 `git revert`，浪费整轮改造；
- 放行与回滚都建立在主观判断上，不同执行者对同一组产出可得出相反结论，验收结果不可复现；
- 由于回滚判据同样不可判定，即使事后发现质量下降，也难以证明"当时验收本应失败"。

#### Evidence

显式证据：第 0 节「在不损失审核质量、不改变三角色并行独立审核架构的前提下」；第 6 节「功能验收」第 2 条原文「Finding 数量与严重度分布基本一致」；第 6 节「回滚」原文「若功能验收质量下降，直接 git revert 到留底提交」。

推断部分：三份独立审核由 LLM subagent 生成（第 5 节「subagent 提示词仍指示…」、第 1 节「一次 Product Reviewer 真实抽样运行」），因此输出具有非确定性——该推断基于 Spec 自身对流水线形态的描述。

#### Recommendation

为「不损失审核质量」定义最小可判定验收标准，至少包含：

1. 明确比较口径：按角色分别比较，还是合计比较；比较对象是 Finding 数量、严重度分布，还是基线关键 Finding 的复现情况；
2. 明确通过阈值：给出数值化条件（例如"基线中所有 P0/P1 Finding 必须在改动后被语义等价地再次识别，允许缺失 0 条"）；
3. 明确消除波动的方法：例如同一 spec 前后各运行同样次数，或以人工对照的关键 Finding 复现表作为主判据、数量分布仅作参考；
4. 用同一套条件反向定义回滚触发条件，使「质量下降」成为可计算结论。

#### Source References

* Design Spec 第 0 节：目标
* Design Spec 第 6 节：回滚与验收 → 功能验收
* Design Spec 第 6 节：回滚与验收 → 回滚

#### Reviewer Notes

本 Finding 只针对验收判据的可判定性，不评价瘦身方案本身是否合理，也不主张必须引入自动化对比工具。

---

### TD-002 — 共享定义外移到 `references/common.md` 后，运行时是否真正生效无法验证，且失效表现为静默降级

#### Severity

P0

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

BLIND_SPOT

#### Location

Design Spec 第 3.1 节「新增 `references/common.md`」；第 3.2 节「瘦身角色文件」（删除严重度、证据等级、Finding 格式、独立评审规则等共享块，替换为对 `references/common.md` 的引用）；第 5 节「数据流向（行为不变）」第 1 条。

#### Verification Gap

第 3.2 节要求把严重度定义、证据等级定义、Finding 必填字段格式、独立评审/上下文隔离规则从三个角色文件中**删除**，改为「见 `references/common.md`」的引用；但第 5 节明确描述 subagent 的读取清单仍为「读 roles/X.md + templates/X.md + spec 路径」，其中**不包含** `references/common.md`。

由此产生的生产盲点是：瘦身后每个 subagent 的实际上下文里可能不再包含严重度/证据等级/Finding 格式/独立评审规则的任何定义，只剩一句指向另一个文件的引用。这种失效不会报错、不会中断流水线——subagent 仍会输出一份结构看似完整的审核文件，只是其中的 P0/P1/P2 判定、CONFIRMED_DEFECT/MATERIAL_RISK/CONFIRMED_GAP 归类、字段完整性都退化为模型的默认理解。

Spec 未定义任何可观测证据来区分「共享定义已在运行时生效」与「共享定义已丢失但输出看起来正常」。第 6 节的一致性校验只做静态 grep（确认字符串仍存在于文件中），恰恰无法覆盖这一运行时行为。

#### Trigger Scenario

1. 前置条件：按第 3.1/3.2 节完成改造，`references/common.md` 已建立，三个角色文件中的共享块已删除并替换为引用；Orchestrator 的 subagent 提示词按第 5 节保持不变（仍只指示读 roles + templates + spec）。
2. 动作：发起一次完整审核，三个 subagent 分别加载各自角色文件与模板并产出审核。
3. 应被判定的行为：subagent 在判定严重度与证据等级时，实际依据的是 `references/common.md` 中的权威定义。
4. 变得不可观测的点：subagent 是否真的加载了 `references/common.md`，Spec 未定义任何可观测信号；产出文件中仍会出现 P0/P1/P2 与 CONFIRMED_GAP 等枚举值（模型自行产生也会写出这些值），因此审核产出本身无法证明定义是否生效。第 6 节的四项功能验收全部通过的情况下，该失效仍可能存在。

#### Expected Verification

若要在生产中检出该失效，至少需要以下可观测证据之一：

- subagent 的实际读取行为可被观察或核对（例如审核产出中记录已加载的定义来源文件清单，或 Orchestrator 提示词中显式列出 `references/common.md` 并可被逐条核对）；
- 一个针对性的判别用例：故意让 `references/common.md` 缺失或内容被替换，预期结果是审核流程给出可识别的失败/告警信号，而不是照常产出一份"正常"的审核文件；
- 严重度/证据等级判定的一致性可被对照：例如同一段已知问题，在共享定义生效与不生效两种条件下产出的等级归类存在可观测差异，并记录为验收依据。

#### Verification Method

当前未定义客观验证方法。Spec 既未把 `references/common.md` 纳入 subagent 的读取清单，也未定义任何证明"共享定义已生效"的可观测结果；静态 grep 只能证明文件里有字符串，不能证明运行时被加载。

#### Consequence

- 严重度与证据等级判定失去权威依据，三个角色之间口径漂移，Phase 3 合并时的等级比较与冲突判定建立在不一致的基础上；
- 失效完全静默：不报错、不缺文件、不缺章节，四项功能验收均可通过；
- 质量退化会被 TD-001 中「基本一致」的模糊阈值进一步掩盖，最终以"验收通过"的形式发布；
- 该缺陷一旦上线，后续每一次真实审核都受影响，且事后难以归因（历史产出中没有任何字段记录当时是否加载了共享定义）。

#### Evidence

显式证据：第 3.2 节原文「删除：严重度、证据等级、Finding 格式、独立评审规则等共享块 → 替换为对 `references/common.md` 的引用」；第 5 节原文「subagent 提示词仍指示『读 roles/X.md + templates/X.md + spec 路径』」；第 6 节「一致性校验」原文仅为 grep 确认字符串存在。

推断部分：两处描述之间存在未被 Spec 解决的衔接问题——若 Orchestrator 提示词确实不变，则被删除的定义不会进入 subagent 上下文。本 Finding 关注的是"该风险没有任何验证手段"，此结论不依赖于该衔接问题是否为笔误。

#### Recommendation

在实现前明确并定义可验证条件：

1. 明确 subagent 的权威读取清单是否包含 `references/common.md`，并把该清单作为可核对的验收项；
2. 定义至少一个判别性验收用例：在 `references/common.md` 不可用或被篡改时，流水线应产生可识别的失败信号（而非静默产出），并规定该信号的观察位置；
3. 若选择不引入运行时信号，则至少要求每份审核产出中可追溯其依据的共享定义来源，使事后能够判断某次审核是否在共享定义生效的条件下完成。

#### Source References

* Design Spec 第 3.1 节：新增 `references/common.md`
* Design Spec 第 3.2 节：瘦身角色文件
* Design Spec 第 5 节：数据流向（行为不变）
* Design Spec 第 6 节：回滚与验收 → 一致性校验

#### Reviewer Notes

本 Finding 不主张保留角色文件中的重复定义，也不设计加载机制；仅指出"共享定义是否在运行时生效"目前没有任何可观测判据，而其失效方式是静默的。

---

### TD-003 — MISSING / INCOMPLETE 与 Source Finding 完整性校验属负向路径，Happy-Path 验收运行无法触发

#### Severity

P1

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

ACCEPTANCE_TEST

#### Location

Design Spec 第 4 节「质量不变量」第 4、5 条（MISSING 审核硬规则；INCOMPLETE 触发条件 = MISSING + 完整性校验失败；Source Finding 完整性校验：总数 = 合并引用 + 未合并 + 重复/取代）；第 6 节「功能验收」第 3、4 条（「Source Finding 完整性校验通过」「INCOMPLETE 逻辑 intact」）。

#### Verification Gap

第 4 节把 MISSING 硬规则、INCOMPLETE 触发条件与 Source Finding 完整性校验列为不可改动的质量不变量，而这三条逻辑正好位于被大幅压缩的 `consolidation-protocol.md`（1583 → ~700 行）中。但第 6 节定义的功能验收是一次**正常成功**的完整审核运行：三份独立审核正常产出、合并审核正常产出。在这种 happy-path 运行中：

- 不会出现任何角色审核缺失，MISSING 规则根本不被触发；
- 完整性校验不会失败，INCOMPLETE 分支不会进入；
- 「Source Finding 完整性校验通过」只证明"在所有 Finding 都被正常处理时公式成立"，无法证明"当有 Finding 被遗漏时校验会失败"——即无法区分"校验有效"与"校验被压缩时删掉了、恒返回通过"。

同时「INCOMPLETE 逻辑 intact」中的 intact 没有定义可观测判定：是指协议文件里还有这段文字（这是静态 grep 的事），还是指运行时确实会产出 INCOMPLETE 状态？Spec 未说明。

具体的验收测试场景缺失：没有任何一项验收会制造"缺失"或"不完整"的输入。

#### Trigger Scenario

1. 前置条件：`consolidation-protocol.md` 已按第 3.3 节压缩到约一半篇幅，压缩过程中不慎删除或弱化了完整性校验的失败分支（例如只保留了公式描述，删掉了"校验失败时如何处置"的规则）。
2. 动作：按第 6 节执行功能验收——用小 spec 跑一次完整审核，三个角色全部正常产出，合并正常完成。
3. 应被判定的行为：MISSING 硬规则、INCOMPLETE 触发条件、Source Finding 完整性校验在瘦身后依然有效。
4. 不可观测的点：本次运行从未进入任何负向分支，四项功能验收全部通过；被删弱的失败分支不会以任何形式暴露。缺陷会一直潜伏到未来某次真实审核出现角色产出缺失或 Finding 遗漏时才显现，而那时已无基线可比。

#### Expected Verification

应能通过故障注入型验收用例得到确定结论，例如：

- **MISSING 场景**：构造一次审核，其中某一角色的审核产出文件不存在或为空。预期可观测结果：合并阶段明确将该角色标记为 MISSING，而不是把剩余两份当作完整输入静默合并；
- **INCOMPLETE 场景**：在 MISSING 基础上使完整性校验失败。预期可观测结果：合并审核产出中出现 INCOMPLETE 状态；
- **完整性校验负向场景**：在合并输入中故意遗漏一条 Source Finding（使"总数 = 合并引用 + 未合并 + 重复/取代"不成立）。预期可观测结果：完整性校验**失败**并被显式记录，而不是通过。

这三个用例都有明确、唯一、可在合并审核产出文件中直接读到的预期结果。

#### Verification Method

当前未定义客观验证方法。第 6 节的四项功能验收全部基于一次正常运行；Spec 未定义任何制造 MISSING / 校验失败的验收场景，也未定义 INCOMPLETE 的可观测判定位置与形式。静态 grep（一致性校验）只能确认字符串存在，不能确认失败分支仍会被触发。

#### Consequence

- 被压缩掉的失败分支逻辑可以在四项验收全绿的情况下发布；
- 合并阶段可能在输入不完整时照常输出一份"看起来完整"的合并审核，遗漏的 Finding 永久丢失且无告警；
- 完整性校验退化为形式化步骤（恒通过）时无人察觉，第 4 节第 5 条的质量不变量名存实亡；
- 该退化只在真实审核出现异常输入时才显现，届时已无法与瘦身改动建立因果关系。

#### Evidence

显式证据：第 4 节第 4 条「MISSING 审核硬规则；INCOMPLETE 触发条件（MISSING + 完整性校验失败）」、第 5 条完整性校验公式；第 6 节「功能验收」列出的四项均描述正常产出情形；第 3.3 节表格显示 `consolidation-protocol.md` 从 1583 行压缩到约 700 行，且「Source Finding 完整性校验算法」被列为保留项——说明该逻辑确实位于被大幅改写的文件中。

推断部分：一次正常运行不会触发 MISSING/INCOMPLETE 分支，属逻辑必然，非猜测。

#### Recommendation

在功能验收中补充可判定的负向用例（最少三条），并为每条定义唯一预期可观测结果与观察位置：

1. 缺少一份角色审核产出 → 合并产出中该角色被标记 MISSING；
2. MISSING 且完整性校验失败 → 合并产出状态为 INCOMPLETE；
3. 输入中故意遗漏一条 Source Finding → 完整性校验判定失败并被显式记录。

同时把「INCOMPLETE 逻辑 intact」替换为上述可观测判据，避免以 intact 这类无判定口径的表述作为验收条件。

#### Source References

* Design Spec 第 4 节：质量不变量（第 4、5 条）
* Design Spec 第 6 节：回滚与验收 → 功能验收
* Design Spec 第 3.3 节：瘦身协议文件（consolidation-protocol.md）

#### Reviewer Notes

无。

---

### TD-004 — 「固定框架 tokens 降幅 ≥40%」的基线、口径与测量工具不可复现，量化验收结论不唯一

#### Severity

P1

#### Evidence Class

CONFIRMED_GAP

#### Confidence

HIGH

#### Finding Type

UNTESTABLE_REQUIREMENT

#### Location

Design Spec 第 0 节「目标」（固定框架开销降低 ≥40%）；第 1 节「量化结论」表格第 1 行（约 40–78K tokens，随 spec 大小变化）；第 6 节「静态验收」（重跑 `/tmp/yy_spec_token_analyzer.py` 同类脚本）；第 2 节各文件的目标行数（如 864 → ~400 行）。

#### Verification Gap

「降幅 ≥40%」形式上是一个数值判据，但构成该判据的三个要素都未被固定，导致结论不唯一：

1. **基线值未固定**：第 1 节给出的是区间「约 40–78K tokens」，并说明该值「随 spec 大小变化」。基线取 40K 还是 78K、用哪个 spec 测得，会直接改变分母。Spec 未记录一个具体的基线快照数值。
2. **统计口径自相矛盾**：同一行同时声称该开销「随 spec 大小变化」又「与 spec 内容无关」。若确实随 spec 大小变化，则"固定框架开销"的边界（是否包含 spec 本身、是否包含 SKILL.md、是否按 Phase 分别统计、是否计入 spec 被读取 4 次）就未被定义；第 1 节还专门指出 spec 4× 读取是大型 spec 的主导成本且本轮不动，这部分是否计入分母将显著改变降幅百分比。
3. **测量工具不可复现**：验收要求重跑「`/tmp/yy_spec_token_analyzer.py` **同类脚本**」。`/tmp` 下的脚本不受版本控制、随时可能不存在；「同类脚本」意味着允许换一个实现，而不同的 token 估算方法（中文感知估算尤其敏感）会得出不同数值。

此外第 2 节的目标行数使用「~400」「~700」这类近似值，未说明是硬性上限还是参考值：压缩后为 480 行算达标还是不达标，没有判定规则。

#### Trigger Scenario

1. 前置条件：瘦身完成，协议与角色文件均已压缩。
2. 动作：执行第 6 节「静态验收」，重跑 token 分析脚本，计算固定框架 tokens 降幅。
3. 应被判定的行为：降幅是否达到 ≥40%，即本次改造是否达成核心量化目标。
4. 变得不可判定的点：测试者 A 以 78K 为基线、统计口径包含 SKILL.md 与 CLAUDE.md，算出降幅 45%，判定达标；测试者 B 以 40K 为基线、口径仅含 4 个协议文件、并使用另一个"同类"估算脚本，算出降幅 32%，判定不达标。Spec 无法裁决谁正确。

#### Expected Verification

测试者应能得到唯一的量化结论，前提是 Spec 固定以下内容：

- 一个明确的基线数值及其测量条件（用哪个 spec、包含哪些文件、按哪个阶段统计），并作为可复查的记录留存；
- 一个明确的"固定框架开销"文件清单与是否计入 spec 读取的规则；
- 一个可复现的测量方法（脚本纳入仓库或明确指定估算规则），使前后两次测量在同一口径下可比；
- 第 2 节行数目标是硬指标还是参考值的说明。

#### Verification Method

当前未定义客观验证方法。基线为区间而非定值，统计口径存在内部矛盾，测量脚本位于 `/tmp` 且允许替换为"同类脚本"，因此前后两次测量不能保证在同一口径下产生可比数值。

#### Consequence

- 量化验收结果可被口径选择左右，实际未达标的改造可以被论证为达标（或相反）；
- 前后两次测量若使用不同脚本，降幅数字失去意义，核心目标事实上未被验证；
- 验收记录不可复查：未来无法重算当时的降幅，也就无法在方案 B（第 7 节）启动前判断方案 A 的真实收益；
- 由于第 7 节明确以"方案 A 落地且验证有效"作为方案 B 的前置条件，一个不可判定的量化结论会把后续决策也建立在主观判断上。

#### Evidence

显式证据：第 0 节「降低 ≥40%」；第 1 节表格「约 40–78K tokens（随 spec 大小变化，但与 spec 内容无关、且大量重复）」；第 1 节「spec 4× 读取…是大型 spec 的主导成本，但…本轮不动」；第 6 节「重跑 token 分析器（`/tmp/yy_spec_token_analyzer.py` 同类脚本），固定框架 tokens 降幅 ≥40%」；第 2 节「864 → ~400 行」等近似目标。

推断部分：不同 token 估算实现会给出不同数值——此为估算方法本身的性质，Spec 亦自述采用"中文感知估算"。

#### Recommendation

把量化目标改造为可复现判据，最小要求：

1. 在验收前记录一个具体基线数值，并写明其测量条件（测量所用 spec、纳入统计的文件清单、是否计入 spec 多次读取）；
2. 固定测量工具：将分析脚本纳入仓库（或明确写死估算规则），禁止以"同类脚本"替代；
3. 明确第 2 节行数目标是硬性上限还是参考值；
4. 要求验收结果以「基线值 / 改动后值 / 降幅 / 测量条件」四元组形式留存，可被独立复算。

#### Source References

* Design Spec 第 0 节：目标
* Design Spec 第 1 节：量化结论
* Design Spec 第 2 节：目标文件结构变化
* Design Spec 第 6 节：回滚与验收 → 静态验收

#### Reviewer Notes

本 Finding 不质疑 40% 这一目标值是否合理，只指出其当前不可被唯一判定。

---

### TD-005 — 单一小 spec 的单次验收无法覆盖合并阶段的关系分类与冲突记录能力，退化只会在真实审核中显现

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Finding Type

BLIND_SPOT

#### Location

Design Spec 第 3.3 节（`consolidation-protocol.md` 1583 → ~700 行，保留合并规则与关系分类 DUPLICATE / SAME_ROOT_CAUSE / RELATED / INDEPENDENT / CONTRADICTORY / SUBSET / CONSEQUENCE、冲突记录，砍掉「冗长 rationale、重复示例」）；第 6 节「功能验收」（用同一个小 spec 跑一次完整审核）。

#### Verification Gap

被压缩幅度最大的能力是合并阶段的**关系分类**与**冲突记录**——这类判断高度依赖被砍掉的 rationale 与示例（这正是模型判定 SAME_ROOT_CAUSE 与 RELATED、SUBSET 与 DUPLICATE 边界的主要依据）。但验收样本是「同一个小 spec」的一次运行。

问题在于：小 spec 产出的 Finding 少、跨角色重叠少，很可能整场运行只出现 INDEPENDENT 关系，根本不会触发 DUPLICATE、SUBSET、CONSEQUENCE，更不会触发 CONTRADICTORY 及其冲突记录路径。也就是说，压缩风险最集中的能力，恰好是验收覆盖不到的能力。

这类退化在生产中同样是静默的：合并审核照常产出，只是把本应判为 DUPLICATE 的两条 Finding 当成两条独立问题，或把三个角色对同一根因的描述拆成三条——产出文件结构完整，无任何异常信号，且由于第 4 节第 5 条的完整性公式在"全部按未合并处理"时依然成立，完整性校验也会通过。

#### Trigger Scenario

1. 前置条件：`consolidation-protocol.md` 压缩后，关系分类的判定依据（示例与 rationale）被大幅削减，枚举名称仍完整保留。
2. 动作：按第 6 节用小 spec 跑一次完整审核；由于 Finding 少且交叉少，本次合并只产生 INDEPENDENT 关系，且未触发任何冲突。
3. 应被判定的行为：瘦身后合并阶段仍能正确识别 DUPLICATE / SAME_ROOT_CAUSE / SUBSET / CONTRADICTORY 等关系并正确记录冲突。
4. 不可观测的点：本次验收从未产生这些关系，四项功能验收全部通过；一致性校验（grep）只能看到枚举名称仍在文件中，无法反映判定能力是否退化。缺陷延后到未来复杂 spec 的真实审核中才显现，而那时既无基线也无对照。

#### Expected Verification

若要在发布前检出该退化，应能观察到：

- 一次包含跨角色重叠 Finding 的合并运行结果——至少覆盖 DUPLICATE（两角色提出同一问题）、SAME_ROOT_CAUSE（不同表述同一根因）与 CONTRADICTORY（两角色给出相反判断）三类关系；
- 对每类关系，合并审核产出中应能直接读到：该关系被识别、参与合并的 Source Finding 被正确引用、冲突被显式记录；
- 该结果可与改动前同一输入下的合并结果逐条对照。

若要在生产中检出，则需要合并产出中保留可核对的关系判定痕迹（哪些 Source Finding 因何种关系被合并），使事后能判断关系分类是否失效。

#### Verification Method

当前未定义客观验证方法。验收只规定了一个小 spec 的一次正常运行，未要求覆盖任一关系分类分支，也未定义如何观察关系判定是否正确。

#### Consequence

- 合并阶段的关系分类与冲突记录能力可能已退化却通过全部验收；
- 生产中表现为合并质量下降（重复 Finding 未合并、根因被拆散、角色间冲突未被记录），但产出结构完整、完整性校验通过，属静默失效；
- 冲突未被记录时，决策阶段会在不知情的情况下对相互矛盾的 Finding 分别作出决定；
- 由于第 6 节的对比基线只覆盖同一个小 spec，该退化在事后无回归基线可用于归因。

#### Evidence

显式证据：第 3.3 节表格明确 `consolidation-protocol.md` 保留关系分类与冲突记录、砍掉「冗长 rationale、重复示例」，压缩幅度约 55%；第 6 节「功能验收」原文「用同一个小 spec…在改动前后各跑一次完整审核」。

推断部分：小 spec 的 Finding 数量与跨角色重叠较少，因而难以触发 DUPLICATE / CONTRADICTORY 等关系——该推断基于 Spec 自身对该 spec 的"小"的描述与关系分类的触发前提；本审核未读取该 spec 内容，故置信度记为 MEDIUM。

#### Recommendation

在验收中增加对关系分类与冲突记录的针对性覆盖，最小要求：

1. 至少补充一个能产生跨角色重叠与相互矛盾判断的验收输入（可使用已有的复杂 spec，或构造一组含重复/矛盾 Finding 的合并输入）；
2. 为 DUPLICATE、SAME_ROOT_CAUSE、CONTRADICTORY 三类关系各定义一条唯一预期结果，并指明在合并审核产出中的观察位置；
3. 明确要求合并产出中保留关系判定与冲突记录的可核对痕迹，使该能力在后续版本中仍可回归验证。

#### Source References

* Design Spec 第 3.3 节：瘦身协议文件（consolidation-protocol.md）
* Design Spec 第 4 节：质量不变量（第 5 条）
* Design Spec 第 6 节：回滚与验收 → 功能验收

#### Reviewer Notes

本审核未读取 `docs/superpowers/specs/2026-07-20-chinese-output-support-design.md` 的实际内容，对"该 spec 难以触发关系分类分支"的判断基于 Spec 自身的描述，故置信度为 MEDIUM。若该 spec 实际能够稳定产生跨角色重复与矛盾 Finding，本 Finding 的严重度可下调。

---

## Testability Coverage

记录本次评估覆盖的验证维度。

| Verification Dimension                 | Status         | Finding IDs      |
| -------------------------------------- | -------------- | ---------------- |
| Happy Path Verification                | REVIEWED       | TD-001, TD-005   |
| Boundary and Limit Verification        | REVIEWED       | TD-004           |
| Duplicate and Idempotency Verification | REVIEWED       | TD-005           |
| Invalid Input Verification             | REVIEWED       | TD-003           |
| Failure and Timeout Verification       | REVIEWED       | TD-003           |
| Partial Failure Verification           | REVIEWED       | TD-003, TD-005   |
| Data Integrity Verification            | REVIEWED       | TD-003           |
| State Transition Verification          | REVIEWED       | TD-002, TD-003   |
| Permission Boundary Verification       | NOT_APPLICABLE | —                |
| Backward Compatibility Verification    | REVIEWED       | TD-001, TD-002   |
| Temporal Verification                  | NOT_APPLICABLE | —                |
| Migration Verification                 | REVIEWED       | TD-002           |
| External Dependency Verification       | NOT_APPLICABLE | —                |
| Observability Verification             | REVIEWED       | TD-002, TD-004   |
| Recovery Verification                  | REVIEWED       | TD-001           |

标记为 NOT_APPLICABLE 的维度说明：

- **Permission Boundary Verification**：本次改动仅涉及仓库内的提示词、协议、角色与模板文档，Spec 未引入任何权限模型、访问控制或身份边界，无相应可验证行为。
- **Temporal Verification**：Spec 未定义任何时间相关行为（无过期、无延迟处理、无定时任务、无随时间累积的状态）；唯一的时间维度是历史审核产出的可比性，已在 Backward Compatibility 维度下经 TD-001 / TD-002 评估。
- **External Dependency Verification**：本次改动不引入外部系统、外部 API 或第三方集成；唯一的运行时依赖是 subagent 执行环境，其非确定性与加载行为已分别在 TD-001 与 TD-002 中评估，不重复列为独立维度。

---

## Unresolved Verification Questions

以下问题影响可验证性，但无法从当前 Design Spec 得到答案。

### Q-001 — 「Finding 数量与严重度分布基本一致」的判定阈值是什么

#### Question

改动前后的对比中，Finding 数量差异与严重度分布差异在多大范围内判定为「一致」？比较是按角色分别进行还是合计进行？是否需要对基线中的 P0/P1 Finding 逐条建立语义对应关系？

#### Why It Matters

这是「不损失审核质量」这一核心目标的唯一验收判据。阈值缺失导致放行与回滚均依赖主观裁量，两名测试者可对同一组产出得出相反结论，验收结果不可复现。

#### Required Clarification

需给出可计算的通过条件，以及消除 subagent 输出波动的比较协议（重复运行次数或以关键 Finding 复现率为主判据）。

#### Status

OPEN

---

### Q-002 — subagent 的权威读取清单是否包含 `references/common.md`

#### Question

第 3.2 节将共享定义从角色文件中删除并改为引用，而第 5 节描述 subagent 仍只读「roles/X.md + templates/X.md + spec 路径」。瘦身后 subagent 的读取清单究竟是什么？若不包含 `references/common.md`，共享定义如何进入其上下文？

#### Why It Matters

该问题决定了严重度、证据等级、Finding 格式、独立评审规则是否在运行时真实生效。答案不明确时，无法为该行为设计任何可观测的验收判据，失效将表现为静默降级。

#### Required Clarification

需明确读取清单，并给出「共享定义已生效」的可观测判据或判别性用例（例如共享定义缺失时应产生可识别的失败信号）。

#### Status

OPEN

---

### Q-003 — token 降幅的基线数值与统计口径如何固定

#### Question

「固定框架 tokens 降幅 ≥40%」的基线取值是多少（第 1 节给出的是 40–78K 区间）？统计口径包含哪些文件、是否计入 spec 的 4 次读取？测量脚本是否会纳入版本控制以保证前后可比？

#### Why It Matters

基线、口径与工具三者任一不固定，降幅结论即不唯一，量化验收失去判定力；且第 7 节把方案 B 的启动条件建立在方案 A「验证有效」之上，会将后续决策一并置于主观判断之上。

#### Required Clarification

需记录具体基线数值及其测量条件，固定文件清单与测量工具，并明确第 2 节各文件目标行数属硬性上限还是参考值。

#### Status

OPEN

---

## Review Limitations

以下信息限制实质影响了本次审核的部分结论置信度：

1. 本审核仅依据 Design Spec 本身进行，未读取被瘦身的现有协议、角色与模板文件的实际内容，因此无法判断"哪些具体规则会在压缩中丢失"，只能就 Spec 所声明的保留/删除项评估其可验证性。
2. 本审核未读取用于功能验收的样本 spec `docs/superpowers/specs/2026-07-20-chinese-output-support-design.md`，TD-005 中关于该样本覆盖能力不足的判断因此记为 MEDIUM 置信度。
3. 本审核未观察 Orchestrator 实际下发给 subagent 的提示词，TD-002 中关于运行时读取清单的部分依据 Spec 第 5 节的书面描述；但该 Finding 的核心结论（缺少验证手段）不依赖于该细节的最终取值。

---

## Reviewer Conclusion

### Critical Testability Finding Count

* P0: 2
* P1: 3
* P2: 0

### Finding Type Breakdown

* Acceptance Tests: 1
* Untestable Requirements: 2
* Blind Spots: 2

### Review Result

REQUIRES_REVIEW

本审核识别出的验证缺口集中于一点：该 Design Spec 的验收体系只能证明"流水线还能跑通"，无法证明"审核质量未下降"。两条 P0 分别对应核心目标不可判定（TD-001）与共享定义运行时失效不可观测（TD-002）；三条 P1 分别对应负向路径未被验收覆盖（TD-003）、量化目标不可复现（TD-004）与合并能力退化不可检出（TD-005）。五条 Finding 共同指向同一类风险：本次改造的主要失效模式都是静默的，而现有验收全部为 happy-path 与静态字符串检查。

本审核仅提出验证缺口、不可测试需求与生产盲点，供 Consolidation 阶段考虑。

Test Designer 不决定 Finding 最终被接受、拒绝、延期或以其他方式处置。

最终处置由 Decision Protocol 决定。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-04-review-001"
  reviewer: "yy-test-designer"
  review_type: "TEST_REVIEW"
  status: "COMPLETED"

findings:
  - id: "TD-001"
    severity: "P0"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "UNTESTABLE_REQUIREMENT"
    title: "核心目标「不损失审核质量」缺少可判定的验收阈值，且单次前后对比无法区分质量回归与模型波动"
    source_references:
      - "Design Spec 第 0 节：目标"
      - "Design Spec 第 6 节：回滚与验收 → 功能验收"
      - "Design Spec 第 6 节：回滚与验收 → 回滚"
    status: "PENDING_DECISION"

  - id: "TD-002"
    severity: "P0"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "BLIND_SPOT"
    title: "共享定义外移到 references/common.md 后，运行时是否真正生效无法验证，且失效表现为静默降级"
    source_references:
      - "Design Spec 第 3.1 节：新增 references/common.md"
      - "Design Spec 第 3.2 节：瘦身角色文件"
      - "Design Spec 第 5 节：数据流向（行为不变）"
      - "Design Spec 第 6 节：回滚与验收 → 一致性校验"
    status: "PENDING_DECISION"

  - id: "TD-003"
    severity: "P1"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "ACCEPTANCE_TEST"
    title: "MISSING / INCOMPLETE 与 Source Finding 完整性校验属负向路径，Happy-Path 验收运行无法触发"
    source_references:
      - "Design Spec 第 4 节：质量不变量（第 4、5 条）"
      - "Design Spec 第 6 节：回滚与验收 → 功能验收"
      - "Design Spec 第 3.3 节：瘦身协议文件（consolidation-protocol.md）"
    status: "PENDING_DECISION"

  - id: "TD-004"
    severity: "P1"
    evidence_class: "CONFIRMED_GAP"
    confidence: "HIGH"
    finding_type: "UNTESTABLE_REQUIREMENT"
    title: "「固定框架 tokens 降幅 ≥40%」的基线、口径与测量工具不可复现，量化验收结论不唯一"
    source_references:
      - "Design Spec 第 0 节：目标"
      - "Design Spec 第 1 节：量化结论"
      - "Design Spec 第 2 节：目标文件结构变化"
      - "Design Spec 第 6 节：回滚与验收 → 静态验收"
    status: "PENDING_DECISION"

  - id: "TD-005"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    finding_type: "BLIND_SPOT"
    title: "单一小 spec 的单次验收无法覆盖合并阶段的关系分类与冲突记录能力，退化只会在真实审核中显现"
    source_references:
      - "Design Spec 第 3.3 节：瘦身协议文件（consolidation-protocol.md）"
      - "Design Spec 第 4 节：质量不变量（第 5 条）"
      - "Design Spec 第 6 节：回滚与验收 → 功能验收"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "「Finding 数量与严重度分布基本一致」的判定阈值、比较口径与消除输出波动的方法是什么？"
  - id: "Q-002"
    status: "OPEN"
    question: "瘦身后 subagent 的权威读取清单是否包含 references/common.md？共享定义如何进入其运行时上下文？"
  - id: "Q-003"
    status: "OPEN"
    question: "token 降幅的基线数值、统计口径与测量工具如何固定，以保证前后测量可比且结论可复算？"
```

