---
illustration_id: 02
type: flowchart
style: sketch-notes
palette: macaron
---

# DFA到正则表达式：状态消除法

Layout: step-by-step process flow

STEPS:
1. 原始DFA - 带有多个状态
2. 消除非初始/接受状态 - 逐个移除中间状态
3. 状态合并 - 组合进入/离开转移
4. 最终正则表达式 - 只剩下初始和接受状态

CONNECTIONS: 箭头从左到右展示转换过程
      中间步骤显示R_{pq} ○ R_{qr}* 的公式

KEY INSIGHTS:
- 如果 q_start = q_accept，正则表达式为ε
- 初始到接受路径的并 = 最终表达式
- 消除状态时，p → q → r 变为 p → r = R_{pq} ○ R_{qr}*

PALETTE: macaron — soft pastel color blocks
COLORS: DFA states in Macaron Blue (#A8D8EA), eliminated states in Coral Red (#E8655A),
        final expression in Mint (#B5E5CF), arrows in Black (#1A1A1A),
        Warm Cream background (#F5F0E8)
ELEMENTS: Hand-drawn flowchart showing 3-4 stages. Stage 1: complex DFA.
          Stage 2: DFA with X mark on one state. Stage 3: combined transitions.
          Stage 4: simplified DFA with 2 states, final regex shown below.
          Wavy arrows between stages. Small formula annotations.

STYLE: Hand-drawn educational flowchart on warm cream paper. Slight wobble on all lines.
        Hand-lettered stage labels. Generous white space.

Color values (#hex) and color names are rendering guidance only — do not display color names, hex codes, or palette labels as visible text in the image.

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords.

ASPECT: 16:9
