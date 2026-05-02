---
illustration_id: 04
type: flowchart
style: vector-illustration
palette: macaron
---

3D生成AI学习路径 - Flowchart View

PHASE 1 (Week 1-2): 数学与3D基础
- 线性代数: 矩阵变换、特征值分解
- 概率论: 贝叶斯推断、变分下界(ELBO)
- 优化: 梯度下降、Adam、Langevin动力学
- 3D表示: 网格(顶点/面/UV)、SDF、体素
- 产出: 手推体渲染公式, Blender基础操作

PHASE 2 (Week 3-4): NeRF实战
- 安装nerfstudio, 训练lego场景
- 消融实验: 位置编码频率L的影响
- Instant-NGP: 哈希编码对比
- PSNR目标: >30dB
- 产出: 2组不同频率重建结果, 速度对比

PHASE 3 (Week 5-6): 文本到3D
- 安装threestudio, 运行DreamFusion
- 诊断Janus问题, 调整CFG scale
- Magic3D两阶段: coarse+refine
- SDS vs VSD对比实验
- 产出: 3个prompt生成结果, Janus诊断报告

PHASE 4 (Week 7-8): 网格处理与引擎集成
- PyTorch3D: 简化/平滑/导出
- Marching Cubes提取NeRF表面
- xatlas UV展开 + Blender纹理烘焙
- Unity/Unreal导入 + PBR配置
- 产出: 引擎中可运行场景, 帧率>60fps

PHASE 5 (Week 9-10): 前沿探索
- 3DGS深入: 官方代码+自有数据
- DreamGaussian: 快速Text-to-3D
- MVDream/Zero-1-to-3: 多视图一致性
- 产出: 3DGS重建, DreamGaussian生成结果

PHASE 6 (Week 11-12): 综合项目
- 选定领域+技术路线
- 端到端Demo: 文本/图像→3D→引擎
- 结果评估与对比
- 产出: 完整Demo+技术文档

ARROW FLOW: 基础 → NeRF → Text-to-3D → 引擎 → 前沿 → 项目

BOTTOM: Level 1(终端用户) → Level 2(调参师) → Level 3(实现者) → Level 4(研究者)

Flat vector flowchart with vertical learning path. Clear phase progression.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for Phase 1-2, Mint (#B5E5CF) for Phase 3-4, Lavender (#D5C6E0) for Phase 5-6, Coral Red (#E8655A) for outputs and milestones, Mustard Yellow (#F2CC8F) for week labels and level indicators
ELEMENTS: Vertical path with 6 phase cards, stepping-stone or stair layout from bottom to top, each card with week range + topics + output, milestone badges between phases, level progression bar on the side, book/lab/code icons for each phase
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
