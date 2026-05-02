---
illustration_id: 04
type: flowchart
style: vector-illustration
palette: macaron
---

PBR纹理烘焙管线 - Flowchart View

INPUT: 高模(密集网格/NeRF) + 低模(简化网格+UV) + UV展开

STEP 1: 射线投射 (Ray Casting)
- 对低模每个UV像素(texel)
- 从纹理空间反投影到3D表面
- 沿法线方向投射射线到高模
- 获取命中点的材质属性

STEP 2: 烘焙目标 (Bake Targets) — 五通道PBR:

  2a. Albedo (漫反射)
  - 物理含义: 漫反射固有颜色
  - 值域: [0,1]³
  - 角色: 漫反射项系数

  2b. Normal (法线贴图)
  - 切线空间: n_tangent = TBN⁻¹ · n_world
  - TBN矩阵: 切线T + 副切线B + 法线N
  - 编码: RGB → [-1,1]³ (128,128,255=朝上)
  - 核心: 高模微观法向→低模表面扰动

  2c. Roughness (粗糙度)
  - 物理含义: 微表面朝向随机度
  - 值域: [0,1]
  - 角色: NDF参数 α = r²

  2d. Metallic (金属度)
  - 物理含义: 金属/电介质切换
  - 值域: {0,1}
  - 角色: Fresnel F₀的选择

  2e. AO (环境遮蔽)
  - 物理含义: 漫反射环境光衰减
  - 方法: 每texel发射多条射线, 统计遮挡比例
  - 值域: [0,1]

STEP 3: 输出 (Output)
- 低模 + 五通道PBR贴图集
- 分辨率: 2048×2048 或 4096×4096
- 引擎即可使用

ARROW FLOW: 高模+低模 → 射线投射 → 五通道烘焙 → 低模+PBR贴图

Flat vector flowchart with vertical pipeline. Clean hierarchical layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for input/raycasting, Mint (#B5E5CF) for Albedo, Lavender (#D5C6E0) for Normal, Peach (#FFD5C2) for Roughness/Metallic, Coral Red (#E8655A) for AO and key formulas (TBN), Mustard Yellow (#F2CC8F) for output and resolution
ELEMENTS: Vertical flow with input at top, 5 bake target cards arranged in a row (step 2), ray casting diagram showing high-poly to low-poly projection, TBN matrix diagram, output asset icon at bottom
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
