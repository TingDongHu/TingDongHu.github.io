---
title: "【深度学习】Day 3：Transformer——从注意力机制到 Encoder-Decoder"
date: 2026-05-08T00:00:00+08:00
categories: ["机器学习"]
tags: ["机器学习", "深度学习", "transformer"]
description: "自注意力机制、QKV、多头注意力、位置编码、LayerNorm、Encoder-Decoder 架构详解"
cover: "/img/machinelearning.png"
headerImage: "/img/rthykless.png"
math: true
---


> 日期：2026-05-08
> 学习方式：苏格拉底式对话 + 理论推导
> 核心目标：理解自注意力机制、多头注意力、位置编码、LayerNorm，以及 Transformer 的完整架构

---

## 一句话串起来

我从自注意力机制出发，理解了 QKV 三者的分工——Q（查询）问"我和谁有关系"，K（键）答"我有这些特征值得被关注"，V（值）说"我的实际信息内容在这里"，通过 $QK^T$ 算出所有词两两的相似度分数、softmax 转权重、加权 V 得到融合了上下文的新表示；然后学到多头注意力让 8 组独立的 QKV 并行计算、从不同角度理解句子；再理解位置编码（正弦函数）告诉模型词的顺序——因为 Transformer 一次性看到所有词，不像 RNN 一个字一个字读；接着学到 LayerNorm 对每个词向量的所有维度做标准化（和 BN 跨样本不同，LN 跨特征且不受序列长度影响），配合残差连接稳定训练；最后理解了 Encoder（编码器, 双向理解输入）和 Decoder（解码器, 逐词生成输出）各自由 N 个纵向堆叠的 Transformer Block 组成——每个 Block 里是"多头注意力 → 残差+LN → 前馈网络 → 残差+LN"的结构。

---

## 第一章：Transformer 整体架构

### 1.1 原始 Transformer（翻译任务）

```
输入: "I love deep learning"
    ↓
Encoder（6 个 Block 纵向堆叠）—— 理解输入
    ↓
Encoder 输出送到 Decoder 每一层（cross-attention）
    ↓
Decoder（6 个 Block 纵向堆叠）—— 逐词生成：
<start> → "我"
<start> 我 → "爱"
<start> 我 爱 → "深度"
...
```

### 1.2 现实中的变体

```
原始 Transformer：Encoder + Decoder（翻译）
BERT：只用 Encoder（理解任务：分类、情感分析、QA）
GPT：只用 Decoder（生成任务：对话、写文章、代码生成）
```

### 1.3 核心哲学

> CNN 手动设计了"只看局部邻居"这个归纳偏置，Transformer 不做任何假设——让模型自己从数据中学"谁和谁该有关系"。

---

## 第二章：Token——模型的最小处理单位

### 2.1 Token 是什么

Token 是介于"词"和"字"之间的切分单位，不是词也不是句子。

| 内容 | 中文词数 | Token 数 |
|------|---------|----------|
| "我爱深度学习" | 4 | ~4 |
| "I love deep learning" | 4 | 4 |
| "unbelievably" | 1 | **3**（un-believ-ably） |
| "😊" | 0 | **1** |

### 2.2 Token 计费

模型的上下文窗口有固定的最大 Token 数（如 GPT-4 有 128K），你输入的内容和模型输出的内容都按 Token 计费。

### 2.3 补齐（Padding）

不同长度的句子在同一个 batch 里需要补齐到一样长：

```
句子1: "我爱深度学习" → 5 个 token
句子2: "你好"         → 2 个 token → 补齐 ["你","好","<pad>","<pad>","<pad>"]

attention mask 告诉模型：忽略 <pad> 位置，不要算注意力。
```

---

## 第三章：Embedding——词到向量的映射

### 3.1 定义

Embedding 是一个可训练的查询表：给 token id，返回一个 $d_{model}$ 维的稠密向量。

```python
import torch.nn as nn

embedding = nn.Embedding(vocab_size=30000, d_model=512)
# 输入: token id（整数）
# 输出: [d_model] 维向量
```

### 3.2 训练得来，不是人为指定

```
初始化时：Embedding("猫") = [0.12, -0.34, 0.56, ...]  ← 随机
训练之后：Embedding("猫") = [0.89, 0.23, -0.45, ...]  ← 有语义

"猫"和"狗"经常出现在相似上下文（"我养了一只__"）
→ 它们的向量被拉到相近位置 → cos(猫, 狗) ≈ 0.8
→ 这完全是从语料库统计规律学出来的
```

