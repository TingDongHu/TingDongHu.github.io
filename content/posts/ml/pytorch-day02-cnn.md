---
title: "【深度学习】Day 2：CNN 架构与深度学习进阶理论"
date: 2026-05-07T00:00:00+08:00
categories: ["机器学习"]
tags: ["机器学习", "深度学习", "CNN"]
description: "卷积层、池化、Dropout、正则化、优化器（SGD/Momentum/Adam）、ResNet、Batch Normalization、迁移学习"
cover: "/img/machinelearning.png"
headerImage: "/img/rthykless.png"
math: true
---


> 日期：2026-05-07 ~ 2026-05-08
> 学习方式：苏格拉底式对话 + 理论推导
> 核心目标：理解 CNN 各组件的作用，以及优化器、正则化、残差网络、Batch Normalization 的核心思想

---

## 一句话串起来

我从卷积层理解到每个卷积核就是一个小型模式检测器（一堆可学习的 $W$），MaxPool 负责在保留最强信号的同时缩小特征图；学会了 Dropout 通过随机关神经元来防过拟合，L1/L2 正则化通过在 loss 上加权重惩罚实现类似效果；沿着优化器路线从 SGD（朴素梯度下降）走到 Momentum（加惯性）再到 Adam（自适应学习率 + 动量，当代默认选择）；然后理解了残差网络通过捷径连接给梯度开了一条"高速公路"来防止梯度消失；接着学到 Batch Normalization 在每层 Conv/Linear 后做标准化 + 可学习的缩放平移（$\gamma, \beta$），把每层的输出拉回均匀尺度——用一个具体数字例子来看，不加 BN 时 $w_1$ 和 $w_2$ 的梯度差 6 个数量级，加了 BN 后同量级。然后动手搭了一个 CNN 跑 MNIST（测试集 98.96%，比全连接版高 2 个百分点），最后理解了迁移学习——预训练模型在大数据集上先训好，然后通过特征提取（只训最后几层）或全参数微调或 LoRA（加小分支）来适配自己的任务。

---

## 第一章：CNN 整体架构

### 1.1 标准 CNN 结构

```
输入 [B, C, H, W]
    → [Conv2d → ReLU → (MaxPool2d)] × N   ← 特征提取阶段
    → Flatten (view)                       ← 格式转换（4D → 2D）
    → Linear → ReLU → ... → Linear         ← 分类决策阶段
    → CrossEntropyLoss
```

### 1.2 各组件的分工

| 组件 | 角色 | 有无参数 |
|------|------|---------|
| Conv2d | 局部模式检测（边缘、纹理、形状） | ✅ 有（权重 + 偏置） |
| ReLU | 注入非线性 | ❌ 无 |
| MaxPool2d | 下采样压缩，保留最强信号 | ❌ 无 |
| Linear | 全局决策分类 | ✅ 有 |

### 1.3 我当时的问题

**Q：** "Conv 和 Linear 是什么关系？卷积是替换了全连接层吗？"

**A：** 不是替换，是**分工合作**——Conv 负责提取特征，Linear 负责做分类决策。先看典型结构：

```
Conv2d → Pooling → Conv2d → Pooling → Flatten → Linear → Linear
          ↑ 特征提取阶段 ↑          ↑ 分类阶段 ↑
```

---

## 第二章：MaxPool2d（最大池化）

### 2.1 定义

$$
\text{MaxPool}(x)_{i,j} = \max_{p,q \in \text{窗口}} x_{i+p, j+q}
$$

在 $k \times k$ 窗口内取最大值，以此遍历整个特征图。

### 2.2 直觉类比

把 4K 高清图压成 720p——丢掉细节噪声，保留主要信息。

### 2.3 关键参数

```python
nn.MaxPool2d(kernel_size=2)  # 默认 stride = kernel_size，尺寸直接减半
```

$28 \times 28$ → MaxPool(2) → $14 \times 14$

### 2.4 池化的作用

