---
illustration_id: 01
type: framework
style: vector-illustration
palette: macaron
---

3D GenAI生态地图 - Framework View

LAYER 1 (底层) - 几何基础设施 (Geometry Infrastructure):
- Kaolin (NVIDIA): 3D NumPy/SciPy
  * 点云↔体素↔网格转换 (CUDA加速)
  * Chamfer Distance / IoU / 法向量
  * DIB-R可微光栅化
- PyTorch3D (Meta): 批处理+可微渲染管线
  * Meshes异构批处理 / 多种相机模型
  * SoftPhongShader可微渲染
  * Laplacian平滑 / 法向一致性 / 边长损失
- 定位: "底层原语, 不提供端到端训练"

LAYER 2 (中层) - 神经渲染框架 (Neural Rendering):
- nerfstudio: NeRF的PyTorch
  * models(策略) ↔ fields(表示) 分离设计
  * 20+NeRF变体 (nerfacto/mipnerf/instant-ngp)
  * 数据加载 ↔ 训练 ↔ 渲染 ↔ 导出
  * CLI: ns-train / ns-render / ns-export
- 定位: "重建为主, 模块化研究平台"

LAYER 3 (上层) - 生成式3D框架 (Generative 3D):
- threestudio: Text-to-3D的PyTorch Lightning
  * System = Geometry + Guidance + PromptProcessor
  * Geometry: NeRF / 3DGS / Mesh (可替换)
  * Guidance: SDS / VSD / Zero123 (可替换)
  * YAML配置即可切换方法
- 定位: "生成为主, 解耦设计快速实验"

ARROWS: 底层→中层→上层 (依赖关系)
- Kaolin/PyTorch3D提供几何原语
- nerfstudio提供NeRF训练能力
- threestudio调用2D扩散先验+3D表示

Flat vector framework with three-layer architecture. Clear hierarchy.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Lavender (#D5C6E0) for Layer 1 (bottom), Blue (#A8D8EA) for Layer 2 (middle), Mint (#B5E5CF) for Layer 3 (top), Coral Red (#E8655A) for framework names and key features, Mustard Yellow (#F2CC8F) for positioning labels
ELEMENTS: Three horizontal layers stacked vertically, each layer as a wide card with framework boxes inside, vertical dependency arrows between layers, framework logo/name labels, positioning badges ("NumPy for 3D", "PyTorch for NeRF", "PyTorch Lightning for T23D")
ASPECT: 3:4

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
