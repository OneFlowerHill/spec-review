# spec-review — 设计规格结构化多视角审核技能

> 一套基于 Claude Code Skill 的 AI 审核方法论框架，通过三个独立视角（产品、系统、测试）并行审核 Design Spec，合并发现项，生成结构化审核文档供决策使用。

---

## 📋 项目简介

**spec-review** 是一个 Claude Code Skill（AI 审核技能），用于对 Design Spec（设计规格）进行结构化、多视角、独立审核。它不是可执行代码项目，而是一套由 Markdown 协议、角色定义和输出模板组成的方法论框架，供 Claude Code 的 skill 系统调用。

### 核心流程

```
Design Spec（设计规格）
    ↓
三角色 Subagent 并行独立审核
    ↓
Finding（发现项）合并与去重
    ↓
决策（规格所有者）
    ↓
规格修订
```

### 核心价值

- **独立视角**：三个审核员上下文隔离，互不阅读对方结论，避免群体思维
- **结构化发现**：每个 Finding 包含完整的因果链、证据分类和严重度评估
- **可追溯决策**：从发现到决策全程可追溯，不静默丢弃任何发现项
- **跨轮次追踪**：支持多轮审核，累积记录趋势和状态变化

---

## 🏗️ 架构概览

### 三角色独立审核 + 合并 + 决策

```
                    ┌─────────────────────┐
                    │   Design Spec 输入   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐ ┌───▼───────────┐ ┌──▼──────────────┐
    │  产品审核员 (PR)   │ │ 系统批评员(SC) │ │  测试设计师(TD)  │
    │  需求完整性？      │ │ 技术自洽性？    │ │  行为可验证？    │
    └─────────┬─────────┘ └────┬──────────┘ └──┬──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Finding 合并      │
                    │  去重/关联/冲突检测  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   决策交接          │
                    │  规格所有者做决策    │
                    └─────────────────────┘
```

### 审核流程（4 个 Phase）

| Phase | 名称 | 说明 |
|-------|------|------|
| 1 | **Context Acquisition** | 读取 Design Spec + 相关代码/测试/架构；记录 Consolidator Predispositions |
| 2 | **Independent Reviews** | 三个 subagent 并行审核，上下文隔离，互不阅读对方结论 |
| 3 | **Finding Consolidation** | 合并三个审核的 Finding，去重/关联/识别冲突；执行完整性校验 |
| 4 | **Output + Handoff** | 写入审核文件 + 更新 index.md；生成 Superpowers Instructions，等待规格所有者做决策 |

---

## 📁 项目结构

```
spec-review/
├── SKILL.md                          # Skill 主定义（单一入口，4 Phase 流程，subagent 并行审核）
├── CLAUDE.md                         # Claude Code 项目指导文件
├── update.sh                         # 自更新脚本（快进拉取最新版本）
├── agents/                           # 智能体接口定义
│   └── openai.yaml                   # 调用策略：allow_implicit_invocation: false（仅用户主动触发）
├── roles/                            # 审核员角色定义
│   ├── product-reviewer.md           # 产品审核员（product-reviewer）
│   ├── system-critic.md             # 系统批评员（system-critic）
│   └── test-designer.md             # 测试设计师（test-designer）
├── protocols/                        # 协议定义
│   ├── finding-protocol.md          # 发现协议——单个 Finding 的结构与质量标准
│   ├── consolidation-protocol.md    # 合并协议——跨审核员 Finding 的去重/关联/合并规则
│   ├── decision-protocol.md         # 决策协议——Finding 的最终处置
│   └── review-orchestrator-protocol.md  # 编排协议——主 agent 的调度与失败处理
├── templates/                        # 输出模板
│   ├── product-review.md            # 产品审核输出模板（PR-001 格式）
│   ├── system-review.md             # 系统审核输出模板（SC-001 格式）
│   ├── test-review.md               # 测试审核输出模板（TD-001 格式）
│   ├── consolidated-review.md       # 合并审核输出模板（CR-001 格式）
│   └── index.md                     # 跨轮次汇总模板
└── docs/                             # 文档
    ├── superpowers/
    │   ├── specs/                    # 设计规格输入
    │   └── plans/                    # 相关计划
    ├── 项目一期建设审查报告.md
    └── 项目二期审查报告.md
```

---

## 🎭 三角色边界

### 产品审核员（Product Reviewer）

