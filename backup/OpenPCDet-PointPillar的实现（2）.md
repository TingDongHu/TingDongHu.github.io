### Loss计算代码实现
在Pointpillars的loss计算中，使用了与SECOND相同的loss计算方式，每个GT框都包含了 (x, y, z, w, l, h, θ)这7个参数。
在loss计算的代码实现中涉及的代码量比较多，因此解析分为如下三个部分分别完成 
- 先验框的生成
- GT和先验框的匹配
- loss计算实现

#### 先验框的生成
代码在pcdet/models/dense_heads/target_assigner/anchor_generator.py
```python
import torch


class AnchorGenerator(object):
    def __init__(self, anchor_range, anchor_generator_config):
        super().__init__()
        self.anchor_generator_cfg = anchor_generator_config  # list:3
        # 得到anchor在点云中的分布范围[0, -39.68, -3, 69.12, 39.68, 1]
        self.anchor_range = anchor_range
        # 得到配置参数中所有尺度anchor的长宽高
        # list:3 --> 车、人、自行车[[[3.9, 1.6, 1.56]],[[0.8, 0.6, 1.73]],[[1.76, 0.6, 1.73]]]
        self.anchor_sizes = [config['anchor_sizes'] for config in anchor_generator_config]
        # 得到anchor的旋转角度，这是是弧度，也就是0度和90度
        # list:3 --> [[0, 1.57],[0, 1.57],[0, 1.57]]
        self.anchor_rotations = [config['anchor_rotations'] for config in anchor_generator_config]
        # 得到每个anchor初始化在点云中z轴的位置，其中在kitti中点云的z轴范围是-3米到1米
        # list:3 -->  [[-1.78],[-0.6],[-0.6]]
        self.anchor_heights = [config['anchor_bottom_heights'] for config in anchor_generator_config]
        # 每个先验框产生的时候是否需要在每个格子的中间，
        # 例如坐标点为[1,1]，如果需要对齐中心点的话，需要加上0.5变成[1.5, 1.5]
        # 默认为False
        # list:3 --> [False, False, False]
        self.align_center = [config.get('align_center', False) for config in anchor_generator_config]

        assert len(self.anchor_sizes) == len(self.anchor_rotations) == len(self.anchor_heights)
        self.num_of_anchor_sets = len(self.anchor_sizes)  # 3

    def generate_anchors(self, grid_sizes):
        assert len(grid_sizes) == self.num_of_anchor_sets
        # 1.初始化
        all_anchors = []
        num_anchors_per_location = []
        # 2.三个类别的先验框逐类别生成
        for grid_size, anchor_size, anchor_rotation, anchor_height, align_center in zip(
                grid_sizes, self.anchor_sizes, self.anchor_rotations, self.anchor_heights, self.align_center):
            # 2 = 2x1x1 --> 每个位置产生2个anchor，这里的2代表两个方向
            num_anchors_per_location.append(len(anchor_rotation) * len(anchor_size) * len(anchor_height))
            # 　不需要对齐中心点来生成先验框
            if align_center:
                x_stride = (self.anchor_range[3] - self.anchor_range[0]) / grid_size[0]
                y_stride = (self.anchor_range[4] - self.anchor_range[1]) / grid_size[1]
                # 中心对齐，平移半个网格
                x_offset, y_offset = x_stride / 2, y_stride / 2
            else:
                # 2.1计算每个网格的在点云空间中的实际大小
                # 用于将每个anchor映射回实际点云中的大小
                # (69.12 - 0) / (216 - 1) = 0.3214883848678234  单位：米
                x_stride = (self.anchor_range[3] - self.anchor_range[0]) / (grid_size[0] - 1)
                # (39.68 - (-39.68.)) / (248 - 1) = 0.3212955490297634  单位：米
                y_stride = (self.anchor_range[4] - self.anchor_range[1]) / (grid_size[1] - 1)
                # 由于没有进行中心对齐，所有每个点相对于左上角坐标的偏移量都是0
                x_offset, y_offset = 0, 0

            # 2.2 生成单个维度x_shifts，y_shifts和z_shifts
            # 以x_stride为step，在self.anchor_range[0] + x_offset和self.anchor_range[3] + 1e-5，
            # 产生x坐标 --> 216个点 [0, 69.12]
            x_shifts = torch.arange(
                self.anchor_range[0] + x_offset, self.anchor_range[3] + 1e-5, step=x_stride, dtype=torch.float32,
            ).cuda()
            # 产生y坐标 --> 248个点 [0, 79.36]
            y_shifts = torch.arange(
                self.anchor_range[1] + y_offset, self.anchor_range[4] + 1e-5, step=y_stride, dtype=torch.float32,
            ).cuda()
            """
            new_tensor函数可以返回一个新的张量数据，该张量数据与指定的有相同的属性
            如拥有相同的数据类型和张量所在的设备情况等属性；
            并使用anchor_height数值个来填充这个张量
            """
            # [-1.78]
            z_shifts = x_shifts.new_tensor(anchor_height)
            # num_anchor_size = 1
            # num_anchor_rotation = 2
            num_anchor_size, num_anchor_rotation = anchor_size.__len__(), anchor_rotation.__len__()  # 1, 2
            #  [0, 1.57] 弧度制
            anchor_rotation = x_shifts.new_tensor(anchor_rotation)
            # [[3.9, 1.6, 1.56]]
            anchor_size = x_shifts.new_tensor(anchor_size)

            # 2.3 调用meshgrid生成网格坐标
            x_shifts, y_shifts, z_shifts = torch.meshgrid([
                x_shifts, y_shifts, z_shifts
            ])
            # meshgrid可以理解为在原来的维度上进行扩展,例如:
            # x原来为（216，）-->（216，1, 1）--> (216,248,1)
            # y原来为（248，）--> (1，248，1）--> (216,248,1)
            # z原来为 (1, )  --> (1,1,1)    --> (216,248,1)

            # 2.4.anchor各个维度堆叠组合，生成最终anchor(1,432,496,1,2,7）
            # 2.4.1.堆叠anchor的位置 
            # [x, y, z, 3]-->[216, 248, 1, 3] 代表了每个anchor的位置信息
            # 其中3为该点所在映射tensor中的（z, y, x）数值
            anchors = torch.stack((x_shifts, y_shifts, z_shifts), dim=-1)  
            # 2.4.2.将anchor的位置和大小进行组合，编程为将anchor扩展并复制为相同维度（除了最后一维），然后进行组合
            # (216, 248, 1, 3) --> (216, 248, 1 , 1, 3)
            # 维度分别代表了： z，y，x， 该类别anchor的尺度数量，该个anchor的位置信息
            anchors = anchors[:, :, :, None, :].repeat(1, 1, 1, anchor_size.shape[0], 1)
            # (1, 1, 1, 1, 3) --> (216, 248, 1, 1, 3)
            anchor_size = anchor_size.view(1, 1, 1, -1, 3).repeat([*anchors.shape[0:3], 1, 1])
            # anchors生成的最终结果需要有位置信息和大小信息 --> (216, 248, 1, 1, 6)
            # 最后一个纬度中表示（z, y, x, l, w, h）
            anchors = torch.cat((anchors, anchor_size), dim=-1)
            # 2.4.3.将anchor的位置和大小和旋转角进行组合
            # 在倒数第二个维度上增加一个维度，然后复制该维度一次
            # (216, 248, 1, 1, 2, 6)        长， 宽， 深， anchor尺度数量， 该尺度旋转角个数，anchor的6个参数
            anchors = anchors[:, :, :, :, None, :].repeat(1, 1, 1, 1, num_anchor_rotation, 1)
            # (216, 248, 1, 1, 2, 1)        两个不同方向先验框的旋转角度
            anchor_rotation = anchor_rotation.view(1, 1, 1, 1, -1, 1).repeat(
                [*anchors.shape[0:3], num_anchor_size, 1, 1])
            # [z, y, x, num_size, num_rot, 7] --> (216, 248, 1, 1, 2, 7)
            # 最后一个纬度表示为anchors的位置+大小+旋转角度（z, y, x, l, w, h, theta）
            anchors = torch.cat((anchors, anchor_rotation), dim=-1)  # [z, y, x, num_size, num_rot, 7]

            # 2.5 置换anchor的维度
            # [z, y, x, num_anchor_size, num_rot, 7]-->[x, y, z, num_anchor_zie, num_rot, 7]
            # 最后一个纬度代表了 : [x, y, z, dx, dy, dz, rot]
            anchors = anchors.permute(2, 1, 0, 3, 4, 5).contiguous()
            # 使得各类anchor的z轴方向从anchor的底部移动到该anchor的中心点位置
            # 车 ： -1.78 + 1.56/2 = -1.0
            # 人、自行车 ： -0.6 + 1.73/2 = 0.23
            anchors[..., 2] += anchors[..., 5] / 2
            all_anchors.append(anchors)
        # all_anchors： [(1，248，216，1，2，7），(1，248，216，1，2，7），(1，248，216，1，2，7）]
        # num_anchors_per_location：[2,2,2]
        return all_anchors, num_anchors_per_location
```
#### GT和先验框的匹配(target assignment)
此处代码注释已经写得很详细，可以按照注释理解如果和计算GT和所有anchor的匹配；
> assign_targets完成对一帧点云数据中所有的类别和anchor的正负样本分配，
assign_targets_single完成对一帧中每个类别的GT和anchor的正负样本分配。

