---
illustration_id: 06
type: framework
style: vector-illustration
palette: macaron
---

Magic3D两阶段策略 - Framework View

STAGE 1 - 粗粒度NeRF (Coarse Stage):
- 表示: Instant-NGP哈希编码NeRF
- 分辨率: 64×64
- 损失: L_coarse = L_SDS^64 + λ_dens·L_dens
- 密度正则化: L_dens = Σσ(x)² (抑制浮点)
- 作用: 拓扑探索 — 隐式场可表示任意亏格表面
- 哈希编码: 16级, 每级2维特征, 学习率1e-2
- 训练: 约5000步, 30分钟

TRANSITION - 隐式→显式转换:
- DMTet提取: 四面体网格上定义SDF → 可微Marching Tetrahedra → 三角网格
- 关键: 拓扑已确定, 转为高效显式表示
- 箭头标注: "拓扑固化"

STAGE 2 - 精细DMTet网格 (Fine Stage):
- 表示: DMTet网格 + 可微纹理 + 光照
- 分辨率: 512×512
- 渲染: nvdiffrast可微光栅化
- 损失: L_fine = L_SDS^512 + λ_norm·L_normal + λ_lap·L_laplace
- 法向平滑: 惩罚相邻面法向差异
- 拉普拉斯正则化: 防止顶点漂移和自相交
- 作用: 几何精修 — 像素级精度优化
- 训练: 约2000步, 20分钟

BOTTOM INSIGHT:
- "隐式探索拓扑 + 显式精修几何" — 为什么有效?
- 隐式: 拓扑灵活, 适合快速探索整体形状
- 显式: 高效渲染, 适合精细表面和真实感材质
- 后续: Fantasia3D, Rodin等均采用此范式

Flat vector framework with two-stage vertical layout. Clear stage separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for coarse stage, Mint (#B5E5CF) for fine stage, Lavender (#D5C6E0) for transition, Coral Red (#E8655A) for key insight, Mustard Yellow (#F2CC8F) for resolution/step highlights
ELEMENTS: Two large rounded cards stacked vertically, transition arrow between them, small NeRF icon in stage 1, mesh icon in stage 2, loss formula cards inside each stage, bottom insight box with lightbulb icon
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
