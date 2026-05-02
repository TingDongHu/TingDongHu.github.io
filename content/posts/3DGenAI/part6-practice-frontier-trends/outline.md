---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 6
---

## Illustration 1
**Position**: 6.1 核心开源框架详解
**Purpose**: 可视化3D GenAI生态的框架层级关系
**Visual Content**: 生态地图展示三层架构：底层几何基础设施（Kaolin/PyTorch3D：点云操作、可微渲染、Chamfer Distance），中层神经渲染框架（nerfstudio：模型↔场↔采样器↔渲染器），上层生成式3D框架（threestudio：几何↔引导↔提示→System），标注各框架定位和核心功能
**Filename**: 01-framework-ecosystem-map.png

## Illustration 2
**Position**: 6.1.1 nerfstudio
**Purpose**: 可视化nerfstudio的模块化架构
**Visual Content**: 信息图展示nerfstudio管线：DataManager(射线生成)↔Model(策略:proposal sampling+损失)↔Field(表示:哈希编码+MLP→σ,c)↔Sampler(均匀/PDF采样)↔Renderer(体渲染积分)，标注models与fields分离的设计哲学
**Filename**: 02-infographic-nerfstudio-architecture.png

## Illustration 3
**Position**: 6.1.2 threestudio
**Purpose**: 可视化threestudio的解耦生成管线
**Visual Content**: 信息图展示threestudio管线：文本/图像→PromptProcessor→Guidance(SDS/VSD/Zero123)→Geometry(NeRF/3DGS/Mesh)→渲染，标注System=Geometry+Guidance+Prompt的设计模式，YAML配置即可切换方法
**Filename**: 03-infographic-threestudio-pipeline.png

## Illustration 4
**Position**: 6.2 推荐入门实验路线
**Purpose**: 可视化8-12周的学习路径
**Visual Content**: 流程图展示学习路径：数学基础(线性代数/概率/优化)→3D表示基础(网格/SDF/体素)→NeRF实战(nerfstudio)→扩散模型理论→SDS方法(threestudio)→原生3D扩散(LRM/InstantMesh)→研究前沿(4D/世界模型/物理)，标注每周主题和关键产出
**Filename**: 04-flowchart-learning-path.png

## Illustration 5
**Position**: 6.6 总结与学习路线图
**Purpose**: 可视化3D GenAI的关键技术演进时间线
**Visual Content**: 时间线信息图：3D-GAN(2016, 体素生成首次成功)→NeRF(2020, 隐式场革命)→DreamFusion(2022, SDS突破2D→3D)→3DGS(2023, 实时神经渲染)→LRM(2023, 前馈大规模重建)→InstantMesh(2024, 端到端高质量Mesh)，每个节点标注核心创新
**Filename**: 05-timeline-3d-genai-evolution.png

## Illustration 6
**Position**: 6.5 前沿方向/6.6 总结
**Purpose**: 可视化未来趋势的四大方向
**Visual Content**: 框架图展示四大未来趋势：数据规模化(Objaverse-XL千万级→3D数据缩放定律)、多模态统一(3D+文本+图像统一编码→Any-to-3D)、3D大语言模型(场景理解+对话式编辑+布局生成)、物理合理化(可微物理引擎+物理引导扩散)，标注各方向的技术瓶颈和预期时间线
**Filename**: 06-framework-future-trends.png
