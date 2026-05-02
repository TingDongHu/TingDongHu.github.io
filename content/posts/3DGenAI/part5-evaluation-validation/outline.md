---
type: mixed
density: rich
style: vector-illustration
palette: macaron
image_count: 6
---

## Illustration 1
**Position**: 5.4 建立完整评估矩阵
**Purpose**: 可视化多维评估框架的四大支柱
**Visual Content**: 框架图展示四大评估支柱：几何精度（CD/EMD/F-Score）、视觉保真（LPIPS/SSIM/PSNR）、语义对齐（CLIP Score/R-Precision）、物理合规（抓取成功率/水密性），中心为被评估的3D资产，四支柱环绕，标注权重建议
**Filename**: 01-framework-evaluation-dimensions.png

## Illustration 2
**Position**: 5.2.1 几何质量指标
**Purpose**: 可视化三大几何指标的数学含义和视觉差异
**Visual Content**: 信息图展示三个指标：Chamfer Distance（双向最近邻距离公式+覆盖/精度分解）、EMD（最优传输/Sinkhorn迭代）、F-Score（Precision/Recall/F_τ调和平均+阈值可视化），每个指标配简图说明
**Filename**: 02-infographic-geometric-metrics.png

## Illustration 3
**Position**: 5.2.2 视觉质量指标
**Purpose**: 可视化三大视觉指标的层级关系
**Visual Content**: 信息图展示三个指标层级：PSNR（像素级MSE变换，标注"与感知非单调"缺陷）、SSIM（亮度+对比度+结构三分量，局部窗口统计）、LPIPS（VGG深度特征+可学习权重，标注"与人类感知对齐"），从低级到高级的递进关系
**Filename**: 03-infographic-visual-metrics.png

## Illustration 4
**Position**: 5.4 指标间的关联与冲突
**Purpose**: 可视化指标间的矛盾和trade-off
**Visual Content**: 信息图展示冲突案例：CD↓但视觉质量↓（过平滑表面CD低但看起来模糊）、CLIP↑但几何↓（纹理符合文本但几何扭曲，如"毛茸茸"→膨胀几何）、多样性↑但保真度↓，用trade-off曲线/跷跷板图表示，标注帕累托改进要求
**Filename**: 04-infographic-metric-conflicts.png

## Illustration 5
**Position**: 5.2.3 CLIP Score
**Purpose**: 可视化CLIP Score在3D评估中的计算流程
**Visual Content**: 信息图展示：3D资产→多视角渲染(4+视角)→CLIP图像编码→文本CLIP编码→余弦相似度→CLIP Score，标注提示工程敏感性和训练分布偏差两个陷阱，以及CLIP R-Precision作为补充
**Filename**: 05-infographic-semantic-alignment.png

## Illustration 6
**Position**: 5.3 下游任务驱动评估
**Purpose**: 展示功能性验证的完整流程
**Visual Content**: 流程图展示：生成3D资产→碰撞体生成(V-HACD凸包分解)→骨骼绑定测试→物理仿真(抓取/碰撞/稳定性)→引擎渲染(帧率/Draw Call)→通过/失败判定，标注"看起来对≠功能上对"的核心洞察
**Filename**: 06-flowchart-functional-validation.png
