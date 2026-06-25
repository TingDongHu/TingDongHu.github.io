# 启用 Dream 主题内置功能 实施计划(子项目 A)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 打开 Dream 主题 v3.13.0 已内置但未启用的功能(目录、图片放大、上下篇、吸顶、RSS、站内搜索),并清除一段被主题忽略的死配置,让这个自用复习博客「好查、好读」。

**Architecture:** 纯配置 + 内容文件改动,不碰主题源码、不引外部服务。三处改动:(1) 在 `hugo.toml` 的 `[params]` 追加五个布尔开关;(2) 新建 `content/search/_index.md` 激活 Fuse.js 搜索页与导航搜索图标;(3) 删除 `hugo.toml` 中失效的 `[menu]` 块。

**Tech Stack:** Hugo extended、Dream 主题 v3.13.0、TOML 配置、Hugo Markdown front matter。

## Global Constraints

- 不修改 `themes/dream-3.13.0/` 源码;只改 `hugo.toml` 与 `content/`。(来自 CLAUDE.md:主题用 override,不直接改)
- 文件保持 Unix-LF 换行(历史上 CRLF 导致过 YAML front matter 渲染问题)。
- 不引入评论、统计分析、社交分享(YAGNI,已在设计阶段移除)。
- 参数名必须与主题一致,逐字采用:`showTableOfContents`、`imageZoomableInPost`、`showPrevNextPost`、`stickyNav`、`rss`(来源:`themes/dream-3.13.0/hugo.example.toml` 与对应 partial)。

## ⚠️ 环境前置条件(执行前必读)

当前会话中,命令行 Bash 与 Read 对**仓库内预先存在的文件**报 `Operation not permitted`(macOS 完全磁盘访问权限刚授予,需**重启终端 / Claude Code App** 才对运行中的进程生效)。

- **编辑步骤**(Edit/Write):需要能读到 `hugo.toml`。若执行时 Edit 仍报 EPERM,先让用户重启 App。
- **验证步骤**(`hugo server` / `hugo`):必须在权限生效后才能运行。
- 建议:**执行本计划前先重启一次终端 / Claude Code**,一次性解决读写与构建权限。

---

## Task 1: 在 `hugo.toml` 启用五个显示开关

**Files:**
- Modify: `hugo.toml`(`[params]` 段内,`siteStartYear = 2021` 之后)

**Interfaces:**
- Consumes: 无。
- Produces: 站点参数 `showTableOfContents`、`imageZoomableInPost`、`showPrevNextPost`、`stickyNav`、`rss` 均为 `true`,供主题 partial(`nav.html` 等)读取。

- [ ] **Step 1: 编辑 `hugo.toml`,在站点选项区追加五个开关**

用 Edit 工具做精确替换。

`old_string`:
```toml
  # --- 4. 站点选项 ---
  siteStartYear = 2021
  # 如果不想在首页卡片显示默认占位图，取消下面注释
  # noDefaultSummaryCover = true 
```

`new_string`:
```toml
  # --- 4. 站点选项 ---
  siteStartYear = 2021
  # 如果不想在首页卡片显示默认占位图，取消下面注释
  # noDefaultSummaryCover = true 

  # --- 4b. 阅读体验开关 (子项目A: 启用主题内置功能) ---
  showTableOfContents = true   # 长文目录,复习时快速跳转
  imageZoomableInPost  = true  # 文章内图片点击放大(信息图/截图多)
  showPrevNextPost     = true  # 上一篇/下一篇导航
  stickyNav            = true  # 导航栏滚动吸顶
  rss                  = true  # 显示导航栏 RSS 图标(feed 已自动生成)
```

- [ ] **Step 2: 构建验证无报错**

> 需完全磁盘访问权限已生效。若 Bash 仍 EPERM,先重启 App 再跑。

Run: `hugo`
Expected: 构建成功(`Pages | XX ... Total in ... ms`),无 `ERROR`、无新增 deprecation 警告。

- [ ] **Step 3: 本地预览确认四项生效**

Run: `hugo server -D`
打开 http://localhost:1313,确认:
- 导航栏出现 **RSS** 图标;
- 打开任一长文(如 `/posts/...games101.../`),显示 **目录(TOC)** 与底部 **上一篇/下一篇**;
- 文章内图片点击可 **放大**;
- 页面下滑时导航 **吸顶**。
Expected: 四项全部可见且工作。

- [ ] **Step 4: 提交**

```bash
git add hugo.toml
git commit -m "feat: 启用主题阅读体验开关(TOC/图片放大/上下篇/吸顶/RSS)"
```

---

## Task 2: 新建搜索 section 激活站内搜索

**Files:**
- Create: `content/search/_index.md`

**Interfaces:**
- Consumes: 无。
- Produces: 一个 `Type=search` 的 section 页面 `/search/`。满足 `themes/dream-3.13.0/layouts/partials/renderNavItem.html` 中搜索图标的出现条件 `(gt (len (where site.Pages "Type" "search")) 0)`,并由 `layouts/section/search.html`(Fuse.js)渲染。

