---
illustration_id: 07
type: infographic
style: vector-illustration
palette: macaron
---

3D高斯溅射(3DGS)核心原理 - Data Visualization

Layout: left-to-right 3-step pipeline with annotations

ZONES:
- Zone 1 (左侧): 场景编码 — 数百万个各向异性3D高斯椭球表示场景
  - 每个高斯参数: 位置μ, 协方差Σ=R·S·Sᵀ·Rᵀ, 颜色(SH球谐系数), 不透明度α
  - 可视化: 散布的半透明椭圆体，标注关键参数

- Zone 2 (中间): EWA Splatting投影 — 3D高斯投影到2D图像平面
  - 投影公式: Σ' = JWΣWᵀJᵀ
  - 可视化: 3D椭球被"压扁"为2D椭圆，展示投影过程

- Zone 3 (右侧): α混合渲染 — 按深度排序，从前到后混合
  - 公式: C = Σ cᵢαᵢ∏(1-αⱼ)
  - 结果: 100+ FPS实时渲染
  - 对比标注: NeRF需要每光线128-512次MLP查询 → 3DGS每像素混合10-100个高斯

底部对比条:
- NeRF: MLP查询 | 计算密集 | 1-2天训练
- 3DGS: 显式基元 | GPU光栅化 | 10-30分钟训练

LABELS: "μ, Σ, SH, α", "Σ'=JWΣWᵀJᵀ", "100+ FPS", "10-100个高斯/像素", "10-30分钟"
COLORS: Warm Cream background (#F5F0E8), Zone 1 in Macaron Blue (#A8D8EA), Zone 2 in Lavender (#D5C6E0), Zone 3 in Mint (#B5E5CF), NeRF comparison bar in Coral Red (#E8655A), 3DGS bar in Mint (#B5E5CF), black outlines
STYLE: Flat vector illustration infographic. Clean black outlines on all elements. Semi-transparent ellipsoid shapes for Gaussians, projection arrows, depth-sort visualization
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
