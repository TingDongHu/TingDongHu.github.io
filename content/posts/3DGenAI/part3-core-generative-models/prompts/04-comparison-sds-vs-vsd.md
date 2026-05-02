---
illustration_id: 04
type: comparison
style: vector-illustration
palette: macaron
---

SDS vs VSD: 分布假设对比 - Comparison View

LEFT SIDE - SDS (Score Distillation Sampling):
- 分布假设: Delta分布 δ(g(θ)) — 单点估计
- 渲染图像被视为确定值
- 问题1: 过饱和 — 梯度倾向于提高对比度
- 问题2: Janus问题 — 无3D一致性约束
- 问题3: 模式崩溃 — 找到"平均解"
- 问题4: 梯度方差大 — 需小学习率+长训练
- 公式: ∇_θ L = E[w(t)·(ε_φ - ε)·∂z/∂θ]
- 图示: 一个尖锐的尖峰(delta函数)代表渲染分布

RIGHT SIDE - VSD (Variational Score Distillation):
- 分布假设: 变分分布 q(x|y) — 分布估计
- 渲染图像被视为随机变量
- 优势1: 熵正则化 — 保持生成多样性
- 优势2: LoRA近似 — q由LoRA微调扩散模型建模
- 优势3: 细节更丰富 — 避免过度平滑
- 优势4: 多视图一致性更好
- 公式: min KL(q(x|y) || p_φ(x|y))
- 两项: 数据流形吸引 + 熵奖励(多样性保持)
- 图示: 一个宽泛的高斯分布代表渲染分布

CENTER: 箭头标注"从点到分布的范式升级"

BOTTOM: 训练时间对比 — SDS: 1-2h, VSD: 2-4h (需要维护LoRA)

Flat vector comparison with split layout. Clear visual separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Left side in Peach (#FFD5C2) with Coral Red (#E8655A) for problems, Right side in Mint (#B5E5CF) with Blue (#A8D8EA) for advantages, Lavender (#D5C6E0) for distribution curves, Mustard Yellow (#F2CC8F) for center arrow
ELEMENTS: Distribution curve diagrams on each side, bullet lists, delta vs Gaussian visual contrast, center transformation arrow, bottom comparison bar
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
