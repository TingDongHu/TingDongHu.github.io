---
illustration_id: 07
type: comparison
style: vector-illustration
palette: macaron
---

前馈 vs 优化: 3D生成两大范式 - Comparison View

LEFT SIDE - 前馈模型 (Feedforward):
- 代表方法: LRM, InstantMesh, TripoSR
- 核心思想: 单次前向传播生成3D
- 生成时间: 0.5-10秒 (秒级)
- 几何质量: 中等, 受训练数据覆盖限制
- 输出确定性: 高, 相同输入→相近输出
- 泛化能力: 受限于训练数据分布
- 部署友好: 高, 易批处理, 适合服务化
- 表示: 三平面(Tri-plane)/FlexiCube
- 数据需求: 需大规模3D训练数据(Objaverse)
- 图示: 单箭头 输入→模型→输出

RIGHT SIDE - 优化模型 (Optimization-based):
- 代表方法: DreamFusion, ProlificDreamer, Magic3D
- 核心思想: 迭代优化3D表示
- 生成时间: 1-30分钟 (分钟级)
- 几何质量: 较高, 2D扩散先验强约束
- 输出确定性: 低, 受随机种子和SDS方差影响
- 泛化能力: 2D先验带来更广语义覆盖
- 部署友好: 低, 每样本需独立优化循环
- 表示: NeRF/3DGS/DMTet
- 数据需求: 无需3D训练数据(利用2D扩散模型)
- 图示: 循环箭头 渲染→评估→更新→渲染

BOTTOM - 融合趋势:
- "前馈初始化 + 优化精修" 成为有前景方向
- InstantMesh生成初态 → DreamFusion精修细节
- 箭头: 两种范式向中间靠拢

Flat vector comparison with split layout. Clear visual separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Left side in Blue (#A8D8EA), Right side in Lavender (#D5C6E0), Coral Red (#E8655A) for time/quality emphasis, Mint (#B5E5CF) for convergence trend, Mustard Yellow (#F2CC8F) for method names
ELEMENTS: Two-column layout with bullet comparisons, small icons (straight arrow for feedforward, circular arrow for optimization), bottom merger diagram showing both paradigms converging, speed badges (0.5s vs 30min)
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