1. **降维** — 特征图缩小，后续计算量指数级减少
2. **增强鲁棒性** — 像素偏移一两格，结果基本不变（平移不变性）
3. **扩大感受野** — 后面卷积虽然核还是 3×3，但看到的是池化前的 6×6 区域

### 2.5 池化 vs 卷积

| | 卷积 | 池化 |
|---|---|---|
| 有参数？ | ✅ 有（可学习） | ❌ 无 |
| 目的 | 检测特征/模式 | 压缩信息/降维 |
| 操作 | 逐元素乘后求和 | 取最大值或平均值 |
| 通道数 | 可以改变 | 不变（独立处理每通道） |

---

## 第三章：Dropout——随机关神经元

### 3.1 定义

训练时以概率 $p$ 随机将神经元的输出置 0，剩下的输出放大 $1/(1-p)$ 倍保持总值不变。

### 3.2 直觉类比

团队 10 个人，每次开会只随机来 5 个——久而久之每个人都能独当一面，不会过度依赖别人。

### 3.3 训练 vs 推理

```
训练模式：随机关 p% 神经元，剩余输出 × 1/(1-p) 做补偿
推理模式：所有神经元正常输出，Dropout 完全消失
```

PyTorch 自动切换：`model.train()` / `model.eval()`

### 3.4 代码验证

```python
import torch
import torch.nn as nn

dropout = nn.Dropout(p=0.5)
x = torch.ones(10)

dropout.train()
print(dropout(x))  # 约 5 个 2.0, 5 个 0.0（总和 ≈ 10）

dropout.eval()
print(dropout(x))  # [1, 1, 1, ...]（全部保留）
```

### 3.5 Dropout 本质 = 隐式模型集成

每次随机关一半神经元 = 训练一个不同的子网络。100 个神经元，潜在 $2^{100}$ 种子网络。推理时全部打开 ≈ 所有子网络投票表决。

### 3.6 实际应用

| 场景 | 效果 |
|------|------|
| 全连接层多（参数量大） | ✅ 有用 |
| 数据量小 | ✅ 有用 |
| 卷积层后 | ❌ 效果不明显 |
| 数据量极大 | ❌ 数据本身已够防过拟合 |

---

## 第四章：L1/L2 正则化

### 4.1 核心思想

在 loss 上加一个惩罚项，让权重不要太大，防止模型"死记硬背"训练数据。

### 4.2 公式对比

原始 Loss：
$$
L_{data} = \frac{1}{n}\sum (y_{pred} - y_{true})^2
$$

加 L2 正则化：
$$
L_{total} = L_{data} + \lambda \cdot \sum w^2
$$

加 L1 正则化：
$$
L_{total} = L_{data} + \lambda \cdot \sum |w|
$$

### 4.3 L1 vs L2 对比

| | L2 | L1 |
|---|---|---|
| 惩罚项 | $\lambda \cdot \sum w^2$ | $\lambda \cdot \sum \|w\|$ |
| 梯度 | $\partial/\partial w = 2w$（大权重压得狠） | $\partial/\partial w = \text{sign}(w)$（一直推直到 0） |
| 效果 | 大权重变小 | 小权重变零 |
| 用途 | 防止过拟合（标配） | 特征选择（自动剔除无关特征） |

### 4.4 代码实现

```python
# L2 正则化（PyTorch 自带，一行搞定）
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)
#                                               weight_decay = λ ↑

# L1 正则化（需手动添加）
l1_lambda = 1e-4
l1_loss = l1_lambda * sum(p.abs().sum() for p in model.parameters())
total_loss = loss + l1_loss
```

### 4.5 我当时的问题

**Q：** "如果上海和鹤岗房价差别就是很大，不正就需要大权重吗？"

**A：** 没错。L2 惩罚的是"过度特化于训练集噪声"的大权重，不是"真正的强相关"的大权重。问题在于模型分不清哪个是噪声哪个是信号——所以 L2 不是清零，而是往 0 方向"拉一点"，迫使模型用更多特征共同决策。

---

## 第五章：优化器——SGD → Momentum → Adam