### 3.3 我当时的问题

**Q：** "Embedding 是独立的模型吗？换一个 Embedding 模型，原来训练好的参数会不会白费？"

**A：** Embedding 层就是 Transformer 模型**内部的第一层**，和整个模型一起训练（端到端）。不存在"换 Embedding"这个操作——换掉等于切掉模型的一层，整个模型就废了。如果要换，你需要做的是用别人训练好的**完整预训练模型**（迁移学习），而不是只换 Embedding。

### 3.4 One-hot 编码 vs Embedding

| | One-hot（最早做法） | Embedding（现代做法） |
|---|---|---|
| 向量表示 | [1,0,0,0] 只有一个 1 | [0.12, -0.34, 0.56, ...] 稠密向量 |
| 维度 | 等于词表大小（10 万维） | 通常 512 或 768 维 |
| 语义关系 | 所有词正交，看不出相似度 | 相似词距离近 |
| 训练得来？ | 人工设置 | ✅ 端到端训练 |

---

## 第四章：位置编码（Positional Encoding）

### 4.1 为什么需要

```
CNN 看图片：像素天然有位置，卷积核滑窗自带位置信息
RNN 看句子：一个字一个字读进来，顺序隐含在"读"的过程中
Transformer：所有词同时输入 → 没有任何顺序信息
              不加位置编码，"我爱深度学习"和"学习深度爱我"对模型没区别

但语言本身依赖顺序：
"我打你" vs "你打我" → 词相同但意思完全相反
```

### 4.2 实现方式

用一组不同频率的正弦和余弦函数生成编码：

$$
PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{model}})
$$
$$
PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{model}})
$$

位置编码直接**加到**词向量上（不是拼接）：

```
词向量 [6, 512] + 位置编码 [6, 512] = [6, 512]
           ↑ 形状不变，但向量已带位置信息
```

### 4.3 我当时的问题

**Q：** "Mask 和位置编码有什么区别？"

**A：** 位置编码告诉模型"词在什么位置"，Mask 在训练时挡住未来的词不让偷看。你之前说的是 Mask（遮挡后面内容），不是位置编码。

---

## 第五章：自注意力机制（Self-Attention）

### 5.1 QKV 三者的角色

Q、K、V 都来自输入 $x$，通过三个不同的 Linear 层算出：

```python
Q = x @ W_q  # 查询 —— "我想关注别人什么特征"
K = x @ W_k  # 键 —— "我有什么特征值得被关注"
V = x @ W_v  # 值 —— "我的实际信息内容"
```

**打个比方——搜索引擎：**

```
Q = 你输入的关键词（"深度学习"）
K = 所有网页的标题（匹配关键词）
V = 网页的内容（实际提取的信息）
```

### 5.2 注意力公式

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

**分步拆解：**

```
1. Q @ K.T → 算所有词两两相似度分数 [seq_len, seq_len]
2. ÷ √d_k → 缩放，防止分数太大 softmax 后过于尖锐
3. softmax → 转成概率分布（和为1），每行是"当前词对其他词的关注度"
4. × V → 按注意力权重加权融合所有词的信息
```

### 5.3 形状追踪

```python
# 输入 x 假设是 "我爱深度学习"（6 个词，d_model=512）
# x: [6, 512]

# 三个不同的 Linear 层
Q = x @ W_q  # [6, 512]
K = x @ W_k  # [6, 512]
V = x @ W_v  # [6, 512]

# 注意力分数
scores = Q @ K.T            # [6, 512] @ [512, 6] = [6, 6]
scores = scores / (512**0.5)  # 缩放
weights = scores.softmax(dim=-1)  # [6, 6] 注意力权重
output = weights @ V        # [6, 6] @ [6, 512] = [6, 512]
```

**对角线理解**：$QK^T$ 矩阵中第 $i$ 行第 $j$ 列 = 第 $i$ 个词对第 $j$ 个词的相关分数。自己和自己总是最高（对角线）。

### 5.4 代码验证

```python
import torch
import torch.nn.functional as F

def attention(Q, K, V):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / (d_k ** 0.5)
    weights = F.softmax(scores, dim=-1)
    return weights @ V

# 验证形状
x = torch.randn(6, 512)
W_q = torch.randn(512, 512)
Q, K, V = x @ W_q, x @ W_q, x @ W_q
out = attention(Q, K, V)
print(out.shape)  # [6, 512] —— 输入输出形状不变
```

