---
title: "【深度学习】Day 1：PyTorch 基础——从线性回归到神经网络"
date: 2026-05-05T00:00:00+08:00
categories: ["机器学习"]
tags: ["机器学习", "深度学习", "PyTorch"]
description: "Tensor、自动求导、线性层、激活函数、Softmax、交叉熵——PyTorch 深度学习入门笔记"
cover: "/img/machinelearning.png"
headerImage: "/img/rthykless.png"
math: true
---


> 日期：2026-05-05
> 学习方式：苏格拉底式对话 + 代码实践
> 核心目标：理解自动求导与梯度下降的底层机制，并跑通第一个分类项目

---

## 一句话串起来

我从 Tensor 这个"数字集装箱"出发，理解了维度就是形状方括号里的数字个数；然后发现 `nn.Linear` 本质上是一排并行的线性回归——每个神经元有自己的 $w$ 和 $b$；接着意识到没有 ReLU 这样的激活函数，叠再多层也只等价于一层线性变换；通过链式法则明白反向传播就是沿着计算图往回走、每层乘上局部梯度；最后用 Softmax 把分数转概率、用交叉熵衡量预测与真实标签的差距，完成了第一个手写数字识别项目，测试准确率 97%。

---

## 第一章：Tensor——高维数据容器

### 1.1 张量是什么

张量（Tensor）是 PyTorch 的核心数据结构，是不管数据几维都能装的**通用化容器**。

| 阶数 | 名称 | 形状示例 | 类比 |
|------|------|---------|------|
| 0 阶 | 标量（scalar） | `[]` | 一个苹果 |
| 1 阶 | 向量（vector） | `[3]` | 一排苹果 |
| 2 阶 | 矩阵（matrix） | `[4, 3]` | 一板鸡蛋 |
| 3 阶 | 3 维张量 | `[4, 32, 32]` | 多板鸡蛋叠成一箱 |
| 4 阶 | 4 维张量 | `[8, 4, 32, 32]` | 多箱堆在一起 |

**关键理解**：张量不只是"多维数组"，它还携带了**计算图信息**（如何被计算出来的）和**梯度信息**（`requires_grad`）。

### 1.2 维度是怎么数的

**我当时的问题**："四维向量和四维矩阵是一个东西吗？4 层堆叠也算 4 维吗？"

**解答**：在 PyTorch 中，**维度 = 形状方括号里数字的个数**。


$$
[4, 32, 32] \text{ 是 3 维（3 个数字）}
$$



$$
[8, 4, 32, 32] \text{ 是 4 维（4 个数字）}
$$


你说的"4 层堆叠的矩阵"其实是 $[C, H, W]$ 的 **3 维**张量。深度学习中彩色图片通常表示为 $[B, C, H, W]$（批次 × 通道 × 高 × 宽）。

### 1.3 代码验证

```python
import torch
s = torch.tensor(42)              # 0维: shape=[]
v = torch.tensor([1, 2, 3])       # 1维: shape=[3]
m = torch.randn(4, 3)             # 2维: shape=[4, 3]
t = torch.randn(4, 32, 32)        # 3维: shape=[4, 32, 32]
b = torch.randn(8, 4, 32, 32)     # 4维: shape=[8, 4, 32, 32]

print(f"{s.ndim}维, {list(s.shape)}")
```

---

## 第二章：从线性回归到 nn.Linear

### 2.1 一元线性回归

最简单的线性模型：


$$
y = wx + b
$$


其中 $w$ 是权重（斜率），$b$ 是偏置（截距）。只有 **2 个可学习参数**。

### 2.2 多元线性回归

扩展到多个特征：


$$
y = w_1 x_1 + w_2 x_2 + \cdots + w_n x_n + b = w^T x + b
$$


矩阵形式（批量计算 m 个样本）：


$$
y_{pred} = Xw + b
$$


其中 $X$ 是 $m \times n$ 矩阵，$w$ 是 $n \times 1$ 向量，$b$ 是标量。

**关键**：$X @ w$ 一次性算出 m 个样本的预测值，**没有 for 循环**。向量化计算是深度学习的核心效率来源。

### 2.3 nn.Linear = 并行的线性回归

