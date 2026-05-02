---
illustration_id: 05
type: framework
style: sketch-notes
palette: macaron
---

# Savitch定理：递归可达性

STRUCTURE: central recursion formula with surrounding explanation

NODES:
- 可达性函数 - REACH(q_a, q_b, t): t步内从q_a到q_b
- 递归公式 - ∃q_c REACH(q_a, q_c, ⌈t/2⌉) ∧ REACH(q_c, q_b, ⌊t/2⌋)
- 时间折叠 - 将t折叠到log t层
- 空间复杂度 - 每层只需O(s(n))空间

RELATIONSHIPS:
- 配置爆炸 - NSPACE(s)最多有2^{O(s)}个配置
- 空间优化 - 只存储当前可达性，不存储整个路径
- 非确定性优势 - "猜测"中间状态而非枚举所有可能

KEY MESSAGE: NSPACE(s(n)) ⊆ SPACE(s(n)²) for s(n) ≥ log n

PALETTE: macaron — soft pastel color blocks
COLORS: Formula in Coral Red (#E8655A), recursion levels in Macaron Blue (#A8D8EA),
        configurations in Lavender (#D5C6E0), Mint (#B5E5CF) for space savings,
        Warm Cream background (#F5F0E8), Black (#1A1A1A) for outlines
ELEMENTS: Hand-drawn framework. Center: large formula with circled "REACH".
          Surrounding: small boxes showing recursion tree with 2-3 levels.
          Annotations showing "O(s(n)) space", "2^{O(s)} configs",
          "guess vs enumerate". Wavy arrows connecting elements.

STYLE: Hand-drawn educational framework on warm cream paper. Slight wobble on all lines.
        Hand-lettered formulas and annotations. Generous white space.

Color values (#hex) and color names are rendering guidance only — do not display color names, hex codes, or palette labels as visible text in the image.

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords.

ASPECT: 16:9
