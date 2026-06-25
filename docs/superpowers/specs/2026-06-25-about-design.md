# 设计文档:about 页重做(子项目 I)

- 日期:2026-06-25
- 状态:已确认,待实施
- 分支:建议新建 `feature/about`(基于 H 合并后的 main)
- 所属:博客样式优化子项目 I(样式问题清单第 7 项)

## 背景与目的

博客自用复习。当前 about 页问题(#7):

- **内容空洞**:`content/about/` 是 headless bundle + 6 个子页(me/hobby/now/uses/uses1),共约 105 词,纯 bullet/链接,无叙述、无人设。
- **呈现难看**:经主题 `back.html` 以 masonry 卡片 grid 渲染,无图、无层级;`uses`/`uses1` 两张工具卡重复、分类乱。
- **结构乱**:6 张卡片间无联系。
- **交互绕**:about 不是独立页,靠导航/头像 `@click="flip"` 翻转到 back 面展示卡片。

诉求:做一个有人设叙述 + 结构化展示、视觉有极客折腾感的独立 about 页。

## 决策(已与用户确认)

- **调性:混合(叙述 + 展示)** —— 顶部个人叙述段,下面分区块展示。
- **气质:极客/折腾感**。博客定位:个人复习/笔记库。作者:多栖(图形学/游戏 + LLM/Agent),兴趣驱动。
- **实现:独立 `/about/` 页 + 自定义模板**,弃用 flip 卡片交互。
- **导航 + 头像**:都改为跳转 `/about/`(彻底弃 flip)。
- **内容载体:单个 `content/about/index.md`** —— 叙述段走正文(markdown,好编辑);技术栈/now/uses/hobby/社交走 front matter 数组(模板渲染成 pill/列表)。
- **展示分区(5 块 + 社交)**:技术栈/领域、最近在学(now)、工具装备(uses 合并去重,软件/网络工具)、好物橱窗(gear,实物电子设备)、兴趣爱好(hobby)、社交链接(链接用户稍后给)。
- **好物橱窗(gear)**:商品卡片形式,每件含 名称 + 一句推荐语 + 图片 + 链接(图与链接用户后续给,先留结构 + 占位)。与 uses 区分:uses=软件/网络工具,gear=实物硬件设备。
- **样式:纯 CSS `.about-*`**(Tailwind 预编译铁律),响应式网格卡片,技术栈用 pill,**跟随主题明暗**(不恒深)。
- **不删主题文件**,仅在 `layouts/` 覆盖。

## 关键事实(已核实)

- 现有内容:`content/about/index.md`(headless 标记)+ me/hobby/now/uses/uses1 五个子页。内容详见各文件,now(4 条学习链接)、uses(7 工具)、uses1(7 资源)、hobby(6 条)、me(姓名/居住地)。
- 现有渲染:主题 `themes/dream-3.13.0/layouts/index.html` → `back.html`(非 zen)。`back.html` 背面三块:about 卡片、social links(仅当 `data/socials.toml` 存在)、Disqus(仅当配置)。**经核实 `data/socials.toml` 不存在、无 Disqus 配置**,故 back 面实际只有 about 卡片 —— 弃 flip 不丢任何现有内容。
- 导航:主题 `nav.html` 硬编码导航列表;about 项渲染在 `renderNavItem.html`(`@click="flip = !flip"`);头像在 `nav.html:15`(`@click="flip = !flip"`)。
- `hugo.toml` 无 `[menu]`(主题不读),导航靠主题默认列表 + `params.reorderNavItems`。
- 模板覆盖现状:本仓 `layouts/` 有 `_default/single.html`、`_default/baseof.html`、`_default/terms.html`(子项目 H 新增)、`_default/_markup/render-codeblock.html`(G)、`partials/{head,scripts,math}.html`。**无 about 专属模板、无 renderNavItem 覆盖**。
- 样式:`static/css/custom.css`(裸路径加载)现含子项目 F(排版/两列)、H(标签云/badge);**无 about 相关**。
- Tailwind 预编译铁律(CLAUDE.md):新 utility 类失效,须用内联 style 或 custom.css 纯 CSS(稳定类名)。

## 范围

### 包含
1. 改 `content/about/index.md` —— 单页:front matter(title + 技术栈/now/uses/hobby/gear/socials 数组)+ 正文(叙述段 markdown)。
2. 删旧子页:`me.md`/`hobby.md`/`now.md`/`uses.md`/`uses1.md`(内容迁入单页)。
3. 新建 `layouts/about/single.html` —— 独立 about 页模板(叙述段 `.Content` + 五区块 + 社交,由 front matter 渲染)。
4. 覆盖 `layouts/partials/renderNavItem.html` —— about 导航项从 flip 改为 `<a href="/about/">`。
5. 覆盖 `layouts/partials/nav.html` —— 头像 `@click="flip"` 改为链接到 `/about/`(其余导航逻辑保持)。
6. `static/css/custom.css` 增 `.about-*` 样式(纯 CSS,跟随主题明暗)。

### 不包含
- 不删/改 `themes/dream-3.13.0/` 源码(含 `back.html`/`zen-back.html`/`grid.js` 的 about 逻辑保持,独立页后不再驱动 about 但无害)。
- flip 翻转机制本身不拆(其他地方若用到不动);仅 about/头像两个入口改为跳转。
- 社交链接的具体 URL(用户稍后提供,先留结构 + 占位)。
- 其余清单项(工程清理 → 子项目 D)。

## 详细设计

### 内容:`content/about/index.md`

front matter(结构化部分):
```yaml
---
title: 关于
techStack: ["图形学", "C++", "游戏引擎", "LLM", "Agent", "3D生成", "机器学习"]
now:
  - { icon: "🎨", name: "GAMES104", url: "https://games104.boomingtech.com/", desc: "现代游戏引擎入门" }
  - { icon: "🏔️", name: "Houdini 基础", url: "https://www.sidefx.com/learn/", desc: "程序化建模与特效" }
  - { icon: "🤗", name: "HuggingFace", url: "https://huggingface.co/learn", desc: "探索开源 AI 社区" }
  - { icon: "🤖", name: "HelloAgent", url: "https://github.com/datawhalechina/hello-agents", desc: "优秀的 Agent 入门项目" }
uses:
  - { name: "Typora", url: "https://typora.io/", desc: "Markdown 极简编辑器" }
  # …合并 uses + uses1 去重
hobby:
  - "🚀 喜欢折腾各种好玩的应用技术"
  # …沿用 hobby.md
gear:
  - { name: "", desc: "", img: "", url: "" }   # 实物电子设备:名称+推荐语+图+链接,用户稍后填
socials:
  - { name: "GitHub", url: "", icon: "" }   # 用户稍后给链接
---
```
正文(叙述段,已与用户定稿,markdown):
> 我是 **古月月仔**(Shimizu Tou / Ethan Hu),一名计算机在校生。山西平遥人,现居上海。
>
> 兴趣多栖——既折腾**计算机图形学**与**游戏引擎**,也一头扎进 **LLM / Agent** 和 **3D 生成**。喜欢上手拆解新工具、新技术,是个停不下来的折腾型选手。
>
> 这个博客是我的**个人复习与笔记库**:把学过的东西写清楚、留个档,顺便公开分享给同样在路上的同好。

### 模板:`layouts/about/single.html`

- 顶部:叙述段 `{{ .Content }}`(prose 样式,但解除 65ch 死限);可选头像。
- 技术栈区:`range .Params.techStack` → pill(`.about-tag`)。
- 最近在学:`range .Params.now` → 链接列表(icon + name + desc)。
- 工具装备:`range .Params.uses` → 链接列表,可分小列。
- 好物橱窗:`range .Params.gear` → 商品卡片(图 + 名称 + 推荐语,整卡链接到 url);空条目(name 为空)不渲染。
- 兴趣爱好:`range .Params.hobby` → bullet。
- 社交:`range .Params.socials` → 图标链接(URL 空则不渲染或占位)。
- 各区块包在 `.about-section` 卡片里,响应式网格 `.about-grid`。
- 复用 `baseof.html` 的 main block;type=about 自动匹配 `layouts/about/single.html`。

### 导航/头像:`renderNavItem.html` + `nav.html`

- `renderNavItem.html`:about 分支由 `<div @click="flip">` 改为 `<a href="{{ "/about/" | relURL }}">`,保留 class/i18n 文案。其余导航项(search/rss/posts/categories/tags)分支不动。
- `nav.html`:头像 `<div @click="flip = !flip">` 改为 `<a href="/about/">` 包裹,保留 avatar 样式。其余不动。

### 样式:`static/css/custom.css`

纯 CSS,稳定类名,跟随主题明暗(用主题 CSS 变量/中性色,不硬编码深色):
- `.about-hero`:叙述段容器,舒适行宽,居中或左。
- `.about-grid`:响应式网格(宽屏 2 列,窄屏 1 列)。
- `.about-section`:区块卡片,描边/圆角/内距;标题 `.about-section__title`。
- `.about-tag`:技术栈 pill(复用标签云观感)。
- `.about-link`:now/uses 链接项,hover 高亮,等宽字体/小图标点缀(极客感)。
- `.about-gear`:好物橱窗网格;`.about-gear__card` 商品卡(图 + 名 + 推荐语,hover 浮起);图用固定比例占位防抖动。
- `.about-socials`:社交图标行。

## 验证方式

1. `hugo` 构建无 ERROR、无新增 deprecation 警告(`.Site.LanguageCode` 既有除外)。
2. 本地 `hugo server -D` 打开 `/about/`:独立页渲染叙述段 + 五区块 + 社交;非 flip。
3. 导航点 "about" → 跳 `/about/`(不再翻转);头像点击 → 跳 `/about/`。
4. 技术栈 pill、now/uses 链接列表、好物橱窗卡片、hobby、社交 渲染正常;链接可点;gear 空条目不渲染、有图条目图片正常。
5. 明暗主题切换:about 页配色跟随(不恒深)。
6. 窄屏(<lg):网格单列,不溢出。
7. 旧子页删除后无 404、无残留引用(站内无指向 me/hobby/now 等的链接)。
8. 首页(原 flip 背面)不再因缺 about 卡片报错(back.html 仍在,但 about 入口已不触发 flip;首页正常)。

## 风险与回滚

- 风险:中。改导航/头像交互 + 删内容文件 + 新模板。缓解:独立分支;改前 git clean;本地逐项验证。
- 主题 flip 机制残留:back.html/grid.js 仍在但 about 不再用,需确认首页/翻转不报错(验证 8)。
- front matter 数组渲染:Hugo `.Params.xxx` map/slice 取值需对齐(icon/name/url/desc 键名)。
- 社交链接 URL 待用户给,先留占位(空 URL 不渲染)。
- 回滚:`git checkout` 还原 content/about/ 与 layouts/;删 `layouts/about/single.html`。

## 后续子项目
- **D**:工程清理(git 大小写重影 598 文件 + 废弃脚本 + .gitignore;牵涉 3dgenai)。
- 原始 B(图片)/C(3dgenai 重构)待排期。
