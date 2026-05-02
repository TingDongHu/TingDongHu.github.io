---
illustration_id: 05
type: infographic
style: vector-illustration
palette: macaron
---

CLIP Score语义对齐评估 - Infographic View

STEP 1: 多视角渲染 (Multi-view Rendering)
- 3D资产 → 渲染4+个视角图像
- 固定渲染器/光照/相机分布
- 视角: 菲波那契球面采样/均匀分布

STEP 2: CLIP编码 (CLIP Encoding)
- 图像编码器: E_I(I) → 图像特征向量
- 文本编码器: E_T(T) → 文本特征向量
- 模型: ViT-B/32 或 ViT-L/14

STEP 3: 相似度计算 (Similarity)
- CLIP-Score = max(100·cos(E_I, E_T), 0)
- 取多视角平均
- 值域: [0, 100]

STEP 4: 对齐评估 (Alignment Assessment)
- 高分: 生成内容与文本语义一致
- 低分: 语义偏离

TRAP 1 - 提示工程敏感性:
- "a dog" vs "a photo of a dog" → 分数差异显著
- 必须固定提示模板
- 禁止对不同方法使用不同模板

TRAP 2 - 训练分布偏差:
- CLIP偏好照片级真实感 → 低估卡通/风格化
- 渲染图 vs 自然图像的域差异
- 解决: 领域特定CLIP微调

SUPPLEMENT - CLIP R-Precision:
- 给定生成图像 + N个候选文本(1正确+N-1干扰)
- 计算正确文本的top-k检索比例
- 更好反映模型是否"理解"文本

ARROW FLOW: 3D资产 → 多视角渲染 → CLIP编码 → 余弦相似度 → CLIP Score

Flat vector infographic with horizontal flow. Clean sequential layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for rendering/encoding steps, Mint (#B5E5CF) for similarity step, Lavender (#D5C6E0) for assessment, Coral Red (#E8655A) for trap warnings, Mustard Yellow (#F2CC8F) for CLIP Score formula and supplement
ELEMENTS: Horizontal pipeline with 4 main steps, two warning/trap cards below the pipeline (with alert icons), supplement card for R-Precision, CLIP encoder diagram (image→feature, text→feature), cos similarity diagram
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
