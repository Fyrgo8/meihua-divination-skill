---
name: meihua-divination
description: "Interpret Meihua Yishu hexagrams into structured judgments when the user provides a formed hexagram or enough raw casting info such as upper/lower trigram, moving line, question context, and optional month/day or external signs, and wants a step-by-step reading, intake check, or drill review. Do not use for Bazi, Ziwei, full Liuyao NaJia analysis, generic fortune talk without a hexagram, or purely historical discussion. Output one of: missing-info checklist, structured reading, or teaching-style review."
compatibility: "Optional local Python for structured case normalization via scripts/normalize_case_input.py."
---

# Meihua Divination

## 路由契约（触发 AND / 排除 OR）

### 触发 AND
- 同时满足下面两类条件各至少一项：
- `梅花对象`：用户给出本卦/变卦/互卦、上卦下卦、动爻、体用、月令、日辰、外应，或明确说的是梅花易数起卦结果。
- `梅花任务`：用户要的是解卦、断卦、复盘一卦、检查断卦流程、按步骤教学、把零散卦例整理成结构化判断。
- 如果请求同时包含“卦例对象 + 解读任务”，优先触发本 Skill，不要退化成泛泛玄学闲聊。

### 排除 OR
- 用户问的是 `八字 / 四柱 / 合盘 / 紫微 / 六壬 / 奇门 / 塔罗 / 星盘`。
- 用户要的是完整 `六爻纳甲` 体系，如六亲、六神、世应、伏神、旬空、月破等，不是梅花主轴。
- 用户没有给出任何卦例，只是要生活建议、情绪安慰、决策代办。
- 用户要的是梅花易数历史、流派考据、书单、概念科普，而不是实际解卦。
- 用户只要排版整理现有结论，不要重新断卦。

### 高频触发表达
- 中文：`帮我解这个梅花卦`、`按梅花易数断一下`、`复盘这卦哪里断歪了`、`这卦体用怎么定`、`把这个卦例整理成完整断语`
- English mixed: `read this meihua hexagram`, `review my meihua reading`, `walk through this hexagram step by step`

### 路由优先级
- `梅花卦例的结构化解读 / 复盘 / 教学` -> 本 Skill
- `八字合婚 / 大运流年` -> 对应命理 Skill，不触发本 Skill
- `六爻纳甲细断` -> 不触发本 Skill
- `纯理论介绍` -> 通用问答，不触发本 Skill

## 必需输入（字段: 类型 / 示例 / 缺失默认行为）

| 字段 | 类型 | 示例 | 缺失默认行为 |
| --- | --- | --- | --- |
| `task_mode` | 字符串 | `intake` / `quick-reading` / `full-reading` / `review` | 由模型根据用户目标判定；无法判定时按 `intake -> full-reading` 走 |
| `question_context` | 字符串 | `问华为 offer 能不能过` | 缺失时先追问问事对象与关注点；不要直接开断 |
| `hexagram_source` | 字符串或结构化对象 | `泰之升，初爻动` / `上坤下乾，一爻动` | 若能从上下文唯一还原则继续；否则只追问最小缺口 |
| `time_context` | 字符串或结构化对象 | `未月，庚申日` | 默认可缺；仅在旺衰难分时再要求更完整信息 |
| `external_signs` | 字符串或列表 | `起卦时杯子摔碎`、`面朝西，下雨` | 默认可缺；缺失不等于“没有外应”，`full-reading` 的第八步必须给出非阻塞回忆提示，禁止编造 |
| `output_target` | 字符串 | `chat` / `markdown` | 默认 `chat`；若用户说“整理成清单/笔记”，默认 `markdown` |

## 执行步骤（标注执行者：模型 / 脚本）

### 资源加载规则
- 触发后先读本文件，不要默认整包加载所有参考材料。
- 只在需要时加载：
- `references/workflow.md`：九步断卦主流程与边界
- `references/modes.md`：不同任务模式的执行深度
- `references/output-contracts.md`：固定输出模板
- `scripts/normalize_case_input.py`：当用户给的是 JSON 或字段化卦例时，做低自由度校验与归一化
- `resources/case-input.example.json`：用户要求结构化样例时再引用

### 执行闭环
1. `模型`：判定任务模式。
   从用户请求中判断当前是 `intake / quick-reading / full-reading / review` 哪一种。若用户说“帮我看看”，但信息不完整，先进入 `intake`。

2. `模型`：校验输入契约。
   最少确认 `问什么 + 卦怎么起出来的或已经成了什么卦`。信息不够时，只补齐最小缺口，不要开放式盘问。