`nn.Linear(in_features, out_features)` 做的事情：


$$
y = xW^T + b
$$


**我的理解**：这其实就是 `out_features` 个神经元并排，每个神经元有自己的权重 $w$ 和偏置 $b$。

```
神经元1: h1 = w11*x1 + w12*x2 + b1    ← 自己的 w 和 b
神经元2: h2 = w21*x1 + w22*x2 + b2
...
神经元10: h10 = w101*x1 + w102*x2 + b10
```

`nn.Linear(2, 10)` = 10 个神经元 = 2×10 个权重 + 10 个偏置 = **30 个可学习参数**

**我当时的问题**："nn.Linear(2, 10) 里面的数代表什么？30 个常数是通过拟合算出来的吗？"

**解答**：2 是输入特征数，10 是输出神经元数。参数量 = 输入×输出 + 输出（偏置）= 2×10 + 10 = 30。**对，训练就是通过反向传播调整这 30 个参数，让预测越来越准。**

### 2.4 中间层的"不可解释性"

中间层的输出（比如那 10 个隐藏特征）**人类不一定能解释**每个神经元代表什么——它们是网络自己学出来的中间表示。这和生物神经网络很像：单个神经元只能做简单的信号映射，但通过大量堆叠就能涌现复杂能力，这是深度学习"黑箱"问题的来源。

```python
import torch.nn as nn
layer = nn.Linear(2, 10)
print(f"权重: {layer.weight.shape}")  # [10, 2]
print(f"偏置: {layer.bias.shape}")    # [10]
```

---

## 第三章：损失函数的本质

### 3.1 损失就是一个函数

**误解**：损失函数是某种特殊机制。

**正解**：损失函数和你写的任何函数没有区别，只是：
1. 输入是（预测值，真实值）
2. 输出是一个 **标量**（一个数字）
3. 必须 **可导**（才能 `backward()`）

### 3.2 MSE 损失函数的推导

均方误差（Mean Squared Error）：


$$
L = \frac{1}{n} \sum_{i=1}^{n} (y_{pred}^{(i)} - y_{true}^{(i)})^2
$$


**为什么用平方而不是绝对值？**

| 特性 | 平方 | 绝对值 |
|------|------|--------|
| 可导性 | 处处可导 | 在 0 处不可导 |
| 对大误差的惩罚 | 更重（平方放大） | 线性 |
| 梯度 | 连续变化 | 在 0 处突变 |

**对单个样本求偏导**：

$$
L = (y_{pred} - y_{true})^2\\[4pt]
\frac{\partial L}{\partial y_{pred}} = 2(y_{pred} - y_{true})
$$


**关键观察**：
- 当 $y_{pred} > y_{true}$（预测偏大），$\partial L / \partial y_{pred} > 0$
- 当 $y_{pred} < y_{true}$（预测偏小），$\partial L / \partial y_{pred} < 0$
- 当 $y_{pred} = y_{true}$（完美预测），$\partial L / \partial y_{pred} = 0$

梯度自动告诉我们"预测值该往哪调"。

### 3.3 损失函数与模型参数的关系

损失函数不只是 $y_{pred}$ 的函数，更是**模型参数**的函数：

$$
L(w, b) = (wx + b - y_{true})^2\\[4pt]
\frac{\partial L}{\partial w} = 2(wx + b - y_{true}) \cdot x = 2(y_{pred} - y_{true}) \cdot x\\[4pt]
\frac{\partial L}{\partial b} = 2(wx + b - y_{true}) \cdot 1 = 2(y_{pred} - y_{true})
$$

因为链式法则。$y_{pred} = wx + b$，所以 $\partial y_{pred} / \partial w = x$（$w$ 变化 1 单位，$y_{pred}$ 变化 $x$ 单位），而 $\partial y_{pred} / \partial b = 1$（$b$ 变化 1 单位，$y_{pred}$ 变化 1 单位）。由链式法则：

$$
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y_{pred}} \cdot \frac{\partial y_{pred}}{\partial w} = 2(y_{pred} - y_{true}) \cdot x\\[4pt]
\frac{\partial L}{\partial b} = \frac{\partial L}{\partial y_{pred}} \cdot \frac{\partial y_{pred}}{\partial b} = 2(y_{pred} - y_{true}) \cdot 1
$$


