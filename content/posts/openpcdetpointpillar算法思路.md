--- 
title: 【OpenPCDet】PointPillar算法思路
date: 2024-12-31T00:00:00+08:00
categories: ["3DComputerVison"]
tags: ["视觉算法", "自动驾驶", "目标检测"]
description: "PointPillar是一种高效的激光雷达点云3D检测模型，通过将点云划分为柱体并编码为伪图像，在保持高精度的同时实现了显著的实时检测速度优势。"
cover: "/img/pointcloud.png"
headerImage: "/img/Makima.png"
math: true
--- 


PointPillar 是一种用于三维物体检测的深度学习模型，尤其适用于激光雷达点云数据的处理。它的设计思想相对简洁，并且在保持高效性的同时能获得较高的精度。
[论文地址](https://arxiv.org/abs/1812.05784)
[代码地址](https://link.zhihu.com/?target=https%3A//github.com/SmallMunich/nutonomy_pointpillars)
## 前言
本文要解析的模型叫做[PointPillars](https://zhida.zhihu.com/search?content_id=167602095&content_type=Article&match_order=1&q=PointPillars&zhida_source=entity)，是2019年出自工业界的一篇Paper。
该模型最主要的特点是**检测速度和精度的平衡**。该模型的平均检测速度达到了62Hz，最快速度达到了105Hz，确实遥遥领先了其他的模型。这里我们引入[CIA-SSD](https://zhida.zhihu.com/search?content_id=167602095&content_type=Article&match_order=1&q=CIA-SSD&zhida_source=entity)**模型中的精度-速度图**，具体对比如下所示。
![Image](https://github.com/user-attachments/assets/2b4acd80-8c42-4b92-a8ee-34f9be41f0b4)
截止CIA-SSD论文发表前，PointPillars的检测速度都是遥遥领先的，而且精度也不低。
现有的一些研究喜欢将不规则、稀疏的点云数据按照以下两种方式进行处理，然后引入RPN层进行3D Bbox Proposal，这两种方法为：

- 一种是将点云数据划纳入一个个**体素（Voxel）**中，构成规则的、密集分布的体素集。常见的有**VoxelNet**和**SECOND**；
- 另一种从**俯视角度**将点云数据进行处理，获得一个个**伪图片**的数据。常见的模型有**MV3D和AVOD**。
PointPillar模型采用了一种不同于上述两种思路的点云建模方法。从模型的名称PointPillars可以看出，该方法将Point转化成一个个的**Pillar（柱体）**，从而构成了**伪图片**的数据。
然后对伪图片数据进行**BBox Proposal**就很简单了，作者采用了**SSD**的网络结构进行了Proposal。
## 数据处理
PointPillar的一大亮点是将点云划分为一个个的Pillar，从而构成了伪图片的数据。
如何构成这个伪图片呢？作者在论文中是给出了这样的图，如下。
![Image](https://github.com/user-attachments/assets/24ae971c-0384-4019-897b-37a988259979)
具体实现步骤如下：
- 按照点云数据所在的X，Y轴（不考虑Z轴）将点云数据划分为**一个个的网格**，凡是落入到一个网格的点云数据被视为其处在**一个pillar**里，或者理解为它们构成了一个Pillar。
- 每个点云用一个 $ D=9$ 维的向量表示，分别为 $(x,y,z,r,x_c,y_c,z_c,x_p,y_p)$。其中 $(x,y,z,r)$ 为该点云的真实坐标信息（三维）和反射强度（注在openpcdet的代码实现中是10维，多了一个zp，也就是该点在z轴上与该点所处pillar的z轴中心的偏移量）. $(x_c,y_c,z_c)$ 为该点云所处Pillar中所有点的几何中心; $x_p$ , $y_p$ 为 $x-x_c$ , $y-y_c$ ,反应了点与几何中心的**相对位置**。 
 - 假设每个样本中有 $P$ 个非空的pillars，每个pillar中有 $N$ 个点云数据，那么这个样本就可以用一个 $(D,P,N)$ 张量表示。
那么可能就有人问了，怎么保证每个pillar中有 $N$ 个点云数据呢？
如果每个pillar中的点云数据数据超过 $N$ 个，那么我们就随机采样至 $N$ 个；如果每个pillar中的点云数据数据少于 $N$ 个，少于的部分我们就填充为0；这样就实现了点云数据的张量化，具体过程如下图所示

![Image](https://github.com/user-attachments/assets/d66b3bbb-0681-4947-b1a6-a997bd14ed40)
实现张量化后，作者利用简化版本的PointNet对张量化的点云数据进行处理和特征提取。
特征提取可以理解为对点云的维度进行处理，原来的点云维度为  $D=9$  ,处理后的维度为 $C$ ,那么我们就获得了一个 $(C,P,N)$ 的张量。
接着，我们按照Pillar所在维度进行Max Pooling操作，即获得了 $(C,P)$ 维度的特征图。
为了获得伪图片特征，作者将 $ P$ 转换为 $(H,W)$ ,即 $P->H*W$ .那么我们就获得了形如 $(C,H,W)$ 的伪图片了。具体过程如下：
![Image](https://github.com/user-attachments/assets/5d8d4957-d83a-43b1-8a67-7b45fd05fb12)

 ## 网络结构
![Image](https://github.com/user-attachments/assets/4976b9ce-37d2-40f8-bad5-fc8508496d1e)
伪图片作者2D CNN的输入，用来进一步提取图片特征。
从图中可以看出，该2D CNN采用了两个网络。其中一个网络**不断缩小特征图的分辨率**，同时提升特征图的维度，因此获得了**三个不同分辨率的特征图**。
另一个网络对三个特征图进行上采样至相同大小，然后进行concatenation。
之所以选择这样架构，是因为不同分辨率的特征图负责不同大小物体的检测。比如分辨率大的特征图往往感受野较小，适合捕捉小物体（在[KITTI]中就是行人）。