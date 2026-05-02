--- 
title: 【OpenPCDet】模型预测结果解读
date: 2024-03-02T00:00:00+08:00
categories: ["3DComputerVison"]
tags: ["OpenPCDet", "自动驾驶", "目标检测"]
description: "OpenPCDet模型推理输出为字典，包含目标类别、位置、尺寸等关键字段，不同模型结构类似但字段可能略有差异。"
cover: "/img/pointcloud.png"
headerImage: "/img/Makima.png"
math: true
--- 

OpenPCDet模型的推理结果以字典形式输出，包含检测目标的类别、位置、尺寸等关键信息。不同模型输出结构类似，但具体字段可能略有差异。 



![在这里插入图片描述](openpcdet模型预测结果解读/aab43926a7fe400898d4bfc41f661d63.png)
在 OpenPCDet  中，每个模型的推理结果通常是**一个包含多个键值对的字典**，其中包含与 3D 检测任务相关的信息。不同模型的输出结构可能略有不同，但一般来说，模型输出通常包含以下几个关键字段：
以下给一段`output/kitti_models/pointrcnn/default/eval/eval_with_train/epoch_80/val/result.pkl`中选取某一帧的结果示例,提取为json文件便于阅读：

```json
{
"pointrcnn": [
        {
            "name": [
                "Car",
                "Pedestrian",
                "Pedestrian",

            ],
            "truncated": [
                0.0,
                0.0,
                0.0,

            ],
            "occluded": [
                0.0,
                0.0,
                0.0,

            ],
            "alpha": [
                -4.0102105140686035,
                -1.6028798818588257,
                -4.731999397277832,

            ],
            "bbox": [
                [
                    0.0,
                    196.87057495117188,
                    410.6382141113281,
                    373.0
                ],
                [
                    688.0215454101562,
                    172.8148193359375,
                    709.7300415039062,
                    224.52003479003906
                ],
                [
                    667.0341186523438,
                    172.51962280273438,
                    687.4990844726562,
                    223.23146057128906
                ],
              
            ],
            "dimensions": [
                [
                    4.10535192489624,
                    1.4689395427703857,
                    1.6220554113388062
                ],
                [
                    0.9827990531921387,
                    1.7112400531768799,
                    0.6871805191040039
                ],
                [
                    0.5967018008232117,
                    1.6898497343063354,
                    0.67041015625
                ],

            ],
            "location": [
                [
                    -2.7540218830108643,
                    1.6045180559158325,
                    4.157565593719482
                ],
                [
                    3.2612111568450928,
                    1.4242191314697266,
                    24.295761108398438
                ],
                [
                    2.5298221111297607,
                    1.3910222053527832,
                    24.260332107543945
                ],

            ],
            "rotation_y": [
                -4.574054718017578,
                -1.476109504699707,
                -4.6344404220581055,

            ],
            "score": [
                0.9997606873512268,
                0.9978153705596924,
                0.9920910596847534,

            ],
            "boxes_lidar": [
                [
                    4.406521797180176,
                    2.786322832107544,
                    -0.915142297744751,
                    4.10535192489624,
                    1.6220554113388062,
                    1.4689395427703857,
                    3.003258228302002
                ],
                [
                    24.574119567871094,
                    -3.132066488265991,
                    -0.7385169863700867,
                    0.9827990531921387,
                    0.6871805191040039,
                    1.7112400531768799,
                    -0.09468691051006317
                ],
                [
                    24.53524398803711,
                    -2.4012603759765625,
                    -0.7080038189888,
                    0.5967018008232117,
                    0.67041015625,
                    1.6898497343063354,
                    3.0636441707611084
                ],

            ],
        }
    ],
}
```
## 内容解读
### name
含义：检测到的物体类别。
​示例：`["Car", "Pedestrian", "Pedestrian", ...]`
​说明：
- "Car" 表示检测到的物体是车辆。
- "Pedestrian" 表示检测到的物体是行人。

### truncated
含义：物体被截断的程度。
​示例：`[0.0, 0.0, 0.0, ...]`
​说明：
取值范围为 `[0, 1]`，`0.0` 表示物体未被截断，`1.0 `表示物体被完全截断。
### occluded
含义：物体被遮挡的程度。
​示例：`[0.0, 0.0, 0.0, ...]`
​说明：
取值范围为 `[0, 2]`，`0.0` 表示物体未被遮挡，`1.0` 表示物体被部分遮挡，`2.0` 表示物体被完全遮挡。
### alpha
含义：物体的视角角度（观察角度）。
​示例：`[-4.0102105140686035, -1.6028798818588257, ...]`
​说明：

- 表示物体相对于相机的视角角度（以弧度为单位）。
- 取值范围为`[-π, π]`。

### bbox
含义：物体在图像中的 2D 边界框。
​示例：`[[0.0, 196.87057495117188, 410.6382141113281, 373.0], ...]`
​说明：
- 每个边界框的格式为 `[x_min, y_min, x_max, y_max]`，表示边界框的左上角和右下角坐标。
- 坐标单位为像素。

