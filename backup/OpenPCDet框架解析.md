随着自动驾驶与机器人技术的不断发展，基于点云表征的3D目标检测领域在近年来取得了不断的发展。然而，层出不穷的[点云数据集]（KITTI、NuScene、Lyft、Waymo、PandaSet等）在数据格式与3D坐标系上往往定义各不相同，各式各样的点云感知算法（point-based、 voxel-based、one-stage/two-stage等）也形态各异，使得相关研究者难以在一个统一的框架内进行各种组合实验。
## OpenPCDet简介
### OpenPCDet是什么
OpenPCDet: Open-MMLab 面向LiDAR点云表征的3D目标检测代码库
[OpenPCDet的github链接](https://github.com/open-mmlab/OpenPCDet)
- OpenPCDet 是一套基于**PyTorch**实现的点云3D目标检测代码库。

- **设计思想**：点云数据集（KITTI、NuScene、Lyft、Waymo、PandaSet等）在数据格式与3D坐标系上往往定义各不相同，各式各样的点云感知算法（point-based、 voxel-based、one-stage/two-stage等）也形态各异，因此基于**数据-模型分离的顶层代码框架设计思想**，设计一个统一的架构，使得相关研究者可以在一个统一的框架内进行各种组合实验。

### 数据-模型分离的顶层代码框架
不同于图像处理，点云3D目标检测中不同数据集的繁多3D坐标定义与转换往往使研究者迷失其中。为此，PCDet定义了统一的规范化3D坐标表示贯穿整个数据处理与模型计算，从而将数据模块与模型处理模块完全分离，其优势体现在: 
-  研究者在研发不同**结构模型**时，统一使用标准化的3D坐标系进行各种相关处理（比如计算loss、RoI Pooling和模型后处理等），而无需理会不同数据集的坐标表示差异性；
-  研究者在添加新数据集时，只需写少量代码将原始数据转化到标准化坐标定义下，PCDet将**自动进行数据增强并适配**到各种模型中。

![Image](https://github.com/user-attachments/assets/85dba052-0252-408b-b17d-e660239476c2)
### 统一的3D目标检测坐标定义
PCDet 中采用了固定的统一点云坐标系，以及更规范的3D检测框定义，贯穿整个数据增强、处理、模型计算以及检测后处理过程。3D检测框的7维信息定义如下：
``` python
3D bounding box: (cx, cy, cz, dx, dy, dz, heading)
```
其中，(cx, cy, cz) 为物体3D框的**几何中心**位置，(dx, dy, dz)分别为物体3D框在heading角度为0时沿着x-y-z三个方向的长度，heading为物体在**俯视图下的朝向角**(沿着x轴方向为0度角，逆时针x到y角度增加)。

![Image](https://github.com/user-attachments/assets/5dc81efb-791f-4d33-901e-1887a064c1e3)

### 灵活全面的模块化模型拓扑设计
如下图所示的灵活且全面的模块化设计，我们在PCDet中搭建3D目标检测框架只需要写config文件将所需模块定义清楚，然后PCDet将自动根据模块间的拓扑顺序组合为3D目标检测框架，来进行训练和测试。
![Image](https://github.com/user-attachments/assets/5e9bfe4c-c3ff-424a-a85f-a8d9bdffd679)
PCDet可以支持目前已有的绝大多数面向LiDAR点云的3D目标检测算法，包括[voxel-based](https://zhida.zhihu.com/search?content_id=121936716&content_type=Article&match_order=2&q=voxel-based&zhida_source=entity)，point-based，point-voxel hybrid以及one-stage/two-stage等等3D目标检测算法

## 代码解析
### 框架文件结构
文件结构如下图所示：
![Image](https://github.com/user-attachments/assets/6d4be273-4f95-4807-b33a-e78b94d08b19)
各目录作用如下所示：
![Image](https://github.com/user-attachments/assets/764e707c-7684-4ced-abcc-dc970b61ad6e)

### 数据处理流程
结构示意图：
![Image](https://github.com/user-attachments/assets/b621e896-d444-4d79-bd4a-11d716ac48dc)
- **步骤1:getitem** 从磁盘上加载数据并统一坐标系。如果只更换数据集，则需要重写__getitem__
- **步骤2:data_augmentor** 数据增强的方法。例如随机裁剪、随机旋转等...
![Image](https://github.com/user-attachments/assets/78f9b9cb-e991-481f-8a96-e6d0ab641a04)
- **步骤3:point_feature_encoder** 选择一些特征编码，输入的特征是points:(N,3+C_in)经过选择和编码后，输出的特征是points:(N,3+C_out)
![Image](https://github.com/user-attachments/assets/389cb585-372d-4594-ad27-becd63137539)
- **步骤4:data_processor**处理输入的数据，比如mask_point_boxes_outside_range、sample_points等
![Image](https://github.com/user-attachments/assets/a0d7e935-a771-4212-9854-efa5f56b0581)
- **步骤5:collate_batch**将数据整理为batch

### 模型的前向传播和最优
以point_rcnn 为例，定义了一个PointRCNN的类，继承的是Detector3DTemplate的类。

![Image](https://github.com/user-attachments/assets/407dbb91-fef7-4426-9857-de599280f75a)

#### 前向传播
首先遍历**module_list**, 通过**topology** 顺序的调用各个模型。如果是训练过程(training ), 则调用**get_traing_loss** 计算损失。如果是推理过程，则调用**post_processing** 进行后处理
#### 最优化
计算的损失包括两个部分
DETECTOR.get_training_loss()
HEAD.get_loss()

## 模型
### detector文件
detector文件的结构如下
![Image](https://github.com/user-attachments/assets/0224efbe-ebe5-4f9b-a8cb-268b0a6f90aa)
模板基本内容包括：
- 继承DetectorTemplate 来写自定义的detector
- 写自定义的配置文件
- 在对应的目录下写对应的模型
- 重载forward() 函数
- 重载get_training_loss() 函数

### 3Dbackbone network
backones_3d的存放位置：
![Image](https://github.com/user-attachments/assets/ce8f4bcf-56a3-4a6e-8af5-0963de9190d4)
3d主干网络的作业：提取基于提体素的或者基于点云的特征
3d主干网络主要要有如下几种：
**3d encoder with sparse convolution(with VFE）**
功能：通过稀疏卷积进行编码
实例：VoxelBackBone8x、VolxelResBackBone8x
**3d UNet with sparse convolution(with VFE)**
功能：通过稀疏网络进行编码和解码两个部分
实例：UNetV2
**point-wise networks(PointNet++)**
功能: 用PointNet++ 直接提取点的特征
实例：PointNet2MSG

### 2Dbackbone network
文件目录：
![Image](https://github.com/user-attachments/assets/f007dcff-7277-4d19-abc9-95b520b2a7d1)
**2d主干网络的作用**： 提取2d特征图。
2D主干网络主要有如下几种：
**Map_to_bev_module(把3d特征映射到2d上)**
- HeightCompression
- PointPillarScatter

**2d convolution encoder with FPN-like unsampling**
- BaseBEVBackbone
### Denseheads
Denseheads文件目录：
![Image](https://github.com/user-attachments/assets/980ccc52-e7d9-445a-9803-2ed5010ab561)
**Denseheads的作用**：
生成dense 3d boxes, 真正进行检测的过程
**AnchorHead包含如下两部分：**
target assigning：对于每个anchor判断是否是正样本以及要朝着那个groud truth 回归。
head loss calculation：计算loss，包括分类和回归的损失。
分类：
**基于BEV 特征的 Dense head （继承于AnchorHeadTemplate）**
- AnchorHeadSingle: 只输入一个特征图，基于anchor进行检测
- AnchorHeadMulti：输入多个特征图,基于anchor检测
- CentorHead：anchor- free检测，对于每个pixel输出一个检测框。

**基于点特征的Dense head （继承于PointHeadTemplate）**
- PointHeadSimple： 只做分割，判断每个点是前景点还是背景点。
- PointHeadBox： 不仅做分割，还做预测。对于每个点预测一个3d 的bonding box。
- PointIntraPartOffsetHead： 除了分割和预测外，还可以预测Intra part offset。
### RolHeads
RoIHeads的存放位置：
![Image](https://github.com/user-attachments/assets/17a5b138-1960-4093-b1f6-2e736157fc86)
**RolHeads的作用**：Refine 3D proposals with RoI-aligned features、
Extract RoI-aligned features
proposal_layer
ProposalTargetLayer
Head loss calcution
二阶段的ROI检测（继承于ROITemplate）。
PointRCNNHead
PartA2Head
PVRCNNHead
### 配置文件
配置文件的存放路径：
![Image](https://github.com/user-attachments/assets/7c784dba-6c63-48f9-b8ee-777e084d709f)
通过.yaml文件进行多层次的配置。
例如如下图所示的pv_rcnn.yaml 是个整体的配置。其中嵌套了三个下一级的配置，包括DATA_CONFIG、MODEL、OPTIMIZATION

![Image](https://github.com/user-attachments/assets/340064d8-6c57-4b27-9f2d-ce5f90a4ed60)

## 框架拓展
### 使用自定义的数据集
步骤如下：
- 继承DatesetTemplate 写自己的DatasetModule
- 重载self.__getitem__() 函数来加载点云或者gt_boxes, 并把它们转换成统一的坐标系。
- 调用self.prepare_data() 去处理数据
- 重载self.generate_prediction_dicts() 函数把预测结果转换成我们需要的格式。
- 重载self.evaluation() 函数来评估模型的性能

### 使用自定义的模型
步骤如下：
- 继承DetectorTemplate 来写自定义的detector
- 写自定义的配置文件
- 在对应的目录下写对应的模型
- 重载forward() 函数
- 重载get_training_loss() 函数