### 5.1 优化器到底在做什么

训练循环的第 5 步：
```python
loss.backward()        # 算出每个参数的梯度
optimizer.step()       # 执行参数更新：w = w - lr · grad
```

不同优化器的区别就是这个公式的**具体策略不同**。

### 5.2 SGD（随机梯度下降）

$$
w = w - lr \cdot \nabla L(w)
$$

实际 PyTorch 里的 `optim.SGD` 是 Mini-batch SGD：
- 每次用 batch_size 个样本算平均梯度
- "随机"体现在 shuffle 打乱顺序 + 每次随机抽 batch

| 方法 | 每次用多少数据 | 更新次数（1 epoch） |
|------|--------------|-------------------|
| BGD（Batch GD） | 全部 60000 张 | 1 次 |
| SGD（真·随机） | 1 张 | 60000 次 |
| Mini-batch SGD | 64 张 | 938 次 ✅ 最常用 |

### 5.3 Momentum——加惯性

```
问题：SGD 在山谷两侧来回震荡，因为只盯着当前最陡方向

解决：加入"速度"项，积累历史梯度方向
```

$$
v = \alpha \cdot v_{old} + lr \cdot \nabla L(w)
$$
$$
w = w - v
$$

### 5.4 Adam——Momentum + 自适应学习率

**两个创新：**
1. **动量**（同 Momentum）— 惯性
2. **自适应学习率** — 每个参数有自己的步长

```
梯度稳定指向同一方向 → 步长大胆一点
梯度正正反反（噪声大） → 步长保守一点
```

### 5.5 三者对比

| 优化器 | 公式思想 | 特点 |
|--------|---------|------|
| SGD | $w -= lr \cdot grad$ | 笨但稳，需要仔细调 lr |
| Momentum | $v = \alpha v + lr \cdot grad$ | 加惯性，冲过小坑 |
| Adam | 动量 + 每参数自适应步长 | 开箱即用，默认首选 |

**实践建议：新手无脑选 Adam，设 $lr=0.001$，基本好用。**

---

## 第六章：残差网络（ResNet）

### 6.1 问题：层数越深效果反而越差

$$
20 \text{ 层: 准确率 } 90\% \quad\quad 56 \text{ 层: 准确率 } 89\%
$$

不是过拟合——56 层的**训练集**准确率也更低。

### 6.2 根因：梯度消失

链式法则让梯度指数级衰减：
$$
\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial y_{pred}} \cdot \frac{\partial y_{pred}}{\partial a_{55}} \cdot \frac{\partial a_{55}}{\partial a_{54}} \cdots \frac{\partial a_2}{\partial w_1}
$$

每层梯度 $\approx 0 \sim 1$，乘 55 次后 $\approx 0$ → 浅层参数几乎不动。

### 6.3 ResNet 的解决方案——捷径连接

```
普通块：输出 = F(x)                  ← 全靠权重层
ResNet块：输出 = F(x) + x             ← 当前层结果 + 原始输入
```

**如果两层什么都没学到（F(x) ≈ 0）：**
- 普通块：输出 = 0 → 信息全丢
- ResNet：输出 = 0 + x = x → **原始输入无损通过**

### 6.4 梯度视角

$$
\text{普通块梯度：} \frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial F}{\partial x}
$$
$$
\text{ResNet块梯度：} \frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \left( \frac{\partial F}{\partial x} + 1 \right)
$$

$+1$ 保证了梯度至少是 $\partial L / \partial y$——即使 $\partial F / \partial x = 0$，梯度也不消失。

这就是**梯度的高速公路**。

### 6.5 代价

1. **显存增加** — 需要保存每个残差块的输入 $x$，训练时显存约翻倍
2. **有效深度可能较低** — 大部分梯度走短捷径路径，152 层的实际有效深度可能远不到 152

**但收益远大于代价——没有 ResNet，152 层根本训不动。**

### 6.6 我当时的问题

**Q：** "最后一层的输出岂不是包含了前 1 到 n-1 层所有输出？"

