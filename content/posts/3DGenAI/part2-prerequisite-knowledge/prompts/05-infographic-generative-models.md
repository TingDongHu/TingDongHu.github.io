---
illustration_id: 05
type: infographic
style: vector-illustration
palette: macaron
---

# 四大生成模型推导总览

## Layout
Four quadrants in a 2x2 grid, each quadrant dedicated to one generative model. A central circle connects all four with the label "生成模型". Title "生成模型全家桶" at top.

## ZONES
- **Title Zone**: Top center, "生成模型" in large handwritten font
- **Center Circle**: Small circle with "p(x)" text connecting all four quadrants
- **Top-Left Quadrant - GAN**: Generator vs Discriminator diagram
  - Show G(z)→fake, D(x)→real/fake judgment
  - Min-max game visual
- **Top-Right Quadrant - VAE**: Encoder-Decoder with latent space
  - Show x→Encoder→z→Decoder→x̂
  - Reparameterization trick: z = μ + σ⊙ε
- **Bottom-Left Quadrant - Diffusion**: Forward/reverse process
  - x₀→(add noise)→x_T and x_T→(denoise)→x₀
  - Show noise level increasing then decreasing
- **Bottom-Right Quadrant - Autoregressive**: Sequential token generation
  - Show chain of conditional distributions
  - x₁→x₂→x₃→...→x_N

## LABELS
- **GAN quadrant**: "GAN 对抗生成", "min_G max_D V(D,G)", "D* = p_data/(p_data+p_g)", "JS散度", "WGAN: Wasserstein-1", "模式崩溃 Mode Collapse", "3D: 渲染图判别器最易训练"
- **VAE quadrant**: "VAE 变分自编码", "ELBO = E[log p(x|z)] - KL(q‖p)", "重参数化 z = μ + σ⊙ε", "信息瓶颈: 压缩vs保留", "KL项→压缩 重构项→保留", "ShapeVAE: 潜空间插值"
- **Diffusion quadrant**: "扩散模型 Diffusion ★最重要", "前向: q(x_t|x_{t-1}) = N(√α_t·x_{t-1}, β_t·I)", "x_t = √ᾱ_t·x₀ + √(1-ᾱ_t)·ε", "反向: L = E[‖ε - ε_θ(x_t,t)‖²]", "DDPM采样 T→1", "DDIM: 非马尔可夫 加速", "3D: 训练稳定 分数精确"
- **AR quadrant**: "自回归 AR", "p(x) = ∏p(xᵢ|x_{<i})", "链式法则分解", "3D序列化: Z-order/Morton", "类比GPT: 3D token序列", "体素: 0/1 token"
- **Center**: "p(x) 目标分布"

## COLORS
- Background: Warm Cream (#F5F0E8)
- GAN quadrant: Macaron Blue (#A8D8EA) light background, elements in darker blue outlines
- VAE quadrant: Lavender (#D5C6E0) light background
- Diffusion quadrant: Peach (#FFD5C2) light background, with a small star ★ icon next to title
- AR quadrant: Mint (#B5E5CF) light background
- Center circle: Mustard Yellow (#F2CC8F) fill
- Key formulas: Coral Red (#E8655A)
- Arrows in diagrams: matching quadrant accent colors
- "最重要" tag: Coral Red (#E8655A) border

## STYLE
Flat vector illustration. Clean black outlines on all elements. Quadrants are rounded rectangles with colored headers. Generator/Encoder/Decoder are simple box icons with arrows. Noise level shown as progressive dots getting more scattered. Token chain shown as connected circles. Small decorative elements. No gradients. Keywords in bold handwritten-style font, formulas in clean sans-serif.

## ASPECT
1:1 square (balanced 2x2 grid)

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
