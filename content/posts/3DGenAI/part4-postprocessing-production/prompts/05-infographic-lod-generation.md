---
illustration_id: 05
type: infographic
style: vector-illustration
palette: macaron
---

LOD多级细节生成 - Infographic View

LEVEL 0 - LOD0 (完整细节):
- 面数: 100K三角面
- 距离阈值: 0-5m
- 内容: 全部几何细节 + 完整纹理
- 法线贴图: 不需要
- 屏幕误差: ε < ε_threshold

LEVEL 1 - LOD1 (中度简化):
- 面数: 50K (50%简化)
- 距离阈值: 5-7m
- 内容: 主要结构保留, 细小特征简化
- 法线贴图补偿: 烘焙丢失的几何细节到法线贴图
- 简化方法: QEM边坍缩

LEVEL 2 - LOD2 (低细节):
- 面数: 25K (25%简化)
- 距离阈值: 7-10m
- 内容: 核心轮廓保留
- 法线贴图补偿: 更强依赖法线贴图
- 远处细节不可感知

LEVEL 3 - LOD3 (最低细节):
- 面数: 12.5K (12.5%简化)
- 距离阈值: 10m+
- 内容: 基本形状
- 法线贴图: 核心补偿手段
- 极端: Imposter/Sprite (1-2个三角面billboard)

KEY FORMULAS:
- 投影误差: ε ∝ 1/d (与距离成反比)
- LOD选择: LOD_k = argmin_k {ε_k < ε_threshold}
- 切换距离: √2倍递增 (5→7→10→14m)
- QEM简化链: 从最高面数逐步QEM简化生成

VISUAL: 四个递减细节的网格模型并排，下方对应距离刻度尺

Flat vector infographic with horizontal level layout. Clear visual hierarchy.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for LOD0, Mint (#B5E5CF) for LOD1, Lavender (#D5C6E0) for LOD2, Peach (#FFD5C2) for LOD3, Coral Red (#E8655A) for formulas and key thresholds, Mustard Yellow (#F2CC8F) for face count percentages
ELEMENTS: Four level cards arranged left to right with decreasing detail, mini mesh wireframe icons showing progressive simplification, distance ruler at bottom, arrow showing √2 distance progression, normal map compensation badge on each level
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
