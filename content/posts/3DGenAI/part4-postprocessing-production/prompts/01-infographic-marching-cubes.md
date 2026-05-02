---
illustration_id: 01
type: infographic
style: vector-illustration
palette: macaron
---

Marching Cubes网格提取 - Infographic View

STEP 1: SDF网格构建 (SDF Grid)
- 在AABB内建立N×N×N体素网格 (如256³)
- 每个角点计算场值 v_i = f(p_i)
- 分辨率权衡: 256³=够用, 512³=硬表面细节

STEP 2: 占据状态编码 (Occupancy Encoding)
- 8个角点 → 8位索引: cube_index = Σ 1[v_i<0]·2^i
- 索引范围: 0-255 (2^8=256种配置)

STEP 3: 对称归约 (Symmetry Reduction)
- 256种 → 立方体对称群(48种旋转+反射) → 15种唯一配置
- 配置0: 全外/全内, 无输出
- 配置1: 单角在内, 1-3个三角形
- 对角配置: 最易产生歧义

STEP 4: 歧义面与解决 (Ambiguous Face)
- 交替符号模式(+-+-): 两种合法剖分
- 不一致 → 裂缝(hole)
- 解决方案: 渐近判定器(Asymptotic Decider)或Marching Tetrahedra

STEP 5: 查表与插值 (Table Lookup & Interpolation)
- EDGE_TABLE[256]: 确定哪些边与零水平集相交
- TRI_TABLE[256]: 三角形顶点索引
- 线性插值: p = p1 + v1/(v1-v2)·(p2-p1)
- 数值稳定: |v1-v2|<ε时取中点

STEP 6: 输出 (Output)
- 密集三角网格(可能数百万面)
- 需后续QEM简化

ARROW FLOW: SDF网格 → 编码 → 归约 → 查表 → 插值 → 三角网格

Flat vector infographic with horizontal flow. Clean sequential layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for grid steps, Mint (#B5E5CF) for encoding, Lavender (#D5C6E0) for reduction, Coral Red (#E8655A) for ambiguity problem, Mustard Yellow (#F2CC8F) for output and key numbers (256, 15)
ELEMENTS: Horizontal 6-stage pipeline, mini cube diagram in step 2 showing 8 corners, 15-configuration mini grid in step 3, ambiguity face diagram in step 4, interpolation formula card in step 5
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
