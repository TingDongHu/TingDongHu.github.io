---
illustration_id: 02
type: infographic
style: vector-illustration
palette: macaron
---

几何质量三大指标 - Infographic View

METRIC 1: Chamfer Distance (CD)
- 公式: d_CD = (1/|S₁|)Σmin‖x-y‖ + (1/|S₂|)Σmin‖y-x‖
- 分解: 覆盖度(Coverage) + 精度(Accuracy)
- 计算: k-d树 O(NlogM), FAISS GPU加速
- 优势: 计算高效, 实现简单
- 缺陷: 法向不敏感(翻折不可检测), 对异常值敏感, 不衡量拓扑, 采样密度依赖
- 图示: 两组点云, 箭头表示最近邻连接

METRIC 2: Earth Mover's Distance (EMD)
- 公式: min_γ Σγ_ij·‖x_i-y_j‖ (最优传输)
- 核心: 全局结构感知 — 每个点都被"传输"
- 计算: 精确O(n³), Sinkhorn近似O(NM)迭代
- 熵正则: +ε·Σγ_ij·log(γ_ij) → 可微, GPU友好
- 优势: 捕捉整体结构差异(如扶手缺失)
- 缺陷: 计算成本远高于CD

METRIC 3: F-Score
- 公式: F_τ = 2·P·R/(P+R), 阈值τ下
- Precision_τ: 预测点在真值τ邻域内的比例
- Recall_τ: 真值点被预测覆盖的比例
- 优势: 对细节结构缺失更敏感(硬判断, 非平均)
- vs CD: CD是平均值(被大面积正确区主导), F-Score是硬判断
- 多阈值: τ∈{0.01, 0.02, 0.05} 或 Precision-Recall曲线AUC
- 图示: 阈值圆环, 点在内/外

BOTTOM: 采样密度必须统一! 不同密度下CD/EMD不可比较

Flat vector infographic with three-column layout. Clear metric separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for CD column, Mint (#B5E5CF) for EMD column, Lavender (#D5C6E0) for F-Score column, Coral Red (#E8655A) for defects/warnings, Mustard Yellow (#F2CC8F) for formulas and emphasis
ELEMENTS: Three equal columns, each with metric name header, formula card, pros/cons bullet list, mini diagram (point clouds for CD, transport arrows for EMD, threshold circles for F-Score), bottom warning banner
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
