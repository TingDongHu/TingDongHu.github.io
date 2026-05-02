---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 7
---

# Part2 先修知识体系 - 插图大纲

## Illustration 01: 五种3D表示方法总览
- **Position**: Section 2.1.1 开头，五种核心表示方法概述处
- **Filename**: `01-infographic-3d-representations.png`
- **Content**: 五种3D表示（Mesh/Voxel/PointCloud/SDF/NeRF）的核心数学定义、直觉比喻、优缺点对比卡片

## Illustration 02: 表示转换链
- **Position**: Section 2.1.1 末尾，表示转换链的数学细节处
- **Filename**: `02-diagram-representation-conversion.png`
- **Content**: Mesh/Voxel/PointCloud/SDF/NeRF之间的转换路径与关键算法（Marching Cubes, Poisson重建, FPS, Ball-Pivoting等）

## Illustration 03: 多视图几何与对极约束
- **Position**: Section 2.1.2，多视图几何基础处
- **Filename**: `03-infographic-multi-view-geometry.png`
- **Content**: 针孔相机模型、内外参矩阵K/[R|t]、对极几何要素、SfM/MVS流程、Janus问题的对极几何解释

## Illustration 04: 渲染管线双路径
- **Position**: Section 2.1.3，渲染基础处
- **Filename**: `04-infographic-rendering-pipeline.png`
- **Content**: 光栅化管线5步骤（顶点处理→图元装配→光栅化→片元着色→深度测试）与光线追踪（Whitted-Style + 路径追踪 + 渲染方程）双路径对照

## Illustration 05: 四大生成模型推导总览
- **Position**: Section 2.2.1，生成模型全家桶处
- **Filename**: `05-infographic-generative-models.png`
- **Content**: GAN（JS散度/WGAN）、VAE（ELBO/重参数化）、扩散模型（前向加噪/反向去噪）、自回归（链式法则）四者核心公式与直觉

## Illustration 06: PointNet系列架构
- **Position**: Section 2.2.2，PointNet系列深度解析处
- **Filename**: `06-infographic-pointnet-architecture.png`
- **Content**: PointNet对称性定理（共享MLP+Max Pooling）、T-Net对齐、PointNet++分层架构（FPS→Ball Query→Mini-PointNet）、与2D CNN类比

## Illustration 07: 扩散模型完整数学
- **Position**: Section 2.2.1，扩散模型从零推导处（最重要）
- **Filename**: `07-infographic-diffusion-math.png`
- **Content**: 前向过程 x_t公式推导、反向过程损失函数、DDPM采样算法、CFG公式与直觉解释、在3D中的优势