**A：** 直觉方向对了。但关键是——捷径是**局部的**（跨 2 层卷积的一个残差块），不是从第 1 层直连最后一层。ResNet 由多个残差块堆叠而成，每个块内部有捷径。梯度回传时多了一条不走权重层的直达通道，所以不会衰减。

**Q：** "残差连接的代价是什么？"

**A：** 显存多了（需存每个残差块的输入），且网络可能没看起来那么"深"（大部分梯度走捷径）。但收益远大于代价——ResNet 从 2015 年至今已经是几乎所有深度网络的标配，包括 Transformer（GPT 里也有残差连接）。

---

## 第七章：Batch Normalization

### 7.1 为什么需要标准化？

不同特征的尺度差异过大 → 导致不同权重的梯度量级差几个数量级。

**具体例子（不加 BN）：**

房价 $x_1 = 5,000,000$，卧室数 $x_2 = 3$，初始 $w_1 = w_2 = 0.1$

前向：
$$
z = w_1 x_1 + w_2 x_2 + b = 0.1 \times 5,000,000 + 0.1 \times 3 + 0 = 500,000.3
$$

梯度：
$$
\frac{\partial L}{\partial w_1} = 2(z - y_{true}) \cdot x_1 \approx -4.5 \times 10^{13}
$$
$$
\frac{\partial L}{\partial w_2} = 2(z - y_{true}) \cdot x_2 \approx -2.7 \times 10^{7}
$$

$w_1$ 梯度比 $w_2$ 大 6 个数量级。同一个学习率：大了 $w_1$ 震荡甚至飞出去，小了 $w_2$ 几乎不动。**永远找不到一个适合所有参数的学习率。**

### 7.2 BN 做了什么（数字对比）

**加了 BN 后，同样的 $z = 500,000.3$：**

假设该 batch 的均值 $\mu = 480,000$，标准差 $\sigma = 200,000$：

$$
\hat{z} = \frac{z - \mu}{\sigma} = \frac{500,000 - 480,000}{200,000} = 0.1
$$

$$
\text{output} = \gamma \cdot \hat{z} + \beta
$$

| | 不加 BN | 加 BN |
|---|---|---|
| $z$ 的值 | 500,000.3 | $\hat{z} = 0.1$ |
| $\partial L/\partial w_1$ | $-4.5 \times 10^{13}$（爆炸） | 缩减到可控范围 |
| $\partial L/\partial w_2$ | $-2.7 \times 10^{7}$ | 和 $w_1$ 同一量级 |
| 一个 lr 同时训两个参数？ | ❌ 不能 | ✅ 能 |

### 7.3 BN 的位置

```
没有 BN：输入 → [Conv/Linear] → [ReLU] → 输出
有 BN：  输入 → [Conv/Linear] → [BN] → [ReLU] → 输出
```

### 7.4 BN 的完整公式

对一个 batch 中某通道的所有值：

$$
\mu_B = \frac{1}{m}\sum_{i=1}^{m} x_i \quad\quad \sigma_B^2 = \frac{1}{m}\sum_{i=1}^{m} (x_i - \mu_B)^2
$$
$$
\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \quad (\epsilon \text{ 防止除零})
$$
$$
y_i = \gamma \cdot \hat{x}_i + \beta
$$

其中 $\gamma$（缩放）和 $\beta$（平移）是**可学习参数**，每通道两个。

**为什么需要 $\gamma$ 和 $\beta$？**

网络不一定想要 0 均值 1 方差——如果原始分布对任务更好，网络可以学出：
$$
\gamma = \sigma, \quad \beta = \mu \quad \rightarrow \quad y = \sigma \cdot \frac{x - \mu}{\sigma} + \mu = x
$$

**恢复原始分布。BN 给了网络选择权，不是强制标准化。**

### 7.5 BN 的参数量

每通道两个参数。`Conv2d(3, 32, 3)` 输出 32 通道 → 64 个参数。相比卷积的 3×3×3×32 + 32 = 896 个参数，可以忽略不计。

