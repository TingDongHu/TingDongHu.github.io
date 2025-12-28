--- 
title: 【OpenPCDet】模型的数据采样训练
date: 2024-12-20T00:00:00+08:00
categories: ["3DComputerVison"]
tags: ["OpenPCDet", "自动驾驶"]
description: "OpenPCDet框架通过修改KITTI数据集的ImageSet索引文件，可便捷创建不同训练子集，无需操作原始点云文件。通过脚本采样生成新索引文件，并在配置文件中指定即可启动训练。"
cover: "/img/pointcloud.png"
headerImage: "/img/Makima.png"
math: true
--- 



在**OpenPCDet**中，KITTI 数据集的 ImageSet 中已经包含了训练和测试数据的索引信息，这使得可以不必直接扫描点云数据文件来获取某个特定的数据集。通过修改 ImageSet 中的索引，就可以直接选择不同的数据帧来进行训练、测试或推理。
### 1. KITTI 数据集中的 ImageSet
imageset 文件夹包含了多个文本文件，其中每个文件列出了训练和测试数据的帧索引。这些文件通常以如下格式命名：
``` bash
data/
  ├── kitti/
  │   ├── ImageSets/
  │   │   ├── train.txt      # 训练集的帧索引
  │   │   ├── val.txt        # 验证集的帧索引
  │   │   └── test.txt       # 测试集的帧索引
```
每个 txt 文件中列出了一系列的帧编号，例如：
``` python
000000
000001
000002
...
```
这些帧编号对应的是 velodyne 文件夹中的 .bin 点云数据文件.

### 2. 修改索引文件
此处我想要基于Kitti数据集进行采样，生成十个不同的用于训练的数据集
可以直接原本的train.txt进行采样，将其保存为一个新的索引集
在kitti文件路径下新建一个脚本文件
``` python
import random

# 读取原始的 train.txt 文件
with open('kitti/training/imageset/train.txt', 'r') as f:
    lines = f.readlines()

# 随机采样 10 组数据
num_samples = 1000  # 每组采样的帧数量
num_groups = 10  # 需要采样的组数

# 随机生成 10 组数据集
for i in range(1, num_groups + 1):
    # 随机选择 1000 个帧
    sampled_lines = random.sample(lines, num_samples)

    # 保存到不同的 train_sampledX.txt 文件中
    sampled_file_path = f'kitti/training/imageset/train_sampled{i}.txt'
    with open(sampled_file_path, 'w') as f:
        f.writelines(sampled_lines)

    print(f"Group {i} saved to {sampled_file_path}")
```
运行以上代码即可在原本的目录下生成一系列的采样数据集
![image](https://github.com/user-attachments/assets/ac52c130-cc24-4b59-b33c-db3ccc6649a5)
### 2.使用采样数据进行训练
首先找到kitti_dataset.yaml文件
#### 关于Kitti_dataset.yaml文件
xxxxxxxxxx pip uninstall spconv-cu113pip install spconv-cu102python
- 数据集根目录 (DATASET_ROOT)：指示 KITTI 数据集所在的根路径。
- 训练和验证集的索引文件路径 (TRAIN_SET, VAL_SET)：指定训练和验证集的帧索引文件路径（即 train.txt 和 val.txt）。
- 类别定义：包括 3D 检测任务中所使用的类别，例如 Car、Pedestrian、Cyclist 等。
- 其他参数：可能包括图像和点云的预处理设置，数据增强方法等。
#### 如何修改 kitti_dataset.yaml 使用新生成的 train_sampled.txt
在该文件内容中找到DATA_SPLIT
默认值如下示例：
``` yaml
DATA_SPLIT: {
    'train': train,
    'test': val
}
```
使用上面生成的新的索引只需修改‘train’键的值为train_sampled1/train_sampled2保存即可
### 3.启动训练
``` bash
python tools/train.py --cfg_file tools/cfgs/kitti_models/pointpillar.yaml
```
训练中
![image](https://github.com/user-attachments/assets/5387318c-bf71-464a-b56f-48ef65f28e88)