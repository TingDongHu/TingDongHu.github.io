---
illustration_id: 01
type: framework
style: sketch-notes
palette: macaron
---

# NFA等价于DFA：子集构造法

STRUCTURE: left-right mapping visualization

NODES:
- 左侧NFA - 非确定性有限自动机，状态可以有多个转移和ε转移
- 右侧DFA - 确定性有限自动机，每状态对每输入唯一转移
- 映射关系 - Q_D = P(Q_N)：DFA状态是NFA状态的子集

RELATIONSHIPS:
- ε闭包计算 - 从NFA状态出发，通过ε转移可达的所有状态集合
- 转移函数映射 - δ_D(S, a) = ε-closure(move(S, a))
- 接受状态 - 任何包含NFA接受状态的子集都是DFA接受状态

KEY MESSAGE: 非确定性没有增加计算能力，但需要指数状态数量

PALETTE: macaron — soft pastel color blocks
COLORS: NFA states in Macaron Blue (#A8D8EA), DFA subsets in Mint (#B5E5CF),
        arrows in Coral Red (#E8655A), Warm Cream background (#F5F0E8),
        Black (#1A1A1A) for outlines
ELEMENTS: Hand-drawn framework diagram. Left side: simple NFA with 3 states.
          Right side: DFA with power set states (shown as overlapping circles).
          Wavy arrows showing subset construction. Labels showing Q_D = P(Q_N).

STYLE: Hand-drawn educational framework on warm cream paper. Slight wobble on all lines.
        Hand-lettered state labels and formulas. Generous white space.

Color values (#hex) and color names are rendering guidance only — do not display color names, hex codes, or palette labels as visible text in the image.

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords.

ASPECT: 16:9
