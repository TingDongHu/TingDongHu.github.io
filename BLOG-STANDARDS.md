# 博客写作规范

> 给 AI 的 Prompt：写博客文章时请遵循以下规范。

## 文件结构

```
content/posts/
  llm/                  ← LLM / Agent / AI编程
  cpp/                  ← C++ 语言与设计模式
  computer-graphics/    ← 图形学 / 3D生成 / 3D视觉
  game-dev/             ← 虚幻引擎 / 游戏设计
  ml/                   ← 机器学习 / 深度学习 / ComfyUI
  algorithms/           ← 算法刷题
  dev-notes/            ← 博客搭建 / 杂项笔记
  essays/               ← 随笔
```

## 文件名

- 英文 kebab-case，如 `mcp-overview.md`、`unreal-gamemode-gamestate.md`
- 不要中文、空格、特殊字符

## Front Matter（YAML 格式）

```yaml
---
title: "【分类】文章标题"
date: 2026-07-20T00:00:00+08:00
categories: ["LLM"]
tags: ["LLM", "Agent", "MCP"]
description: "一句话摘要，用于 SEO 和首页卡片"
cover: "/img/封面图.png"
headerImage: "/img/Banner图.png"
math: true
---
```

### 分类对照

| 目录 | categories 值 |
|------|-------------|
| `llm/` | `["LLM"]` |
| `cpp/` | `["C++"]` |
| `computer-graphics/` | `["计算机图形学"]` |
| `game-dev/` | `["游戏开发"]` |
| `ml/` | `["机器学习"]` |
| `algorithms/` | `["算法刷题"]` |
| `dev-notes/` | `["开发工具"]` |
| `essays/` | `["随笔"]` |

### 标签规范

第一标签必须是对应领域标签（与 categories 一致），然后加 1-3 个技术标签：

| 领域 | 可用标签 |
|------|---------|
| LLM | agent, mcp, rag, transformer, prompt, function-calling, ai编程 |
| C++ | 面向对象, 设计模式, memory, 泛型, unreal-engine |
| 计算机图形学 | 渲染, 光线追踪, 光栅化, 着色, 纹理, 几何, 动画, games101, diffusion, 3d生成, openpcdet, 3d检测, point-cloud |
| 游戏开发 | unreal-engine, 游戏设计, 多人联机, 事件系统, 游戏模式 |
| 机器学习 | 深度学习, CNN, 梯度下降, 损失函数, 激活函数, diffusion, comfyui |
| 算法刷题 | 排序, 搜索, DP |
| 开发工具 | 博客搭建, 可计算理论 |
| 随笔 | 年度总结 |

## 图片

- 拖入 Typora 或粘贴截图，PicGo CLI 自动上传到 Cloudflare R2
- markdown 中自动生成 `![](https://pub-500a3a9e99b44ef29efa70fd87011d69.r2.dev/日期/md5.png)` 格式
- 不要使用本地相对路径引用图片

## 数学公式

- front matter 中设置 `math: true`
- 行内公式用 `$...$`
- 行间公式用 `$$...$$`

## 写作风格

- 正文用中文，代码和术语保持英文
- 不使用 emoji
- 有意义的命名，不缩写
- 复杂逻辑处加注释，不写废话注释
- 偏好函数式风格