所以一个Batch样本中anchor与GT的匹配这里是逐帧逐类别进行的。与图像目标检测中稍有不同。
代码在pcdet/models/dense_heads/target_assigner/axis_aligned_target_assigner.py
``` python
import numpy as np
import torch

from ....ops.iou3d_nms import iou3d_nms_utils
from ....utils import box_utils


class AxisAlignedTargetAssigner(object):
    def __init__(self, model_cfg, class_names, box_coder, match_height=False):
        super().__init__()
        # anchor生成配置参数
        anchor_generator_cfg = model_cfg.ANCHOR_GENERATOR_CONFIG
        # 为预测box找对应anchor的参数
        anchor_target_cfg = model_cfg.TARGET_ASSIGNER_CONFIG
        # 编码box的7个残差参数(x, y, z, w, l, h, θ) --> pcdet.utils.box_coder_utils.ResidualCoder
        self.box_coder = box_coder
        # 在PointPillars中指定正负样本的时候由BEV视角计算GT和先验框的iou，不需要进行z轴上的高度的匹配，
        # 想法是：1、点云中的物体都在同一个平面上，没有物体在Z轴发生重叠的情况
        #        2、每个类别的高度相差不是很大，直接使用SmoothL1损失就可以达到很好的高度回归效果
        self.match_height = match_height
        # 类别名称['Car', 'Pedestrian', 'Cyclist']
        self.class_names = np.array(class_names)
        # ['Car', 'Pedestrian', 'Cyclist']
        self.anchor_class_names = [config['class_name'] for config in anchor_generator_cfg]
        # anchor_target_cfg.POS_FRACTION = -1 < 0 --> None
        # 前景、背景采样系数 PointPillars不考虑
        self.pos_fraction = anchor_target_cfg.POS_FRACTION if anchor_target_cfg.POS_FRACTION >= 0 else None
        # 总采样数  PointPillars不考虑
        self.sample_size = anchor_target_cfg.SAMPLE_SIZE  # 512
        # False 前景权重由 1/前景anchor数量 PointPillars不考虑
        self.norm_by_num_examples = anchor_target_cfg.NORM_BY_NUM_EXAMPLES
        # 类别iou匹配为正样本阈值{'Car':0.6, 'Pedestrian':0.5, 'Cyclist':0.5}
        self.matched_thresholds = {}
        # 类别iou匹配为负样本阈值{'Car':0.45, 'Pedestrian':0.35, 'Cyclist':0.35}
        self.unmatched_thresholds = {}
        for config in anchor_generator_cfg:
            self.matched_thresholds[config['class_name']] = config['matched_threshold']
            self.unmatched_thresholds[config['class_name']] = config['unmatched_threshold']

        self.use_multihead = model_cfg.get('USE_MULTIHEAD', False)  # False
        # self.separate_multihead = model_cfg.get('SEPARATE_MULTIHEAD', False)
        # if self.seperate_multihead:
        #     rpn_head_cfgs = model_cfg.RPN_HEAD_CFGS
        #     self.gt_remapping = {}
        #     for rpn_head_cfg in rpn_head_cfgs:
        #         for idx, name in enumerate(rpn_head_cfg['HEAD_CLS_NAME']):
        #             self.gt_remapping[name] = idx + 1

    def assign_targets(self, all_anchors, gt_boxes_with_classes):
        """
        处理一批数据中所有点云的anchors和gt_boxes，
        计算每个anchor属于前景还是背景，
        为每个前景的anchor分配类别和计算box的回归残差和回归权重
        Args:
            all_anchors: [(N, 7), ...]
            gt_boxes_with_classes: (B, M, 8)  # 最后维度数据为 (x, y, z, w, l, h, θ，class)
        Returns:
            all_targets_dict = {
                # 每个anchor的类别
                'box_cls_labels': cls_labels, # (batch_size，num_of_anchors）
                # 每个anchor的回归残差 -->（∆x, ∆y, ∆z, ∆l, ∆w, ∆h, ∆θ）
                'box_reg_targets': bbox_targets, # (batch_size，num_of_anchors，7）
                # 每个box的回归权重
                'reg_weights': reg_weights # (batch_size，num_of_anchors）
            }
        """
        # 1.初始化结果list并提取对应的gt_box和类别
        bbox_targets = []
        cls_labels = []
        reg_weights = []

        # 得到批大小
        batch_size = gt_boxes_with_classes.shape[0]  # 4
        # 得到所有GT的类别
        gt_classes = gt_boxes_with_classes[:, :, -1]  # （4，num_of_gt）
        # 得到所有GT的7个box参数
        gt_boxes = gt_boxes_with_classes[:, :, :-1]  # （4，num_of_gt，7）
        # 2.对batch中的所有数据逐帧匹配anchor的前景和背景
        for k in range(batch_size):
            cur_gt = gt_boxes[k]  # 取出当前帧中的 gt_boxes (num_of_gt，7）
            """
            由于在OpenPCDet的数据预处理时，以一批数据中拥有GT数量最多的帧为基准，
            其他帧中GT数量不足，则会进行补0操作，使其成为一个矩阵，例：
            [
                [1,1,2,2,3,2],
                [2,2,3,1,0,0],
                [3,1,2,0,0,0]
            ]
            因此这里从每一行的倒数第二个类别开始判断，
            截取最后一个非零元素的索引，来取出当前帧中真实的GT数据
            """
            cnt = cur_gt.__len__() - 1  # 得到一批数据中最多有多少个GT
            # 这里的循环是找到最后一个非零的box，因为预处理的时候会按照batch最大box的数量处理，不足的进行补0
            while cnt > 0 and cur_gt[cnt].sum() == 0:
                cnt -= 1
            # 2.1提取当前帧非零的box和类别
            cur_gt = cur_gt[:cnt + 1]
            # cur_gt_classes 例: tensor([1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3], device='cuda:0', dtype=torch.int32)
            cur_gt_classes = gt_classes[k][:cnt + 1].int()

            target_list = []
            # 2.2 对每帧中的anchor和GT分类别，单独计算前背景
            # 计算时候 每个类别的anchor是独立计算的 不同于在ssd中整体计算iou并取最大值
            for anchor_class_name, anchors in zip(self.anchor_class_names, all_anchors):
                # anchor_class_name : 车 | 行人 | 自行车
                # anchors : (1, 200, 176, 1, 2, 7)  7 --> (x, y, z, l, w, h, θ)
                if cur_gt_classes.shape[0] > 1:
                    # self.class_names : ["car", "person", "cyclist"]
                    # 这里减1是因为列表索引从0开始，目的是得到属于列表中gt中哪些类别是与当前处理的了类别相同，得到类别mask
                    mask = torch.from_numpy(self.class_names[cur_gt_classes.cpu() - 1] == anchor_class_name)
                else:
                    mask = torch.tensor([self.class_names[c - 1] == anchor_class_name
                                         for c in cur_gt_classes], dtype=torch.bool)
                # 在检测头中是否使用多头，是的话 此处为True，默认为False
                if self.use_multihead:  # False
                    anchors = anchors.permute(3, 4, 0, 1, 2, 5).contiguous().view(-1, anchors.shape[-1])
                    # if self.seperate_multihead:
                    #     selected_classes = cur_gt_classes[mask].clone()
                    #     if len(selected_classes) > 0:
                    #         new_cls_id = self.gt_remapping[anchor_class_name]
                    #         selected_classes[:] = new_cls_id
                    # else:
                    #     selected_classes = cur_gt_classes[mask]
                    selected_classes = cur_gt_classes[mask]
                else:
                    # 2.2.1 计算所需的变量 得到特征图的大小
                    feature_map_size = anchors.shape[:3]  # （1, 248, 216）
                    # 将所有的anchors展平  shape : (216, 248, 1, 1, 2, 7) -->  (107136, 7)
                    anchors = anchors.view(-1, anchors.shape[-1])
                    # List: 根据累呗mask索引得到该帧中当前需要处理的类别  --> 车 | 行人 | 自行车
                    selected_classes = cur_gt_classes[mask]

                # 2.2.2 使用assign_targets_single来单独为某一类别的anchors分配gt_boxes，
                # 并为前景、背景的box设置编码和回归权重
                single_target = self.assign_targets_single(
                    anchors,  # 该类的所有anchor
                    cur_gt[mask],  # GT_box  shape : （num_of_GT_box, 7）
                    gt_classes=selected_classes,  # 当前选中的类别
                    matched_threshold=self.matched_thresholds[anchor_class_name],  # 当前类别anchor与GT匹配为正样本的阈值
                    unmatched_threshold=self.unmatched_thresholds[anchor_class_name]  # 当前类别anchor与GT匹配为负样本的阈值
                )
                target_list.append(single_target)
                # 到目前为止，处理完该帧单个类别和该类别anchor的前景和背景分配

            if self.use_multihead:
                target_dict = {
                    'box_cls_labels': [t['box_cls_labels'].view(-1) for t in target_list],
                    'box_reg_targets': [t['box_reg_targets'].view(-1, self.box_coder.code_size) for t in target_list],
                    'reg_weights': [t['reg_weights'].view(-1) for t in target_list]
                }

                target_dict['box_reg_targets'] = torch.cat(target_dict['box_reg_targets'], dim=0)
                target_dict['box_cls_labels'] = torch.cat(target_dict['box_cls_labels'], dim=0).view(-1)
                target_dict['reg_weights'] = torch.cat(target_dict['reg_weights'], dim=0).view(-1)
            else:
                target_dict = {
                    # feature_map_size:(1，200，176, 2）
                    'box_cls_labels': [t['box_cls_labels'].view(*feature_map_size, -1) for t in target_list],
                    # (1，248，216, 2, 7)
                    'box_reg_targets': [t['box_reg_targets'].view(*feature_map_size, -1, self.box_coder.code_size)
                                        for t in target_list],
                    # (1，248，216, 2)
                    'reg_weights': [t['reg_weights'].view(*feature_map_size, -1) for t in target_list]
                }

                # list : 3*anchor (1, 248, 216, 2, 7) --> (1, 248, 216, 6, 7) -> (321408, 7)
                target_dict['box_reg_targets'] = torch.cat(
                    target_dict['box_reg_targets'], dim=-2
                ).view(-1, self.box_coder.code_size)
                # list:3 (1, 248, 216, 2) --> (1，248, 216, 6) -> (1*248*216*6, )
                target_dict['box_cls_labels'] = torch.cat(target_dict['box_cls_labels'], dim=-1).view(-1)
                # list:3 (1, 200, 176, 2) --> (1, 200, 176, 6) -> (1*248*216*6, )
                target_dict['reg_weights'] = torch.cat(target_dict['reg_weights'], dim=-1).view(-1)

            # 将结果填入对应的容器
            bbox_targets.append(target_dict['box_reg_targets'])
            cls_labels.append(target_dict['box_cls_labels'])
            reg_weights.append(target_dict['reg_weights'])
            # 到这里该batch的点云全部处理完

        # 3.将结果stack并返回
        bbox_targets = torch.stack(bbox_targets, dim=0)  # (batch_size，321408，7）

        cls_labels = torch.stack(cls_labels, dim=0)  # (batch_size，321408）
        reg_weights = torch.stack(reg_weights, dim=0)  # (batch_size，321408）
        all_targets_dict = {
            'box_cls_labels': cls_labels,  # (batch_size，321408）
            'box_reg_targets': bbox_targets,  # (batch_size，321408,7）
            'reg_weights': reg_weights  # (batch_size，321408）

        }
        return all_targets_dict

    def assign_targets_single(self, anchors, gt_boxes, gt_classes, matched_threshold=0.6, unmatched_threshold=0.45):
        """
        针对某一类别的anchors和gt_boxes，计算前景和背景anchor的类别，box编码和回归权重
        Args:
            anchors: (107136, 7)
            gt_boxes: （该帧中该类别的GT数量，7）
            gt_classes: (该帧中该类别的GT数量, 1)
            matched_threshold:0.6
            unmatched_threshold:0.45
        Returns:
        前景anchor
            ret_dict = {
                'box_cls_labels': labels, # (107136,)
                'box_reg_targets': bbox_targets,  # (107136,7)
                'reg_weights': reg_weights, # (107136,)
            }
        """
        # ----------------------------1.初始化-------------------------------#
        num_anchors = anchors.shape[0]  # 216 * 248 = 107136
        num_gt = gt_boxes.shape[0]  # 该帧中该类别的GT数量

        # 初始化anchor对应的label和gt_id ，并置为 -1，-1表示loss计算时候不会被考虑，背景的类别被设置为0
        labels = torch.ones((num_anchors,), dtype=torch.int32, device=anchors.device) * -1
        gt_ids = torch.ones((num_anchors,), dtype=torch.int32, device=anchors.device) * -1

        # ---------------------2.计算该类别中anchor的前景和背景------------------------#
        if len(gt_boxes) > 0 and anchors.shape[0] > 0:
            # 1.计算该帧中某一个类别gt和对应anchors之间的iou（jaccard index）
            # anchor_by_gt_overlap    shape : (107136, num_gt)
            # anchor_by_gt_overlap代表当前类别的所有anchor和当前类别中所有GT的iou
            anchor_by_gt_overlap = iou3d_nms_utils.boxes_iou3d_gpu(anchors[:, 0:7], gt_boxes[:, 0:7]) \
                if self.match_height else box_utils.boxes3d_nearest_bev_iou(anchors[:, 0:7], gt_boxes[:, 0:7])

            # NOTE: The speed of these two versions depends the environment and the number of anchors
            # anchor_to_gt_argmax = torch.from_numpy(anchor_by_gt_overlap.cpu().numpy().argmax(axis=1)).cuda()

            # 2.得到每一个anchor与哪个的GT的的iou最大
            # anchor_to_gt_argmax表示数据维度是anchor的长度，索引是gt
            anchor_to_gt_argmax = anchor_by_gt_overlap.argmax(dim=1)
            # anchor_to_gt_max得到每一个anchor最匹配的gt的iou数值
            anchor_to_gt_max = anchor_by_gt_overlap[
                torch.arange(num_anchors, device=anchors.device), anchor_to_gt_argmax]

            # gt_to_anchor_argmax = torch.from_numpy(anchor_by_gt_overlap.cpu().numpy().argmax(axis=0)).cuda()

            # 3.找到每个gt最匹配anchor的索引和iou
            # (num_of_gt,) 得到每个gt最匹配的anchor索引
            gt_to_anchor_argmax = anchor_by_gt_overlap.argmax(dim=0)
            # （num_of_gt，）找到每个gt最匹配anchor的iou
            gt_to_anchor_max = anchor_by_gt_overlap[gt_to_anchor_argmax, torch.arange(num_gt, device=anchors.device)]
            # 4.将GT中没有匹配到的anchor的iou数值设置为-1
            empty_gt_mask = gt_to_anchor_max == 0  # 得到没有匹配到anchor的gt的mask
            gt_to_anchor_max[empty_gt_mask] = -1  # 将没有匹配到anchor的gt的iou数值设置为-1

            # 5.找到anchor中和gt存在最大iou的anchor索引，即前景anchor
            """
            由于在前面的实现中，仅仅找出来每个GT和anchor的最大iou索引，但是argmax返回的是索引最小的那个，
            在匹配的过程中可能一个GT和多个anchor拥有相同的iou大小，
            所以此处要找出这个GT与所有anchors拥有相同最大iou的anchor
            """
            # 以gt为基础，逐个anchor对应，比如第一个gt的最大iou为0.9，则在所有anchor中找iou为0.9的anchor
            # nonzero函数是numpy中用于得到数组array中非零元素的位置（数组索引）的函数
            """
            矩阵比较例子 :
            anchors_with_max_overlap = torch.tensor([[0.78, 0.1, 0.9, 0],
                                                      [0.0, 0.5, 0, 0],
                                                      [0.0, 0, 0.9, 0.8],
                                                      [0.78, 0.1, 0.0, 0]])
            gt_to_anchor_max = torch.tensor([0.78, 0.5, 0.9,0.8]) 
            anchors_with_max_overlap = anchor_by_gt_overlap == gt_to_anchor_max
            
            # 返回的结果中包含了在anchor中与该GT拥有相同最大iou的所有anchor
            anchors_with_max_overlap = tensor([[ True, False,  True, False],
                                                [False,  True, False, False],
                                                [False, False,  True,  True],
                                                [ True, False, False, False]])
            在torch中nonzero返回的是tensor中非0元素的位置，此函数在numpy中返回的是非零元素的行列表和列列表。
            torch返回结果tensor([[0, 0],
                                [0, 2],
                                [1, 1],
                                [2, 2],
                                [2, 3],
                                [3, 0]])
            numpy返回结果(array([0, 0, 1, 2, 2, 3]), array([0, 2, 1, 2, 3, 0]))     
            所以可以得到第一个GT同时与第一个anchor和最后一个anchor最为匹配                     
            """
            """所以在实际的一批数据中可以到得到结果为
            tensor([[33382,     9],
                    [43852,    10],
                    [47284,     5],
                    [50370,     4],
                    [58498,     8],
                    [58500,     8],
                    [58502,     8],
                    [59139,     2],
                    [60751,     1],
                    [61183,     1],
                    [61420,    11],
                    [62389,     0],
                    [63216,    13],
                    [63218,    13],
                    [65046,    12],
                    [65048,    12],
                    [65478,    12],
                    [65480,    12],
                    [71924,     3],
                    [78046,     7],
                    [80150,     6]], device='cuda:0')
            在第0维度拥有相同gt索引的项，在该类所有anchor中同时拥有多个与之最为匹配的anchor
            """
            # (num_of_multiple_best_matching_for_per_GT,)
            anchors_with_max_overlap = (anchor_by_gt_overlap == gt_to_anchor_max).nonzero()[:, 0]
            # 得到这些最匹配anchor与该类别的哪个GT索引相对应
            # 其实和(anchor_by_gt_overlap == gt_to_anchor_max).nonzero()[:, 1]的结果一样
            gt_inds_force = anchor_to_gt_argmax[anchors_with_max_overlap]  # （35，）
            # 将gt的类别赋值到对应的anchor的label中
            labels[anchors_with_max_overlap] = gt_classes[gt_inds_force]
            # 将gt的索引也赋值到对应的anchors的gt_ids中
            gt_ids[anchors_with_max_overlap] = gt_inds_force.int()

            # 6.根据matched_threshold和unmatched_threshold以及anchor_to_gt_max计算前景和背景索引，并更新labels和gt_ids
            """这里对labels和gt_ids的操作应该已经包含了上面的anchors_with_max_overlap"""
            # 找到最匹配的anchor中iou大于给定阈值的mask #(107136,)
            pos_inds = anchor_to_gt_max >= matched_threshold
            # 找到最匹配的anchor中iou大于给定阈值的gt的索引 #(105,)
            gt_inds_over_thresh = anchor_to_gt_argmax[pos_inds]
            # 将pos anchor对应gt的类别赋值到对应的anchor的label中
            labels[pos_inds] = gt_classes[gt_inds_over_thresh]
            # 将pos anchor对应gt的索引赋值到对应的anchor的gt_id中
            gt_ids[pos_inds] = gt_inds_over_thresh.int()

            bg_inds = (anchor_to_gt_max < unmatched_threshold).nonzero()[:, 0]  # 找到背景anchor索引
        else:
            bg_inds = torch.arange(num_anchors, device=anchors.device)

        # 找到前景anchor的索引--> (num_of_foreground_anchor,)
        # 106879 + 119 = 106998 < 107136 说明有一些anchor既不是背景也不是前景，
        # iou介于unmatched_threshold和matched_threshold之间
        fg_inds = (labels > 0).nonzero()[:, 0]
        # 到目前为止得到哪些anchor是前景和哪些anchor是背景

        # ------------------3.对anchor的前景和背景进行筛选和赋值--------------------#
        # 如果存在前景采样比例，则分别采样前景和背景anchor，PointPillar中没有前背景采样操作，前背景均衡使用了focal loss损失函数
        if self.pos_fraction is not None:  # anchor_target_cfg.POS_FRACTION = -1 < 0 --> None
            num_fg = int(self.pos_fraction * self.sample_size)  # self.sample_size=512
            # 如果前景anchor大于采样前景数
            if len(fg_inds) > num_fg:
                # 计算要丢弃的前景anchor数目
                num_disabled = len(fg_inds) - num_fg
                # 在前景数目中随机产生索引值，并取前num_disabled个关闭索引
                # 比如：torch.randperm(4)
                # 输出：tensor([ 2,  1,  0,  3])
                disable_inds = torch.randperm(len(fg_inds))[:num_disabled]
                # 将被丢弃的anchor的iou设置为-1
                labels[disable_inds] = -1
                # 更新前景索引
                fg_inds = (labels > 0).nonzero()[:, 0]

            # 计算所需背景数
            num_bg = self.sample_size - (labels > 0).sum()
            # 如果当前背景数大于所需背景数
            if len(bg_inds) > num_bg:
                # torch.randint在0到len(bg_inds)之间，随机产生size为(num_bg,)的数组
                enable_inds = bg_inds[torch.randint(0, len(bg_inds), size=(num_bg,))]
                # 将enable_inds的标签设置为0
                labels[enable_inds] = 0
            # bg_inds = torch.nonzero(labels == 0)[:, 0]
        else:
            # 如果该类别没有GT的话，将该类别的全部label置0，即所有anchor都是背景类别
            if len(gt_boxes) == 0 or anchors.shape[0] == 0:
                labels[:] = 0
            else:
                # anchor与GT的iou小于unmatched_threshold的anchor的类别设置类背景类别
                labels[bg_inds] = 0
                # 将前景赋对应类别
                """
                此处分别使用了anchors_with_max_overlap和
                anchor_to_gt_max >= matched_threshold来对该类别的anchor进行赋值
                但是我个人觉得anchor_to_gt_max >= matched_threshold已经包含了anchors_with_max_overlap的那些与GT拥有最大iou的
                anchor了，所以我对这里的计算方式有一点好奇，为什么要分别计算两次，
                如果知道这里原因的小伙伴希望可以给予解答，谢谢！
                """
                labels[anchors_with_max_overlap] = gt_classes[gt_inds_force]

        # ------------------4.计算bbox_targets和reg_weights--------------------#
        # 初始化每个anchor的7个回归参数，并设置为0数值
        bbox_targets = anchors.new_zeros((num_anchors, self.box_coder.code_size))  # (107136,7)
        # 如果该帧中有该类别的GT时候，就需要对这些设置为正样本类别的anchor进行编码操作了
        if len(gt_boxes) > 0 and anchors.shape[0] > 0:
            # 使用anchor_to_gt_argmax[fg_inds]来重复索引每个anchor对应前景的GT_box
            fg_gt_boxes = gt_boxes[anchor_to_gt_argmax[fg_inds], :]
            # 提取所有属于前景的anchor
            fg_anchors = anchors[fg_inds, :]
            """
            PointPillar编码gt和前景anchor，并赋值到bbox_targets的对应位置
            7个参数的编码的方式为
            ∆x = (x^gt − xa^da)/d^a , ∆y = (y^gt − ya^da)/d^a , ∆z = (z^gt − za^ha)/h^a
            ∆w = log (w^gt / w^a) ∆l = log (l^gt / l^a) , ∆h = log (h^gt / h^a)
            ∆θ = sin(θ^gt - θ^a) 
            """
            bbox_targets[fg_inds, :] = self.box_coder.encode_torch(fg_gt_boxes, fg_anchors)

        # 初始化回归权重,并设置值为0
        reg_weights = anchors.new_zeros((num_anchors,))  # (107136,)

        if self.norm_by_num_examples:  # PointPillars回归权重中不需要norm_by_num_examples
            num_examples = (labels >= 0).sum()
            num_examples = num_examples if num_examples > 1.0 else 1.0
            reg_weights[labels > 0] = 1.0 / num_examples
        else:
            reg_weights[labels > 0] = 1.0  # 将前景anchor的回归权重设置为1

        ret_dict = {
            'box_cls_labels': labels,  # (107136,)
            'box_reg_targets': bbox_targets,  # (107136,7)编码后的结果
            'reg_weights': reg_weights,  # (107136,)
        }
        return ret_dict
```
### box编码实现
此处根据论文中的公式对匹配被正样本的anchor_box和与之对应的GT-box的7个回归参数进行编码。
编码公式：

