---
illustration_id: 02
type: infographic
style: vector-illustration
palette: macaron
---

法线烘焙原理 — 高模细节编码到低模 - Data Visualization

Layout: left-to-right pipeline with 3 zones

ZONES:
- Zone 1 (左侧): 高模 (High-Poly Mesh) — 显示一个高细节3D头部模型，表面有毛孔皱纹等微观细节，标注"500万-2000万面"，用密集三角形网格表示
- Zone 2 (中间): 法线贴图 (Normal Map) — 一张RGB纹理图，显示为彩虹色的表面方向编码，标注"切线空间 TBN"，"R=法线X偏移, G=法线Y偏移, B=法线Z偏移"
- Zone 3 (右侧): 低模+法线渲染 (Low-Poly + Normal Map) — 低面数模型(标注"5000-10000面")但渲染效果接近高模，展示视觉欺骗效果

连接箭头: Zone1 → 烘焙(Baking) → Zone2 → 施加(Apply) → Zone3

LABELS: "500万-2000万面", "5000-10000面", "切线空间 TBN", "RGB编码法线方向", "视觉欺骗：低模假装高模"
COLORS: Warm Cream background (#F5F0E8), Macaron Blue (#A8D8EA) for high-poly zone, Lavender (#D5C6E0) for normal map zone, Mint (#B5E5CF) for low-poly result, Coral Red (#E8655A) for key annotations
STYLE: Flat vector illustration infographic. Clean black outlines on all elements. Geometric simplified icons, no gradients, playful decorative elements (dots, stars). Arrow-style pipeline flow.
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