### 7.6 BN 的效果

| | 无 BN | 有 BN |
|---|---|---|
| 最高可用学习率 | 0.001 就炸了 | 0.01 稳如狗 |
| 收敛速度 | 慢 | **快 10 倍** |
| 对初始化敏感度 | 高 | 低 |
| 梯度量级一致性 | ❌ 各层各参数差悬殊 | ✅ 统一量级 |

---

## 第八章：CNN MNIST 实战结果

### 8.1 网络结构

```
Conv2d(1, 32, 3, padding=1) → ReLU → MaxPool2d(2)     # [B,1,28,28] → [B,32,14,14]
Conv2d(32, 64, 3, padding=1) → ReLU → MaxPool2d(2)    # [B,32,14,14] → [B,64,7,7]
Flatten → Linear(64×7×7, 128) → ReLU → Linear(128, 10) # [B,3136] → [B,10]
```

### 8.2 代码

```python
import torch.nn as nn
import torch.nn.functional as F

class MNISTCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))   # [B,32,14,14]
        x = self.pool(F.relu(self.conv2(x)))   # [B,64,7,7]
        x = x.view(x.size(0), -1)              # [B, 3136]
        x = F.relu(self.fc1(x))                # [B, 128]
        x = self.fc2(x)                        # [B, 10]
        return x
```

### 8.3 三种方法对比

| 方法 | 参数量 | 测试准确率 | 特点 |
|------|--------|-----------|------|
| MLP 全连接（Day 1） | 109,386 | 97.07% | 基础，简单 |
| **CNN 从零训（Day 2）** | 421,642 | **98.96%** | 卷积提取空间特征 |
| ResNet-18 迁移（冻结 fc） | 11,181,642（仅 5K 可训） | 96.13% | 预训练域不匹配时反而不如小网络 |

**关键发现**：迁移学习不是万能的——预训练数据和目标任务差异大时（如 ImageNet 自然图像 → MNIST 黑白线条），从零训练专门设计的小网络反而更好。

---

## 第九章：迁移学习（Transfer Learning）

### 9.1 核心思想

别人在大数据集（ImageNet：1400 万张，1000 类）上训好了模型，你把它的权重拿过来，在自己的小数据上"微调"一下就能用。

```
传统做法：自己从零训 → 需要大量数据 + 大量算力
迁移学习：下载预训练权重 → 在自己的数据上微调 → 少量数据即可
```

### 9.2 预训练模型学到了什么

```
第1层卷积：检测边缘和色块（通用，所有图像任务都用得上）
中间层卷积：检测纹理和形状（也通用）
最后几层：检测"猫眼""车轮""机翼"（特定于预训练任务）
全连接层：对 1000 类分类（对你基本没用）
```

### 9.3 三种迁移策略

**策略一：特征提取（Feature Extraction）**

冻结所有预训练层，只训练自己新换上的分类层。

```python
for param in model.parameters():
    param.requires_grad = False     # 冻结

model.fc = nn.Linear(512, 10)       # 换上新分类头（10 类）
# 只训练这一层
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
```

```
冻结 → → → → → → → → → → → → → → → 不冻结
[Conv] [Conv] [Conv] ... [Conv] [fc(512→10)]
   ↑ 不更新（11M 参数冻结）    ↑ 只更新这层（5K 参数）
```

| 优点 | 缺点 |
|------|------|
| 训练极快，显存极低 | 预训练域和目标任务差异大时效果受限 |
| 数据少也不容易过拟合 | 模型无法适应新域的特殊特征 |

**策略二：全参数微调（Full Fine-tuning）**

下载预训练权重后，不冻结任何层，用很小的学习率在整个网络上继续训练。

```python
# 不冻结任何层
model.fc = nn.Linear(512, 10)
optimizer = optim.Adam(model.parameters(), lr=0.0001)  # 小学习率
```

| 优点 | 缺点 |
|------|------|
| 效果最好（所有层都适配你的任务） | 显存爆炸（需存所有层的梯度+优化器状态） |
| 域差距大时也能适应 | 数据少容易过拟合 |