3. `脚本 + 模型`：必要时归一化卦例输入。
   如果用户提供结构化字段或文件，优先运行 `scripts/normalize_case_input.py` 做字段校验；脚本只负责确定性检查，不负责解卦。

4. `模型`：读取 `references/workflow.md`，按主轴断卦。
   必须先走 `体用 -> 生克 -> 旺衰 -> 动爻位置 -> 变卦路径 -> 变卦落点 -> 互卦 -> 外应 -> 错综`，不要见一象断一象。

5. `模型`：读取 `references/modes.md` 中对应模式的小节。
   `quick-reading` 压缩输出，`full-reading` 逐步展开，`review` 专查别人断语中的逻辑跳步和口径混乱。

6. `模型`：读取 `references/output-contracts.md`，按固定模板产出。
   始终先给结论，再给证据；明确区分“卦象支持”“推断补充”“信息不足”。

7. `模型`：做失败前自检。
   检查是否出现：体用没定稳、把卦名直接当吉凶、把外应硬贴成结论、混入六爻纳甲术语、在信息不足时强断。发现后先降级说明，再输出。

### 自由度控制
- 当前 Skill 采用“脚本处理确定性校验，模型处理解释判断”的分层方式。
- 低自由度动作：
- 字段完整性检查
- 八卦名与动爻序号校验
- 结构化案例转成统一 JSON 或 Markdown 工作单
- 高自由度动作：
- 体用判定
- 旺衰权衡
- 变卦、互卦、外应的综合解释
- 最终断语写作

## 输出格式（固定模板或 JSON Schema）

### 通用要求
- 默认输出 Markdown。
- 先给人话结论，再展开九步依据。
- 任何不确定处都要显式标注 `这里是推断，不是硬证据`。
- 不要混入完整六爻纳甲系统的六亲、六神、世应等术语，除非用户明确要求切换体系。

### 模式到输出的固定映射
- `intake` -> `缺什么 / 为什么缺 / 补到什么程度就能断`
- `quick-reading` -> `结论 / 主因 / 风险点 / 下一步`
- `full-reading` -> `完整九步断卦 + 最终落人话`
- `review` -> `原断语哪里站得住 / 哪里跳步 / 应该怎样改`

## 失败处理（场景 / 检测 / 动作）

| 场景 | 检测 | 动作 |
| --- | --- | --- |
| 卦例不完整 | 只有问题，没有卦；只有卦名，没有动爻也无说明 | 进入 `intake`，只索要最小必要字段 |
| 体系混杂 | 用户同时提六亲、世应、旬空、八字十神等 | 明确提示当前 Skill 只按梅花主轴断；若要切体系，先停下 |
| 体用不清 | 动静分配不明、上下两卦都动、或用户明确采用其他流派 | 先按“动卦为用、静卦为体”复核；若仍歧义，再退回主体/客体原则并显式说明 |
| 旺衰难判 | 只看月令拉不开强弱，或月令与卦气给出的方向不一致 | 先分开说明月令与卦气各自怎么影响，再落到体用相对强弱；若仍不足，降低结论强度 |
| 外应未提供 | `full-reading` 中没有给出起卦瞬间的外应 | 不要写成“无外应”；在第八步给出常见现象的非阻塞回忆提示，主断仍可继续 |
| 外应喧宾夺主 | 只凭一个突兀事件推翻全部卦象 | 把外应退回“高权重校验”，重新审视主断 |
| 结论过满 | 信息不完整却直接断成败时间点 | 显式改写为区间判断或条件判断 |
| 用户其实要理论 | 问的是“梅花易数怎么学”而非具体卦例 | 不走完整断卦链，转为简短说明或建议对应学习流程 |

## 示例（正例 + 反例）

### 正例
- `问工作变动：上坤下乾，初爻动，泰之升，未月。按梅花易数完整断一下。`
- `我断这个卦总觉得哪里不对：问感情，体用比和，变卦是解。你帮我复盘逻辑漏洞。`
- `我只有这些字段：问 offer、上卦离、下卦乾、五爻动、申日。先帮我检查信息够不够。`

### 反例
- `帮我看八字什么时候结婚。`
- `用六爻纳甲断这个卦。`
- `给我推荐几本易经入门书。`
- `我最近很焦虑，怎么办。`

## 版本边界

- 当前版本是 `会话触发型 Skill`，目标是 `高精度路由 + 稳定解卦输出`，不是自动起卦器。
- 当前版本不负责：
- 从随机数字、时间戳、声音等原始材料自动起卦
- 六爻纳甲全体系断法
- 八字、紫微等跨体系联断
- 后续如扩展起卦功能，优先新增脚本或子 Skill，而不是继续把本文件堆大。