---

## 第六章：多头注意力（Multi-Head Attention）

### 6.1 为什么需要多个头？

每个头独立做 QKV → attention，从不同角度理解句子：

```
头1：关注语法关系（主谓宾）
头2：关注语义关系（实体之间的关联）
头3：关注位置关系（哪个词修饰哪个词）
...

8 个头各有所长，信息互相补充
```

### 6.2 实现方式

```python
# BERT-base: 12 个头，每个头 64 维，12×64=768
# GPT-3:    96 个头

# 每个头有自己的 W_q, W_k, W_v（完全独立）
head_0: W_q_0, W_k_0, W_v_0
head_1: W_q_1, W_k_1, W_v_1
...
head_7: W_q_7, W_k_7, W_v_7

# 8 个头并行算 attention
输出0 = attention(x @ W_q_0, x @ W_k_0, x @ W_v_0)  # [6, 64]
输出1 = attention(x @ W_q_1, x @ W_k_1, x @ W_v_1)  # [6, 64]
...
# 拼起来，再经过一个 Linear 映射回 d_model
output = concat([输出0, 输出1, ...]) @ W_o  # [6, 512]
```

### 6.3 参数量估算

```python
# BERT-base 的注意力参数：
12 层 × 12 个头 × 3 组(W_q, W_k, W_v) = 432 个权重矩阵
# 每层还有 MLP 的其他权重
```

---

## 第七章：Transformer Block——基本单元

### 7.1 结构总览

一个 Block = 注意力 + 前馈网络 + 残差连接 + LayerNorm

```
输入 x [seq_len, d_model]
    │
    ├── 多头注意力（8个头并行 QKV→attention）
    ├── (+) 残差连接（输出 = attention(x) + x）
    ├── LayerNorm
    │
    ├── 前馈网络 FFN（Linear → ReLU → Linear）
    ├── (+) 残差连接
    └── LayerNorm
          │
          输出 [seq_len, d_model]（形状不变）
```

### 7.2 前馈网络（FFN）

就是两层全连接，你已经写熟的操作：

```python
# BERT-base: 768 → 3072 → 768
FFN(x) = Linear(768, 3072) → ReLU → Linear(3072, 768)
```

和 Day 1 的 `Linear(784, 128) → ReLU → Linear(128, 10)` 原理完全一样。

### 7.3 残差连接

和你学的 ResNet 完全相同：

```python
# ResNet：输出 = Conv(x) + x
# Transformer：输出 = Attention(x) + x
```

保证梯度多一条"高速公路"，防止深层梯度消失。

### 7.4 Transformer Block vs Encoder/Decoder

```
Block = 砖（多头注意力 + FFN + LN + 残差）
Encoder = N 块砖纵向堆叠（双向注意力）
Decoder = N 块砖纵向堆叠（掩码注意力 + cross-attention）

原始 Transformer：Encoder 6 层 + Decoder 6 层
BERT：Encoder 12 层（仅 Encoder）
GPT：Decoder 12 层（仅 Decoder）
```

---

## 第八章：LayerNorm

### 8.1 定义

LayerNorm 对**单个样本内部**的所有特征维度做标准化：

```python
# 对于形状 [seq_len=6, d_model=512] 的输入
# LN 对每个位置（每个词）的 512 维独立做标准化
# 每个词算自己的 μ 和 σ
```

$$
\mu = \frac{1}{d}\sum_{i=1}^{d} x_i \quad\quad \sigma^2 = \frac{1}{d}\sum_{i=1}^{d} (x_i - \mu)^2
$$
$$
\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \quad\quad y = \gamma \cdot \hat{x} + \beta
$$

### 8.2 BN vs LN（关键区别）

| | BN | LN |
|---|---|---|
| 统计量范围 | 跨样本，同通道 | 单样本，跨所有特征 |
| 标准化对象 | 一个 batch 某通道所有值 | 每个样本内部所有维度 |
| 受序列长度影响？ | ✅ 会（padding 干扰 μ,σ） | ❌ 不受影响 |
| 训练/推理行为 | 不同（需维护全局 μ,σ） | 一致（当场算） |
| 适合场景 | CNN（图片 batch 固定） | NLP/T（序列变长） |

