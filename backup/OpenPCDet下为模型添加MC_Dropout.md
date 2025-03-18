## 什么是MC_DropOut
**MC DropOut(Monte Carlo Dropout)** 是一种在深度学习中使用Dropout技术进行不确定性估计的方法。它由Yarin Gal和Zoubin Ghahramani在2016年提出，主要用于贝叶斯神经网络中，通过Dropout机制来近似贝叶斯推断。

**特征：**
在传统的神经网络中，模型训练完成后，Dropout通常会被关闭，以获得确定的预测结果。然而，Dropout在训练时引入的随机性实际上可以用于估计模型的不确定性。**MC DropOut的核心思想是在测试阶段（推理阶段）仍然保留DropOut，通过多次前向传播（Monte Carlo采样）来估计模型预测的分布。**

## 总体思路与引文

主要实验思路参考这篇文章https://arxiv.org/pdf/[2206.00214](https://arxiv.org/pdf/2206.00214)
选用**PointPillar**和**SECOND**两个3D目标检测模型。
框架为OpenPCDet https://github.com/open-mmlab/OpenPCDet

> We evaluate LiDAR-MIMO against MC dropout and ensembles on two detectors, PointPillars (PP) and SECOND (SC). We use the PP and SC implementations provided in OpenPCDet [33], and extend them with MC dropout, ensembling, and MIMO-BEV. We refer to the resulting detectors for MC dropout, ensemble and MIMO-BEV as multi-output. More efficient ensemble approaches such as TreeNet [34] or BatchEnsemble [35] were not tested due to their lower performance compared to a standard ensemble [7].
> **Baseline:** The baseline models for evaluating detection performance use the original PP and SC implementations. For KITTI, we use the PP and SC models provided with OpenPCDet. All baseline models are trained with the sigmoid focal loss for 80 epochs.
> **Multi-output:** Each multi-input model shares the same voxel-feature network, backbone, and head from the original PP and SC, with some exceptions for MC dropout and MIMO-BEV as described shortly. Further, all multi-output detectors use the softmax focal classification loss, smooth L1 regression losses, and the previously described aleatoric regression losses, and share the same clustering and merging stage. Each multi-input model is trained for an extra 40 epochs compared to the baseline models in order to have the models converge with the new loss functions.
> **MC dropout:** We create a variant of the backbone by inserting a dropout layer, with 0.5 probability, after the ReLU of each deconvolution block. During inference, we keep the dropout layers active for MC dropout. This model is trained with a batch size of 6 for 120 epochs.
> **Ensemble:** We train four unique models to form our ensemble. Each model is trained with a different random seed for frame order shuffling, for a batch size of 6 with 120 epochs.
> **MIMO-BEV:** MIMO-BEV requires additional code for pseudo images combination and adding multiple heads. There are three hyper parameters for MIMO: number of heads, input repetition (IR) and batch repetition (BR). We selected the number of heads to be 2 as the base networks have low capacity. IR is used to select a percentage of frame groupings in a batch to have matching frame, while BR duplicates each frame in a batch for smoother training. Since we are using a low batch size we were able to train with an IR of 0% and a BR of 0. This model is trained with a batch size of 3 with 120 epochs.


