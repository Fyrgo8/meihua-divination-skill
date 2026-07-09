# 梅花易数解卦 Skill

这是一个公开的 Codex Skill 仓库，用来做 **结构化的梅花易数解卦**。

它的设计目标不是“写一段很长的 Prompt”，而是把 Skill 当成一个小型服务来做：有清晰的路由契约、输入输出契约、失败处理、确定性脚本和分层参考材料，方便后续迭代、复用和公开维护。

## 这个 Skill 解决什么问题

这个 Skill 面向的是：**用户已经有了卦例，或者已经给出了足够的起卦结果字段，希望按梅花易数做结构化解读。**

它当前重点覆盖四类任务：

- 完整逐步解卦
- 快速判断
- 卦例信息检查
- 对既有断语做复盘和审查

它明确 **不处理** 下面这些内容：

- 八字 / 四柱
- 紫微
- 六爻纳甲全体系
- 没有卦例的泛泛运势闲聊
- 从随机数字、声音、时间戳等原始输入自动起卦

## 当前采用的核心口径

这个 Skill 当前写死的默认逻辑是：

- `动卦为用，静卦为体`
- 旺衰不能只看月令，要同时看 `月令 + 卦气`
- 最终旺衰判断必须落到 `体相对用谁更强`
- 外应是高权重校验器，但不是自动推翻主断的覆盖器

## 仓库结构

```text
meihua-divination/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
├── references/
│   ├── modes.md
│   ├── output-contracts.md
│   └── workflow.md
├── resources/
│   └── case-input.example.json
└── scripts/
    └── normalize_case_input.py
```

## 关键文件说明

### `SKILL.md`

Skill 的薄契约层，负责：

- 路由条件
- 输入输出定义
- 执行步骤
- 失败处理
- 版本边界

### `references/workflow.md`

主解卦流程文档，负责定义这套 Skill 的九步断卦主轴。

### `references/modes.md`

不同模式的执行深度说明，目前包括：

- `intake`
- `quick-reading`
- `full-reading`
- `review`

### `references/output-contracts.md`

固定输出模板，保证不同模式下的输出结构稳定，不会每次都漂。

### `scripts/normalize_case_input.py`

一个低自由度的辅助脚本，只做结构化卦例输入校验与归一化，不负责真正解卦。

## 安装方式

### 方式一：作为本地 Codex Skill 安装

把仓库放到你的 Codex Skill 目录下，例如：

```text
C:\Users\<你的用户名>\.codex\skills\meihua-divination
```

随后重启 Codex，或者新开一个线程，让技能列表刷新。

### 方式二：打包成 `.skill`

如果你的环境里已经装了 `skill-creator`，可以先校验再打包：

```powershell
$env:PYTHONUTF8='1'
py -3 C:\Users\冯\.codex\skills\skill-creator\scripts\quick_validate.py C:\Users\冯\.codex\skills\meihua-divination
py -3 -m scripts.package_skill C:\Users\冯\.codex\skills\meihua-divination C:\Users\冯\.codex\skills\dist
```

## 示例触发语句

```text
问工作变动：上坤下乾，初爻动，泰之升，未月。按梅花易数完整断一下。
```

预期行为：

- 路由到 `full-reading`
- 先按 `动卦为用，静卦为体` 定体用
- 再看生克、旺衰、动爻、变卦、互卦、外应和错综
- 最后输出一份结构化断语，而不是散乱的玄学感想

## 设计思路

这个仓库遵循的是一种“Skill 作为微服务”的思路：

- 路由要准，宁可少触发，也别乱触发
- 主文件要薄，把大段方法细节下沉到 `references/`
- 确定性动作尽量下沉到 `scripts/`
- 失败场景要显式写出来，而不是藏在提示词气氛里
- 输出模板要固定，方便复盘和迭代
