# 设计文档:标签治理(子项目 H)

- 日期:2026-06-25
- 状态:已确认,待实施
- 分支:建议新建 `feature/tags`(基于 main 或承接 G 合并后)
- 所属:博客样式优化子项目 H(样式问题清单第 6 项)

## 背景与目的

博客自用复习。当前标签系统问题(#6):

- **标签泛滥**:68 篇文章产生 **182 个去重标签**,其中 **138 个只出现 1 次**。
- **同义/大小写重复**:`c++`(7) 与 `C++`(3);`Diffusion`(3)、`扩散模型`(4)、`AI绘画`(3)、`文生图`(2)、`视觉图像生成`(2)、`生成式人工智能`(2) 等同概念散落。
- **标签页展示差**:`/tags/` 总览页把全部标签**等大字母序平铺**,无频次区分、无计数,精简后也需要更有效的呈现。

诉求:① 精简标签数据(合并重复 + 归并碎标签);② 改 `/tags/` 总览页为频次标签云;③ 优化单篇文章内标签 badge 观感。

## 决策(已与用户确认)

- **精简力度:适中** —— 合并大小写/同义重复,并把碎标签归并到上级主题词或删除。目标 **182 → 约 40–60**。
- **categories 不动** —— 本次只治 `tags`,不碰 `categories`。
- **映射方式:分领域逐批审** —— 按内容领域(图形学 / C++ / LLM·Agent / 算法 / 杂)分批产出「旧→新」映射草案,用户逐批审定。
- **改写工具:Python 脚本 + JSON 映射表** —— 与现有 `compress_images.py` 工具链一致;数据(映射)与逻辑(脚本)分离;dry-run → apply;幂等可复跑;只动 tags 行。
- **标签页:左云 + 右网格** —— 保留现有左右布局,仅把左侧标签列表改为频次云;不动右侧文章网格。
- **标签云:纯服务端** —— 模板按 `.Count` 映射字号 + 计数输出,无 JS、无 FOUC。
- **文章内 badge:小改** —— 复用主题 `.badge`,custom.css 微调样式。

## 关键事实(已核实)

- 标签数据:182 去重标签 / 138 个频次=1 / 68 篇文章。高频:图形学(14)、GAMES课程(14)、LLM(11)、UnrealEngine(9)、Agent(8)、c++(7)、语法(6)、3D生成(6)…
- 标签页模板:主题 `themes/dream-3.13.0/layouts/_default/terms.html`(taxonomy 总览,左侧 `.Data.Terms.Alphabetical` 平铺 badge + 右侧分页文章网格)与 `term.html`(单标签页)。**本仓 layouts 下尚无覆盖**。
- 单篇文章标签用主题 `.badge` 类(DaisyUI)显示。
- Tailwind 预编译铁律(见 CLAUDE.md):新 utility 类在预编译 `output.css` 里不存在则失效;字号/容器样式须用**内联 style**(动态值)或 `custom.css` 纯 CSS(稳定类名)。
- front matter 为 YAML,`tags:` 行形如 `tags: ["A", "B", "C"]`;须保持 LF 行尾(CRLF 致 Typora/YAML 问题,见 CLAUDE.md)。
- 内容目录结构:每篇 `content/posts/<topic>/<post>.md`(或同名目录),`compress_images.py` 已能遍历。

## 范围

### 包含
1. 新建 `retag.py`(仓库根)—— 标签审计 + 按映射表批量改写 tags。
2. 新建 `tag-map.json`(仓库根)—— 旧→新标签映射 + 删除列表;分领域逐批审定。
3. 批量改写 68 篇文章 front matter 的 `tags` 行(经脚本)。
4. 覆盖 `layouts/_default/terms.html` —— 左侧标签列表改频次标签云(字号按 `.Count` + 计数),保留右侧文章网格。
5. `assets/css/custom.css` 或 `static/css/custom.css` 增标签云 + 文章内 badge 样式(纯 CSS,稳定类名)。

> CSS 落点:沿用当前 `custom.css`(`head.html:66` 仍以裸路径 `/css/custom.css` 加载)。本子项目不改 custom.css 的加载方式;如需防缓存可后续统一处理(G 已为 chroma-mac 做过 fingerprint,custom.css 暂沿用裸路径)。

### 不包含
- `categories` 治理(本次不动)。
- 受控词表(激进方案,YAGNI)。
- `term.html` 单标签页改造(本次只改总览页 terms.html;单页保留主题原样)。
- 不改 `themes/dream-3.13.0/` 源码(仅在 `layouts/` 覆盖)。
- 其余清单项(about #7 → 子项目 I)。

## 详细设计

### 组件 1:`retag.py`(审计 + 改写)

两种模式:

**`--audit`**:遍历 `content/posts/**/*.md`,解析每篇 YAML front matter 的 `tags`,聚合输出「标签 → 频次 → 所属文章相对路径列表」。供产出映射草案;按领域分组(领域判定靠人工/脚本辅助分类,初版可仅按频次排序输出,领域归类在 tag-map 审定阶段人工完成)。

**改写(默认 dry-run,`--apply` 落盘)**:
- 读 `tag-map.json`。
- 逐篇:定位 front matter(首个 `---` … `---` 块),仅匹配其中的 `tags:` 行。
- 对该行的标签数组:套映射(命中 key → 换 value;在 `__delete__` 列表 → 移除;未命中 → 原样保留)→ **去重**(保序)→ 重写 `tags:` 行。
- 不触碰 `title`/`description`/`categories`/正文。
- 输出:dry-run 打印将改动的文件 + 旧/新 tags 行;`--apply` 写回(LF 行尾)。
- 幂等:已改过的文件再跑映射(新标签不在 key 中)不变。

**映射表 `tag-map.json` 格式**:
```json
{
  "rename": {
    "扩散模型": "Diffusion",
    "文生图": "Diffusion",
    "AI绘画": "Diffusion",
    "c++": "C++",
    "插入排序": "排序算法",
    "面相对象": "面向对象"
  },
  "delete": ["入门", "环境配置"]
}
```
- `rename`:旧→新;多个旧标签指同一新标签即合并。
- `delete`:直接移除的标签。
- 未列出的标签 = 原样保留。

### 组件 2:`terms.html`(频次标签云)

覆盖 `layouts/_default/terms.html`。仅改左侧标签区:

- 遍历 `.Data.Terms.ByCount`(按文章数降序)。
- 字号:取当前 taxonomy 的 min/max Count,线性插值到 `[0.8rem, 2.0rem]`:
  `size = 0.8 + (count - min) / (max - min) * 1.2`(min==max 时取中值,防除零)。
- 每项:`<a class="tag-cloud__item" style="font-size:{{size}}rem">标签<span class="tag-cloud__count">N</span></a>`,挂在 `.tag-cloud` 容器内。
- 高频项可同步加粗/提亮(纯 CSS 由字号无法表达的部分,可选;初版仅字号 + 计数)。
- 右侧文章网格 + 分页 + zenMode 分支:**保留原样**。

### 组件 3:`custom.css`(标签云 + badge 样式)

纯 CSS,稳定类名:
- `.tag-cloud`:flex wrap,行间距、对齐。
- `.tag-cloud__item`:padding、圆角、描边、hover 提亮、过渡;字号由内联 style 控制。
- `.tag-cloud__count`:弱化色、小一号、左间距。
- 文章内 badge:在单篇标签容器下微调 `.badge`(间距/圆角/hover),不动模板结构。

## 验证方式

1. `retag.py --audit` 改写后复跑:去重标签数降至约 40–60;无意外残留(如 `c++`/`C++` 已并)。
2. `git diff content/posts/` 抽查若干篇:仅 `tags:` 行变化,title/description/categories/正文未动;LF 行尾。
3. `hugo` 构建无 ERROR、无新增 deprecation 警告(`.Site.LanguageCode` 既有除外)。
4. 本地 `hugo server -D` 打开 `/tags/`:左侧为频次云(高频字大、低频字小)、每标签带计数 `(N)`、点击进单标签页正常;右侧文章网格保留。
5. 单篇文章底部/顶部标签 badge 观感改善(间距/hover),窄屏不溢出。
6. 全站标签链接无 404(精简后旧标签页 `/tags/<旧>/` 不再被引用)。

## 风险与回滚

- **风险:中**。批量改 68 篇 front matter 是主要风险点。缓解:独立分支 + 改前 git clean + 脚本 dry-run 先审 + git diff 复核 + 脚本只动 tags 行(正则锚定 front matter 内)。
- 映射语义靠分领域逐批人工审,避免误并。
- 标签云字号用内联 style,绕开 Tailwind 预编译坑。
- 回滚:`git checkout` 还原 content/ 与 layouts/;删 `retag.py`/`tag-map.json`。

## 后续子项目
- **I**:about 页重做(#7)。
- 原始 B(图片)/C(3dgenai 重构)/D(工程清理)待排期。
