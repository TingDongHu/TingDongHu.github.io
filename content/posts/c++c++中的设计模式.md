---
title: 【C++】C++中的设计模式
date: 2025-05-01T00:00:00+08:00
categories: ["C++"]
tags: ["语法", "c++", "设计模式", "编程内功"]
description: "设计模式是针对软件设计中常见问题的通用解决方案，核心在于提升代码复用性，避免重复造轮子。"
cover: "/img/cpp.png"
headerImage: "/img/pink.png"
math: true
---

设计模式是针对软件设计中反复出现问题的通用解决方案，其核心在于提升代码复用性，避免重复劳动。 

## 什么是设计模式

引用**克里斯托弗·亚历山大（Christopher Alexander）**在1977年的著作《**A Pattern Language: Towns, Buildings, Construction**》中提出了关于设计模式的经典定义。

**英文原版**：

> *"Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice."*
> — Christopher Alexander, *A Pattern Language*, 1977

**中文翻译**：

> “每一个模式描述了一个在我们环境中反复出现的问题，并描述了该问题解决方案的核心。通过这种方式，你可以无数次地使用该解决方案，而无需以相同的方式重复两次。”

说人话就是:`不需要重复造轮子`

推荐一本历史性著作《设计模式:可复用面相对象软件的基础》

![undefined](%E3%80%90C++%E3%80%91C++%E4%B8%AD%E7%9A%84%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B8%AD%E6%96%87%E7%89%88%E5%B0%81%E9%9D%A2.jpg)

> [!TIP]
>
>  设计模式的核心关键词: 复用