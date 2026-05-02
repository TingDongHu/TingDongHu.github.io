---
illustration_id: 05
type: infographic
style: vector-illustration
palette: macaron
---

3DGS生成管线 - Infographic View

STAGE 1: 初始化高斯 (Initialize Gaussians)
- 来源: SfM点云 / 椭球初始化
- 每个高斯: 位置μ, 协方差Σ=RSS^TR^T, 颜色SH, 不透明度α
- 初始数量: 5K-10K

STAGE 2: SDS优化循环 (Optimization Loop)
- 随机采样相机 → 3DGS光栅化渲染
- 投影: EWA Splatting, Σ' = JWΣW^TJ^T
- α混合: C = Σ c_i·α_i·Π(1-α_j)
- SDS损失 → 反向传播更新高斯参数

STAGE 3: 自适应密度控制 (Adaptive Density Control)
- 每100步检查:
  * 高梯度 + 小尺度 → 克隆(Clone): 复制高斯
  * 高梯度 + 大尺度 → 分裂(Split): 拆为两个更小高斯
  * 低不透明度 → 剪枝(Prune): 删除
- 每3000步: 重置不透明度(防累积)

STAGE 4: 渲染输出 (Render Output)
- 最终高斯数: 100K-500K
- 渲染速度: RTX 3090上100+ FPS
- DreamGaussian生成时间: 5-10分钟/物体

ARROW FLOW: 初始化 → 优化循环 → 密度控制 → 输出
(优化循环与密度控制之间有反馈箭头)

Flat vector infographic with horizontal pipeline. Clean sequential layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for initialization, Mint (#B5E5CF) for optimization, Lavender (#D5C6E0) for density control, Peach (#FFD5C2) for output, Coral Red (#E8655A) for adaptive control rules, Mustard Yellow (#F2CC8F) for speed/quantity highlights
ELEMENTS: Horizontal 4-stage pipeline with rounded cards, small gaussian ellipsoid icons in stage 1, mini flowchart for density control in stage 3, feedback loop arrow between stage 2 and 3, speed badge in stage 4
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