- **核心问题**：需求是否完整一致？
- **评估维度**：需求完整性、业务规则、工作流完整性、状态转换、边界条件、数据生命周期、时间一致性、隐含假设
- **审核视角**：愤世嫉俗的 QA、沮丧的工程师、恶意/对抗性用户、过度劳累的管理员
- **Finding ID 前缀**：`PR-001`

### 系统批评员（System Critic）

- **核心问题**：技术方案是否自洽可靠？
- **评估维度**：数据完整性、故障恢复、并发/竞态、外部依赖、状态生命周期、可扩展性、安全边界、可观测性、部署/迁移/兼容性
- **审核视角**：首席工程师、可靠性与运维负责人、安全审核员、未来维护者
- **Finding ID 前缀**：`SC-001`

### 测试设计师（Test Designer）

- **核心问题**：行为是否可客观验证？
- **评估维度**：验收标准完整性、可观测结果、状态转换验证、边界验证、故障验证、数据完整性验证、时间验证、向后兼容验证、运维验证
- **审核视角**：QA 负责人、生产支持工程师、未来维护者
- **Finding ID 前缀**：`TD-001`
- **Finding Type**：`ACCEPTANCE_TEST` / `UNTESTABLE_REQUIREMENT` / `BLIND_SPOT`

---

## 📊 Finding 分类体系

### 严重等级

| 等级 | 含义 | 示例 |
|------|------|------|
| **P0** | 必须在继续前解决 | 核心需求失败、数据损坏、安全漏洞、不可恢复的系统故障 |
| **P1** | 通常应在实现前解决 | 重大功能失败、数据不一致、严重风险 |
| **P2** | 需评估但可延迟 | 边界情况、可维护性问题、中等风险 |

### 证据等级

| 等级 | 含义 | 使用角色 |
|------|------|----------|
| **CONFIRMED_DEFECT** | 规格/代码直接证明的问题 | 产品审核员、系统批评员 |
| **MATERIAL_RISK** | 未直接证明但后果严重的可信风险 | 所有角色 |
| **CONFIRMED_GAP** | 已确认的验证缺口 | 测试设计师 |
| **DESIGN_PREFERENCE** | 仅内部使用，不作为 Finding 输出 | 所有角色（分析阶段） |

### 合并后 Finding 关系分类

| 关系 | 含义 |
|------|------|
| `DUPLICATE` | 描述同一问题，证据高度重叠 |
| `SAME_ROOT_CAUSE` | 不同表现但共享同一根本原因 |
| `RELATED` | 有关联但可独立处置 |
| `INDEPENDENT` | 不应合并 |
| `CONTRADICTORY` | 对同一问题得出相反结论 |
| `SUBSET` | 一个 Finding 的范围完全包含在另一个中 |
| `CONSEQUENCE` | 一个 Finding 是另一个的直接因果后果 |

---

## 🔀 决策体系

### 决策状态

每个 Consolidated Finding 最终必须进入以下状态之一：

| 状态 | 含义 |
|------|------|
| `PENDING_DECISION` | 等待决策 |
| `ACCEPTED` | 接受——必须对规格或实现要求做出变更 |
| `REJECTED` | 拒绝——必须有具体理由 |
| `DEFERRED` | 延期——必须有明确的后续条件 |
| `PARTIALLY_ACCEPTED` | 部分接受——必须明确接受/拒绝/延期的范围 |
| `DUPLICATE` | 重复——必须引用权威 Finding |
| `INVALIDATED` | 失效——事实基础已被推翻 |

### 最终审核状态

| 状态 | 触发条件 |
|------|----------|
| `BLOCKED` | 存在未解决的 P0 Finding |
| `CHANGES_REQUIRED` | 已接受的 P1/P2 变更尚未完成 |
| `CONDITIONAL_APPROVAL` | 无阻塞 Finding，但仍有条件 |
| `APPROVED` | 所有必需变更已纳入 |
| `INCOMPLETE` | 审核记录不完整或有 MISSING 审核 |

---

## 📦 安装与更新

### 安装

本技能通过 Git 仓库分发。将仓库克隆到本地，或直接把 Git 地址交给 Claude / 其他智能体由其克隆：

```bash
git clone https://github.com/OneFlowerHill/spec-review.git
```

### 更新

在技能根目录运行自更新脚本，拉取最新版本（仅快进合并：不产生 merge commit、不丢失本地改动）：

```bash
bash update.sh
```

**让智能体代为更新** —— 直接对 Claude 或其他智能体说：

- `更新这个技能`
- `update this skill`
- `更新 spec-review`