- [ ] **Step 1: 创建 `content/search/_index.md`**

用 Write 工具写入(注意保持 Unix-LF):

```markdown
---
title: 搜索
layout: search
---
```

> 说明:`layout: search` 对该 section 是冗余的(Hugo 会按 section 名自动套 `section/search.html`),但写上更明确、无副作用。`content` 已挂载到 `static`,新增 section 不影响现有文章图片路径。

- [ ] **Step 2: 本地预览确认搜索可用**

> 需权限已生效。

Run: `hugo server -D`
- 导航栏(及窄屏菜单)出现 **搜索** 图标;
- 访问 http://localhost:1313/search/,输入某文章标题关键词(如「排序」),能列出匹配文章并点击跳转。
Expected: 搜索图标出现,搜索结果正确。

- [ ] **Step 3: 提交**

```bash
git add content/search/_index.md
git commit -m "feat: 新建搜索section,激活Fuse.js站内搜索与导航图标"
```

---

## Task 3: 删除被主题忽略的 `[menu]` 死配置

**Files:**
- Modify: `hugo.toml`(删除 `[menu]` 整段)

**Interfaces:**
- Consumes: 无。
- Produces: `hugo.toml` 不再含 `[menu]` 块。导航由主题默认列表 `["about","search","rss","posts","categories","tags"]`(`nav.html`)驱动,表现不变(posts/categories/tags 仍渲染)。

- [ ] **Step 1: 编辑 `hugo.toml`,删除 `[menu]` 块**

用 Edit 工具做精确替换,把整段菜单配置(含其上方两行注释)连同后面的空行一起去掉,直接衔接 `[markup]`。

`old_string`:
```toml
# --- 5. 菜单配置 (注意：Dream 的图标处理方式与 LoveIt 不同) ---
# LoveIt 用 pre 写 HTML，Dream 建议直接在 menu 结构中配置
[menu]
  [[menu.main]]
    identifier = "posts"
    name = "文章"
    url = "/posts/"
    weight = 1
  [[menu.main]]
    identifier = "categories"
    name = "分类"
    url = "/categories/"
    weight = 3
  [[menu.main]]
    identifier = "tags"
    name = "标签"
    url = "/tags/"
    weight = 4
  
[markup]
```

`new_string`:
```toml
# --- 5. 菜单配置 ---
# 注意: Dream 主题不读 Hugo 的 [menu] 块,导航由 nav.html 的默认列表
# ["about","search","rss","posts","categories","tags"] 驱动,需重排时用 params.reorderNavItems。

[markup]
```

- [ ] **Step 2: 构建并预览确认导航不变**

> 需权限已生效。

Run: `hugo server -D`
打开 http://localhost:1313,确认导航栏仍含 **文章 / 分类 / 标签**(现在还应有 Task 1/2 加入的 **搜索 / RSS** 图标)。
Expected: 导航表现正常,无丢项,`hugo` 构建无报错。

- [ ] **Step 3: 提交**

```bash
git add hugo.toml
git commit -m "chore: 删除被Dream主题忽略的[menu]死配置"
```

---

## Task 4: 补提交设计文档(若权限恢复前未提交)

**Files:**
- 已存在: `docs/superpowers/specs/2026-06-25-enable-theme-features-design.md`
- 已存在: `docs/superpowers/plans/2026-06-25-enable-theme-features.md`(本文件)

**Interfaces:**
- Consumes: 无。
- Produces: 设计与计划文档纳入版本控制。

- [ ] **Step 1: 提交设计与计划文档**

> 仅当这两份文档尚未提交时执行(brainstorming 阶段因 EPERM 跳过了 spec 提交)。

```bash
git add docs/superpowers/specs/2026-06-25-enable-theme-features-design.md docs/superpowers/plans/2026-06-25-enable-theme-features.md
git commit -m "docs: 子项目A设计文档与实施计划"
```

---

## 完成标准(整体)

1. `hugo` 生产构建无 ERROR、无新增 deprecation 警告。
2. 本地预览:导航有 搜索 + RSS 图标;长文有 TOC + 上下篇;图片可放大;导航吸顶。
3. `/search/` 能按标题搜索并跳转。
4. `hugo.toml` 不再含 `[menu]` 块,导航表现不变。
5. 所有改动已分任务提交;设计与计划文档已入库。

## Self-Review(已执行)

- **Spec coverage:** 设计文档三处改动 → Task 1(开关)、Task 2(搜索)、Task 3(删 [menu])逐一对应;另补 Task 4 收尾提交文档。无遗漏。
- **Placeholder scan:** 无 TBD/TODO;每个编辑步骤给出了精确的 `old_string`/`new_string` 或文件全文;验证步骤给出确切命令与预期。
- **Type consistency:** 五个参数名在设计、计划、验证中一致;搜索出现条件 `Type=search` 与 `content/search/` section 名一致;`[menu]`/`reorderNavItems` 引用与主题 `nav.html` 实际机制一致。
