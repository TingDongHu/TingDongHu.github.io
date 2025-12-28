--- 
title: 【OpenPCDet】关于spconv的一些问题解决方案
date: 2024-12-30T00:00:00+08:00
categories: ["3DComputerVison"]
tags: ["OpenPCDet", "环境配置"]
description: "在Ubuntu20.04与CUDA 11.3环境下改进OpenPCDet时，针对spconv模块的版本冲突、API变更及初始化错误，通过重装指定版本、修改导入语句和降级版本得以解决。"
cover: "/img/pointcloud.png"
headerImage: "/img/Makima.png"
math: true
--- 


最近在修改对OpenPCDet中一些算法做改进评估的时候碰到了一系列的和spconv模组相关的问题，找到了一些解决方法。
本人的服务器环境：
>操作系统版本：Ubuntu20.04
GPU：3090Ti
CUDA版本:11.3
Pytorch：1.8.1
Python:3.8

问题1：
>  File "/home/OpenPCDet/pcdet/utils/spconv_utils.py", line 4, in <module>
    if float(spconv.__version__[2:]) >= 2.2:
AttributeError: module 'spconv' has no attribute '__version__'
原本以为是版本过低的问题，查资料发现是安装了多个spconv版本
``` python
pip uninstall spconv-cu113
pip uninstall spconv
pip install spconv-cu113
```
测试版本：
```python
import spconv
print(spconv.__version__)
```

问题2：
> AttributeError: module 'spconv' has no attribute 'SparseModule'
研究后发现是spconv版本更新导致，在spconv2的使用中，mport spconv 要改写成 import spconv.pytorch as spconv

问题3：
> ImportError: generic_type: cannot initialize type "ExternalAllocator": an object with that name is already defined
解决方法：
降低版本
``` python
pip uninstall spconv-cu113
pip install spconv-cu102
```