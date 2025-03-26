前段时间在做实验的时候，想将多个模型的可视化结果绘制在一张点云数据上，批量保存后进行观测和实验，发现OpenPCDet本身没有这样的功能，提供的可视化工具Demo也不好用，所以自己鼓捣了一段时间，作此博客。
## 框架本身提供的工具
OpenPCDet框架本身提供了一些可视化的工具,工具在目录`tools/visual_utils`下，以及一个示例demo。在`tools/demo.py`中可以看到框架提供的demo样式。
框架demo的几个特点；
- **即时推理**，通过传入三个形参`xx.yaml`,`xx.epochxx.pth`,`xx.bin`，将X模型对X点云数据的推理结果可视化。
- **库二选一**，通过可选择的库`open3d`或者`Mayavi`库进行可视化，
- **残缺性**，通过demo可视化的结果由于性能考虑，会裁切四分之一进行推理和展示。

### 工具的解读与注释
`tools/visual_utils/open3d_vis_utils.py`内代码注释如下：
```python
"""
Open3d visualization tool box
Written by Jihan YANG
All rights preserved from 2021 - present.
"""
import open3d  # 导入Open3D库，用于3D数据可视化
import torch  # 导入PyTorch库，用于处理张量
import matplotlib  # 导入Matplotlib库，用于颜色映射
import numpy as np  # 导入NumPy库，用于数值计算

# 预定义的颜色映射，用于不同类别的框
box_colormap = [
    [1, 1, 1],  # 白色
    [0, 1, 0],  # 绿色
    [0, 1, 1],  # 青色
    [1, 1, 0],  # 黄色
]

def get_coor_colors(obj_labels):
    """
    根据对象的标签为每个点分配颜色。

    Args:
        obj_labels: 1表示地面，大于1的标签表示不同的实例簇。

    Returns:
        rgb: [N, 3]. 每个点的颜色。
    """
    colors = matplotlib.colors.XKCD_COLORS.values()  # 获取Matplotlib的XKCD颜色集
    max_color_num = obj_labels.max()  # 获取最大的标签值

    color_list = list(colors)[:max_color_num+1]  # 根据最大标签值截取颜色列表
    colors_rgba = [matplotlib.colors.to_rgba_array(color) for color in color_list]  # 将颜色转换为RGBA格式
    label_rgba = np.array(colors_rgba)[obj_labels]  # 根据标签值分配颜色
    label_rgba = label_rgba.squeeze()[:, :3]  # 去掉透明度通道，只保留RGB

    return label_rgba

def draw_scenes(points, gt_boxes=None, ref_boxes=None, ref_labels=None, ref_scores=None, point_colors=None, draw_origin=True):
    """
    绘制3D场景，包括点云、地面真值框和参考框。

    Args:
        points: 点云数据，可以是NumPy数组或PyTorch张量。
        gt_boxes: 地面真值框，可以是NumPy数组或PyTorch张量。
        ref_boxes: 参考框，可以是NumPy数组或PyTorch张量。
        ref_labels: 参考框的标签。
        ref_scores: 参考框的置信度分数。
        point_colors: 点云的颜色。
        draw_origin: 是否绘制坐标原点。
    """
    if isinstance(points, torch.Tensor):
        points = points.cpu().numpy()  # 如果点云是PyTorch张量，转换为NumPy数组
    if isinstance(gt_boxes, torch.Tensor):
        gt_boxes = gt_boxes.cpu().numpy()  # 如果地面真值框是PyTorch张量，转换为NumPy数组
    if isinstance(ref_boxes, torch.Tensor):
        ref_boxes = ref_boxes.cpu().numpy()  # 如果参考框是PyTorch张量，转换为NumPy数组

    vis = open3d.visualization.Visualizer()  # 创建Open3D可视化对象
    vis.create_window()  # 创建可视化窗口

    vis.get_render_option().point_size = 1.0  # 设置点云的点大小
    vis.get_render_option().background_color = np.zeros(3)  # 设置背景颜色为黑色

    # 绘制坐标原点
    if draw_origin:
        axis_pcd = open3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])  # 创建坐标系
        vis.add_geometry(axis_pcd)  # 将坐标系添加到可视化窗口

    pts = open3d.geometry.PointCloud()  # 创建点云对象
    pts.points = open3d.utility.Vector3dVector(points[:, :3])  # 设置点云的坐标

    vis.add_geometry(pts)  # 将点云添加到可视化窗口
    if point_colors is None:
        pts.colors = open3d.utility.Vector3dVector(np.ones((points.shape[0], 3)))  # 如果未指定颜色，设置为白色
    else:
        pts.colors = open3d.utility.Vector3dVector(point_colors)  # 设置点云的颜色

    if gt_boxes is not None:
        vis = draw_box(vis, gt_boxes, (0, 0, 1))  # 绘制地面真值框，颜色为蓝色

    if ref_boxes is not None:
        vis = draw_box(vis, ref_boxes, (0, 1, 0), ref_labels, ref_scores)  # 绘制参考框，颜色为绿色

    vis.run()  # 运行可视化
    vis.destroy_window()  # 关闭可视化窗口

def translate_boxes_to_open3d_instance(gt_boxes):
    """
    将3D框转换为Open3D的实例。

    Args:
        gt_boxes: 3D框的参数，包括中心点、长宽高和旋转角度。

    Returns:
        line_set: 框的线集。
        box3d: 3D框的实例。
    """
    center = gt_boxes[0:3]  # 获取框的中心点
    lwh = gt_boxes[3:6]  # 获取框的长宽高
    axis_angles = np.array([0, 0, gt_boxes[6] + 1e-10])  # 获取框的旋转角度
    rot = open3d.geometry.get_rotation_matrix_from_axis_angle(axis_angles)  # 根据旋转角度获取旋转矩阵
    box3d = open3d.geometry.OrientedBoundingBox(center, rot, lwh)  # 创建有向包围盒

    line_set = open3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)  # 从有向包围盒创建线集

    # 添加额外的线条以完整显示框
    lines = np.asarray(line_set.lines)
    lines = np.concatenate([lines, np.array([[1, 4], [7, 6]])], axis=0)

    line_set.lines = open3d.utility.Vector2iVector(lines)

    return line_set, box3d

def draw_box(vis, gt_boxes, color=(0, 1, 0), ref_labels=None, score=None):
    """
    在可视化窗口中绘制3D框。

    Args:
        vis: Open3D可视化对象。
        gt_boxes: 3D框的参数。
        color: 框的颜色。
        ref_labels: 参考框的标签。
        score: 参考框的置信度分数。

    Returns:
        vis: 更新后的可视化对象。
    """
    for i in range(gt_boxes.shape[0]):
        line_set, box3d = translate_boxes_to_open3d_instance(gt_boxes[i])  # 将框转换为Open3D实例
        if ref_labels is None:
            line_set.paint_uniform_color(color)  # 如果未指定标签，使用默认颜色
        else:
            line_set.paint_uniform_color(box_colormap[ref_labels[i]])  # 根据标签设置颜色

        vis.add_geometry(line_set)  # 将框添加到可视化窗口

        # 如果提供了置信度分数，可以在框上显示分数
        # if score is not None:
        #     corners = box3d.get_box_points()
        #     vis.add_3d_label(corners[5], '%.2f' % score[i])
    return vis
```

