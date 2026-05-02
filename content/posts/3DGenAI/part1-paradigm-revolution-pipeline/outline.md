---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 7
---

## Illustration 1
**Position**: 1.1 工时金字塔章节开头
**Purpose**: 可视化传统3D角色资产制作各环节工时与AI压缩效果
**Visual Content**: 左右对比信息图：左侧为传统管线工时金字塔（高模2-5天→重拓扑1-2天→UV 0.5-2天→纹理3-7天→绑定3-10天→动画2-5天），右侧为AI辅助后压缩工时，用箭头和百分比标注人力替代比
**Filename**: 01-comparison-pipeline-hours.png

## Illustration 2
**Position**: 1.1.1 高模雕刻小节
**Purpose**: 展示法线烘焙原理——高模微观法线编码到低模法线贴图
**Visual Content**: 信息图展示高模→法线贴图→低模渲染的管线，标注关键概念：切线空间、TBN坐标系、RGB编码
**Filename**: 02-infographic-normal-baking.png

## Illustration 3
**Position**: 1.2 三重范式转移章节开头
**Purpose**: 可视化3D生成AI带来的三大范式转移
**Visual Content**: 框架图展示三个核心概念：门槛民主化（工具链精通→意图表达）、创意涌现性（确定性→概率性）、表示连续化（离散多边形→连续神经场），用三列对比布局
**Filename**: 03-framework-paradigm-shifts.png

## Illustration 4
**Position**: 1.3 应用场景章节
**Purpose**: 量化展示3D生成AI在不同领域的价值
**Visual Content**: 信息图展示6大应用场景的核心数据：游戏($500-$50K/角色)、影视Previs($4M-$10M)、VR/AR(500 vs 180万应用)、工业设计(1-3月→数小时)、数字孪生($1M-$5M/km²)、具身智能(40-60%迁移提升)
**Filename**: 04-infographic-application-value.png

## Illustration 5
**Position**: 1.4 全流程管线总览章节
**Purpose**: 将文字描述的管线架构可视化为清晰流程图
**Visual Content**: 流程图展示：输入侧(文本/图像/视频/点云/多视图)→核心生成层(VAE/GAN/Diffusion/AR + SDS/VSD)→输出侧(Mesh/NeRF/SDF/纹理)→后处理→验证与应用，各层用颜色区分
**Filename**: 05-flowchart-full-pipeline.png

## Illustration 6
**Position**: 1.5 AI阶梯式定位章节
**Purpose**: 可视化AI在3D管线中各环节的替代率阶梯
**Visual Content**: 阶梯/金字塔信息图，从底部"概念设计90%替代"到顶部"绑定与动画5-15%替代"，每层标注环节名和替代百分比，颜色渐变表示成熟度
**Filename**: 06-infographic-ai-positioning.png

## Illustration 7
**Position**: 1.5 三层解释法示例——3D高斯溅射
**Purpose**: 直观展示3DGS核心原理：离散高斯椭球→可微光栅化→实时渲染
**Visual Content**: 信息图展示3DGS三步过程：1)数百万各向异性3D高斯椭球编码场景 2)投影到2D平面(EWA Splatting) 3)α混合渲染，标注关键参数(μ,Σ,SH,α)和速度优势(100+ FPS vs NeRF)
**Filename**: 07-infographic-3dgs-principle.png
