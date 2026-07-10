# Output Contracts

## Global Rules

- Default to Markdown.
- Start with the conclusion in plain language.
- Separate `direct hexagram support` from `inference`.
- Mark uncertainty explicitly.
- Keep structure flat and readable.

## intake

Always use this template:

```markdown
# 卦例信息检查

## 已有信息
- 

## 必须补充
- 

## 可选补充
- 

## 现在能不能先断
- 可以 / 不可以
- 原因：
```

## quick-reading

Always use this template:

```markdown
# 快断结论

## 结论

## 主因
- 体用：
- 旺衰：
- 动爻起点：
- 变卦落点：

## 风险点
- 

## 下一步
- 
```

## full-reading

Always use this template:

```markdown
# 梅花易数断卦

## 结论先说

## 第一步：体用

## 第二步：体用生克

## 第三步：旺衰

## 第四步：动爻位置

## 第五步：变卦路径

## 第六步：变卦落点

## 第七步：互卦

## 第八步：外应

## 第九步：错综

## 最后翻译成人话
- 整体倾向：
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

## review

Always use this template:

```markdown
# 断语复盘

## 总评

## 站得住的部分
- 

## 逻辑跳步
- 

## 体系混入或口径冲突
- 

## 如果重断，应该怎么改
- 
```

## Style Guardrails

- Do not turn the answer into mystical slogan fragments.
- Do not output bare labels without explanation.
- Do not silently import another divination system.
- When evidence is weak, prefer conditional phrasing over false certainty.