智能体应在本技能根目录执行 `bash update.sh`（等价于 `git pull --ff-only`）。

> 说明：Claude Code / Codex 等工具对“通过 Git 地址克隆安装”的技能**没有内置自动更新机制**（内置的 `/plugin update` 仅适用于 marketplace 安装的技能）。这类技能的更新本质就是在本仓库执行 `git pull`，`update.sh` 对其做了安全封装。

### 已有用户迁移指南

若你之前从用友内部 git（`git@git.yyrd.com`）clone 过本技能，部署迁移到 GitHub 后，在旧 clone 副本执行：

```bash
git remote set-url origin https://github.com/OneFlowerHill/spec-review.git
gh auth setup-git   # 配置 git credential helper 使用 gh token（HTTPS 认证）
```

---

## 📝 使用方式

### 输入

Design Spec 文件放置于：

```
docs/superpowers/specs/<spec>.md
```

### 输出

每次审核创建新的 Review Round，不覆盖之前的轮次：

```
docs/superpowers/reviews/<spec-stem>/
├── index.md                          # 跨轮次汇总（累积更新）
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md             # 产品审核结果
    ├── system-review.md              # 系统审核结果
    ├── test-review.md                # 测试审核结果
    └── consolidated-review.md        # 合并审核结果
```

`<spec-stem>` 从规格文件名提取：移除 `YYYY-MM-DD-` 前缀和 `.md` 后缀。

**示例**：

```
输入规格：docs/superpowers/specs/2026-07-19-customer-operation.md
Stem：customer-operation
输出目录：docs/superpowers/reviews/customer-operation/2026-07-19-review-001/
```

### 触发方式

在 Claude Code 中使用以下方式触发审核：

- `review this spec`
- `审核这个规格`
- `run a spec review`

---

## 🔒 核心原则

### 审核原则

1. **不修改 Design Spec** —— 审核只产出 Finding，不直接改规格
2. **不跨角色阅读** —— 独立审核阶段，角色间互不参考
3. **不静默丢弃 Finding** —— 每个发现都必须有明确的处置记录
4. **不将假设升级为事实** —— 证据等级必须严格区分
5. **不在合并阶段做决策** —— 合并只组织问题，不做接受/拒绝判断
6. **不按关键词/组件/后果/严重度合并** —— 只按"同一根本问题"合并
7. **不压制少数派 Finding** —— 单一审核员的发现不能因其他审核员未发现而丢弃

### 质量保证

- **合并后必须执行完整性校验**：Source Finding 总数 = 合并引用 + 未合并 + 重复/取代记录
- **完整性校验失败时最终状态必须为 INCOMPLETE**：防止不完整审核被当作完整审核使用
- **严重度变更理由为强制字段**：必须引用具体源 Finding 证据，不得使用泛化推理
- **模板末尾的 Machine-Readable YAML 索引必须与详细内容保持同步**
- **Subagent 提示词不得包含主代理的分析**：只传递路径信息，禁止注入理解或假设
- **合并后必须记录 Consolidator Predispositions**：使认知偏差可审计

---

## 📐 协议体系

### Finding Protocol（发现协议）

定义单个 Finding 的通用结构与质量标准：

- 因果链要求：`触发条件 → Design Spec 行为 → 问题 → 后果`
- 证据分类：CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE
- 严重等级：P0 / P1 / P2
- 置信度：HIGH / MEDIUM / LOW
- Finding ID：审核员本地 ID（PR/SC/TD）→ 合并后全局 ID（CR）
- 每个审核员最多输出 5 个 Finding

### Consolidation Protocol（合并协议）

定义跨审核员 Finding 的去重、关联、合并规则：

- 7 种关系分类（DUPLICATE / SAME_ROOT_CAUSE / RELATED / INDEPENDENT / CONTRADICTORY / SUBSET / CONSEQUENCE）
- 根因分析
- 冲突检测与记录
- 证据合成（CONFIRMED / INFERRED / ASSUMED / UNKNOWN）
- 合并反模式：机械拼接、多数投票、严重度投票、强制共识、静默删除、过早决策、方案重设计

### Decision Protocol（决策协议）

定义 Finding 的最终处置与追踪：

- 7 种决策状态
- 决策权威要求
- 决策生命周期与变更历史
- 拒绝理由分类（INCORRECT_PREMISE / INAPPLICABLE_SCENARIO / IMMATERIAL_CONSEQUENCE / ALREADY_ADDRESSED / INTENTIONAL_BEHAVIOR / OUT_OF_SCOPE）
- 最终审核状态确定规则