![Image](https://github.com/user-attachments/assets/e5ee6854-6430-4d71-806b-3ec61916b431)

代码在：pcdet/utils/box_coder_utils.py
```python
class ResidualCoder(object):
    def __init__(self, code_size=7, encode_angle_by_sincos=False, **kwargs):
        """
        loss中anchor和gt的编码与解码
        7个参数的编码的方式为
            ∆x = (x^gt − xa^da)/d^a , ∆y = (y^gt − ya^da)/d^a , ∆z = (z^gt − za^ha)/h^a
            ∆w = log (w^gt / w^a) ∆l = log (l^gt / l^a) , ∆h = log (h^gt / h^a)
            ∆θ = sin(θ^gt - θ^a)
        """
        super().__init__()
        self.code_size = code_size
        self.encode_angle_by_sincos = encode_angle_by_sincos
        if self.encode_angle_by_sincos:
            self.code_size += 1

    def encode_torch(self, boxes, anchors):
        """
        Args:
            boxes: (N, 7 + C) [x, y, z, dx, dy, dz, heading, ...]
            anchors: (N, 7 + C) [x, y, z, dx, dy, dz, heading or *[cos, sin], ...]

        Returns:

        """
        # 截断anchors的[dx,dy,dz]，每个anchor_box的l, w, h数值如果小于1e-5则为1e-5
        anchors[:, 3:6] = torch.clamp_min(anchors[:, 3:6], min=1e-5)
        # 截断boxes的[dx,dy,dz] 每个GT_box的l, w, h数值如果小于1e-5则为1e-5
        boxes[:, 3:6] = torch.clamp_min(boxes[:, 3:6], min=1e-5)
        # If split_size_or_sections is an integer type, then tensor will be split into equally sized chunks (if possible).
        # Last chunk will be smaller if the tensor size along the given dimension dim is not divisible by split_size.

        # 这里指torch.split的第二个参数   torch.split(tensor, split_size, dim=)  split_size是切分后每块的大小，不是切分为多少块！，多余的参数使用*cags接收
        xa, ya, za, dxa, dya, dza, ra, *cas = torch.split(anchors, 1, dim=-1)
        xg, yg, zg, dxg, dyg, dzg, rg, *cgs = torch.split(boxes, 1, dim=-1)
        # 计算anchor对角线长度
        diagonal = torch.sqrt(dxa ** 2 + dya ** 2)

        # 计算loss的公式，Δx,Δy,Δz,Δw,Δl,Δh,Δθ
        # ∆x = x ^ gt − xa ^ da
        xt = (xg - xa) / diagonal
        # ∆y = (y^gt − ya^da)/d^a
        yt = (yg - ya) / diagonal
        # ∆z = (z^gt − za^ha)/h^a
        zt = (zg - za) / dza
        # ∆l = log(l ^ gt / l ^ a)
        dxt = torch.log(dxg / dxa)
        # ∆w = log(w ^ gt / w ^ a)
        dyt = torch.log(dyg / dya)
        # ∆h = log(h ^ gt / h ^ a)
        dzt = torch.log(dzg / dza)
        # False
        if self.encode_angle_by_sincos:
            rt_cos = torch.cos(rg) - torch.cos(ra)
            rt_sin = torch.sin(rg) - torch.sin(ra)
            rts = [rt_cos, rt_sin]
        else:
            rts = [rg - ra]  # Δθ

        cts = [g - a for g, a in zip(cgs, cas)]
        return torch.cat([xt, yt, zt, dxt, dyt, dzt, *rts, *cts], dim=-1)
```
### loss计算实现
在PointPillars损失计算分别有三个，每个anhcor和GT的类别分类损失、box的7个回归损失、还有一个方向角预测的分类损失构成。
1、分类损失计算：
代码在pcdet/models/dense_heads/anchor_head_template.py
```python
 def get_cls_layer_loss(self):
        # (batch_size, 248, 216, 18) 网络类别预测
        cls_preds = self.forward_ret_dict['cls_preds']
        # (batch_size, 321408) 前景anchor类别
        box_cls_labels = self.forward_ret_dict['box_cls_labels']
        batch_size = int(cls_preds.shape[0])
        # [batch_szie, num_anchors]--> (batch_size, 321408)
        # 关心的anchor  选取出前景背景anchor, 在0.45到0.6之间的设置为仍然是-1，不参与loss计算
        cared = box_cls_labels >= 0
        # (batch_size, 321408) 前景anchor
        positives = box_cls_labels > 0
        # (batch_size, 321408) 背景anchor
        negatives = box_cls_labels == 0
        # 背景anchor赋予权重
        negative_cls_weights = negatives * 1.0
        # 将每个anchor分类的损失权重都设置为1
        cls_weights = (negative_cls_weights + 1.0 * positives).float()
        # 每个正样本anchor的回归损失权重，设置为1
        reg_weights = positives.float()
        # 如果只有一类
        if self.num_class == 1:
            # class agnostic
            box_cls_labels[positives] = 1

        # 正则化并计算权重     求出每个数据中有多少个正例，即shape=（batch， 1）
        pos_normalizer = positives.sum(1, keepdim=True).float()  # (4,1) 所有正例的和 eg:[[162.],[166.],[155.],[108.]]
        # 正则化回归损失-->(batch_size, 321408)，最小值为1,根据论文中所述，用正样本数量来正则化回归损失
        reg_weights /= torch.clamp(pos_normalizer, min=1.0)
        # 正则化分类损失-->(batch_size, 321408)，根据论文中所述，用正样本数量来正则化分类损失
        cls_weights /= torch.clamp(pos_normalizer, min=1.0)
        # care包含了背景和前景的anchor，但是这里只需要得到前景部分的类别即可不关注-1和0
        # cared.type_as(box_cls_labels) 将cared中为False的那部分不需要计算loss的anchor变成了0
        # 对应位置相乘后，所有背景和iou介于match_threshold和unmatch_threshold之间的anchor都设置为0
        cls_targets = box_cls_labels * cared.type_as(box_cls_labels)
        # 在最后一个维度扩展一次
        cls_targets = cls_targets.unsqueeze(dim=-1)

        cls_targets = cls_targets.squeeze(dim=-1)
        one_hot_targets = torch.zeros(
            *list(cls_targets.shape), self.num_class + 1, dtype=cls_preds.dtype, device=cls_targets.device
        )  # (batch_size, 321408, 4)，这里的类别数+1是考虑背景

        # target.scatter(dim, index, src)
        # scatter_函数的一个典型应用就是在分类问题中，
        # 将目标标签转换为one-hot编码形式 https://blog.csdn.net/guofei_fly/article/details/104308528
        # 这里表示在最后一个维度，将cls_targets.unsqueeze(dim=-1)所索引的位置设置为1

        """
            dim=1: 表示按照列进行填充
            index=batch_data.label:表示把batch_data.label里面的元素值作为下标，
            去下标对应位置(这里的"对应位置"解释为列，如果dim=0，那就解释为行)进行填充
            src=1:表示填充的元素值为1
        """
        # (batch_size, 321408, 4)
        one_hot_targets.scatter_(-1, cls_targets.unsqueeze(dim=-1).long(), 1.0)
        # (batch_size, 248, 216, 18) --> (batch_size, 321408, 3)
        cls_preds = cls_preds.view(batch_size, -1, self.num_class)
        # (batch_size, 321408, 3) 不计算背景分类损失
        one_hot_targets = one_hot_targets[..., 1:]

        # 计算分类损失 # [N, M] # (batch_size, 321408, 3)
        cls_loss_src = self.cls_loss_func(cls_preds, one_hot_targets, weights=cls_weights)
        # 求和并除以batch数目
        cls_loss = cls_loss_src.sum() / batch_size
        # loss乘以分类权重 --> cls_weight=1.0
        cls_loss = cls_loss * self.model_cfg.LOSS_CONFIG.LOSS_WEIGHTS['cls_weight']
        tb_dict = {
            'rpn_loss_cls': cls_loss.item()
        }
        return cls_loss, tb_dict
```
与之对应的focal_loss分类计算的详细实现代码在：pcdet/utils/loss_utils.py
``` python
class SigmoidFocalClassificationLoss(nn.Module):
    """
    多分类
    Sigmoid focal cross entropy loss.
    """

    def __init__(self, gamma: float = 2.0, alpha: float = 0.25):
        """
        Args:
            gamma: Weighting parameter to balance loss for hard and easy examples.
            alpha: Weighting parameter to balance loss for positive and negative examples.
        """
        super(SigmoidFocalClassificationLoss, self).__init__()
        self.alpha = alpha  # 0.25
        self.gamma = gamma  # 2.0

    @staticmethod
    def sigmoid_cross_entropy_with_logits(input: torch.Tensor, target: torch.Tensor):
        """ PyTorch Implementation for tf.nn.sigmoid_cross_entropy_with_logits:
            max(x, 0) - x * z + log(1 + exp(-abs(x))) in
            https://www.tensorflow.org/api_docs/python/tf/nn/sigmoid_cross_entropy_with_logits

        Args:
            input: (B, #anchors, #classes) float tensor.
                Predicted logits for each class
            target: (B, #anchors, #classes) float tensor.
                One-hot encoded classification targets

        Returns:
            loss: (B, #anchors, #classes) float tensor.
                Sigmoid cross entropy loss without reduction
        """
        loss = torch.clamp(input, min=0) - input * target + \
               torch.log1p(torch.exp(-torch.abs(input)))
        return loss

    def forward(self, input: torch.Tensor, target: torch.Tensor, weights: torch.Tensor):
        """
        Args:
            input: (B, #anchors, #classes) float tensor. eg:(4, 321408, 3)
                Predicted logits for each class :一个anchor会预测三种类别
            target: (B, #anchors, #classes) float tensor. eg:(4, 321408, 3)
                One-hot encoded classification targets，:真值
            weights: (B, #anchors) float tensor. eg:(4, 321408)
                Anchor-wise weights.
        Returns:
            weighted_loss: (B, #anchors, #classes) float tensor after weighting.
        """
        pred_sigmoid = torch.sigmoid(input)  # (batch_size, 321408, 3) f(x) = 1 / (1 + e^(-x))
        # 这里的加权主要是解决正负样本不均衡的问题:正样本的权重为0.25，负样本的权重为0.75
        # 交叉熵来自KL散度，衡量两个分布之间的相似性，针对二分类问题：
        # 合并形式: L = -(y * log(y^) + (1 - y) * log(1 - y^)) <--> 
        # 分段形式:y = 1, L = -y * log(y^); y = 0, L = -(1 - y) * log(1 - y^)
        # 这两种形式等价，只要是0和1的分类问题均可以写成两种等价形式，针对focal loss做类似处理
        # 相对熵 = 信息熵 + 交叉熵， 且交叉熵是凸函数，求导时能够得到全局最优值-->(sigma(s)- y)x  https://zhuanlan.zhihu.com/p/35709485
        alpha_weight = target * self.alpha + (1 - target) * (1 - self.alpha)  # (4, 321408, 3)
        pt = target * (1.0 - pred_sigmoid) + (1.0 - target) * pred_sigmoid
        focal_weight = alpha_weight * torch.pow(pt, self.gamma)

        # (batch_size, 321408, 3) 交叉熵损失的一种变形,具体推到参考上面的链接
        bce_loss = self.sigmoid_cross_entropy_with_logits(input, target)

        loss = focal_weight * bce_loss  # (batch_size, 321408, 3)

        if weights.shape.__len__() == 2 or \
                (weights.shape.__len__() == 1 and target.shape.__len__() == 2):
            weights = weights.unsqueeze(-1)

        assert weights.shape.__len__() == loss.shape.__len__()
        # weights参数使用正anchor数目进行平均，使得每个样本的损失与样本中目标的数量无关
        return loss * weights
```
2、box的回归SmoothL1损失计算和方向分类损失计算：
代码在：pcdet/models/dense_heads/anchor_head_template.py
```python 
def get_box_reg_layer_loss(self):
        # (batch_size, 248, 216, 42） anchor_box的7个回归参数
        box_preds = self.forward_ret_dict['box_preds']
        # (batch_size, 248, 216, 12） anchor_box的方向预测
        box_dir_cls_preds = self.forward_ret_dict.get('dir_cls_preds', None)
        # (batch_size, 321408, 7) 每个anchor和GT编码的结果
        box_reg_targets = self.forward_ret_dict['box_reg_targets']
        # (batch_size, 321408)
        box_cls_labels = self.forward_ret_dict['box_cls_labels']
        batch_size = int(box_preds.shape[0])
        # 获取所有anchor中属于前景anchor的mask  shape : (batch_size, 321408)
        positives = box_cls_labels > 0
        # 设置回归参数为1.    [True, False] * 1. = [1., 0.]
        reg_weights = positives.float()  # (4, 211200) 只保留标签>0的值
        # 同cls处理
        pos_normalizer = positives.sum(1,
                                       keepdim=True).float()  # (batch_size, 1) 所有正例的和 eg:[[162.],[166.],[155.],[108.]]

        reg_weights /= torch.clamp(pos_normalizer, min=1.0)  # (batch_size, 321408)

        if isinstance(self.anchors, list):
            if self.use_multihead:
                anchors = torch.cat(
                    [anchor.permute(3, 4, 0, 1, 2, 5).contiguous().view(-1, anchor.shape[-1]) for anchor in
                     self.anchors], dim=0)
            else:
                anchors = torch.cat(self.anchors, dim=-3)  # (1, 248, 216, 3, 2, 7)
        else:
            anchors = self.anchors
        # (1, 248*216, 7） --> (batch_size, 248*216, 7）
        anchors = anchors.view(1, -1, anchors.shape[-1]).repeat(batch_size, 1, 1)
        # (batch_size, 248*216, 7）
        box_preds = box_preds.view(batch_size, -1,
                                   box_preds.shape[-1] // self.num_anchors_per_location if not self.use_multihead else
                                   box_preds.shape[-1])
        # sin(a - b) = sinacosb-cosasinb
        # (batch_size, 321408, 7)
        box_preds_sin, reg_targets_sin = self.add_sin_difference(box_preds, box_reg_targets)
        loc_loss_src = self.reg_loss_func(box_preds_sin, reg_targets_sin, weights=reg_weights)
        loc_loss = loc_loss_src.sum() / batch_size

        loc_loss = loc_loss * self.model_cfg.LOSS_CONFIG.LOSS_WEIGHTS['loc_weight']  # loc_weight = 2.0 损失乘以回归权重
        box_loss = loc_loss
        tb_dict = {
            # pytorch中的item()方法，返回张量中的元素值，与python中针对dict的item方法不同
            'rpn_loss_loc': loc_loss.item()
        }

        # 如果存在方向预测，则添加方向损失
        if box_dir_cls_preds is not None:
            # (batch_size, 321408, 2)
            dir_targets = self.get_direction_target(
                anchors, box_reg_targets,
                dir_offset=self.model_cfg.DIR_OFFSET,  # 方向偏移量 0.78539 = π/4
                num_bins=self.model_cfg.NUM_DIR_BINS  # BINS的方向数 = 2
            )
            # 方向预测值 (batch_size, 321408, 2)
            dir_logits = box_dir_cls_preds.view(batch_size, -1, self.model_cfg.NUM_DIR_BINS)
            # 只要正样本的方向预测值 (batch_size, 321408)
            weights = positives.type_as(dir_logits)
            # (4, 211200) 除正例数量，使得每个样本的损失与样本中目标的数量无关
            weights /= torch.clamp(weights.sum(-1, keepdim=True), min=1.0)
            # 方向损失计算
            dir_loss = self.dir_loss_func(dir_logits, dir_targets, weights=weights)
            dir_loss = dir_loss.sum() / batch_size
            # 损失权重，dir_weight: 0.2
            dir_loss = dir_loss * self.model_cfg.LOSS_CONFIG.LOSS_WEIGHTS['dir_weight']
            # 将方向损失加入box损失
            box_loss += dir_loss

            tb_dict['rpn_loss_dir'] = dir_loss.item()
        return box_loss, tb_dict
```
方向分类的 target assignment，此处是指定该角度下应该是由分配到dir_bin中。
这里使用点云的坐标系减去了45度，可能的原因是：
减去dir_offset(45度)的原因可以参考这个issue:
[https://github.com/open-mmlab/OpenPCDet/issues/80https://github.com/open-mmlab/OpenPCDet/issues/80](https://github.com/open-mmlab/OpenPCDet/issues/80)

说的呢就是因为大部分目标都集中在0度和180度，270度和90度，
这样就会导致网络在这些角度的物体的预测上面不停的摇摆。所以为了解决这个问题，
将方向分类的角度判断减去45度再进行判断，如下图所示。
        这里减掉45度之后，在预测推理的时候，同样预测的角度解码之后
也要减去45度再进行之后测nms等操作。
下图来自FCOS3D论文
[FCOS3D：https://arxiv.org/pdf/2104.10956.pdf](https://arxiv.org/pdf/2104.10956.pdf)

![Image](https://github.com/user-attachments/assets/67f79d5c-f3a0-4cc7-bd8e-88352ea0b4cc)
box cls target assignment代码在：pcdet/models/dense_heads/anchor_head_template.py
```python
  def get_direction_target(anchors, reg_targets, one_hot=True, dir_offset=0, num_bins=2):
        batch_size = reg_targets.shape[0]
        # (batch_size, 321408, 7)
        anchors = anchors.view(batch_size, -1, anchors.shape[-1])
        # (batch_size, 321408)在-pi到pi之间
        # 由于reg_targets[..., 6]是经过编码的旋转角度，如果要回到原始角度需要重新加回anchor的角度就可以
        rot_gt = reg_targets[..., 6] + anchors[..., 6]
        """
        offset_rot shape : (batch_size, 321408)
        rot_gt - dir_offset  由于在openpcdet中x向前，y向左，z向上，
        
        减去dir_offset(45度)的原因可以参考这个issue:
        https://github.com/open-mmlab/OpenPCDet/issues/818
        说的呢就是因为大部分目标都集中在0度和180度，270度和90度，
        这样就会导致网络在一些物体的预测上面不停的摇摆。所以为了解决这个问题，
        将方向分类的角度判断减去45度再进行判断，
        这里减掉45度之后，在预测推理的时候，同样预测的角度解码之后
        也要减去45度再进行之后测nms等操作
        
        common_utils.limit_period:
        将角度限制在0到2*pi之间 原数据的角度在-pi到pi之间
        """
        offset_rot = common_utils.limit_period(rot_gt - dir_offset, 0, 2 * np.pi)
        # (batch_size, 321408) 取值为0和1，num_bins=2
        dir_cls_targets = torch.floor(offset_rot / (2 * np.pi / num_bins)).long()
        # (batch_size, 321408)
        dir_cls_targets = torch.clamp(dir_cls_targets, min=0, max=num_bins - 1)

        if one_hot:
            # (batch_size, 321408, 2)
            dir_targets = torch.zeros(*list(dir_cls_targets.shape), num_bins, dtype=anchors.dtype,
                                      device=dir_cls_targets.device)
            # one-hot编码，只存在两个方向:正向和反向 (batch_size, 321408, 2)
            dir_targets.scatter_(-1, dir_cls_targets.unsqueeze(dim=-1).long(), 1.0)
            dir_cls_targets = dir_targets
        return dir_cls_targets
```
方向回归的smoothL1计算 
代码在pcdet/utils/loss_utils.py
```python
class WeightedSmoothL1Loss(nn.Module):
    """
    Code-wise Weighted Smooth L1 Loss modified based on fvcore.nn.smooth_l1_loss
    https://github.com/facebookresearch/fvcore/blob/master/fvcore/nn/smooth_l1_loss.py
                  | 0.5 * x ** 2 / beta   if abs(x) < beta
    smoothl1(x) = |
                  | abs(x) - 0.5 * beta   otherwise,
    where x = input - target.
    """

    def __init__(self, beta: float = 1.0 / 9.0, code_weights: list = None):
        """
        Args:
            beta: Scalar float.
                L1 to L2 change point.
                For beta values < 1e-5, L1 loss is computed.
            code_weights: (#codes) float list if not None.
                Code-wise weights.
        """
        super(WeightedSmoothL1Loss, self).__init__()
        self.beta = beta  # 默认值1/9=0.111
        if code_weights is not None:
            self.code_weights = np.array(code_weights, dtype=np.float32)  # [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            self.code_weights = torch.from_numpy(self.code_weights).cuda()  # 将权重放到GPU上

    @staticmethod
    def smooth_l1_loss(diff, beta):
        # 如果beta非常小，则直接用abs计算，否则按照正常的Smooth L1 Loss计算
        if beta < 1e-5:
            loss = torch.abs(diff)
        else:
            n = torch.abs(diff)  # (batch_size, 321408, 7)
            # smoothL1公式，如上面所示 --> (batch_size, 321408, 7)
            loss = torch.where(n < beta, 0.5 * n ** 2 / beta, n - 0.5 * beta)

        return loss

    def forward(self, input: torch.Tensor, target: torch.Tensor, weights: torch.Tensor = None):
        """
        Args:
            input: (B, #anchors, #codes) float tensor.
                Ecoded predicted locations of objects.
            target: (B, #anchors, #codes) float tensor.
                Regression targets.
            weights: (B, #anchors) float tensor if not None.

        Returns:
            loss: (B, #anchors) float tensor.
                Weighted smooth l1 loss without reduction.
        """
        # 如果target为nan,则等于input,否则等于target
        target = torch.where(torch.isnan(target), input, target)  # ignore nan targets# (batch_size, 321408, 7)

        diff = input - target  # (batch_size, 321408, 7)
        # code-wise weighting
        if self.code_weights is not None:
            diff = diff * self.code_weights.view(1, 1, -1)  #(batch_size, 321408, 7) 乘以box每一项的权重

        loss = self.smooth_l1_loss(diff, self.beta)

        # anchor-wise weighting
        if weights is not None:
            assert weights.shape[0] == loss.shape[0] and weights.shape[1] == loss.shape[1]
            # weights参数使用正anchor数目进行平均，使得每个样本的损失与样本中目标的数量无关
            loss = loss * weights.unsqueeze(-1)

        return loss
```
方向分类损失计算：
代码在pcdet/utils/loss_utils.py
``` python
class WeightedCrossEntropyLoss(nn.Module):
    """
    二分类
    Transform input to fit the formation of PyTorch official cross entropy loss
    with anchor-wise weighting.
    """

    def __init__(self):
        super(WeightedCrossEntropyLoss, self).__init__()

    def forward(self, input: torch.Tensor, target: torch.Tensor, weights: torch.Tensor):
        """
        Args:
            input: (B, #anchors, #classes) float tensor.
                Predited logits for each class.
            target: (B, #anchors, #classes) float tensor.
                One-hot classification targets.
            weights: (B, #anchors) float tensor.
                Anchor-wise weights.

        Returns:
            loss: (B, #anchors) float tensor.
                Weighted cross entropy loss without reduction
        """
        input = input.permute(0, 2, 1)  # (batch_size, 7, 321408)
        target = target.argmax(dim=-1)  # (batch_size, 321408)
        # cross_entropy = log_softmax + nll_loss
        # 先对input进行softmax，然后取log，最后将y与经过log_softmax()函数激活后的数据，两者相乘，再求平均值，最后取反
        # 计算交叉熵损失并乘权重 (batch_size, 321408)
        loss = F.cross_entropy(input, target, reduction='none') * weights
        return loss
```