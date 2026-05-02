---
illustration_id: 06
type: flowchart
style: vector-illustration
palette: macaron
---

引擎集成完整管线 - Flowchart View

STEP 1: AI生成输出 (AI Output)
- 输入: 文本/图像 → 3D生成模型
- 输出: 隐式场/SDF/点云/NeRF
- 格式: 神经网络权重 + 场参数

STEP 2: 网格提取 (Mesh Extraction)
- 方法: Marching Cubes / Dual Contouring
- 输入: SDF网格或密度场
- 输出: 密集三角网格(可能数百万面)
- 关键: 选择提取分辨率(256³/512³)

STEP 3: 网格简化与Remesh (Simplify & Remesh)
- QEM简化: 百万面→万面, 误差<1%
- Remesh: 改善三角形质量, 规范拓扑
- 平滑: Laplacian/Taubin消除噪声
- 输出: 目标面数网格

STEP 4: UV展开 (UV Unwrap)
- 方法: LSCM/ABF++/xatlas自动展开
- 输出: 带UV坐标的网格
- 质量指标: UV利用率>75%

STEP 5: 纹理烘焙 (Texture Baking)
- 五通道PBR: Albedo + Normal + Roughness + Metallic + AO
- 分辨率: 2048² 或 4096²
- 输出: 低模 + 贴图集

STEP 6: LOD生成 (LOD Chain)
- QEM简化链: LOD0→LOD1→LOD2→LOD3
- 法线贴图补偿每级丢失细节
- 切换距离: √2倍递增

STEP 7: 引擎导入 (Engine Import)
- 格式: FBX/glTF/USD
- 目标: Unity (URP/HDRP) / Unreal
- 操作: 导入模型+贴图, 创建Material

STEP 8: Shader配置 (Shader Setup)
- PBR材质: 连接各通道贴图
- 验证: 金属度/粗糙度值域, 法线贴图切线空间
- 测试: 不同光照条件下渲染效果

STEP 9: 验证 (Validation)
- 帧率: >60fps (PC端)
- Draw Call: 合理范围
- 碰撞: 物理仿真无穿模
- 视觉: 多角度检查无破面

ARROW FLOW: AI输出 → 网格提取 → 简化Remesh → UV → 烘焙 → LOD → 引擎 → Shader → 验证

Flat vector flowchart with horizontal pipeline. Clean connected steps.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for AI/extract steps, Mint (#B5E5CF) for processing steps, Lavender (#D5C6E0) for UV/texture steps, Peach (#FFD5C2) for engine steps, Coral Red (#E8655A) for validation pass/fail, Mustard Yellow (#F2CC8F) for key metrics
ELEMENTS: Horizontal 9-step pipeline with small rounded cards, format labels between steps (SDF→OBJ→UV-OBJ→FBX), mini icons for each step (brain/mesh/scissors/grid/palette/layers/gamepad/shader/checkmark), validation traffic light at end
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
