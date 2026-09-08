# Output Contracts

## Global Rules

- Default to Markdown.
- Start with the conclusion in plain language.
- Separate `direct hexagram support` from `inference`.
- Mark uncertainty explicitly.
- Keep structure flat and readable.
- 最终结论必须是单一明确方向。对“能不能/会不会/是否”必须明确写“能/不能”“会/不会”或“是/否”；禁止在结论中使用“有机会但”“倾向于”“可能”“取决于”“未必”等模糊或反向打补丁的表达。
- 不确定性、风险和条件只能放在证据段；不能用它们撤回结论。问题中的限定词（如“满意”“核心”“有含金量”）必须作为整体对象一次性判断。
- 解释本卦、互卦、变卦时，先写卦的通行本义和核心画面，再写当前问事对应；不能只报卦名或把卦名直接当吉凶。
- 本义必须独立说明六十四卦的卦名原义、上下卦组合画面和核心张力；不能用几个关键词代替，也不能把上下经卦单象冒充六十四卦本义。

## full-reading

Always use this template:

```markdown
# 梅花易数断卦

## 结论先说

结论先说必须是单一明确方向；风险与条件放到后文，不能在此处改写成模棱两可。

## 第一步：体用

先说明本卦的本义：卦名原义、上下卦组合画面和核心张力；再说明本义对应当前的局面。

## 第二步：体用生克

## 第三步：旺衰

## 第四步：动爻位置

## 第五步：变卦路径

## 第六步：变卦落点

先独立解释变卦的通行本义、上下卦组合画面和核心张力，再说明它在当前问题中的后续落点；标注哪些是卦象直接支持，哪些是条件推断。

## 第七步：互卦

先独立解释互卦的通行本义、上下卦组合画面和核心张力，再说明它如何补充事情的内部机制；互卦不是终局。

## 第八步：外应

## 第九步：错综

## 最后翻译成人话
- 整体结论：必须明确写成“会/不会”“能/不能”“成/不成”或“是/否”，只保留一个方向。
- 难点所在：
- 从哪里开始动：
- 哪些判断是硬支撑：
- 哪些地方仍需保留弹性：
```

### 第八步外应的补充规则

如果用户没有主动提供外应，`第八步：外应` 不得直接写成“没有外应”。必须使用下面的非阻塞结构：

```markdown
## 第八步：外应

本次未提供起卦瞬间的外应，这不等于没有外应。

你可以回想一下：起卦当下是否有突然来电、消息、异常提示音、有人叫你、器物碰撞或破损、雷声、断网断电、页面异常卡死或非预期弹窗等突兀事件？

- 若有：补充后可回头校验主断。
- 若无明显事件：按“无明显外应，本步不改主断”处理。
```

这段提示不能阻塞主断。用户没有补充时，继续基于本卦、变卦、互卦等主轴完成结论。

## Style Guardrails

- Do not turn the answer into mystical slogan fragments.
- Do not output bare labels without explanation.
- Do not silently import another divination system.
- When evidence is weak, prefer conditional phrasing over false certainty.