### dimensions
含义：物体的 3D 尺寸（长、宽、高）。
​示例：`[[4.10535192489624, 1.4689395427703857, 1.6220554113388062], ...]`
​说明：
每个物体的尺寸格式为 `[length, width, height]`，单位为米。
### location
含义：物体在相机坐标系中的 3D 位置（中心点坐标）。
​示例：`[[-2.7540218830108643, 1.6045180559158325, 4.157565593719482], ...]`
​说明：
- 每个物体的位置格式为 `[x, y, z]`，单位为米。
- 坐标系为相机坐标系。

### rotation_y
含义：物体绕相机坐标系的 y 轴的旋转角度（偏航角）。
​示例：`[-4.574054718017578, -1.476109504699707, ...]`
​说明：
单位为弧度，取值范围为`[-π, π]`。

### score
含义：检测结果的置信度分数。
​示例：`[0.9997606873512268, 0.9978153705596924, ...]`
​说明：
取值范围为 `[0, 1]`，`1.0 `表示检测结果非常可靠。

### boxes_lidar
含义：物体在激光雷达坐标系中的 3D 边界框。
​示例：`[[4.406521797180176, 2.786322832107544, -0.915142297744751, 4.10535192489624, 1.6220554113388062, 1.4689395427703857, 3.003258228302002], ...]`
​说明：
- 每个边界框的格式为 `[x, y, z, length, width, height, ry]`，单位为米。
- `(x, y, z)` 表示边界框的中心点坐标。
- `(length, width, height)` 表示边界框的尺寸。
- `ry` 表示边界框绕激光雷达坐标系的 z 轴的旋转角度（偏航角），单位为弧度。


## 坐标系说明
相机坐标系：

- x 轴：向右（图像右侧）。
- y 轴：向下（图像底部）。
- z 轴：向前（相机光轴方向）。

激光雷达坐标系：

- x 轴：向前（车辆前进方向）。
- y 轴：向左（车辆左侧）。
- z 轴：向上（垂直于地面）。

## 数据对应关系
### location 和 ​boxes_lidar：
location 是基于相机坐标系的，而 boxes_lidar 是基于激光雷达坐标系的。
如果需要将 location 转换到激光雷达坐标系，可以使用 KITTI 提供的外参矩阵。
### bbox 和 ​boxes_lidar：
bbox 是物体在图像中的 2D 边界框，而 boxes_lidar 是物体在激光雷达坐标系中的 3D 边界框。

## 提取json文件的代码
有朋友留言问我是怎么把pkl文件提取出来的，附下面的代码供参考：
使用时记得替换路径
```python
import pickle
import json
import numpy as np
import os

# 指定需要查看的 frame_id
target_frame_id = "000015"

# 所有模型的推理结果文件路径
result_paths = [
    '/home/tdhu/OpenPCDet/output/kitti_models/PartA2_free/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/pointpillar/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/pointrcnn/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/pointrcnn_iou/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/pv_rcnn/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/second/default/eval/eval_with_train/epoch_80/val/result.pkl',
    '/home/tdhu/OpenPCDet/output/kitti_models/second_iou/default/eval/eval_with_train/epoch_80/val/result.pkl'
]

# 处理 numpy 数据，转换为 Python 可序列化的数据结构
def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # numpy 数组转换为列表
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)  # numpy 浮点数转换为 Python float
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)  # numpy 整数转换为 Python int
    return obj  # 其他数据类型保持不变

# 存储所有模型推理出的 `frame_id` 结果
all_model_results = {}

for result_path in result_paths:
    # 修正模型名称提取方式
    path_parts = result_path.split('/')
    if "kitti_models" in path_parts:
        model_index = path_parts.index("kitti_models") + 1  # 获取模型名索引
        model_name = path_parts[model_index]  # 获取模型名称
    else:
        model_name = "Unknown"

    try:
        with open(result_path, "rb") as f:
            result_data = pickle.load(f)

        # 确保数据是列表
        if isinstance(result_data, list):
            # 查找匹配的 frame_id
            matched_frames = [frame for frame in result_data if frame.get("frame_id") == target_frame_id]

            if matched_frames:
                print(f"模型 {model_name} 找到 {len(matched_frames)} 个匹配 frame_id = {target_frame_id} 的数据")
                all_model_results[model_name] = matched_frames  # 存储该模型的匹配数据
            else:
                print(f"模型 {model_name} 未找到 frame_id = {target_frame_id} 的数据")
        else:
            print(f"模型 {model_name} 数据格式异常: {type(result_data)}")

    except Exception as e:
        print(f"加载模型 {model_name} 的数据时发生错误: {e}")

# 如果找到数据，则保存为 JSON 文件
if all_model_results:
    output_json_path = "output.json"
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_model_results, f, indent=4, ensure_ascii=False, default=convert_to_serializable)
    
    print(f"所有模型推理的 JSON 结果已保存为 {output_json_path}")
else:
    print("未找到任何匹配的 frame_id 数据")

```