附上一段翻译：
>我们在两种检测器（PointPillars (PP) 和 SECOND (SC)）上评估了 LiDAR-MIMO 与 MC Dropout 和集成方法的效果。我们使用了 OpenPCDet [33] 提供的 PP 和 SC 实现，并对其进行了扩展，增加了 MC Dropout、集成方法和 MIMO-BEV。我们将这些扩展后的检测器（MC Dropout、集成方法和 MIMO-BEV）称为多输出检测器。由于性能较低，我们未测试更高效的集成方法，如 TreeNet [34] 或 BatchEnsemble [35] [7]。
**基线模型：**用于评估检测性能的基线模型使用了原始的 PP 和 SC 实现。对于 KITTI 数据集，我们使用了 OpenPCDet 提供的 PP 和 SC 模型。所有基线模型均使用 Sigmoid Focal Loss 训练 80 个 epoch。
**多输出模型：**每个多输入模型共享原始 PP 和 SC 的体素特征网络、骨干网络和头部网络，但 MC Dropout 和 MIMO-BEV 有一些例外，稍后会描述。此外，所有多输出检测器均使用 Softmax Focal 分类损失、平滑 L1 回归损失以及之前描述的偶然性回归损失，并共享相同的聚类和合并阶段。与基线模型相比，每个多输入模型额外训练了 40 个 epoch，以确保模型在新损失函数下收敛。
**MC Dropout：**我们在骨干网络的每个反卷积块的 ReLU 后插入了一个概率为 0.5 的 Dropout 层，创建了一个变体。在推理过程中，我们保持 Dropout 层激活以进行 MC Dropout。该模型以 6 的批量大小训练了 120 个 epoch。
集成方法：我们训练了四个独立的模型来组成集成。每个模型使用不同的随机种子对帧顺序进行打乱，并以 6 的批量大小训练了 120 个 epoch。
**MIMO-BEV：**MIMO-BEV 需要额外的代码来组合伪图像并添加多个头部。MIMO 有三个超参数：头部数量、输入重复（IR）和批次重复（BR）。由于基础网络容量较低，我们选择头部数量为 2。IR 用于选择批次中帧分组的匹配帧百分比，而 BR 则复制批次中的每一帧以实现更平滑的训练。由于我们使用了较小的批量大小，因此能够在 IR 为 0% 和 BR 为 0 的情况下进行训练。该模型以 3 的批量大小训练了 120 个 epoch。

**大致实验思路：**

- 在骨干网络的每个反卷积块的ReLU后插入概率为的DropOut层。
- 以 6 的批量大小训练 120 个 epoch。
- 在推理过程中，保持 Dropout 层激活以进行 MC Dropout。

