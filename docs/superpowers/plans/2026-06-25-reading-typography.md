# 阅读排版重做 + TOC sticky 实施计划(子项目 F)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 拓宽正文(去空广告列 + 解除 prose 65ch)、提升信息密度(紧凑排版)、给目录加 sticky 实现滚动跟随随时跳转。

**Architecture:** 覆盖 `layouts/_default/single.html` 调整两列网格 + TOC sticky;重写 `static/css/custom.css` 死布局段为 `.prose` 紧凑规则;清 `assets/css/custom.css` 死代码。不改主题源码。实施后本地实时微调密度数值。

**Tech Stack:** Hugo extended v0.163.3、Tailwind Typography(`prose`)、DaisyUI、Alpine.js(主题 scrollspy)。

## Global Constraints

- 不修改 `themes/dream-3.13.0/`(仅 `layouts/` 覆盖)。
- Unix-LF。
- 不动 `static/css/custom.css` 第 1–130 行代码块样式(归子项目 G)。
- hugo 二进制:`/opt/homebrew/bin/hugo`(v0.163.3+extended)。
- 已知主题 `baseof.html` 的 `site.LanguageCode` 废弃警告为既有,不算本项目新增。

## 环境

读写/构建正常。命令用绝对路径 `/opt/homebrew/bin/hugo`。`hugo server` 可能已在后台跑;改 layout/CSS 后若未热更新则重启。

---

## Task 1: 覆盖 `single.html` —— 拓宽网格 + TOC sticky

**Files:**
- Create: `layouts/_default/single.html`(复制主题版,改 2 处)

**Interfaces:**
- Consumes: 主题 `themes/dream-3.13.0/layouts/_default/single.html`。
- Produces: 文章主区两列网格(文章 `1fr` + TOC `16rem`),TOC `sticky`。

- [ ] **Step 1: 复制主题 single.html 到 layouts**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
mkdir -p layouts/_default
cp themes/dream-3.13.0/layouts/_default/single.html layouts/_default/single.html
```

- [ ] **Step 2: 改网格(去空广告列 + 文章吃满主区)**

Edit `layouts/_default/single.html`,精确替换。

`old_string`:
```
<div class="lg:grid lg:grid-cols-4 gap-4 mt-4 px-4">
  <div class="hidden lg:block">
    {{ if fileExists "layouts/partials/adsense.html" }}
      <div class="dream-adsense w-2/3">
        {{ partialCached "adsense.html" . }}
      </div>
    {{ end }}
  </div>

  <div class="lg:col-span-2">
    <article class="mx-auto prose prose-quoteless dark:prose-invert" id="dream-single-post-main" itemscope itemtype="http://schema.org/Article">
```

`new_string`:
```
<div class="lg:grid lg:grid-cols-[1fr_16rem] lg:gap-8 mt-4 px-4">
  <div class="min-w-0">
    <article class="mx-auto prose prose-quoteless dark:prose-invert" id="dream-single-post-main" itemscope itemtype="http://schema.org/Article">
```

- [ ] **Step 3: 给 TOC 容器加 sticky**

Edit 同文件,精确替换。

`old_string`:
```
  <div
    x-data="tocHighlighter()"
    @scroll.window="debouncedScroll"
    class="hidden lg:flex lg:flex-col lg:items-end lg:self-start"
  >
```

`new_string`:
```
  <div
    x-data="tocHighlighter()"
    @scroll.window="debouncedScroll"
    class="hidden lg:flex lg:flex-col lg:self-start lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto"
  >
```

- [ ] **Step 4: 构建验证**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
rm -rf public && /opt/homebrew/bin/hugo 2>&1 | grep -iE "ERROR" || echo "build clean"
POST=$(find public/posts -mindepth 2 -name index.html | head -1)
echo "=== 网格类生效? ==="
grep -o 'grid-cols-\[1fr_16rem\]' "$POST" && echo OK-grid
echo "=== TOC sticky? ==="
grep -o 'lg:sticky lg:top-4' "$POST" && echo OK-sticky
echo "=== 空广告列已移除? ==="
grep -c 'dream-adsense w-2/3' "$POST"
```
Expected:build clean;命中 `grid-cols-[1fr_16rem]` 与 `lg:sticky lg:top-4`;`dream-adsense w-2/3` 计数为 0。

- [ ] **Step 5: 提交**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add layouts/_default/single.html
git commit -m "feat: 覆盖single.html拓宽正文网格+TOC sticky"
```

---

## Task 2: 紧凑排版 CSS(`static/css/custom.css`)

**Files:**
- Modify: `static/css/custom.css`(替换第 132–182 行死布局段)

**Interfaces:**
- Consumes: 文章标记 `#dream-single-post-main.prose`、`#dream-single-post-content`。
- Produces: 解除 65ch、紧凑排版规则。代码块段(1–130 行)不变。

- [ ] **Step 1: 替换死布局段**

Edit `static/css/custom.css`,精确替换(从第 132 行的注释块到文件末尾第 182 行 `}`)。