### 使用框架Demo可视化
使用框架demo进行可视化的命令：
```bash
python demo.py --cfg_file cfgs/kitti_models/pointrcnn.yaml --data_path ../data/kitti/testing/velodyne/000005.bin --ckpt ../output/kitti_models/pointrcnn/default/ckpt/checkpoint_epoch_80.pth
```
可视化的结果：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d8ddb60f091e4429bbef8d7780e9e847.png)
然而就算框架本身为了性能做妥协而裁剪了图形，每次都推理+可视化对于性能的开销仍然是巨大的，并且时间成本也很高。
## 自定义可视化
在我们训练完一个模型后，OpenPCDet框架本身会对 该模型进行一个eval评估,评估得到的推理结果会保存在模型的输出目录下的pkl文件中，例如：`output/kitti_models/pointpillar/default/eval/eval_with_train/epoch_80/val/result.pkl`。
对于该推理结果的解读可以看我的另一篇博客：[OpenPCDet框架下模型预测结果解读]
对于某个/些模型训练推理结果的可视化，我们可以直接根据该推理结果直接使用框架提供的可视化工具进行展示。
### 提取推理结果
pkl我文件本身可读性很差，为了便于分步骤展开工作和验证，我们将其提取为json格式：
提取pointrcnn模型epoch80对于某帧点云数据的推理结果：
```python
import pickle
import json
import numpy as np
import os

# 指定需要查看的 frame_id
target_frame_id = "000018"

# 所有模型的推理结果文件路径
result_paths = [
'/home/tdhu/OpenPCDet/output/kitti_models/pointrcnn/default/eval/eval_with_train/epoch_80/val/result.pkl',
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
>[!TIP]
>这里如果想对多个模型进行提取，直接在字典内添加多个模型的推理结果`result.pkl`即可

该文件结果示例：
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

前面提到，openpcdet框架提供了一些可视化工具，现在我们基于他提供的工具进行改写，这里没有考虑代码的耦合性，直接在`tools/visual_utils/open3d_vis_utils.py`的基础上进行了改写。主要改动为

 1. 从json文件中提取数据，而不是现场推理。
 2. 根据不同颜色对不同模型的结果进行可视化以做区分。

修改后的代码如下：
```python
import open3d
import numpy as np
import json

