---
illustration_id: 04
type: infographic
style: vector-illustration
palette: macaron
---

指标冲突与Trade-off - Infographic View

CONFLICT 1: CD↓ 但 视觉质量↓
- 案例: 过度平滑表面可降低CD(最近邻距离小)
- 但: 整体形状扭曲, 视觉上模糊
- 机制: CD对局部距离敏感, 被大面积正确区主导
- 教训: CD低≠看起来好
- 图示: 平滑球(低CD, 低视觉) vs 正确形状(略高CD, 高视觉)

CONFLICT 2: CLIP Score↑ 但 几何精度↓
- 案例: "毛茸茸的狗" → 生成过度膨胀的几何来表达"毛茸茸"
- 机制: CLIP编码全局语义, 不惩罚几何失真
- SDS方法: 纹理拷贝到表面, 视觉对齐但几何错误
- 教训: 文本对齐≠几何正确
- 图示: 膨胀的狗模型(高CLIP, 低几何) vs 精确模型(略低CLIP, 高几何)

CONFLICT 3: 多样性↑ 但 保真度↓
- 案例: 鼓励生成样本扩散到更多模态
- 但: 增加低质量样本比例, 降低平均Precision
- 机制: 模式覆盖 vs 样本质量的内在张力
- 教训: Recall↑可能伴随Precision↓

CONFLICT 4: 渲染质量↑ 但 拓扑质量↓
- 案例: NeRF渲染极好, 但提取网格充满内部碎片和漂浮物
- 机制: 体渲染与网格提取是不同操作
- 教训: 好看≠好用

BOTTOM RULE: 帕累托改进要求 — 任何声称"全面超越SOTA"的方法必须在多个冲突指标上同时取得改进, 而非仅在单一指标上领先

Flat vector infographic with 2×2 conflict grid layout. Clear visual contrast.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for "improved" metrics, Coral Red (#E8655A) for "degraded" metrics and arrows, Mustard Yellow (#F2CC8F) for conflict numbers and emphasis, Mint (#B5E5CF) for Pareto rule, Lavender (#D5C6E0) for visual examples
ELEMENTS: 2×2 grid of conflict cards, each with up/down arrow pairs showing conflicting trends, small before/after model icons, seesaw/balance icon for trade-off concept, bottom rule banner with Pareto icon, conflict numbered badges
ASPECT: 1:1

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
