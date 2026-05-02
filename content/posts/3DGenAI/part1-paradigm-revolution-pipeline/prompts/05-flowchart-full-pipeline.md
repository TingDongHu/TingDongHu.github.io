---
illustration_id: 05
type: flowchart
style: vector-illustration
palette: macaron
---

3D生成AI全流程管线总览 - Process Flow

Layout: top-to-bottom with 5 layers

STEPS:
1. 输入侧 (Input): 5个输入源横向排列 — 文本(Text), 图像(Image), 视频(Video), 点云(Point), 多视图(Multi-view)
2. 核心生成层 (Core Generation): 中间大框包含 — 3D表示学习 + VAE/GAN/Diffusion/AR + SDS/VSD/Score Matching
3. 输出侧 (Output): 3个输出类型 — 网格(Mesh), 神经场(NeRF/SDF), 纹理/材质(PBR Maps)
4. 后处理与优化层 (Post-processing): 链式流程 — 网格提取→重拓扑→UV展开→纹理烘焙→LOD生成→轻量化
5. 验证与应用层 (Validation): 4个评估维度 — 几何(CD/EMD/F-Score), 视觉(LPIPS/SSIM), 语义(CLIP Score), 物理/引擎

CONNECTIONS: Bold downward arrows between layers, side annotations for key constraints
- 输入→核心: "文本需隐含拓扑/对称性约束"
- 核心→输出: "不同3D表示潜空间差异巨大"
- 输出→后处理: "Mesh是最终交付格式"
- 后处理→验证: "几何+视觉+语义+物理"

Flat vector flowchart with bold arrows and geometric step containers.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Input layer in Macaron Blue (#A8D8EA), Core in Lavender (#D5C6E0), Output in Mint (#B5E5CF), Post-processing in Peach (#FFD5C2), Validation in Mustard Yellow (#F2CC8F), black outlines, thick arrows
ELEMENTS: Rounded rectangles per layer, distinct icons per input/output type, chain-link symbols for post-processing, evaluation gauge icons for validation
ASPECT: 9:16 (tall format for multi-layer pipeline)

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
