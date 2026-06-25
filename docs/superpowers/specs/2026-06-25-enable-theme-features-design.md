# 设计文档:启用 Dream 主题内置功能(子项目 A)

- 日期:2026-06-25
- 状态:已确认,待实施
- 所属:博客优化计划的第 1 个子项目(总顺序 A → D → B → C)

## 背景与目的

本博客是作者**自用的远程复习工具**,核心诉求是「好查、好读」,而非面向读者的运营/互动。本子项目只做一件事:把 Dream 主题 v3.13.0 **已经内置、但当前未启用**的功能打开。全部改动为配置与少量内容文件,不触碰主题源码,不引入外部服务。

定位带来的取舍:不做评论、不做统计分析、不做分享按钮(YAGNI)。

## 关键事实(实施前已核实)

1. 主题导航栏由 `themes/dream-3.13.0/layouts/partials/nav.html` 中硬编码的列表驱动:
   `["about", "search", "rss", "posts", "categories", "tags"]`,可用 `reorderNavItems` 参数重排。
2. **`hugo.toml` 当前的 `[menu]` 块被该主题完全忽略**(主题不读 `site.Menus`)。现在能看到 posts/categories/tags 仅因它们在上述默认列表中。
3. 搜索图标(`renderNavItem.html`)的出现条件是:存在 `Type=search` 的页面。
4. RSS 图标的出现条件是:`site.Params.rss` 为真(feed `index.xml` 本就由 Hugo 默认生成)。
5. 搜索页模板 `layouts/section/search.html` 使用 Fuse.js,在构建时把文章数据内联进页面,**无需配置 `outputs` 或额外 JSON 索引**。
6. 主题原生不支持 giscus(仅支持 disqus/utterances/valine/waline/twikoo)。因评论功能已移出范围,本子项目不涉及。

## 范围

### 包含
1. 在 `hugo.toml` 启用一组零风险显示开关。
2. 新建 `content/search/_index.md` 以激活站内搜索页与导航搜索图标。
3. 删除 `hugo.toml` 中失效的 `[menu]` 块。

### 不包含
- 评论系统(已讨论后移除)。
- 统计分析、社交分享、SEO 结构化数据。
- 主题源码修改。
- 其他子项目(D 工程清理 / B 图片瘦身 / C 内容重组)。

## 详细改动

### 改动 1:启用显示开关(`hugo.toml`,`[params]` 下新增)

```toml
showTableOfContents = true   # 长文目录,复习时快速跳转
imageZoomableInPost  = true  # 文章内图片点击放大(信息图/截图多)
showPrevNextPost     = true  # 上一篇/下一篇导航
stickyNav            = true  # 导航栏滚动吸顶
rss                  = true  # 显示导航栏 RSS 图标(feed 已自动生成)
```

每项对应一个已验证存在的主题参数(来源:`themes/dream-3.13.0/hugo.example.toml` 与对应 partial)。

### 改动 2:激活搜索

新建文件 `content/search/_index.md`,提供最小 front matter 以生成一个 `Type=search` 的 section 页面:

```yaml
---
title: 搜索
layout: search
---
```

效果:
- 生成 `/search/` 页面,使用主题的 Fuse.js 前端搜索;
- 导航栏与移动端菜单自动出现搜索图标(满足 `renderNavItem.html` 的出现条件)。

> 注:`content` 已通过 `[module]` 挂载到 `static`,新建 section 不影响现有文章图片路径。

### 改动 3:删除失效的 `[menu]` 块

从 `hugo.toml` 移除整个 `[menu]`(含 `[[menu.main]]` 各项)。该块被主题忽略,删除不改变现有导航表现(posts/categories/tags 仍由主题默认列表渲染),只是消除误导性死配置。保留 `[taxonomies]` 不动。

不新增 `reorderNavItems`——默认顺序 `about, search, rss, posts, categories, tags` 已满足需求(about 因无 `/about` 页而不显示)。

## 验证方式

1. 本地 `hugo server -D`,打开 http://localhost:1313:
   - 导航栏出现 **搜索** 与 **RSS** 图标;
   - 打开任一长文,显示 **目录(TOC)** 与 **上一篇/下一篇**;
   - 文章内图片可点击 **放大**;
   - 页面下滑时导航 **吸顶**。
2. 访问 `/search/`,输入关键词能搜到文章标题并跳转。
3. `hugo`(生产构建)无报错、无新增 deprecation 警告。
4. 移动端视图(窄屏)菜单中同样出现搜索项。

## 风险与回滚

- 风险等级:低。全部为配置/内容文件改动,不动主题源码。
- 回滚:删除新增的参数行与 `content/search/_index.md` 即可恢复原状;`[menu]` 块如需找回可从 git 历史取回(但其本就无效)。

## 后续子项目(本文档不实施)

- **D**:工程清理 —— 删 `temp_replace.py`、给 `compress_images.py` 加 `--dry-run` 与修嵌套目录链接同步。
- **B**:图片瘦身 —— 降压缩阈值、引入 WebP、加安全保护。
- **C**:用 series 重组 3dgenai 系列(52 篇),服务快速复习查找。
