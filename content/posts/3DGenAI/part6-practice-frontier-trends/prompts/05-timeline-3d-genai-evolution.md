---
illustration_id: 05
type: timeline
style: vector-illustration
palette: macaron
---

3D生成AI技术演进时间线 - Timeline View

NODE 1 - 2016: 3D-GAN
- 核心创新: 深度卷积首次成功扩展到3D体素空间
- 意义: 3D生成从传统方法迈入深度学习时代
- 局限: 64³分辨率, 内存瓶颈, 棋盘伪影
- 位置: 起点阶段

NODE 2 - 2020: NeRF
- 核心创新: 隐式神经辐射场 + 体渲染 = 照片级新视角合成
- 意义: 隐式表示革命, 后续数千篇论文的基础
- 关键: 位置编码突破频谱偏置, coarse-to-fine采样
- 位置: 隐式场革命

NODE 3 - 2022: DreamFusion
- 核心创新: SDS — 利用冻结2D扩散模型引导3D NeRF优化
- 意义: 无需3D训练数据, 文本直接到3D
- 关键: CFG scale=100, 1-2h/物体
- 问题: Janus/过饱和/模式崩溃
- 位置: 2D→3D突破

NODE 4 - 2023: 3D Gaussian Splatting
- 核心创新: 显式高斯椭球 + tile-based光栅化 = 实时渲染
- 意义: 从O(N·MLP)到O(K_gaussians), 100+FPS
- 关键: 自适应密度控制(克隆/分裂/剪枝)
- 位置: 实时神经渲染

NODE 5 - 2023: LRM
- 核心创新: Transformer大规模前馈重建, 三平面表示
- 意义: 0.5秒单图到3D, 5亿参数
- 关键: O(3N²)三平面 vs O(N³)体素
- 位置: 前馈范式崛起

NODE 6 - 2024: InstantMesh
- 核心创新: 多视图扩散 + FlexiCube可微等值面提取
- 意义: 10秒端到端高质量Mesh生成
- 关键: Zero123++多视图 + 可微提取端到端
- 位置: 端到端生产级

TIMELINE ARROW: 2016 → 2020 → 2022 → 2023 → 2023 → 2024
标注加速趋势: 天级 → 小时级 → 分钟级 → 秒级

Flat vector timeline with horizontal progression. Clear chronological layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for 2016-2020 nodes, Mint (#B5E5CF) for 2022 node, Lavender (#D5C6E0) for 2023 nodes, Peach (#FFD5C2) for 2024 node, Coral Red (#E8655A) for key innovations and speed progression, Mustard Yellow (#F2CC8F) for year labels and method names
ELEMENTS: Horizontal timeline with 6 nodes, each node as a card above/below the line (alternating), timeline arrow with speed annotation (天→时→分→秒), mini icons per node (cube/brain/dream/flash/transformer/mesh), gradient color progression along timeline
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
