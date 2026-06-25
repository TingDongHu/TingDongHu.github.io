# 设计文档:修复 0001 空归档 + RSS 美化(子项目 E)

- 日期:2026-06-25
- 状态:已确认,待实施
- 所属:博客样式优化的子项目 E(样式问题清单第 5、4 项)

## 背景与目的

博客自用复习。两个独立小问题:

1. **#5 归档页出现 `0001` 空年份**:`content/posts/` 下混入 53 个**无 date 的非文章**(图像生成 prompts、系列 outline、README、一份演讲草稿),被 Hugo 当作文章渲染,落入 `0001-01-01` 年份桶,污染归档页,同时也污染了文章列表、站内搜索与 RSS。
2. **#4 RSS 浏览器直开是裸 XML**:Hugo 原生行为(RSS 本就给订阅器读),非 bug。希望加美化让浏览器直开也好看。

## 关键事实(已核实)

- `content/posts/` 下无 date 的 md 共 **53 个**,全部为非文章:
  - `**/prompts/*.md`(图像生成提示词,被根目录 `batch-all.json` 引用)
  - `**/outline.md`(系列大纲)
  - `3dgenai/README.md`
  - `agent/RCL组会报告演讲稿.md`(演讲草稿,无 front matter;另有正式文章《论文阅读RCL》)
- 这 4 类用正则 `/prompts/`、`outline\.md$`、`/README\.md$`、`RCL组会报告演讲稿\.md$` 精确命中 **53 个,零真文章**(已逐一校验:命中集合中无任何含 `date` 的文件)。
- 3dgenai 真文章仅 **6 篇**(`part1..6-*.md`,均带 date),不受影响。
- 当前 `hugo` 构建为 539 页,含这 53 个垃圾页。
- RSS 由 Hugo 自动生成 `public/index.xml`,RSS 2.0 格式,无 `xml-stylesheet` 指令。

## 范围

### 包含
1. `hugo.toml` 加 `ignoreFiles`,排除 53 个非文章。
2. 新增 `static/rss.xsl` + 覆盖 `layouts/_default/rss.xml`,为 RSS 注入 XSL 美化。

### 不包含
- 样式清单其余项(TOC/排版/代码块/标签/about)。
- 删除磁盘上的 prompts/outline 文件(保留,供图像生成工具用)。
- 修改文章 front matter。

## 详细改动

### 改动 1:`ignoreFiles` 修 0001(#5)

`hugo.toml` 顶层配置区(与 `baseURL`/`title` 同级,非 `[params]` 内)新增一行:

```toml
ignoreFiles = ['/prompts/', 'outline\.md$', '/README\.md$', 'RCL组会报告演讲稿\.md$']
```

- 语义:Hugo 构建时跳过匹配这些正则的源文件,不渲染、不进列表/归档/搜索/RSS。
- 文件保留在磁盘,不删除。
- 已验证 4 条正则命中且仅命中 53 个非文章。

### 改动 2:RSS 美化(#4)

**2a. 新建 `static/rss.xsl`** —— XSLT 1.0 样式表,将 RSS 2.0 转为带样式的 HTML 列表页:站点标题、描述、文章条目(标题链接 + pubDate)。样式内联,风格简洁(浅色卡片列表)。

**2b. 覆盖 `layouts/_default/rss.xml`** —— 在 XML 声明后注入处理指令:

```xml
<?xml-stylesheet type="text/xsl" href="/rss.xsl"?>
```

正文沿用 Hugo 内置 RSS 模板的标准结构(channel + item:title/link/pubDate/description),保证订阅器兼容。

- 效果:浏览器直开 `/index.xml` 渲染为美化页;Feedly 等订阅器忽略 `xml-stylesheet` 指令,照常读原始 RSS。
- 注意:XSLT 由浏览器渲染,桌面主流浏览器支持;同源 `/rss.xsl` 加载正常。

## 验证方式

1. `hugo`(生产构建)无 ERROR,总页数较基线下降约 53(539 → ~486)。
2. `grep -r "0001" public/` 在归档相关页面无 `0001` 年份桶;归档页只剩 2023–2026。
3. 站内搜索结果、首页文章列表、`public/index.xml` 中不再出现 prompts/outline/演讲稿条目。
4. 本地 `hugo server -D`,浏览器打开 http://localhost:1313/index.xml 显示美化后的文章列表页(非裸 XML)。
5. `public/index.xml` 原始内容仍为合法 RSS 2.0(含 `<?xml-stylesheet ...?>` 指令)。

## 风险与回滚

- 风险:低。`ignoreFiles` 不删文件;RSS 改动只加样式与处理指令,不改 feed 数据结构。
- 回滚:删除 `ignoreFiles` 行 / 删除 `static/rss.xsl` 与 `layouts/_default/rss.xml` 即恢复。
- 唯一需留意:若某真文章正文用相对链接指向了被忽略的 prompt/outline md(可能性极低,prompts 为生成工具用),该链接会 404 —— 验证步骤 3 顺带人工扫一眼无此类链接。

## 后续子项目(本文档不实施)

- **F**:阅读排版重做(重写失效的 custom.css + TOC sticky)。
- **G**:代码块方案替换。
- **H**:标签治理(182→精简 + 展示交互)。
- **I**:about 页重做。
