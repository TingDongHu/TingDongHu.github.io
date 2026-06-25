# 设计文档:阅读排版重做 + TOC sticky(子项目 F)

- 日期:2026-06-25
- 状态:已确认,待实施
- 所属:博客样式优化的子项目 F(样式问题清单第 2、1 项)

## 背景与目的

博客自用复习,诉求"读起来爽":正文够宽、信息密度高、目录可随时跳转。当前问题:

1. **#2 正文窄、左右空白大、密度低**:双重变窄 ——(a)`prose` 锁 `max-width:65ch`;(b)主题 `single.html` 用 `lg:grid-cols-4`,首列是空广告位,文章只占 `col-span-2`(≈50%)。且 `prose` 默认行高/标题尺寸/段距偏大。
2. **#1 目录不跟随滚动**:主题已有 scrollspy(`tocHighlighter()` + `@scroll.window`),但 TOC 容器无 `sticky`,滚过即消失。

## 关键事实(已核实)

- 文章容器:`<article class="mx-auto prose prose-quoteless dark:prose-invert" id="dream-single-post-main">`;正文 section `id="dream-single-post-content"`。
- `prose` 在 `output.min.css` 中含 `max-width:65ch`。
- `single.html` 主区结构:`<div class="lg:grid lg:grid-cols-4 gap-4 mt-4 px-4">` → 列1 空广告占位(`hidden lg:block`)、列2-3 文章(`lg:col-span-2`)、列4 TOC(`hidden lg:flex lg:flex-col lg:items-end lg:self-start`,**无 sticky**)。
- 两个 custom.css 均加载:`assets/css/custom.css`(编入 output.css)与 `static/css/custom.css`(head.html 第 66 行直接加载,**最后加载、层叠取胜**)。两者都含死的 `.dream-article`/`.ui.container` 选择器(旧主题遗留),对当前 `.prose` 标记无效。
- `static/css/custom.css` 第 1–130 行是**活的**代码块 Mac 样式(`.highlight`/One Dark);第 132–182 行是死的布局段。

## 范围

### 包含
1. 覆盖 `layouts/_default/single.html`:改网格拓宽正文 + 给 TOC 加 sticky。
2. 重写 `static/css/custom.css` 第 132–182 行死布局段为正确的 `.prose` 紧凑排版规则。
3. 删除 `assets/css/custom.css` 中死的 `.dream-article` 布局段。
4. 实施后在本地 `hugo server` 实时微调密度数值。