## 模型中插入DropOut层
在`pcdet/models/backbones_2d/base_bev_backbone.py`中找到PointPillar和SECOND网络提取特征的骨干网络`BaseBEVBackbone(nn.Module):`
为该类添加DropOut配置：
```python
class BaseBEVBackbone(nn.Module):
    def __init__(self, model_cfg, input_channels):
        super().__init__()
        self.model_cfg = model_cfg

        # 读取 Dropout 配置
        self.use_dropout = model_cfg.get('USE_DROPOUT', True)
        self.dropout_prob = model_cfg.get('DROPOUT_PROB', 0.5)

        # 配置日志输出
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

        # 读取下采样层参数
        if self.model_cfg.get('LAYER_NUMS', None) is not None:
            assert len(self.model_cfg.LAYER_NUMS) == len(self.model_cfg.LAYER_STRIDES) == len(
                self.model_cfg.NUM_FILTERS)
            layer_nums = self.model_cfg.LAYER_NUMS
            layer_strides = self.model_cfg.LAYER_STRIDES
            num_filters = self.model_cfg.NUM_FILTERS
        else:
            layer_nums = layer_strides = num_filters = []

        # 读取上采样层参数
        if self.model_cfg.get('UPSAMPLE_STRIDES', None) is not None:
            assert len(self.model_cfg.UPSAMPLE_STRIDES) == len(self.model_cfg.NUM_UPSAMPLE_FILTERS)
            num_upsample_filters = self.model_cfg.NUM_UPSAMPLE_FILTERS
            upsample_strides = self.model_cfg.UPSAMPLE_STRIDES
        else:
            upsample_strides = num_upsample_filters = []

        num_levels = len(layer_nums)
        c_in_list = [input_channels, *num_filters[:-1]]
        self.blocks = nn.ModuleList()
        self.deblocks = nn.ModuleList()

        # 添加Dropout层
        for idx in range(num_levels):
            cur_layers = [
                nn.ZeroPad2d(1),
                nn.Conv2d(
                    c_in_list[idx], num_filters[idx], kernel_size=3,
                    stride=layer_strides[idx], padding=0, bias=False
                ),
                nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                nn.ReLU()
            ]

            for k in range(layer_nums[idx]):
                cur_layers.extend([
                    nn.Conv2d(num_filters[idx], num_filters[idx], kernel_size=3, padding=1, bias=False),
                    nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                    nn.ReLU()
                ])

                # 在ReLU后面添加Dropout层,logger用于观测训练时DropOut是否打开
                if self.use_dropout:
                    cur_layers.append(nn.Dropout(p=self.dropout_prob))
                    self.logger.debug(f"Dropout enabled with probability: {self.dropout_prob} at layer {idx}-{k}")

            self.blocks.append(nn.Sequential(*cur_layers))

            if len(upsample_strides) > 0:
                stride = upsample_strides[idx]
                if stride > 1 or (stride == 1 and not self.model_cfg.get('USE_CONV_FOR_NO_STRIDE', False)):
                    self.deblocks.append(nn.Sequential(
                        nn.ConvTranspose2d(
                            num_filters[idx], num_upsample_filters[idx],
                            upsample_strides[idx],
                            stride=upsample_strides[idx], bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))
                else:
                    stride = np.round(1 / stride).astype(np.int)
                    self.deblocks.append(nn.Sequential(
                        nn.Conv2d(
                            num_filters[idx], num_upsample_filters[idx],
                            stride,
                            stride=stride, bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))

        c_in = sum(num_upsample_filters)
        if len(upsample_strides) > num_levels:
            self.deblocks.append(nn.Sequential(
                nn.ConvTranspose2d(c_in, c_in, upsample_strides[-1], stride=upsample_strides[-1], bias=False),
                nn.BatchNorm2d(c_in, eps=1e-3, momentum=0.01),
                nn.ReLU(),
            ))

        self.num_bev_features = c_in

    def forward(self, data_dict):
        """
        Args:
            data_dict:
                spatial_features
        Returns:
        """
        spatial_features = data_dict['spatial_features']
        ups = []
        ret_dict = {}
        x = spatial_features

        self.logger.debug(f"Starting forward pass, Dropout enabled: {self.use_dropout}")

        # 对每个block进行前向传播
        for i in range(len(self.blocks)):
            x = self.blocks[i](x)

            stride = int(spatial_features.shape[2] / x.shape[2])
            ret_dict['spatial_features_%dx' % stride] = x

            if len(self.deblocks) > 0:
                ups.append(self.deblocks[i](x))
            else:
                ups.append(x)

        if len(ups) > 1:
            x = torch.cat(ups, dim=1)
        elif len(ups) == 1:
            x = ups[0]

        if len(self.deblocks) > len(self.blocks):
            x = self.deblocks[-1](x)

        data_dict['spatial_features_2d'] = x
        return data_dict
```
配置新的`pointpillar_MCdropout.yaml`文件添加到`tools/cfgs/kitti_models/`文件路径下,SECOND网络同理。
```yaml
CLASS_NAMES: ['Car', 'Pedestrian', 'Cyclist']

DATA_CONFIG:
    _BASE_CONFIG_: cfgs/dataset_configs/kitti_dataset.yaml

    POINT_CLOUD_RANGE: [0, -39.68, -3, 69.12, 39.68, 1]
    DATA_PROCESSOR:
        - NAME: mask_points_and_boxes_outside_range
          REMOVE_OUTSIDE_BOXES: True

        - NAME: shuffle_points
          SHUFFLE_ENABLED: {
            'train': True,
            'test': False
          }

        - NAME: transform_points_to_voxels
          VOXEL_SIZE: [0.16, 0.16, 4]
          MAX_POINTS_PER_VOXEL: 32
          MAX_NUMBER_OF_VOXELS: {
            'train': 16000,
            'test': 40000
          }
    DATA_AUGMENTOR:
        DISABLE_AUG_LIST: ['placeholder']
        AUG_CONFIG_LIST:
            - NAME: gt_sampling
              USE_ROAD_PLANE: False
              DB_INFO_PATH:
                  - kitti_dbinfos_train.pkl
              PREPARE: {
                 filter_by_min_points: ['Car:5', 'Pedestrian:5', 'Cyclist:5'],
                 filter_by_difficulty: [-1],
              }

              SAMPLE_GROUPS: ['Car:15','Pedestrian:15', 'Cyclist:15']
              NUM_POINT_FEATURES: 4
              DATABASE_WITH_FAKELIDAR: False
              REMOVE_EXTRA_WIDTH: [0.0, 0.0, 0.0]
              LIMIT_WHOLE_SCENE: False

            - NAME: random_world_flip
              ALONG_AXIS_LIST: ['x']

            - NAME: random_world_rotation
              WORLD_ROT_ANGLE: [-0.78539816, 0.78539816]

            - NAME: random_world_scaling
              WORLD_SCALE_RANGE: [0.95, 1.05]

MODEL:
    NAME: PointPillar

    VFE:
        NAME: PillarVFE
        WITH_DISTANCE: False
        USE_ABSLOTE_XYZ: True
        USE_NORM: True
        NUM_FILTERS: [64]

    MAP_TO_BEV:
        NAME: PointPillarScatter
        NUM_BEV_FEATURES: 64

    BACKBONE_2D:
        NAME: BaseBEVBackbone
        LAYER_NUMS: [3, 5, 5]
        LAYER_STRIDES: [2, 2, 2]
        NUM_FILTERS: [64, 128, 256]
        UPSAMPLE_STRIDES: [1, 2, 4]
        NUM_UPSAMPLE_FILTERS: [128, 128, 128]
      # 在这里添加 Dropout 配置
        USE_MC_DROPOUT: True
        DROPOUT_PROB: 0.5  # Dropout 的概率，可根据需要调整
    DENSE_HEAD:
        NAME: AnchorHeadSingle
        CLASS_AGNOSTIC: False

        USE_DIRECTION_CLASSIFIER: True
        DIR_OFFSET: 0.78539
        DIR_LIMIT_OFFSET: 0.0
        NUM_DIR_BINS: 2

        ANCHOR_GENERATOR_CONFIG: [
            {
                'class_name': 'Car',
                'anchor_sizes': [[3.9, 1.6, 1.56]],
                'anchor_rotations': [0, 1.57],
                'anchor_bottom_heights': [-1.78],
                'align_center': False,
                'feature_map_stride': 2,
                'matched_threshold': 0.6,
                'unmatched_threshold': 0.45
            },
            {
                'class_name': 'Pedestrian',
                'anchor_sizes': [[0.8, 0.6, 1.73]],
                'anchor_rotations': [0, 1.57],
                'anchor_bottom_heights': [-0.6],
                'align_center': False,
                'feature_map_stride': 2,
                'matched_threshold': 0.5,
                'unmatched_threshold': 0.35
            },
            {
                'class_name': 'Cyclist',
                'anchor_sizes': [[1.76, 0.6, 1.73]],
                'anchor_rotations': [0, 1.57],
                'anchor_bottom_heights': [-0.6],
                'align_center': False,
                'feature_map_stride': 2,
                'matched_threshold': 0.5,
                'unmatched_threshold': 0.35
            }
        ]

        TARGET_ASSIGNER_CONFIG:
            NAME: AxisAlignedTargetAssigner
            POS_FRACTION: -1.0
            SAMPLE_SIZE: 512
            NORM_BY_NUM_EXAMPLES: False
            MATCH_HEIGHT: False
            BOX_CODER: ResidualCoder

        LOSS_CONFIG:
            LOSS_WEIGHTS: {
                'cls_weight': 1.0,
                'loc_weight': 2.0,
                'dir_weight': 0.2,
                'code_weights': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            }

    POST_PROCESSING:
        RECALL_THRESH_LIST: [0.3, 0.5, 0.7]
        SCORE_THRESH: 0.1
        OUTPUT_RAW_SCORE: False

        EVAL_METRIC: kitti

        NMS_CONFIG:
            MULTI_CLASSES_NMS: False
            NMS_TYPE: nms_gpu
            NMS_THRESH: 0.01
            NMS_PRE_MAXSIZE: 4096
            NMS_POST_MAXSIZE: 500


OPTIMIZATION:
    BATCH_SIZE_PER_GPU: 6
    #增加额外的训练轮数
    NUM_EPOCHS: 120

    OPTIMIZER: adam_onecycle
    LR: 0.003
    WEIGHT_DECAY: 0.01
    MOMENTUM: 0.9

    MOMS: [0.95, 0.85]
    PCT_START: 0.4
    DIV_FACTOR: 10
    DECAY_STEP_LIST: [35, 45]
    LR_DECAY: 0.1
    LR_CLIP: 0.0000001

    LR_WARMUP: False
    WARMUP_EPOCH: 1

    GRAD_NORM_CLIP: 10
```
**进行训练**
```bash
cd tools
```
``` bash
python train.py --cfg_file cfgs/kitti_models/pointpillar_MCdropout.yaml --batch_size 6 --epochs 120 
```
**second同理**
```bash
python train.py --cfg_file cfgs/kitti_models/second_MCdropout.yaml --batch_size 6 --epochs 120
```
训练完成后检查`output/kitti_models/pointpillar_MCdropout`中`ckpt`中有120的epoch，即表明训练成功，second
网络同理