---

## 第四章：ReLU 与非线性激活函数

### 4.1 定义


$$
\text{ReLU}(x) = \max(0, x)
$$


把负数变成 0，正数保留不变。**不需要参数**——它只是一个数学函数，没有可学习的权重。

### 4.2 为什么必须要有激活函数？

多层线性层可以合并：


$$
W_2 @ (W_1 @ x + b_1) + b_2 = (W_2 W_1) @ x + (W_2 b_1 + b_2)
$$


**数学结论：N 层线性层等价于 1 层线性层**。没有激活函数，网络表达能力不会随层数增加。

ReLU 的"砍负数"操作破坏了线性，每一层不再等价于一个简单的矩阵乘法，网络才能表达复杂的非线性关系。**这就是"深度"的意义所在。**

### 4.3 与生物神经元的联系

- 生物神经元：树突接收信号 → 超过阈值才放电
- 人工神经元：$W^T x + b$ → ReLU（>0 才输出，<0 就沉默）

单个神经元极其简单，大规模堆叠就能涌现复杂能力——"不可解释性"正来源于此。

```python
import torch
x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
relu_output = torch.where(x > 0, x, 0)
print(relu_output)  # [0, 0, 0, 1, 2]
```

---

## 第五章：反向传播与链式法则

### 5.1 链式法则

复合函数求导：

若 $z = f(y)$, $y = g(x)$，则：


$$
\frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx}
$$


多维扩展：

若 $L = f(y_1, y_2, ..., y_n)$，且每个 $y_i = g_i(x)$，则：


$$
\frac{\partial L}{\partial x} = \sum_{i} \frac{\partial L}{\partial y_i} \cdot \frac{\partial y_i}{\partial x}
$$


**从 loss 往回，每经过一层就乘上该层的局部梯度。**

### 5.2 计算图上的反向传播

以前向运算链为例：

```
输入 x → (x+1) → a → (a²) → b → sin(b) → loss
```

计算 `loss.backward()` 时，PyTorch 从 loss 出发往回走：

$$
\frac{\partial loss}{\partial b} = \cos(b) \quad \text{(Sin 的求导规则)}\\[4pt]
\frac{\partial loss}{\partial a} = \frac{\partial loss}{\partial b} \cdot \frac{\partial b}{\partial a} = \cos(b) \cdot 2a \quad \text{(链式法则)}\\[4pt]
\frac{\partial loss}{\partial x} = \frac{\partial loss}{\partial a} \cdot \frac{\partial a}{\partial x} = \cos(b) \cdot 2a \cdot 1
$$


### 5.3 梯度累加机制（重要！）

**我当时的问题**："Pytorch 在背后是维护一张表把运算改为查询吗？"

**解答**：不是查表。PyTorch 建了一张**动态计算图**——前向时记录运算顺序，反向时顺着图往回走，每步调用运算的求导规则。

**PyTorch 的梯度默认是累加的，不是覆盖的**。每次调用 `.backward()` 梯度会加到已有值上。这是因为有时需要累积多个损失的梯度（如多任务学习），或分批计算。但这也意味着**必须在每次参数更新后手动清零**：`optimizer.zero_grad()`。

### 5.4 矩阵形式的梯度（多元线性回归）


$$
\frac{\partial L}{\partial w} = \frac{2}{m} X^T(Xw + b - y)
$$


维度验证：$X$ 是 $(m,n)$，$w$ 是 $(n,1)$，$y$ 是 $(m,1)$，$X^T(Xw - y)$ 是 $(n,m)@(m,1) = (n,1) = w$ 的形状 ✓

```python
import torch
x = torch.tensor(2.0, requires_grad=True)
a = x + 1              # dz/dx = 1
b = a ** 2             # dy/dz = 2z, z=3 → 6
loss = b.sin()         # dloss/dy = cos(y), y=9 → cos(9)

loss.backward()        # dloss/dx = cos(9) * 6 * 1
print(x.grad)          # 6*cos(9) ≈ -5.46
```

---

