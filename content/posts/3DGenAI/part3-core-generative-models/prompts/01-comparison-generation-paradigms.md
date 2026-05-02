---
illustration_id: 01
type: comparison
style: vector-illustration
palette: macaron
---

3D生成四大核心范式对比 - Comparison View

COLUMN 1 - 体素/栅格 (Voxel/Grid):
- 核心表示: 规则3D网格，每个体素存储占据值
- 代表方法: 3D-GAN, OGN, Shape-E
- 优势: 结构简单，卷积操作成熟，易于与2D架构对接
- 局限: 分辨率立方增长O(N³)，内存瓶颈(64³上限)，表面粗糙

COLUMN 2 - 点云/结构 (Point Cloud):
- 核心表示: N个3D坐标点，无拓扑连接
- 代表方法: PointFlow, ShapeGF, Point-E
- 优势: 灵活紧凑，天然非结构化，可直接从传感器获取
- 局限: 缺乏拓扑和表面，渲染需后处理，无序性

COLUMN 3 - 隐式场/神经场 (Implicit/Neural Field):
- 核心表示: 连续函数f:R³→R(密度/SDF)，MLP参数化
- 代表方法: NeRF, DreamFusion, 3DGS, ProlificDreamer
- 优势: 无限分辨率，无拓扑限制，照片级真实
- 局限: 训练慢(NeRF)或存储大(3DGS)，提取网格需MC

COLUMN 4 - 可微表面积 (Differentiable Surface):
- 核心表示: 显式三角网格+可微光栅化
- 代表方法: DIB-R, GET3D
- 优势: 直接输出可用网格，高效渲染，与引擎兼容
- 局限: 拓扑固定，需要隐式场辅助

BOTTOM: 当前主流 = 隐式场/神经场（尤其SDS路线）

Flat vector comparison with four-column layout. Clear visual separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), each column in distinct macaron tone (Blue #A8D8EA, Mint #B5E5CF, Lavender #D5C6E0, Peach #FFD5C2), Coral Red (#E8655A) for emphasis on limitations, Mustard Yellow (#F2CC8F) for key method names
ELEMENTS: Column headers with representative 3D shape icon, black outlines, bullet lists, bottom highlight bar
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
