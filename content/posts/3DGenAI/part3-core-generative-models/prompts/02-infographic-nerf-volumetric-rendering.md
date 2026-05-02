---
illustration_id: 02
type: infographic
style: vector-illustration
palette: macaron
---

NeRF体渲染推导链 - Infographic View

STEP 1: 光线生成 (Ray Generation)
- 像素(u,v) → 反投影 → 光线r(t) = o + td
- o: 相机中心, d: 方向, t: 深度参数

STEP 2: 沿光线采样 (Sampling)
- 分层采样: [t_n, t_f]均匀分N段，每段随机取点
- 重要性采样: coarse网络权重→PDF→逆变换采样→fine网络聚焦高密度区域

STEP 3: MLP查询 (Network Query)
- 输入: γ(x)位置编码(60维) + γ(d)视角编码(24维)
- 输出: σ密度 + c颜色
- 跳跃连接: 第5层拼接原始位置输入

STEP 4: 体渲染积分 (Volume Rendering)
- 透射率: T_i = exp(-Σσ_j·δ_j)
- 不透明度: α_i = 1 - exp(-σ_i·δ_i)
- 离散积分: Ĉ(r) = Σ T_i·α_i·c_i
- 物理含义: T_i·σ_i·dt = "首次击中"概率

STEP 5: 损失与优化 (Training)
- L = ||Ĉ_f - C||² + λ||Ĉ_c - C||²
- coarse+fine双网络联合优化

ARROW FLOW: 像素 → 光线 → 采样点 → MLP(σ,c) → 积分 → 像素颜色

Flat vector infographic with horizontal flow. Clean sequential layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Mint (#B5E5CF) for sampling step, Lavender (#D5C6E0) for MLP step, Blue (#A8D8EA) for rendering step, Coral Red (#E8655A) for key formulas, Mustard Yellow (#F2CC8F) for step numbers
ELEMENTS: Horizontal pipeline with 5 connected stages, each stage as a rounded card, arrows between stages, mini formulas below each stage, small diagram of ray sampling in step 2
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
