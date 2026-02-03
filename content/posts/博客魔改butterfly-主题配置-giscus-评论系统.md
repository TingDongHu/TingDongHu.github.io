--- 
title: 【博客魔改】Butterfly 主题配置 Giscus 评论系统
date: 2025-12-03T00:00:00+08:00
categories: ["Hexo博客"]
tags: ["blog", "Giscus", "hexo", "markdown", "GitHub", "Butterfly"]
description: "为Hexo的Butterfly主题配置Giscus评论系统，需先在GitHub创建公开仓库并启用Discussions，安装Giscus应用，获取配置代码后填入主题配置文件即可。"
cover: "/img/BlogMakeover.png"
headerImage: "/img/Raythy.png"
math: true
--- 

本文介绍了为Hexo博客的Butterfly主题配置Giscus评论系统的详细步骤。Giscus是一个基于GitHub Discussions的免费评论工具，无需自建服务器。配置过程主要包括：创建公开的GitHub仓库并启用Discussions功能，安装Giscus应用，最后在配置页面生成并获取必要的代码片段。 



> [!tip]
>
> 最近把很多老博客整理搬运到hexo上面的时候，突然发现自己的博客还没有配置评论系统，刚好前两天刷到一个Giscus官方教程，个人用了也觉得确实是很好用，索性搬来配置到博客上去了，顺带水篇博客记录一下，方便后续主题修改后重新配置。

## Giscus简介

Giscus 是一个基于 GitHub Discussions 的评论系统，完全免费、无需服务器、数据存储在 GitHub 仓库中。本指南详细介绍如何为 Hexo Butterfly 主题配置 Giscus。

`Giscus` 使用 `GitHub Discussions` 作为数据库存储博客下面的评论。

`Giscus` 插件加载时，会使用 `GitHub Discussions` 搜索 API 根据选定的映射方式（如 URL、pathname、 等）来查找与当前页面关联的 discussion。如果找不到匹配的 `discussion`，`giscus bot` 就会在第一次有人留下评论或回应时自动创建一个 `discussion`。

如果要评论，访客必须按 `GitHub OAuth` 流程授权 `giscus app` 代表他发帖。或者访客也可以直接在 `GitHub Discussion` 里评论，作者可以在 `GitHub` 上管理评论。

## Giscus配置

### 第一步：创建 GitHub 仓库

1. 登录 GitHub，点击右上角 `+`→ `New repository`
2. 填写仓库信息：**Repository name**: 例如 `blog-comments`**Visibility**: 必须选择 **Public**（公开）
3. 点击 `Create repository`

### 第二步：启用 Discussions 功能

1. 进入仓库页面 → 点击 `Settings`选项卡
2. 左侧菜单选择 `General`
3. 向下滚动到 `Features`区域
4. 勾选 **Discussions** 复选框
5. 点击 `Save changes`

![image-20251203140248796](博客魔改butterfly-主题配置-giscus-评论系统/image-20251203140248796.png)



### 第三步：安装 Giscus App

1. 点击[这里](https://github.com/apps/giscus)访问 Giscus App 页面
2. 点击 `Install`
3. 选择 `Only select repositories`
4. 选择刚才创建的评论仓库
5. 完成授权

![image-20251203140303878](博客魔改butterfly-主题配置-giscus-评论系统/image-20251203140303878.png)

### 第四步：生成配置信息

1. 打开 Giscus 配置页[giscus](https://giscus.app/zh-CN)
2. 按以下配置选择：

- **Repository**✅: `你的用户名/你的仓库名`

- **映射方式**: ✅ Discussion 的标题包含页面的 `pathname`

- **Discussion分类**✅: `General`（或 `Announcements`）

- **功能设置**

  - 将 discussion 限制为每页一个

  - 启用懒加载，加速网页加载

  -  评论框位于 discussion 上方（可选）

### 第五步：获取配置值

配置工具会自动生成配置信息，，记得先不要关闭配置值的网页，记录下关键值，粘贴到hexo配置文件中：

```
repo: 用户名/仓库名
repo-id: R_xxxxxxxxxx
category: General
category-id: DIC_xxxxxxxxxx
```

## 配置 Butterfly 主题

编辑 Hexo 博客的 `_config.butterfly.yml`文件：

### 1. 启用 Giscus 评论系统

```yaml
comments:
  use: giscus
```

### 2. 填写 Giscus 配置

粘贴来上面Giscus主页配置生成的信息

```yaml
giscus:
  repo: 用户名/仓库名
  repo_id: R_xxxxxxxxxx
  category: General
  category_id: DIC_xxxxxxxxxx
  mapping: pathname
  strict: 0
  reactions_enabled: 1
  emit_metadata: 0
  input_position: bottom
  theme: preferred_color_scheme
  lang: zh-CN
  lazy_loading: true
```

## 测试与部署

依然是hexo三步走

```bash
hexo clean 
hexo g
hexo s
```

访问 `http://localhost:4000`测试评论功能。

![image-20251203140314672](博客魔改butterfly-主题配置-giscus-评论系统/image-20251203140314672.png)

上图所示模样即为配置成功。