## 第六章：梯度下降——盲人下山

### 6.1 核心思想

想象你站在山上，蒙着眼睛，目标是走到山谷最低点。你唯一能做的是：
1. **用脚感受坡度**（计算梯度）
2. **往坡度的反方向迈一步**（更新参数）
3. **重复**（迭代）

### 6.2 更新公式推导

梯度 $\nabla L(w)$ 指向 $L$ **增长最快**的方向。

因此 $L$ **下降最快**的方向是 $-\nabla L(w)$。


$$
w_{new} = w_{old} - lr \cdot \nabla L(w_{old})
$$


**符号分析**：

| 场景 | 梯度符号 | 更新方向 | 效果 |
|------|---------|---------|------|
| $y_{pred} > y_{true}$（预测偏大） | $\nabla L > 0$ | $w$ 减小 | 预测值降低 |
| $y_{pred} < y_{true}$（预测偏小） | $\nabla L < 0$ | $w$ 增大 | 预测值升高 |
| $y_{pred} = y_{true}$（完美） | $\nabla L = 0$ | $w$ 不变 | 已收敛 |

### 6.3 学习率的影响

学习率 $lr$ 控制每一步迈多大：

- **太大**：在谷底两侧震荡，甚至发散
- **太小**：收敛极慢，可能卡在平台
- **合适**：平滑到达谷底（典型值 0.001 ~ 0.01）

### 6.4 三种梯度下降模式

| 方法 | 每次用多少数据 | 优点 | 缺点 |
|------|--------------|------|------|
| **BGD（批量）** | 全部样本 | 梯度准确，稳定收敛 | 大数据时计算慢 |
| **SGD（随机）** | 1 个样本 | 计算快，噪声帮助跳出局部最优 | 梯度噪声大，震荡 |
| **Mini-batch** | m 个样本（如 64） | 平衡两者 | **最常用** |

PyTorch 的 `DataLoader` 默认就是 Mini-batch。

### 6.5 解析解 vs 梯度下降

多元线性回归可以有解析解（正规方程）：


$$
w^* = (X^T X)^{-1} X^T y
$$


但神经网络**没有解析解**，所以我们用梯度下降这把"牛刀"来练手，为后面做准备。

---

## 第七章：Softmax 与交叉熵

### 7.1 Softmax——分数转概率


$$
\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum_{j} e^{x_j}}
$$


把任意实数的分数（logits）转换成正的、总和为 1 的概率分布。

### 7.2 关键澄清：不会把负数归零

负数取指数 $e^{-2} \approx 0.135$，结果是一个**很小的正数**，不是 0。这和 ReLU 完全不同：

| 操作 | 负数变 0？ | 输出范围 | 输出总和 |
|------|-----------|---------|---------|
| ReLU | ✅ 是 | $[0, +\infty)$ | 不一定 |
| Softmax | ❌ 不是 | $(0, 1)$ | 一定是 1 |

### 7.3 CrossEntropyLoss

`CrossEntropyLoss` 内部已经包含 Softmax 操作（准确说是 `LogSoftmax` + `NLLLoss`），所以网络最后一层直接输出原始分数（logits）即可，**不需要手动加 Softmax**。

```python
import torch
scores = torch.tensor([-2.0, -1.0, 0.0, 1.0, 5.0])
prob = torch.softmax(scores, dim=0)
print(prob)        # [0.0009, 0.0024, 0.0066, 0.0178, 0.9723]
print(prob.sum())  # 1.0
```

---

## 第八章：完整项目——MNIST 手写数字识别

### 8.1 网络结构

```
输入 784 维（28×28 拉直）
    → Linear(784, 128) → ReLU       # 参数: 784×128 + 128 = 100,480
    → Linear(128, 64)  → ReLU       # 参数: 128×64 + 64 = 8,256
    → Linear(64, 10)                # 参数: 64×10 + 10 = 650
    → CrossEntropyLoss（内部包含 Softmax）
总参数量: 109,386
```

### 8.2 训练循环的 5 行核心代码

