---
illustration_id: 02
type: infographic
style: vector-illustration
palette: macaron
---

nerfstudio模块化架构 - Infographic View

MODULE 1: DataManager (数据管理)
- VanillaDataManager: 连接原始图像与模型输入
- RayGenerator: 像素坐标→世界空间射线
  d = normalize(R @ K⁻¹ @ [i,j,1]ᵀ)
- 分层采样: 射线→t值→RayBundle
- 可配置: train_num_rays_per_batch (4096/8192)

MODULE 2: Model (策略层)
- NerfactoModel: 默认推荐配置
  * proposal network粗采样(64样本)
  * 权重分布→细采样(16额外样本)
  * 损失: rgb_loss + distortion_loss + interlevel_loss
- get_param_groups: 分组学习率
- 设计: models=策略, fields=表示

MODULE 3: Field (表示层)
- NerfactoField: 哈希编码+小MLP
  * 输入: 多分辨率哈希编码特征
  * 输出: 密度σ + 颜色c
- InstantNGPField: 纯哈希编码场
  * 16级哈希表, 每级2维特征
  * 三线性插值 + MLP解码

MODULE 4: Sampler (采样器)
- UniformSampler: [t_n, t_f]均匀
- PDFSampler: 逆变换采样, 聚焦高密度区域
- ProposalSampler: mip-NeRF 360提案网络

MODULE 5: Renderer (渲染器)
- RGBRenderer: 体渲染方程
  C = Σ T_i(1-exp(-σ_iδ_i))c_i
  T_i = exp(-Σσ_jδ_j) via torch.cumsum
- 支持: 白/黑/last_sample背景

PIPELINE FLOW:
DataManager(RayBundle) → Model → Field(σ,c) → Sampler → Renderer → Image(Loss)

DESIGN PHILOSOPHY:
"models与fields分离 = 策略与表示解耦"
可自由组合不同field和不同model

Flat vector infographic with horizontal modular pipeline. Clean module separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for DataManager, Mint (#B5E5CF) for Model, Lavender (#D5C6E0) for Field, Peach (#FFD5C2) for Sampler, Coral Red (#E8655A) for Renderer and design philosophy, Mustard Yellow (#F2CC8F) for key formulas and module names
ELEMENTS: Horizontal 5-module pipeline with rounded cards, arrows showing data flow between modules, mini ray/camera diagram in DataManager, hash table icon in Field, cumsum diagram in Renderer, design philosophy callout box at bottom
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