### 8.3 我当时的疑问

**Q：** "不同长度的句子进来，LN 需要补齐吗？"

**A：** 补齐不是在 LN 做的，是在输入阶段统一补齐到 batch 最长长度。LN 只关心每个词向量内部的 512 个数值——不管序列里有 1 个还是 1000 个 token，每个 token 独立算自己的 μ 和 σ。LN 自适应序列长度。

**Q：** "LN 做的事情是什么？"

**A：** 随着模型加深，词向量的数值可能变得很大（150.3, -200.1...），分布不均匀。LN 把它们拉回 0 附近、方差为 1，让下一层训练更稳定。做完 LN 后数值看起来像标准正态分布，但本质只是 z-score 标准化，不是假设数据服从正态分布。

---

## 第九章：完整前向流程

### 9.1 形状全程追踪

```
输入: "我爱深度学习" → 6 个 token

1. Tokenizer: ["我","爱","深","度","学","习"] → token ids [6]

2. Embedding: [6] → [6, 512]

3. + 位置编码: [6, 512]（形状不变）

4. × N 个 Transformer Block:
   每个 Block 内部：
   输入 [6, 512]
   → 多头注意力 → [6, 512]
   → + 残差 → [6, 512]
   → LN → [6, 512]
   → FFN → [6, 512]
   → + 残差 → [6, 512]
   → LN → [6, 512]
   输出 [6, 512]（形状不变，数值变了）

5. 输出层: Linear(512, 30000) → [6, 30000]
   softmax → 每个位置预测下一个词的概率
```

### 9.2 关键观察

**Transformer Block 的输入输出形状永远不变**——无论经过多少层，`[seq_len, d_model]` 保持固定。变化的只是向量内部的数值，因为每个词不断融合上下文信息。这在工程上称为**残差流（residual stream）**——信息在固定维度的通道里流动。

---

## 知识关系图

```
输入文本
  → Tokenizer（分词为 token）
    → Embedding（查表得到向量 [seq_len, d_model]）
      → + 位置编码（正弦函数，告诉模型词序）

        ↓ 重复 N 次（纵向堆叠）
    ┌──────────────────────────────────────┐
    │ Transformer Block                    │
    │  多头注意力（8头并行 QKV→attention）   │
    │  → 残差连接 → LayerNorm               │
    │  → 前馈网络（Linear→ReLU→Linear）      │
    │  → 残差连接 → LayerNorm               │
    └──────────────────────────────────────┘
        ↓

Encoder（双向注意力）→ 理解输入
Decoder（掩码注意力）→ 逐词生成

输出 → Linear → softmax → 预测词概率
```

---

## 待探索问题

- [ ] 动手写一个完整的注意力机制代码，验证形状变化
- [ ] GPT 的因果掩码（causal mask）具体怎么实现"看不到未来"？
- [ ] BERT 的 Encoder 怎么用 [CLS] token 做分类？
- [ ] Transformer 训练时的 Teacher Forcing 是什么？
- [ ] 视觉 Transformer（ViT）怎么把图片变成"词"输入 Transformer？

---

## 附录：类比速查表

| Transformer 组件 | 类比 | 你什么时候学过 |
|---|---|---|
| 注意力 | 搜索引荐（Q=关键词, K=标题, V=内容） | ✅ 今天 |
| 多头注意力 | 同时看热搜/朋友圈/新闻，多角度获取信息 | ✅ 今天 |
| 残差连接 | 梯度的高速公路（ResNet） | ✅ Day 2 ResNet |
| LayerNorm | 每个词向量做标准化（类似 BN 但跨特征） | ✅ 今天 |
| 前馈网络 | 两层全连接（Linear→ReLU→Linear） | ✅ Day 1 |
| 位置编码 | 给每个词标序号，告诉模型顺序 | ✅ 今天 |
| Embedding | 可训练的查词表，语义相近的词向量相近 | ✅ 今天 |
| Token | "unbelievably" = un + believ + ably（比词小） | ✅ 今天 |

---

> **复习建议**：先看"一句话串起来"唤醒记忆，然后用附录速查表确认每个组件你对应的前置知识。特别留意 BN vs LN 的区别——这两个名字像但标准化维度完全不同，面试常考。最后对照知识关系图，遮住下半部分自己默写完整前向流程。
