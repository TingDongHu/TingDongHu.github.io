---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 6
---

## Illustration 1
**Position**: 4.1.1 Marching Cubes完全算法详解
**Purpose**: 可视化Marching Cubes从SDF网格到三角网格的提取过程
**Visual Content**: 信息图展示：3D SDF网格→8角点采样→256配置→对称归约15种唯一→EDGE_TABLE/TRI_TABLE查表→线性插值→三角面提取，标注歧义面问题和渐近判定器解决方案
**Filename**: 01-infographic-marching-cubes.png

## Illustration 2
**Position**: 4.2 网格平滑与Remeshing
**Purpose**: 展示重拓扑与Remesh的完整流程
**Visual Content**: 流程图展示：高模（密集三角面）→拓扑分析（非流形边/高价顶点检测）→边分裂/坍缩/翻转→四边面网格→质量验证（三角形质量/Valence/边长均匀性），标注QEM简化与Laplacian平滑的角色
**Filename**: 02-flowchart-retopology-remesh.png

## Illustration 3
**Position**: 4.3 UV展开与纹理管线
**Purpose**: 可视化UV展开的数学过程
**Visual Content**: 信息图展示UV展开四步：3D表面→接缝切割（标注切割线选择）→展开扁平化（LSCM/ABF++最小化畸变）→[0,1]²纹理空间打包（texel密度一致性），标注面积畸变σ₁σ₂和角度畸变σ₁/σ₂
**Filename**: 03-infographic-uv-unwrapping.png

## Illustration 4
**Position**: 4.3.2 纹理烘焙管线
**Purpose**: 展示PBR纹理烘焙的完整管线
**Visual Content**: 流程图展示：高模细节→射线投射→烘焙目标(Albedo漫反射/Normal法线/Roughness粗糙度/Metallic金属度/AO环境遮蔽)→低模+贴图集，标注切线空间TBN矩阵和PBR物理含义
**Filename**: 04-flowchart-texture-baking.png

## Illustration 5
**Position**: 4.4.1 LOD策略
**Purpose**: 可视化LOD多级细节层级
**Visual Content**: 信息图展示LOD层级：LOD0（完整细节10万面, 0-5m）→LOD1（50%面数, 5-7m）→LOD2（25%面数, 7-10m）→LOD3（12.5%面数+法线贴图补偿, 10m+），标注切换距离√2倍递增和屏幕投影误差ε∝1/d
**Filename**: 05-infographic-lod-generation.png

## Illustration 6
**Position**: 4.4.2 自动化管线
**Purpose**: 展示从AI输出到引擎集成的完整管线
**Visual Content**: 流程图展示：AI生成输出→Marching Cubes网格提取→QEM简化→Remesh→UV展开→PBR纹理烘焙→LOD链生成→引擎导入→Shader配置→验证通过，每步标注输入/输出格式
**Filename**: 06-flowchart-engine-integration.png
