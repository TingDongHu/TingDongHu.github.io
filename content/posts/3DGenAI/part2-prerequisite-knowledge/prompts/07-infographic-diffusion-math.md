---
illustration_id: 07
type: infographic
style: vector-illustration
palette: macaron
---

# 扩散模型完整数学

## Layout
Three-row horizontal layout: Row 1 shows "前向过程 Forward" (x₀→x_T with noise increasing), Row 2 shows "反向过程 Reverse" (x_T→x₀ with denoising), Row 3 shows "CFG Classifier-Free Guidance" formula and intuition. A large central vertical arrow connects Row 1 and Row 2. Title "扩散模型" at top.

## ZONES
- **Title Zone**: Top center, "扩散模型 Diffusion" in large handwritten font with a star ★, small noise dots decoration
- **Row 1 - Forward Process**: Left to right flow
  - x₀ (clean image icon) → progressively noisier icons → x_T (pure noise icon)
  - Key formula displayed prominently below the flow
  - Show α_t, ᾱ_t notation
- **Row 2 - Reverse Process**: Right to left flow (opposite direction)
  - x_T (noise) → progressively cleaner icons → x₀ (clean)
  - Loss function formula displayed prominently
  - DDPM sampling algorithm in a small code-like box
  - DDIM note as a side tag
- **Row 3 - CFG**: Two parallel paths merging
  - Left path: ε_unc (unconditional prediction)
  - Right path: ε_cond (conditional prediction)
  - Merging point: CFG formula with guidance scale s
  - Visual: two arrows combining into one stronger arrow
- **Right Side Panel - 3D Advantages**: Small vertical list of why diffusion beats GAN for 3D

## LABELS
- **Forward Process**: "前向加噪 Forward", "q(x_t|x_{t-1}) = N(√α_t·x_{t-1}, β_t·I)", "β_t: 10⁻⁴ → 0.02 线性调度", "★核心公式: x_t = √ᾱ_t·x₀ + √(1-ᾱ_t)·ε", "α_t = 1-β_t", "ᾱ_t = ∏α_s", "ε ~ N(0,I)", "归纳法证明: 方差相加"
- **Reverse Process**: "反向去噪 Reverse", "L = E[‖ε - ε_θ(x_t, t)‖²]", "预测噪声ε而非x₀ (优化landscape更平滑)", "DDPM: x_{t-1} = (1/√α_t)(x_t - (1-α_t)/√(1-ᾱ_t)·ε) + √β_t·z", "DDIM: 非马尔可夫 10~50步加速"
- **CFG**: "Classifier-Free Guidance", "ε̂ = ε_unc + s·(ε_cond - ε_unc)", "s=1: 普通条件采样", "s>1: 增强条件对齐 牺牲多样性", "10%概率丢弃条件(训练时)"
- **3D Panel**: "3D优势", "① MSE损失 训练稳定", "② 分数函数 指向数据流形", "③ CFG灵活条件化", "④ 多尺度学习 粗→细"

## COLORS
- Background: Warm Cream (#F5F0E8)
- Forward row: very light Macaron Blue (#A8D8EA) background strip
- Reverse row: very light Peach (#FFD5C2) background strip
- CFG row: very light Lavender (#D5C6E0) background strip
- Clean data icons (x₀): Macaron Blue (#A8D8EA) fill
- Noisy data icons (x_T): grey with scattered dots
- Central connecting arrow: Mustard Yellow (#F2CC8F)
- Core formula box: Peach (#FFD5C2) border, large Coral Red (#E8655A) text
- Loss function: Coral Red (#E8655A)
- DDPM code box: Mint (#B5E5CF) background
- CFG formula: Coral Red (#E8655A) in large font
- ε_unc path: Lavender (#D5C6E0)
- ε_cond path: Macaron Blue (#A8D8EA)
- Merged arrow: Coral Red (#E8655A) bold
- 3D advantages panel: Mint (#B5E5CF) background with small checkmark icons

## STYLE
Flat vector illustration. Clean black outlines on all elements. Progressive noise shown as icons going from clear geometric shapes to random scattered dots. Arrows are clean with arrowheads. Code-like box uses monospace-style font. Star ★ next to core formula. Small decorative noise patterns. No gradients. Keywords in bold handwritten-style font, formulas in clean sans-serif at large size.

## ASPECT
3:4 portrait (tall format to accommodate three rows of content)

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