### 不包含
- 代码块方案(#3,子项目 G);`static/css/custom.css` 第 1–130 行代码块样式**不动**。
- 其余样式清单项(标签 #6、about #7)。
- 不修改 `themes/dream-3.13.0/` 源码(仅在 `layouts/` 覆盖)。

## 详细设计

### 组件 1:覆盖 `layouts/_default/single.html`

复制主题 `single.html` 全文到 `layouts/_default/single.html`,仅改两处,其余逐字保留:

**1a. 主区网格** —— 将:
```
<div class="lg:grid lg:grid-cols-4 gap-4 mt-4 px-4">
  <div class="hidden lg:block"> ...空广告占位... </div>
  <div class="lg:col-span-2">
    <article ...>
```
改为(去掉空广告列,文章吃主区,TOC 16rem 右栏):
```
<div class="lg:grid lg:grid-cols-[1fr_16rem] lg:gap-8 mt-4 px-4">
  <div class="min-w-0">
    <article ...>
```
(删除原首个空 `<div class="hidden lg:block">…adsense…</div>`;文章外层 `lg:col-span-2` 改为 `min-w-0` 以允许收缩并防止代码块溢出撑破网格。)

**1b. TOC 容器加 sticky** —— 将:
```
<div
  x-data="tocHighlighter()"
  @scroll.window="debouncedScroll"
  class="hidden lg:flex lg:flex-col lg:items-end lg:self-start"
>
```
改为:
```
<div
  x-data="tocHighlighter()"
  @scroll.window="debouncedScroll"
  class="hidden lg:flex lg:flex-col lg:self-start lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto"
>
```
(加 `lg:sticky lg:top-4` 跟随滚动;`max-h`+`overflow-y-auto` 防长目录超屏;去掉 `lg:items-end` 让目录左对齐更易读。)

### 组件 2:紧凑排版 CSS(`static/css/custom.css`)

将第 132–182 行(`Hugo Dream Theme - Layout & Width Optimization` 整段死代码,含 `.dream-article` 与末尾 `.highlight` 宽度补丁)替换为针对 `.prose` 的紧凑规则。初始预设值(实施后本地微调):

```css
/* ==========================================================================
   正文排版:解除 prose 65ch 限制 + 紧凑高密度(子项目F)
   ========================================================================== */
#dream-single-post-main.prose {
    max-width: 100%;   /* 宽度交给网格列控制 */
}
#dream-single-post-content {
    font-size: 16px;
    line-height: 1.6;
}
/* 标题:缩小 + 收紧间距 */
#dream-single-post-content h1 { font-size: 1.7rem; margin: 1.1em 0 .5em; line-height: 1.3; }
#dream-single-post-content h2 { font-size: 1.4rem; margin: 1.0em 0 .45em; line-height: 1.3; }
#dream-single-post-content h3 { font-size: 1.2rem; margin: .9em 0 .4em; }
#dream-single-post-content h4 { font-size: 1.05rem; margin: .8em 0 .35em; }
/* 段落/列表/引用:压缩间距 */
#dream-single-post-content p,
#dream-single-post-content li { margin-top: .4em; margin-bottom: .4em; }
#dream-single-post-content ul,
#dream-single-post-content ol { margin-top: .5em; margin-bottom: .5em; }
#dream-single-post-content blockquote { margin: .8em 0; }
/* 图片:居中 + 适度上下间距 */
#dream-single-post-content img { margin: 1em auto; }
```

- 用 `#dream-single-post-content` ID 选择器提升特异性,压过 `.prose` 默认值(必要时个别加 `!important`,实施时按需)。
- 代码块样式(第 1–130 行)保持不动。

### 组件 3:清死代码

删除 `assets/css/custom.css` 中针对 `.dream-article` / `.ui.container.dream-article` 的死布局段(该文件其余若有有效内容则保留)。

## 验证方式

1. `hugo` 构建无 ERROR、无**新增** deprecation 警告(已知主题 `baseof.html` 的 `site.LanguageCode` 警告为既有,不在本项目范围)。
2. 本地 `hugo server -D` 打开任一长文(如 games101 几何篇):
   - 正文明显变宽(占主区 ~75%,非原 50%);
   - 行距/标题/段距更紧凑,信息密度提升;
   - 右侧 TOC **随页面滚动保持可见**,点击章节跳转,当前章节高亮(scrollspy);
   - 长目录超出视口时 TOC 内部可滚动。
3. 窄屏(<lg)布局回退正常:TOC 隐藏,正文单列全宽,无横向溢出。
4. 代码块外观与改动前一致(未被波及)。

## 风险与回滚

- 风险:中低。`single.html` 覆盖是新增文件,删除即回退主题原版;CSS 改动局限于 prose/布局段。
- 主要风险点:网格 `grid-cols-[1fr_16rem]` 任意值在极宽/极窄屏的表现 —— 由本地实时微调覆盖。
- `min-w-0` 用于防止代码块/长表格撑破网格列(Tailwind grid 子项默认 `min-width:auto` 会溢出)。
- 回滚:删 `layouts/_default/single.html`;还原 `static/css/custom.css` 与 `assets/css/custom.css`。

## 后续子项目

- **G**:代码块方案(#3)。
- **H**:标签治理(#6)。
- **I**:about 重做(#7)。
- 另:主题 `baseof.html` 的 `site.LanguageCode` 废弃警告可在本项目顺手评估是否覆盖(若覆盖则纳入,否则留 G/后续)。
