---
illustration_id: 03
type: flowchart
style: vector-illustration
palette: macaron
---

SDS优化循环流程 - Flowchart View

NODE 1: 可微渲染 (Differentiable Rendering)
- NeRF渲染图像 I = g(θ, c)
- 相机参数c随机采样(仰角0-60°, 方位角0-360°)

NODE 2: 潜空间编码 (Latent Encoding)
- VAE编码: z₀ = Encode(I)
- LDM潜空间表示

NODE 3: 加噪 (Add Noise)
- 采样时间步 t ~ Uniform(min_step, max_step)
- 加噪: z_t = √ᾱ_t · z₀ + √(1-ᾱ_t) · ε
- ε ~ N(0, I)

NODE 4: 噪声预测 (Noise Prediction)
- 冻结U-Net: ε_φ(z_t, t, y)
- Classifier-Free Guidance: ε_pred = ε_uncond + s·(ε_text - ε_uncond)
- s = CFG scale ≈ 100

NODE 5: 梯度计算 (Gradient Computation)
- SDS梯度: ∇_θ L = E[w(t)·(ε_φ - ε)·∂z₀/∂θ]
- w(t) = (1-ᾱ_t)/√ᾱ_t
- 关键: 扩散模型参数冻结(stop-gradient)

NODE 6: 参数更新 (Parameter Update)
- Adam优化器更新NeRF参数θ
- 学习率: 1e-3
- 迭代: 10K-15K步

LOOP ARROW: Node 6 → Node 1 (循环)

ANNOTATIONS:
- 左侧标注"冻结扩散模型(φ固定)"
- 右侧标注"可微渲染=梯度桥梁"
- 底部标注"关键洞察: (ε_φ - ε)指向数据流形方向"

Flat vector flowchart with circular loop layout. Clean connected nodes.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for rendering nodes, Mint (#B5E5CF) for encoding nodes, Lavender (#D5C6E0) for noise prediction, Coral Red (#E8655A) for gradient node and key annotations, Mustard Yellow (#F2CC8F) for loop arrow and emphasis
ELEMENTS: 6 rounded rectangular nodes in circular arrangement, bold arrows connecting nodes, loop arrow returning to start, side annotations in speech bubbles, snowflake icon for "frozen" model
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
