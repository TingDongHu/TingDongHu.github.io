---
illustration_id: 01
type: framework
style: vector-illustration
palette: macaron
---

多维评估框架四大支柱 - Framework View

CENTER: 3D生成资产 (Generated 3D Asset)
- 图标: 小型3D模型

PILLAR 1 - 几何精度 (Geometry):
- 核心指标: Chamfer Distance, EMD, F-Score@τ
- 权重: 高
- 适用: 所有有真值的生成任务
- 关键: 必须固定采样密度; F-Score对细节更敏感
- 覆盖误差 vs 精度误差: 诊断"漏生成"vs"多生成"

PILLAR 2 - 视觉保真 (Visual):
- 核心指标: LPIPS↓, SSIM↑, PSNR↑
- 权重: 高
- 适用: 有参考渲染图像时
- 关键: LPIPS优先于PSNR/SSIM; 多视角平均
- 层级: 像素级(PSNR) → 结构级(SSIM) → 感知级(LPIPS)

PILLAR 3 - 语义对齐 (Semantic):
- 核心指标: CLIP Score↑, R-Precision↑
- 权重: 高
- 适用: 文本/图像条件生成
- 关键: 固定提示模板; 注意CLIP的域偏差
- 陷阱: 提示工程敏感、训练分布偏差

PILLAR 4 - 物理合规 (Physical):
- 核心指标: 抓取成功率, 碰撞稳定性, 水密性
- 权重: 中
- 适用: 机器人、仿真、游戏资产
- 关键: 暴露"看起来对"≠"功能上对"的差距
- 检查: 非流形几何、薄壁结构、内部空洞

BOTTOM: 任何声称"全面超越SOTA"的方法必须在多个冲突指标上同时取得帕累托改进

Flat vector framework with radial/pillar layout. Center + 4 pillars.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for Geometry pillar, Mint (#B5E5CF) for Visual pillar, Lavender (#D5C6E0) for Semantic pillar, Peach (#FFD5C2) for Physical pillar, Coral Red (#E8655A) for center asset and key insights, Mustard Yellow (#F2CC8F) for weight labels and emphasis
ELEMENTS: Center circle with 3D asset icon, 4 pillars radiating outward (top-left, top-right, bottom-left, bottom-right), each pillar as a card with icon and bullet points, bottom insight banner, weight badges on each pillar
ASPECT: 1:1

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