```python
outputs = model(images)              # 1. 前向传播：图片进网络，算出预测
loss = criterion(outputs, labels)    # 2. 算损失：预测 vs 真实标签的差距
optimizer.zero_grad()                # 3. 清空梯度：每轮梯度是累加的，要重置
loss.backward()                      # 4. 反向传播：顺着计算图算每个参数的梯度
optimizer.step()                     # 5. 更新参数：w = w - lr * dloss/dw
```

### 8.3 结果与分析

- **训练集准确率**：98.39%
- **测试集准确率**：97.07%
- **差距仅 1.3%**，没有明显过拟合

**我的发现**：小小全连接层也能做好视觉任务——因为 MNIST 是 28×28 灰度图，背景干净，数字规整，所以全连接就够了。但到了彩色图片（如 CIFAR-10），全连接会掉到约 40%，而卷积能到 75%+。

### 8.4 训练集 vs 测试集

MNIST 的数据是严格分开的：
- `train=True` → 读 `train-images-idx3-ubyte`（60000 张）
- `train=False` → 读 `t10k-images-idx3-ubyte`（10000 张，模型从未见过）

测试集上的 97% 准确率表明模型对陌生数据有良好的**泛化能力**。

---

## 第九章：误解澄清集

### 误解 1：梯度指向最优方向

**错误理解**：梯度指向 loss 最小的方向，所以沿着梯度走。

**正确理解**：梯度指向 **loss 增长最快** 的方向，最优方向是**反方向**。

$$
\nabla L(w) \text{ 指向 } L \text{ 增长最快的方向}\\
-\nabla L(w) \text{ 指向 } L \text{ 下降最快的方向}\\
w_{new} = w_{old} - lr \cdot \nabla L(w) \quad \text{减号是关键}
$$


### 误解 2：反向传播是"传误差"

**错误理解**：把误差 $(y_{pred} - y_{true})$ 传回去，让参数调整。

**正确理解**：传的是**偏导数**，通过链式法则自动计算。每个节点只关心"我收到上游的梯度，乘以我对输入的偏导，传给下游"。

### 误解 3：损失函数是特殊机制

**错误理解**：loss 是 PyTorch 内置的某种魔法。

**正确理解**：loss 就是一个**普通函数**，输出标量，必须可导。PyTorch 内置的 `MSELoss()` 和你手写的 `((y_pred - y_true)**2).mean()` 本质相同。

### 误解 4：收敛 = loss = 0

**正确理解**：收敛 = 梯度 ≈ 0 **且** loss 稳定。
- **loss 不变但梯度很大** → 学习率太大，在谷底震荡，不是收敛
- **梯度 ≈ 0 但 loss 很高** → 卡在局部最优或鞍点
- **梯度 ≈ 0 且 loss 稳定** → 真正的收敛

### 误解 5：参数初始化为 0 没问题

神经网络中，如果所有参数初始化为 0，**对称性破坏**会导致所有神经元学一样的东西——前向输出相同，反向梯度相同，参数永远同步，学不到任何东西。必须**随机初始化**打破对称性。

### 误解 6：梯度下降会陷入局部最优

- **线性回归**：损失函数是**凸函数**（碗状），只有一个全局最优
- **神经网络**：损失函数**非凸**，确实会陷入局部最优

缓解方法：随机初始化、学习率衰减、Momentum（惯性冲出浅坑）、Adam（自适应学习率）、SGD 的随机噪声。

---

## 第十章：知识关系图

```
Tensor（数据容器）
  → 维度 = shape 方括号里数字个数
  → nn.Linear（并行线性回归，每个神经元有自己的 w 和 b）
      → 激活函数 ReLU（砍负数，注入非线性）
          → 多层堆叠（没有 ReLU = 1 层，有了才能表达复杂模式）
              → 前向传播（算出预测）
                  → 损失函数（CrossEntropyLoss，内部含 Softmax）
                      → 反向传播（链式法则 + 计算图）
                          → 梯度下降（w_new = w_old - lr * dloss/dw）
                              → 评估泛化能力（测试集准确率）
```

---

## 工具备忘

```bash
conda activate pytorch           # 进入环境
jupyter notebook                 # 启动笔记本
```

Jupyter 单元格类型切换：`Y` = Code, `M` = Markdown, `R` = Raw