def draw_scenes(points, all_ref_boxes=None, model_colors=None, draw_origin=True):
    """
    绘制3D场景，包括点云和多个模型的检测框。

    Args:
        points: 点云数据，形状为 [N, 3]。
        all_ref_boxes: 所有模型的检测框数据，列表形式，每个元素是一个形状为 [K, 7] 的数组。
        model_colors: 每个模型对应的颜色，列表形式，每个元素是一个 RGB 颜色值，如 [1, 0, 0] 表示红色。
        draw_origin: 是否绘制坐标原点。
    """
    vis = open3d.visualization.Visualizer()
    vis.create_window()
    vis.get_render_option().point_size = 1.0
    vis.get_render_option().background_color = np.zeros(3)

    # 绘制坐标原点
    if draw_origin:
        axis_pcd = open3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
        vis.add_geometry(axis_pcd)

    # 绘制点云
    pts = open3d.geometry.PointCloud()
    pts.points = open3d.utility.Vector3dVector(points[:, :3])
    pts.colors = open3d.utility.Vector3dVector(np.ones((points.shape[0], 3)))
    vis.add_geometry(pts)

    # 绘制每个模型的检测框
    if all_ref_boxes is not None:
        for i, ref_boxes in enumerate(all_ref_boxes):
            color = model_colors[i]  # 获取当前模型对应的颜色
            for box in ref_boxes:
                center = box[:3]  # 检测框的中心点 [x, y, z]
                lwh = box[3:6]    # 检测框的尺寸 [l, w, h]
                ry = box[6]       # 检测框的旋转角度

                # 创建检测框
                rot = open3d.geometry.get_rotation_matrix_from_axis_angle([0, 0, ry])
                box3d = open3d.geometry.OrientedBoundingBox(center, rot, lwh)
                line_set = open3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)
                line_set.paint_uniform_color(color)  # 使用当前模型对应的颜色
                vis.add_geometry(line_set)

    # 运行可视化
    vis.run()
    vis.destroy_window()

# 读取JSON文件
with open('output.json', 'r') as f:
    data = json.load(f)

# 提取点云数据
points = np.fromfile('/home/tdhu/OpenPCDet/data/kitti/testing/velodyne/000018.bin', dtype=np.float32).reshape(-1, 4)

# 将点云的 x 轴坐标取反

points[:, 1] = -points[:, 1]  # y 轴取反

# 打印点云数据的统计信息
print(f"点云数据点数: {points.shape[0]}")
print(f"点云数据范围 (x): [{np.min(points[:, 0])}, {np.max(points[:, 0])}]")
print(f"点云数据范围 (y): [{np.min(points[:, 1])}, {np.max(points[:, 1])}]")
print(f"点云数据范围 (z): [{np.min(points[:, 2])}, {np.max(points[:, 2])}]")
print("----")

# 提取多个模型的检测框数据
all_ref_boxes = []
model_names = [
    'PartA2_free', 'pointpillar', 'pointrcnn',
    'pointrcnn_iou', 'pv_rcnn', 'second', 'second_iou'
]
model_colors = [
    [1, 0, 0],  # 红色
    [0, 1, 0],  # 绿色
    [0, 0, 1],  # 蓝色
    [1, 1, 0],  # 黄色
    [1, 0, 1],  # 紫色
    [0, 1, 1],  # 青色
    [1, 0.5, 0]  # 橙色
]

for model_name in model_names:
    ref_boxes = []
    for detection in data[model_name]:
        for box in detection['boxes_lidar']:
            ref_boxes.append(box)
    all_ref_boxes.append(np.array(ref_boxes))

# 调用可视化函数
draw_scenes(
    points=points[:, :3],  # 只使用点云的坐标信息
    all_ref_boxes=all_ref_boxes,  # 所有模型的检测框数据
    model_colors=model_colors  # 每个模型对应的颜色
)
```

该文件对`/testing/velodyne/000018.bin`点云数据的多模型推理结果进行可视化，结果如下：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c5b0701f2d4049eeb23fc12c2c3f14af.png)
>[!TIP]
>如果想要对其他的点云数据进行修改，需要做两处修改，第一是绘制点云背景的文件路径，第二是json文件中的内容，要与相应的数据进行统一，在上面的提取程序中修改重写，建议两者作为参数传入，并使用一个新的函数一起调用。

## 可视化结果的保存
由于opencv没有提供相应的save工具，目前的保存方式仅限于调一个屏幕捕获函数，如果有小伙伴能提供更好的方案欢迎留言私信。