**策略三：LoRA（Low-Rank Adaptation）**

不在原权重上改，而是在旁边加两个小矩阵学习"偏移量"。

```
原始权重 W（冻结不改）：
输入 → [W] → 输出

LoRA 在旁边加小分支：
输入 ─┬─→ [W（冻结）] ─┬─→ 输出
      │                │
      └─→ [A] → [B] ──┘     ← 只训练这两个小矩阵
```

核心思想：一个大矩阵 $W_{4096 \times 4096}$ 的有效变化，可以用两个小矩阵 $A_{4096 \times r} \times B_{r \times 4096}$ 近似。当 $r=8$ 时，参数量从 16M 降到 65K（节省 256 倍）。

### 9.4 三种策略对比

| | 特征提取（只调最后层） | 全参数微调 | LoRA |
|---|---|---|---|
| 训练参数量 | 几千 | 几千万～几十亿 | 几万～几百万 |
| 显存需求 | 极低 | 极高 | 低 |
| 效果（域接近时） | 好 | 最好 | 接近全参数 |
| 效果（域差异大时） | ❌ 差 | ✅ 好 | ✅ 较好 |
| 适用场景 | 数据少 + 域接近 | 你有大量 GPU | **LLM 微调标配** |

### 9.5 MNIST 迁移实验的教训

在 MNIST 上用预训练 ResNet-18 做特征提取（只训练 fc 层），结果只有 **96.13%**，反而低于从零训的小 CNN（**98.96%**）。

**原因**：预训练域（ImageNet：自然图像，狗/车/猫）和目标任务（MNIST：黑白手写数字）差异巨大。ResNet 冻结的 11M 卷积核学的是"检测狗毛、车轮纹理"——对 MNIST 的数字线条完全不对路。

**迁移学习的黄金法则**：**域越接近，效果越好。** 所以工业上迁移学习最常用的场景是：在 ImageNet 上预训练 → 在自己的"猫狗识别""质检缺陷检测"上微调。这些任务和自然图像接近，迁移效果显著。

```
CNN 架构：Conv（模式检测）→ MaxPool（下采样压缩）→ Flatten → Linear（分类决策）

正则化防过拟合：
  ├── Dropout：随机关神经元 → 隐式模型集成
  ├── L2：λ·Σw² → 大权重变小（标配 weight_decay）
  └── L1：λ·Σ|w| → 小权重变零（特征选择）

优化器进化：
  SGD（w -= lr·grad）→ Momentum（加惯性）→ Adam（自适应 lr + 动量）

ResNet：捷径连接输出 = F(x) + x
  → 梯度多一条高速公路 → 152 层也能训练

Batch Normalization：Conv → BN(γ,β) → ReLU
  → 训练更稳、收敛更快、可用更大 lr

实战：CNN MNIST（98.96%）> MLP（97.07%）> ResNet-18 迁移（96.13%）
  → 预训练域不匹配时，从零训更好

迁移学习：
  ├── 特征提取：冻结卷积，只训分类头（数据少 + 域接近时好用）
  ├── 全参数微调：所有层小 lr 更新（效果好但贵）
  └── LoRA：加小分支学偏移（大模型微调标配，CNN 用得少）
```

---

## 待探索问题

- [ ] 推理时 BN 怎么算均值和方差（训练时和推理时不同）？
- [ ] LayerNorm vs BatchNorm 的区别——为什么 Transformer 用 LN 而不是 BN？
- [ ] Transformer 里的残差连接和 ResNet 的有什么异同？
- [ ] 数据增强——transforms.Compose 里常见的旋转、裁切、翻转操作
- [ ] 用 CIFAR-10 跑一次从零训 vs 迁移学习的对比实验

---

> **复习建议**：先看"一句话串起来"唤醒记忆，然后重点攻克第七章 BN（没消化透的部分）。看完每个章节后遮住公式自己默写一遍，卡住的地方就是需要再理解的。
