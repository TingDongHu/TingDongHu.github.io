---
illustration_id: 03
type: infographic
style: vector-illustration
palette: macaron
---

视觉质量三大指标 - Infographic View

LEVEL 1: PSNR (像素级度量)
- 公式: PSNR = 20·log₁₀(MAX/√MSE)
- MSE = (1/HWC)Σ(I-Î)²
- 含义: 像素值差异的分贝表示
- 评级: >40dB不可感知, 30-40dB良好, <20dB较差
- 根本缺陷:
  * 与感知非单调 — 整体偏亮≠质量差, 但PSNR暴跌
  * 对1像素平移极度敏感
  * 完全忽略语义
- 结论: 仅作补充, 绝非主要依据

LEVEL 2: SSIM (结构级度量)
- 分解: SSIM = l(亮度)·c(对比度)·s(结构)
- l = (2μ_xμ_y+c₁)/(μ_x²+μ_y²+c₁)
- c = (2σ_xσ_y+c₂)/(σ_x²+σ_y²+c₂)
- s = (σ_xy+c₃)/(σ_xσ_y+c₃)
- 局部窗口: 11×11高斯窗
- 优势: 对微小平移有容忍度
- 局限: 基于局部统计, 无法捕捉长程语义

LEVEL 3: LPIPS (感知级度量)
- 核心: 深度网络特征空间 ≈ 人类感知空间
- 公式: d = Σ_l (1/H_lW_l)Σ‖w_l⊙(ŷ_l-ŷ₀_l)‖²
- 骨干: VGG16 (conv1_2→conv5_3)
- w_l: BAPPS数据集上训练的可学习权重
- 优势: 捕捉语义级差异(如"有无扶手")
- 最佳实践: 归一化到[-1,1], 多尺度评估, 空间平均

ARROW: PSNR → SSIM → LPIPS (从低级到高级, 与人类感知对齐度递增)

Flat vector infographic with vertical progression layout. Clear level hierarchy.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Peach (#FFD5C2) for PSNR (lowest level), Blue (#A8D8EA) for SSIM (middle level), Mint (#B5E5CF) for LPIPS (highest level), Coral Red (#E8655A) for defects and warnings, Mustard Yellow (#F2CC8F) for formulas and alignment indicator
ELEMENTS: Three stacked cards with upward arrow showing progression, each card with metric name/formula/pros/cons, small alignment gauge icon (low→high), "与人类感知对齐度" progression bar on the right side, PSNR warning icon
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