`old_string`:
```
/* ==========================================================================
    Hugo Dream Theme - Layout & Width Optimization
    目的：增加正文显示宽度，提升 Games101/C++ 笔记的信息密度，并确保图片居中
   ========================================================================== */

/* 1. 核心正文容器：提升至 1300px 以获取超大视野 */
.ui.container.dream-article {
    max-width: 1300px !important; 
    width: 92% !important;        
}

/* 2. 响应式微调：确保在大屏幕下锁定宽度 */
@media only screen and (min-width: 1200px) {
    .ui.container.dream-article {
        width: 1300px !important; 
    }
}

/* 3. 图片完美居中方案 */
/* 核心逻辑：将图片变为块级元素并利用 margin 自动平衡 */
.dream-article img {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
    
    max-width: 100% !important;   /* 防止图片溢出容器 */
    height: auto !important;
    border-radius: 8px;           /* 圆角风格统一 */
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* 增加轻微阴影，提升质感 */
}

/* 额外处理：Markdown 渲染时图片常被包裹在 p 标签里，强制该 p 标签也居中 */
.dream-article p {
    text-align: center; /* 确保 p 标签内的行内元素居中 */
}

/* 恢复正文文字的左对齐（防止被上面的 p 标签全局居中干扰） */
/* 如果你发现文字也居中了，取消下面这段注释 */
/*
.dream-article p {
    text-align: justify; 
}
*/

/* 4. 代码块自适应：确保横向铺满 */
.highlight {
    width: 100% !important;
    text-align: left; /* 强制代码块内容左对齐，不受全局居中影响 */
}
```

`new_string`:
```
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

/* 代码块横向铺满(保留旧补丁,避免溢出网格列) */
.highlight { width: 100% !important; text-align: left; }
```

- [ ] **Step 2: 构建验证**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
rm -rf public && /opt/homebrew/bin/hugo 2>&1 | grep -iE "ERROR" || echo "build clean"
grep -o "dream-single-post-content" public/css/custom.css | head -1 && echo OK-css
echo "=== 确认代码块段(1-130)仍在 ==="
grep -c "mac-dots\|dot-red" public/css/custom.css
```
Expected:build clean;`custom.css` 含 `dream-single-post-content`;`mac-dots/dot-red` 计数 > 0(代码块段未被破坏)。

- [ ] **Step 3: 提交**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add static/css/custom.css
git commit -m "feat: 重写正文排版CSS,解除prose 65ch+紧凑高密度"
```

---

## Task 3: 清 `assets/css/custom.css` 死代码

**Files:**
- Modify: `assets/css/custom.css`(整文件为死的 `.dream-article`/Prism 选择器)

**Interfaces:**
- Consumes: 无。
- Produces: 文件保留(被 `customCSS` 引用,不可删),内容清为占位注释。

- [ ] **Step 1: 用占位注释覆盖整文件**

Write `assets/css/custom.css` 全文为:
```css
/* 本文件经 hugo.toml customCSS 编入 output.css。
   原有 .dream-article / .ui.container / Prism 选择器为旧主题遗留死代码,已清除。
   当前正文排版见 static/css/custom.css(子项目F)。 */
```

- [ ] **Step 2: 构建验证**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
rm -rf public && /opt/homebrew/bin/hugo 2>&1 | grep -iE "ERROR" || echo "build clean"
```
Expected:build clean(`output.css` 仍正常生成,无 customCSS 缺失报错)。

- [ ] **Step 3: 提交**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add assets/css/custom.css
git commit -m "chore: 清assets/custom.css旧主题死代码"
```

---

## Task 4: 本地实时微调 + 目视验收

**Files:** 可能微调 `static/css/custom.css`(密度数值)、`layouts/_default/single.html`(网格 `16rem`/`gap` 数值)。

- [ ] **Step 1: 启动/重启本地预览**

Run:`cd /Users/ethanhu/Documents/self/my_blog && /opt/homebrew/bin/hugo server -D`(若已在后台跑则确认已热更新,必要时重启)。

- [ ] **Step 2: 目视验收(长文,如 games101 几何篇)**

打开 http://localhost:1313/ 进任一长文,确认:
- 正文明显变宽(占主区 ~75%);
- 行距/标题/段距紧凑,密度提升;
- 右侧 TOC 随滚动保持可见、点击跳转、当前章节高亮;
- 长目录超屏时 TOC 内部可滚动;
- 窄屏(缩窗到 <lg):TOC 隐藏,正文单列全宽,无横向溢出;
- 代码块外观同改动前。

- [ ] **Step 3: 按需微调并提交**

若数值需调(行高/字号/列宽/gap),改对应文件后 `rm -rf public && /opt/homebrew/bin/hugo` 复验,然后:
```bash
cd /Users/ethanhu/Documents/self/my_blog
git add -A static/css/custom.css layouts/_default/single.html
git commit -m "style: 微调正文排版数值"
```
(无需微调则跳过本步。)

---

## Task 5: 提交计划文档

- [ ] **Step 1: 提交本计划**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add docs/superpowers/plans/2026-06-25-reading-typography.md
git commit -m "docs: 子项目F实施计划"
```

---

## 完成标准(整体)

1. `hugo` 构建无 ERROR、无新增 deprecation 警告。
2. 长文正文变宽(~75% 主区)、密度提升;TOC 随滚动跟随、可跳转、高亮、超屏可滚。
3. 窄屏回退正常,无横向溢出;代码块外观不变。
4. 两个 custom.css 死代码已清;改动分任务提交;文档入库。

## Self-Review(已执行)

- **Spec coverage:** spec 三组件 → Task 1(single.html 网格+TOC)、Task 2(prose 紧凑 CSS)、Task 3(清 assets 死码);Task 4 实时微调验收对应 spec "实施后本地微调";Task 5 收尾。无遗漏。
- **Placeholder scan:** 无 TBD;single.html 两处与 CSS 段给出完整 old/new;验证含确切命令与预期。
- **Type consistency:** 选择器 `#dream-single-post-main`/`#dream-single-post-content` 与 spec、主题真实标记一致;网格类 `grid-cols-[1fr_16rem]`、`lg:sticky lg:top-4` 在 Task 与验证中一致;保留的 `.highlight` 宽度补丁与代码块段(1–130 行)不冲突。
