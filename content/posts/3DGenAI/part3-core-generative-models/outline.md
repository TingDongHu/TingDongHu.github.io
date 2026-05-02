---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 7
---

## Illustration 1
**Position**: 3.1 体素与栅格生成 → 3.4 可微表面积生成 四大范式总览
**Purpose**: 对比四大3D生成范式的核心思想、代表方法、优势与局限
**Visual Content**: 四列对比信息图：体素/栅格（3D-GAN, OGN）、点云/结构（PointFlow, Point-E）、隐式场/神经场（NeRF, DreamFusion, 3DGS）、可微表面积（DIB-R, GET3D），每列标注核心表示形式、代表方法、优势、局限，用颜色区分
**Filename**: 01-comparison-generation-paradigms.png

## Illustration 2
**Position**: 3.3.1 NeRF原理完全推导
**Purpose**: 可视化NeRF体渲染推导链——从光线到最终图像
**Visual Content**: 信息图展示推导链：相机发出光线→沿光线采样点→每个点查询MLP得到密度σ和颜色c→透射率T累积→离散体渲染积分→最终像素颜色，标注关键公式和物理含义
**Filename**: 02-infographic-nerf-volumetric-rendering.png

## Illustration 3
**Position**: 3.3.3 DreamFusion与SDS
**Purpose**: 展示SDS优化循环的完整流程
**Visual Content**: 流程图展示SDS闭环：NeRF渲染图像→VAE编码到潜空间→加噪得到z_t→U-Net预测噪声→计算梯度(ε_φ - ε)→链式法则传播到NeRF→更新参数，标注CFG scale=100、冻结扩散模型、可微渲染等关键概念
**Filename**: 03-flowchart-sds-optimization.png

## Illustration 4
**Position**: 3.3.4 ProlificDreamer与VSD
**Purpose**: 对比SDS的delta分布假设与VSD的变分分布假设
**Visual Content**: 左右对比图：左侧SDS将渲染分布建模为delta函数（单点估计，导致过饱和和模式崩溃），右侧VSD建模为变分分布q(x|y)（含熵正则化，保持多样性），标注KL散度最小化和LoRA近似
**Filename**: 04-comparison-sds-vs-vsd.png

## Illustration 5
**Position**: 3.3.4 3D Gaussian Splatting生成式应用
**Purpose**: 展示基于3DGS的生成管线
**Visual Content**: 信息图展示3DGS生成管线：初始化高斯（椭球/SfM点云）→SDS优化循环→自适应密度控制（克隆/分裂/剪枝）→高斯泼溅渲染，标注关键参数（μ,Σ,SH,α）和速度优势
**Filename**: 05-infographic-3dgs-generation.png

## Illustration 6
**Position**: 3.3.4 Magic3D两阶段策略
**Purpose**: 可视化Magic3D由粗到精的两阶段架构
**Visual Content**: 框架图展示两阶段：阶段1粗NeRF（Instant-NGP哈希编码 + 64×64 SDS → 拓扑探索），阶段2精细DMTet（可微Marching Tetrahedra + 512×512 SDS + nvdiffrast光栅化 → 几何精修），中间用箭头标注"隐式→显式转换"
**Filename**: 06-framework-two-stage-strategy.png

## Illustration 7
**Position**: 3.5 前馈vs优化范式对比
**Purpose**: 对比前馈模型与优化模型的核心差异
**Visual Content**: 左右对比框架图：左侧前馈模型（LRM/InstantMesh/TripoSR：单次前向、秒级生成、高确定性、受训练数据限制），右侧优化模型（DreamFusion/ProlificDreamer：迭代优化、分钟级、2D先验强约束、低确定性），底部标注融合趋势
**Filename**: 07-comparison-feedforward-vs-optimization.png
