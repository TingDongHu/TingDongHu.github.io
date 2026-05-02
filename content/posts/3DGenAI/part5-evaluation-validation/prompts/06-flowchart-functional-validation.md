---
illustration_id: 06
type: flowchart
style: vector-illustration
palette: macaron
---

功能性验证流程 - Flowchart View

STEP 1: 生成3D资产 (Generated Asset)
- 输入: AI生成的3D模型(OBJ/GLB/USD)
- 常见缺陷: 非流形几何、内部空洞、薄壁结构

STEP 2: 碰撞体生成 (Collision Generation)
- 方法: V-HACD凸包分解
- 最大凸包数: 64
- 作用: 物理引擎需要简化碰撞体
- 检查: 包围体积IoU

STEP 3: 骨骼绑定测试 (Skeleton Binding)
- 部署骨骼: 自动/手动绑定
- 权重刷: 顶点对骨骼的权重分配
- 测试: 基础姿态是否合理

STEP 4: 动画变形测试 (Animation Deformation)
- 执行基础动画序列
- 检查: 无穿模、无扭曲、变形自然
- 关节处: 蒙皮变形质量

STEP 5: 物理仿真 (Physics Simulation)
- 抓取测试: Franka夹爪闭合-提升-保持-摇晃
- 稳定性: 静置5秒无穿模/抖动
- 碰撞检测: 与环境交互无异常
- 重心: 质心在支撑面内

STEP 6: 引擎渲染验证 (Engine Render)
- 帧率: >60fps (PC端)
- Draw Call: 合理范围
- 纹理内存: 符合平台限制
- 多角度: 无破面/法线翻转

STEP 7: 通过/失败 (Pass/Fail)
- 全部通过 → 生产可用资产
- 任一失败 → 诊断缺陷 → 返回修复

CORE INSIGHT (底部标注):
- "看起来对" ≠ "功能上对"
- 视觉完美但无法在物理世界中交互 = 无实用价值
- NeRF提取网格常含: 内部空洞、薄壁面、非流形拓扑

ARROW FLOW: 3D资产 → 碰撞体 → 骨骼绑定 → 动画变形 → 物理仿真 → 引擎渲染 → 通过/失败
(失败箭头回到修复步骤)

Flat vector flowchart with vertical pipeline. Clear step progression.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for generation steps, Mint (#B5E5CF) for binding/animation, Lavender (#D5C6E0) for physics simulation, Peach (#FFD5C2) for engine render, Coral Red (#E8655A) for pass/fail and core insight, Mustard Yellow (#F2CC8F) for test metrics
ELEMENTS: Vertical 7-step flowchart, each step as a rounded card, test icons (skeleton/bone, animation keyframe, physics apple, gamepad), pass/fail traffic light at bottom, feedback loop arrow for failure case, insight banner with exclamation icon
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
