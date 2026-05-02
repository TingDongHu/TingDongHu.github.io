---
illustration_id: 02
type: flowchart
style: vector-illustration
palette: macaron
---

重拓扑与Remesh流程 - Flowchart View

STEP 1: 输入 (Input)
- AI提取的密集网格(Marching Cubes输出)
- 问题: 不规则三角形、高价顶点(valence>>6)、边长不均匀

STEP 2: 拓扑分析 (Topology Analysis)
- 检测: 非流形边、孔洞、自相交、翻转法向
- 计算: 顶点价(valence)、三角形质量指标
- 目标: 识别需要修复的拓扑缺陷

STEP 3: 修复与平滑 (Repair & Smooth)
- Laplacian平滑: v_i = (1-λ)v_i + λ·avg(neighbors)
- 频域分析: 低通滤波器 — 消除噪声但也模糊锐利特征
- Taubin平滑: 交替正负λ, 抵消收缩
- 阈值: λ=0.5, 迭代次数控制平滑程度

STEP 4: 重网格化 (Remesh)
- 边分裂: 过长的边 → 一分为二
- 边坍缩: 过短的边 → 合并(QEM度量代价)
- 边翻转: 改善valence → 向理想值6靠拢
- 切向重投影: 保持与原网格的逼近误差在阈值内

STEP 5: 质量验证 (Quality Validation)
- 三角形质量: 4√3·A/(l₁²+l₂²+l₃²) → 理想等边=1
- 顶点价: 内部理想6, 边界理想4
- 边长均匀性: 目标l_target附近高斯分布

STEP 6: 输出 (Output)
- 规范拓扑网格(四边面主导或均匀三角面)
- 保留原始形状, 改善网格质量

ARROW FLOW: 密集网格 → 拓扑分析 → 修复平滑 → 重网格化 → 验证 → 规范网格

Flat vector flowchart with horizontal pipeline. Clean connected steps.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for analysis steps, Mint (#B5E5CF) for repair steps, Lavender (#D5C6E0) for remesh operations, Coral Red (#E8655A) for quality metrics, Mustard Yellow (#F2CC8F) for output and target values
ELEMENTS: Horizontal 6-step pipeline with rounded cards, mini mesh wireframe icons showing before/after, operation icons (split/collapse/flip) in step 4, quality gauge icon in step 5, arrows between all steps
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