### Review Orchestrator Protocol（编排协议）

定义主 agent 的调度、失败处理、完整性校验、交接：

- Subagent 标准化提示词模板
- 上下文隔离保证
- 失败重试机制（最多 1 次）
- MISSING 硬性规则
- Source Finding 完整性校验
- Consolidator Predispositions 记录

---

## 🔄 审核轮次与追踪

### 跨轮次追踪

`index.md` 累积记录所有审核轮次：

- **Review Rounds 表**：每轮的 P0/P1/P2 计数、接受/拒绝/延期计数、状态
- **Finding Tracking 表**：跨轮次的 CR-ID 追踪，链接前轮 Finding
- **Trend**：整体状态与开放 Finding 趋势

### Finding 跨轮次状态

| 状态 | 含义 |
|------|------|
| `PENDING_DECISION` | 等待决策 |
| `CARRIED_FORWARD` | 从前轮延期，仍然开放 |
| `RESOLVED` | 已接受且必需行动已实施 |
| `STILL_OPEN` | 已接受但必需行动尚未实施 |
| `REJECTED` | 未接受 |
| `INVALIDATED` | 事实基础已被推翻 |

---

## ✅ 已解决的不一致（v2 已修复）

1. ~~Finding ID 前缀冲突~~ → 统一为 CR-001，所有协议文件 RV→CR 已替换
2. ~~决策状态枚举冲突~~ → 统一为 decision-protocol.md 枚举
3. ~~Test Designer 输出格式~~ → 统一为 TD-001 + Finding Type 字段
4. ~~SKILL.md 缺少 YAML frontmatter~~ → 已添加
5. ~~Consolidator 角色文件缺失~~ → 主 agent 执行合并
6. ~~review-orchestrator 协议缺失~~ → 已创建
7. ~~审核对象路径偏差~~ → 主输入从 plans/ 迁移到 specs/
8. ~~consolidation-protocol.md RV 残留~~ → 已修复为 CR

---

## ⚠️ 当前约束

修改本项目时必须注意：

1. **CR-ID 是唯一的合并 Finding 标识** — 所有文件必须使用 CR-001 格式，不得使用 RV-001
2. **决策状态必须使用 decision-protocol 枚举** — 不得使用已废弃的 OPEN/READY_FOR_DECISION/RESOLVED/SUPERSEDED
3. **Test Designer Finding 必须包含 Finding Type** — ACCEPTANCE_TEST/UNTESTABLE_REQUIREMENT/BLIND_SPOT
4. **MISSING 审核的硬性规则** — 仅当 subagent 审核输出缺失时触发 MISSING
5. **合并后必须执行完整性校验** — Source Finding 总数 = 合并引用 + 未合并 + 重复/取代记录
6. **INCOMPLETE 状态触发条件** — MISSING 审核 + 完整性校验失败

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 运行平台 | Claude Code (CLI / Desktop / IDE Extension) |
| 技能定义 | Markdown + YAML Frontmatter |
| Subagent 调度 | Claude Code Agent Tool（并行调度） |
| 协议语言 | Markdown（结构化协议定义） |
| 输出格式 | Markdown + 嵌入式 YAML（Machine-Readable Index） |
| 版本控制 | Git |

---

## 🤝 贡献指南

### 修改原则

- **保持角色隔离**：不要让一个角色的定义引用另一个角色的结论
- **保持协议独立性**：每个协议文件应能独立理解，不依赖其他协议的内部细节
- **保持模板与协议同步**：模板结构变更必须反映在对应协议中
- **保持 Machine-Readable Index 同步**：详细内容变更必须同步到 YAML 索引
- **不引入已废弃的状态枚举**：始终使用 decision-protocol.md 定义的枚举

### 文件修改检查清单

- [ ] 是否影响 Finding ID 格式？（必须保持 CR-001 格式）
- [ ] 是否影响决策状态枚举？（必须使用 decision-protocol 枚举）
- [ ] 是否影响 Test Designer 输出？（必须包含 Finding Type）
- [ ] 是否影响合并逻辑？（不能按关键词/组件/后果合并）
- [ ] 是否影响完整性校验？（校验失败必须导致 INCOMPLETE）
- [ ] 模板和协议是否同步更新？
- [ ] Machine-Readable Index 是否同步更新？

---

## 📄 许可证

本项目为内部方法论框架，遵循组织内部使用许可。
