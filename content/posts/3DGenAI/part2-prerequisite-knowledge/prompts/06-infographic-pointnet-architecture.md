---
illustration_id: 06
type: infographic
style: vector-illustration
palette: macaron
---

# PointNet系列架构

## Layout
Two-tier vertical layout: top tier shows "PointNet" architecture flow (left to right), bottom tier shows "PointNet++" hierarchical architecture (left to right). A connecting arrow between them labeled "升级: 局部特征". Title "PointNet系列" at top.

## ZONES
- **Title Zone**: Top center, "PointNet 系列" in large handwritten font with scattered dot decoration
- **Top Tier - PointNet**:
  - Input: scattered points {x₁,...,xₙ}
  - Shared MLP: box with "h(xᵢ)" label, applied to each point independently
  - Max Pooling: large "MAX" operation box
  - Output: global feature vector
  - T-Net branch: small side path showing input alignment
- **Bottom Tier - PointNet++**:
  - Three repeating modules shown as stages:
    - Stage 1: "FPS采样" → "Ball Query分组" → "Mini-PointNet"
    - Stage 2: Same pattern with fewer points (showing downsampling)
    - Stage 3: Feature Propagation (upsampling back)
  - Show point cloud getting sparser then denser
- **Right Side - Theorem Box**: Symmetry theorem statement in a highlighted box
- **Bottom Comparison**: 2D CNN analogy table

## LABELS
- **PointNet labels**: "输入: {x₁,...,xₙ}⊂R³", "共享MLP h: R³→R^K", "对称函数: MAX", "γ∘MAX({h(xᵢ)})", "T-Net: x' = A·x 输入对齐", "置换不变: f(S)=f(π(S))", "全局特征"
- **PointNet++ labels**: "FPS 最远点采样", "Ball Query 半径r查询", "Mini-PointNet 局部特征", "特征传播 上采样插值", "n_sample→更少→更少", "局部→全局 逐层提取"
- **Theorem Box**: "对称性定理", "共享MLP + Max Pooling", "= 置换不变函数的通用逼近器", "∀ε>0, ∃h,g: |f(S)-g({h(xᵢ)})|<ε"
- **Analogy labels**: "FPS ↔ Stride降采样", "Ball Query ↔ Receptive Field感受野", "Mini-PointNet ↔ Conv Kernel卷积核"

## COLORS
- Background: Warm Cream (#F5F0E8)
- PointNet tier: Macaron Blue (#A8D8EA) light background
- PointNet++ tier: Lavender (#D5C6E0) light background
- Input points: small Coral Red (#E8655A) dots
- Shared MLP boxes: Macaron Blue (#A8D8EA) fill
- Max Pooling box: Mustard Yellow (#F2CC8F) fill
- FPS step: Mint (#B5E5CF) fill
- Ball Query step: Peach (#FFD5C2) fill
- Mini-PointNet boxes: Lavender (#D5C6E0) fill
- T-Net path: Mustard Yellow (#F2CC8F) dashed line
- Theorem box: Peach (#FFD5C2) border, white fill
- Analogy tags: Mint (#B5E5CF) tags
- Key formulas: Coral Red (#E8655A)

## STYLE
Flat vector illustration. Clean black outlines on all elements. Points are small filled circles. Boxes are rounded rectangles. Arrows are clean with arrowheads. Theorem box has a decorative corner fold. Scattered decorative dots mimicking point cloud. No gradients. Keywords in bold handwritten-style font.

## ASPECT
16:9 landscape

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