![Image](https://github.com/user-attachments/assets/3da38ed3-cc9a-4b64-9c38-fe5bbd622bae)

## 评估过程中打开DropOut
OpenPCDet中，负责评估模型的文件为`test.py`,位于路径`tools/test.py`
修改该文件下的`eval_single_ckpt`函数
```

def eval_single_ckpt(model, test_loader, args, eval_output_dir, logger, epoch_id, dist_test=False):
    logger.info(f'Loading checkpoint from: {args.ckpt}')
    if not os.path.exists(args.ckpt):
        logger.error(f'Checkpoint file not found: {args.ckpt}')
        return

    # 加载检查点
    model.load_params_from_file(filename=args.ckpt, logger=logger, to_cpu=dist_test,
                                pre_trained_path=args.pretrained_model)
    model.cuda()

    # 将整个模型设置为 eval 模式
    model.eval()

    # 如果启用 MC Dropout，手动将 Dropout 层设置为 train 模式
    if args.mc_dropout:
        for m in model.modules():
            if isinstance(m, torch.nn.Dropout):
                m.train()
                logger.info('Dropout layer set to train mode: %s' % str(m))

    # 开始评估
    eval_utils.eval_one_epoch(
        cfg, args, model, test_loader, epoch_id, logger, dist_test=dist_test,
        result_dir=eval_output_dir
    )



```
核心修改为：

```python
for m in model.modules():
    if isinstance(m, torch.nn.Dropout):
        m.train()
        logger.info('Dropout layer set to train mode: %s' % str(m))
```
遍历模型的所有子模块，找到 Dropout 层，并将其设置为 train 模式。
在 train 模式下，Dropout 层会随机丢弃神经元。

```python
num_samples = 10  # 默认采样 10 次
```
定义 MC Dropout 的采样次数（即对每个输入进行多少次前向传播）。
采样次数越多，模型的不确定性估计越准确，但计算成本也越高。
10 次是一个常用的默认值，可以根据实际需求调整。

```python
pred_dicts_list = []
for _ in range(num_samples):
    with torch.no_grad():  # 禁用梯度计算
        pred_dicts, ret_dict = model(batch_dict)
        pred_dicts_list.append(pred_dicts)
```
对每个输入进行多次前向传播，每次前向传播时 Dropout 层会随机丢弃不同的神经元。
将每次前向传播的结果保存到 `pred_dicts_list `中

```python
pred_dicts = pred_dicts_list[-1]
```
使用最后一次前向传播的结果进行后续处理（例如计算指标、保存结果等）。
**此处有争议，尚未弄明白，后续更新**

>[!IMPORTANT]
>注意此处不可以简单粗暴的把整个评估模式由`model.eval()`改为`model.train()` ，虽然看起来在评估过程中一直在输出Dropout enabled with probability：True的消息，但是多次评估的结果并无变化。而是需要保持评估模式为 eval 模式，再手动设置Dropout层为train模式（有先后顺序）。

在eval模式下BatchNorm 层会使用全局统计量（而不是当前 batch 的统计量），MC Dropout 的核心思想是通过多次前向传播（每次随机丢弃不同的神经元）来估计模型的不确定性。

如果不想破坏test.py文件的公共使用性，可以在`tools/eval_utils/eval_utils.py`中写一个专用的MC_Dropout评估，效果是一样的：
```python
#这个是默认打开MC_DropOut的
def eval_one_epoch(cfg, args, model, dataloader, epoch_id, logger, dist_test=False, result_dir=None):
    result_dir.mkdir(parents=True, exist_ok=True)

    final_output_dir = result_dir / 'final_result' / 'data'
    if args.save_to_file:
        final_output_dir.mkdir(parents=True, exist_ok=True)

    metric = {
        'gt_num': 0,
    }
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        metric['recall_roi_%s' % str(cur_thresh)] = 0
        metric['recall_rcnn_%s' % str(cur_thresh)] = 0

    dataset = dataloader.dataset
    class_names = dataset.class_names
    det_annos = []

    if getattr(args, 'infer_time', False):
        start_iter = int(len(dataloader) * 0.1)
        infer_time_meter = common_utils.AverageMeter()

    logger.info('*************** EPOCH %s EVALUATION *****************' % epoch_id)
    if dist_test:
        num_gpus = torch.cuda.device_count()
        local_rank = cfg.LOCAL_RANK % num_gpus
        model = torch.nn.parallel.DistributedDataParallel(
                model,
                device_ids=[local_rank],
                broadcast_buffers=False
        )

    # 将整个模型设置为 eval 模式
    model.eval()

    # 默认开启 MC Dropout，手动将 Dropout 层设置为 train 模式
    for m in model.modules():
        if isinstance(m, torch.nn.Dropout):
            m.train()
            logger.info('Dropout layer set to train mode: %s' % str(m))

    # 设置 MC Dropout 的采样次数
    num_samples = 10  # 默认采样 10 次

    if cfg.LOCAL_RANK == 0:
        progress_bar = tqdm.tqdm(total=len(dataloader), leave=True, desc='eval', dynamic_ncols=True)
    start_time = time.time()

    for i, batch_dict in enumerate(dataloader):
        load_data_to_gpu(batch_dict)

        if getattr(args, 'infer_time', False):
            start_time = time.time()

        # 进行多次前向传播（MC Dropout）
        pred_dicts_list = []
        for _ in range(num_samples):
            with torch.no_grad():  # 禁用梯度计算
                pred_dicts, ret_dict = model(batch_dict)
                pred_dicts_list.append(pred_dicts)

        # 使用最后一次预测结果进行后续处理
        pred_dicts = pred_dicts_list[-1]

        disp_dict = {}

        if getattr(args, 'infer_time', False):
            inference_time = time.time() - start_time
            infer_time_meter.update(inference_time * 1000)
            # use ms to measure inference time
            disp_dict['infer_time'] = f'{infer_time_meter.val:.2f}({infer_time_meter.avg:.2f})'

        statistics_info(cfg, ret_dict, metric, disp_dict)
        annos = dataset.generate_prediction_dicts(
            batch_dict, pred_dicts, class_names,
            output_path=final_output_dir if args.save_to_file else None
        )
        det_annos += annos
        if cfg.LOCAL_RANK == 0:
            progress_bar.set_postfix(disp_dict)
            progress_bar.update()

    if cfg.LOCAL_RANK == 0:
        progress_bar.close()

    if dist_test:
        rank, world_size = common_utils.get_dist_info()
        det_annos = common_utils.merge_results_dist(det_annos, len(dataset), tmpdir=result_dir / 'tmpdir')
        metric = common_utils.merge_results_dist([metric], world_size, tmpdir=result_dir / 'tmpdir')

    logger.info('*************** Performance of EPOCH %s *****************' % epoch_id)
    sec_per_example = (time.time() - start_time) / len(dataloader.dataset)
    logger.info('Generate label finished(sec_per_example: %.4f second).' % sec_per_example)

    if cfg.LOCAL_RANK != 0:
        return {}

    ret_dict = {}
    if dist_test:
        for key, val in metric[0].items():
            for k in range(1, world_size):
                metric[0][key] += metric[k][key]
        metric = metric[0]

    gt_num_cnt = metric['gt_num']
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        cur_roi_recall = metric['recall_roi_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        cur_rcnn_recall = metric['recall_rcnn_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        logger.info('recall_roi_%s: %f' % (cur_thresh, cur_roi_recall))
        logger.info('recall_rcnn_%s: %f' % (cur_thresh, cur_rcnn_recall))
        ret_dict['recall/roi_%s' % str(cur_thresh)] = cur_roi_recall
        ret_dict['recall/rcnn_%s' % str(cur_thresh)] = cur_rcnn_recall

    total_pred_objects = 0
    for anno in det_annos:
        total_pred_objects += anno['name'].__len__()
    logger.info('Average predicted number of objects(%d samples): %.3f'
                % (len(det_annos), total_pred_objects / max(1, len(det_annos))))

    with open(result_dir / 'result.pkl', 'wb') as f:
        pickle.dump(det_annos, f)

    result_str, result_dict = dataset.evaluation(
        det_annos, class_names,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
        output_path=final_output_dir
    )

    logger.info(result_str)
    ret_dict.update(result_dict)

    logger.info('Result is saved to %s' % result_dir)
    logger.info('****************Evaluation done.*****************')
    return ret_dict

```
## 进行评估

```bash
python test.py     --cfg_file /home/tdhu/OpenPCDet/tools/cfgs/kitti_models/pointpillar_MCdropout.yaml     --batch_size 4     --ckpt /home/tdhu/OpenPCDet/output/kitti_models/pointpillar_MCdropout/default/ckpt/checkpoint_epoch_120.pth    
```
>[!TIP]
>打开MC_DropOut后的评估速度会明显下降，这是因为计算量提高了很多，属于正常现象。

由于打开了MC_DropOut后模型会随机丢弃一些节点，所以每次的评估结果是不同的，写个脚本直接评估十次。
修改在`test.py`文件中:
```python
def main():
    args, cfg = parse_config()

    if args.infer_time:
        os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

    if args.launcher == 'none':
        dist_test = False
        total_gpus = 1
    else:
        if args.local_rank is None:
            args.local_rank = int(os.environ.get('LOCAL_RANK', '0'))

        total_gpus, cfg.LOCAL_RANK = getattr(common_utils, 'init_dist_%s' % args.launcher)(args.tcp_port, args.local_rank, backend='nccl')
        dist_test = True

    if args.batch_size is None:
        args.batch_size = cfg.OPTIMIZATION.BATCH_SIZE_PER_GPU
    else:
        assert args.batch_size % total_gpus == 0, 'Batch size should match the number of gpus'
        args.batch_size = args.batch_size // total_gpus

    output_dir = cfg.ROOT_DIR / 'output' / cfg.EXP_GROUP_PATH / cfg.TAG / args.extra_tag
    output_dir.mkdir(parents=True, exist_ok=True)

    eval_output_dir = output_dir / 'eval'

    if not args.eval_all:
        num_list = re.findall(r'\d+', args.ckpt) if args.ckpt is not None else []
        epoch_id = num_list[-1] if num_list.__len__() > 0 else 'no_number'
        eval_output_dir = eval_output_dir / ('epoch_%s' % epoch_id) / cfg.DATA_CONFIG.DATA_SPLIT['test']
    else:
        eval_output_dir = eval_output_dir / 'eval_all_default'

    if args.eval_tag is not None:
        eval_output_dir = eval_output_dir / args.eval_tag

    eval_output_dir.mkdir(parents=True, exist_ok=True)
    log_file = eval_output_dir / ('log_eval_%s.txt' % datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    logger = common_utils.create_logger(log_file, rank=cfg.LOCAL_RANK)

    # log to file
    logger.info('**********************Start logging**********************')
    gpu_list = os.environ['CUDA_VISIBLE_DEVICES'] if 'CUDA_VISIBLE_DEVICES' in os.environ.keys() else 'ALL'
    logger.info('CUDA_VISIBLE_DEVICES=%s' % gpu_list)

    if dist_test:
        logger.info('total_batch_size: %d' % (total_gpus * args.batch_size))
    for key, val in vars(args).items():
        logger.info('{:16} {}'.format(key, val))
    log_config_to_file(cfg, logger=logger)

    test_set, test_loader, sampler = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=args.batch_size,
        dist=dist_test, workers=args.workers, logger=logger, training=False
    )

    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=test_set)
    with torch.no_grad():
        # 运行 10 次评估
        for i in range(10):
            logger.info(f'Running evaluation {i+1}/10')
            # 设置随机种子
            seed = i  # 或者使用其他随机种子生成方式
            torch.manual_seed(seed)
            np.random.seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)

            # 创建子目录保存当前评估结果
            current_eval_dir = eval_output_dir / f'run_{i+1}'
            current_eval_dir.mkdir(parents=True, exist_ok=True)

            # 运行评估
            eval_single_ckpt(model, test_loader, args, current_eval_dir, logger, epoch_id, dist_test=dist_test)


if __name__ == '__main__':
    main()'''#MC_DROPOUT 评估10次版本
```
## 评估结果

![Image](https://github.com/user-attachments/assets/7bce3eb6-0a1a-4f2a-a244-7eccffb40637)

![Image](https://github.com/user-attachments/assets/7aaa9cfc-b3c6-4491-946e-d2b0b27282d8)

![Image](https://github.com/user-attachments/assets/4d99d298-35e5-4c0a-97f7-ba15794b2146)

结果各不相同，MC_dropout在评估过程中成功打开。评估结果用于后续实验，本实验结束。

