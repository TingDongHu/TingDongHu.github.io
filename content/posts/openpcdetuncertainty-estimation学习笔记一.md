--- 
title: 【OpenPCDet】Uncertainty Estimation学习笔记（一）
date: 2024-11-30T00:00:00+08:00
categories: ["3DComputerVison"]
tags: ["CV", "自动驾驶", "目标检测"]
description: "神经网络不确定性研究旨在解决模型对错误或未知输入给出高置信度预测的问题。文章区分了数据不确定性和模型不确定性，并介绍了基于贝叶斯深度学习的建模方法，以帮助使用者做出更可靠的决策。"
cover: "/img/pointcloud.png"
headerImage: "/img/Makima.png"
math: true
--- 


## 为什么要研究uncertainty？
训练好的[神经网络模型本质是一个拥有大量确定参数的函数，不管你给什么输入，它都能给你一个输出。这会导致两种我们不愿意看到的意外情况：

- 对明明错误的预测结果，模型输出的[置信度]却很高
- 对没有见过的输入(OoD，Out-of-ditribution)，比如给一个识别猫/狗的模型输入一张桌子图片，模型一定会输出：”这是猫“ or “这是狗”，而不是告诉我们 “它似乎不是猫，也不是狗”

所以，我们希望模型能输出 uncertainty，辅助使用模型的人进行更好地决策。比如上面的例子中，我们希望对错误分类的样本、OoD样本，模型能够给出一个较高的uncertainty。

## uncertainy是什么？
参考NIPS2017年的论文 [What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision? ](https://link.zhihu.com/?target=https%3A//papers.nips.cc/paper/7141-what-uncertainties-do-we-need-in-bayesian-deep-learning-for-computer-vision.pdf)，Gal阐述了两种uncertainty：Aleatoric uncertainty(i.e. data uncertainty) 和 Epistemic uncertainty(i.e. model uncertainty)，即随机不确定度(也称数据不确定度)，和认知不确定度(也称模型不确定度)。

Epistemic uncertainty可以通过增加数据解决，比如下图：只有一个data point的时候，符合要求的模型有很多种可能，uncertainty很高。当数据点增加，模型逐渐确定，uncertainty减小。
![image](https://github.com/user-attachments/assets/82e8de7c-1ac8-4cbe-82c1-417cf2299c3c)

## How？怎么计算不确定度
### 1.Epistemic uncertainty建模
![image](https://github.com/user-attachments/assets/0a9ea3a7-f202-4c11-919d-b599aed777dd)
Monte-Carlo 和 Ensemble
对一个随机分布，不确定性建模的方法有很多，标准差、方差、风险值（VaR）和熵都是合适的度量。在深度学习中，建模不确定度需要用到Bayesian DeepLearning。从Bayesian的角度，深度学习训练的本质是求一个posterior distribution  $P(W|D)$ ，其中W是参数，D是数据。根据bayes theorem（贝叶斯定理），我们有 $P(W|D)=\frac{P(D|W)P(W)}{P(D)}$
但是这个公式没法用，因为 $P(D)$ 理论上代表的是真实的数据分布，无法获取; $P(W)$ 在神经网络中也是不存在的，因为模型训练好以后，所有参数都是确定的数，而不是distribution，没法计算 $P(W)$ 。于是我们想到bayes theorem的另一个公式: $P(D)=\sum_i{P(D|W_i)P(W_i)}$

如果我们知道所有W，那么就可以计算 $P(D)$了，但这也是不可能的。不过我们可以用[蒙特卡洛法](https://zhida.zhihu.com/search?content_id=125159798&content_type=Article&match_order=1&q=%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E6%B3%95&zhida_source=entity)(Monte-Carlo)多次采样逼近：多次采样W计算 $P_i (D)$ ，得到$P(D)$的近似分布，进而得到 $P(W|D)$ 的估计。具体来说，有3种方式：
- Ensembles方法
用类似[bootstrap](https://zhida.zhihu.com/search?content_id=125159798&content_type=Article&match_order=1&q=bootstrap&zhida_source=entity)的方法，对数据集D，采样N次，用N次的结果分别训练模型，然后ensemble模型结果。这个方法的好处是接近真实的Monte-Carlo方法
- MCDropout方法
在网络中加入Dropout层，在测试时也打开Dropout，让Dropout成为采样器。对采样N次的结果进行ensemble处理得到最后的uncertainty。这个方法的好处是不用做很多实验，节省成本，但是由于使用了Dropout，单次训练的时间会变长。
- MCDropConnect方法
和加Dropout的思路差不多。不过这里不用加Dropout layer，而是通过随机drop connection，来达到[随机采样](https://zhida.zhihu.com/search?content_id=125159798&content_type=Article&match_order=1&q=%E9%9A%8F%E6%9C%BA%E9%87%87%E6%A0%B7&zhida_source=entity)的目的。

从理论层面，MC-Dropout是variantianl inference(BNN的重要概念之一)的近似。
### 2.Aleatoric uncertainty建模
![image](https://github.com/user-attachments/assets/26f4bc29-6aa5-48ed-a355-4135aacc0571)
![image](https://github.com/user-attachments/assets/edf5f90d-81ac-44d1-8f1d-905a5fed4153)
有三种方式可以建模Aleatoric Uncertainty，这里介绍Probabilistic Deep Learning。从表格可以看出，其实就是在原始任务基础上，增加probability prediction，这个probability可用于measure uncertainty。
比如分类任务原来只输出类别，现在还需要输出probability。为了准确表示uncertainty，这里的probability要求[calibrated probability](https://link.zhihu.com/?target=https%3A//scikit-learn.org/stable/modules/calibration.html)，不能直接用用softmax输出的score。由此，对[目标检测](https://zhida.zhihu.com/search?content_id=125159798&content_type=Article&match_order=1&q=%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B&zhida_source=entity)任务也有[Probabilistic Object Detection](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1811.10800)。


参考博客：
https://zhuanlan.zhihu.com/p/166617220
https://proceedings.neurips.cc/paper/2017/hash/2650d6089a6d640c5e85b2b88265dc2b-Abstract.html
https://www.cs.ox.ac.uk/people/yarin.gal/website/thesis/thesis.pdf