---
illustration_id: 03
type: framework
style: sketch-notes
palette: macaron
---

# CFG到PDA：递归构造

STRUCTURE: central PDA with surrounding CFG rules

NODES:
- PDA核心组件 - 状态控制器、无限栈、输入带
- 栈操作 - 推入(PUSH)、弹出(POP)、匹配
- CFG规则 - A → w 的替换规则
- 递归匹配 - S → 0S1 | ε 的展开过程

RELATIONSHIPS:
- 栈顶变量 → 用规则右侧替换
- 栈顶终结符 → 匹配输入并弹出
- 栈只剩$ → 接受并停机

KEY MESSAGE: 栈的LIFO特性完美匹配CFG的递归结构

PALETTE: macaron — soft pastel color blocks
COLORS: PDA frame in Macaron Blue (#A8D8EA), stack in Mint (#B5E5CF),
        CFG rules in Lavender (#D5C6E0), arrows in Coral Red (#E8655A),
        Warm Cream background (#F5F0E8), Black (#1A1A1A) for outlines
ELEMENTS: Hand-drawn framework. Center: PDA showing stack with symbols [S, 0, S, 1, $].
          Surrounding: CFG rule boxes "S → 0S1" and "S → ε".
          Wavy arrows showing stack operations. Small annotations like "用规则替换",
          "匹配输入", "接受".

STYLE: Hand-drawn educational framework on warm cream paper. Slight wobble on all lines.
        Hand-lettered component labels. Generous white space.

Color values (#hex) and color names are rendering guidance only — do not display color names, hex codes, or palette labels as visible text in the image.

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords.

ASPECT: 16:9
