# 修复 0001 空归档 + RSS 美化 实施计划(子项目 E)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把混入 `content/posts/` 的 53 个非文章排除出 Hugo 构建以消除 `0001` 空归档,并为 RSS 加一张 XSL 样式表,让浏览器直开 `/index.xml` 时显示美化页。

**Architecture:** 两处独立改动 —— (1) `hugo.toml` 顶层加 `ignoreFiles` 正则;(2) 新增 `static/rss.xsl` + 覆盖 `layouts/_default/rss.xml` 注入 `xml-stylesheet` 处理指令。纯配置/模板,不删文件、不改文章。

**Tech Stack:** Hugo extended v0.163.3、TOML、Hugo RSS 模板、XSLT 1.0。

## Global Constraints

- 不修改 `themes/dream-3.13.0/` 源码(来自 CLAUDE.md)。
- 文件保持 Unix-LF。
- 不删除磁盘上的 prompts/outline/README/演讲稿(保留供图像生成工具使用)。
- `ignoreFiles` 正则逐字采用:`'/prompts/'`、`'outline\.md$'`、`'/README\.md$'`、`'RCL组会报告演讲稿\.md$'`(已验证精确命中 53 个非文章、零真文章)。
- hugo 二进制在 `/opt/homebrew/bin/hugo`(v0.163.3+extended)。

## 环境

读写与构建均已正常(本会话已验证)。验证命令用绝对路径 `/opt/homebrew/bin/hugo`。

---

## Task 1: `ignoreFiles` 修复 0001 空归档

**Files:**
- Modify: `hugo.toml`(顶层,`theme` 行之后、`[taxonomies]` 之前)

**Interfaces:**
- Consumes: 无。
- Produces: Hugo 构建排除 53 个非文章源文件;归档/列表/搜索/RSS 不再含它们。

- [ ] **Step 1: 记录基线页数**

Run: `cd /Users/ethanhu/Documents/self/my_blog && /opt/homebrew/bin/hugo --quiet --printPathWarnings 2>/dev/null; /opt/homebrew/bin/hugo 2>&1 | grep -iE "Pages"`
Expected: 记下当前 Pages 数(基线约 539)。

- [ ] **Step 2: 编辑 `hugo.toml` 加 `ignoreFiles`**

用 Edit 工具精确替换。

`old_string`:
```toml
theme = "dream-3.13.0" # 确保文件夹名字匹配，通常是 dream

[taxonomies]
```

`new_string`:
```toml
theme = "dream-3.13.0" # 确保文件夹名字匹配，通常是 dream

# 排除非文章文件(图像生成prompts/系列outline/README/演讲草稿),避免被当文章渲染产生0001空归档
ignoreFiles = ['/prompts/', 'outline\.md$', '/README\.md$', 'RCL组会报告演讲稿\.md$']

[taxonomies]
```

- [ ] **Step 3: 重建并确认页数下降、无 0001**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
rm -rf public && /opt/homebrew/bin/hugo 2>&1 | grep -iE "Pages|ERROR"
echo "=== 0001 检查 ==="
grep -rl "0001" public/ 2>/dev/null | head
echo "=== 残留垃圾条目检查 ==="
grep -rl "infographic\|flowchart\|comparison-\|outline" public/posts/*/index.html 2>/dev/null | head
```
Expected: Pages 较基线下降约 53(≈486);无 ERROR;`0001` 无结果(或仅无关命中);归档页不再有 0001 年份桶。

- [ ] **Step 4: 提交**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add hugo.toml
git commit -m "fix: ignoreFiles排除53个非文章,消除0001空归档"
```

---

## Task 2: RSS 加 XSL 美化样式表

**Files:**
- Create: `static/rss.xsl`
- Create: `layouts/_default/rss.xml`

**Interfaces:**
- Consumes: 无。
- Produces: `public/index.xml` 含 `<?xml-stylesheet type="text/xsl" href="/rss.xsl"?>` 指令;`public/rss.xsl` 存在;浏览器直开渲染为 HTML。

- [ ] **Step 1: 创建 `static/rss.xsl`**

用 Write 工具写入(Unix-LF):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="zh-cn">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="/rss/channel/title"/> · RSS</title>
        <style>
          body{max-width:760px;margin:2.5rem auto;padding:0 1rem;
            font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
            color:#222;line-height:1.6;background:#fafafa}
          .banner{background:#f4a261;color:#fff;padding:.6rem 1rem;border-radius:8px;
            font-size:.9rem;margin-bottom:1.5rem}
          h1{font-size:1.6rem;margin:.2rem 0}
          .desc{color:#666;margin-bottom:1.5rem}
          ul{list-style:none;padding:0}
          li{padding:1rem;background:#fff;border:1px solid #eee;border-radius:8px;margin-bottom:.8rem}
          li a{font-size:1.1rem;font-weight:600;color:#1d6fb8;text-decoration:none}
          li a:hover{text-decoration:underline}
          .date{display:block;color:#999;font-size:.85rem;margin-top:.3rem}
        </style>
      </head>
      <body>
        <div class="banner">📡 这是 RSS 订阅源。复制本页网址到 Feedly / Inoreader 等阅读器即可订阅。</div>
        <h1><xsl:value-of select="/rss/channel/title"/></h1>
        <p class="desc"><xsl:value-of select="/rss/channel/description"/></p>
        <ul>
          <xsl:for-each select="/rss/channel/item">
            <li>
              <a href="{link}"><xsl:value-of select="title"/></a>
              <span class="date"><xsl:value-of select="pubDate"/></span>
            </li>
          </xsl:for-each>
        </ul>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
```

- [ ] **Step 2: 创建 `layouts/_default/rss.xml`(覆盖 Hugo 内置 RSS,注入样式表指令)**

用 Write 工具写入(Unix-LF)。基于 Hugo 内置 RSS 模板,首行加 `xml-stylesheet` 处理指令:

```go-html-template
{{- $pctx := . -}}
{{- if .IsHome -}}{{ $pctx = .Site }}{{- end -}}
{{- $pages := slice -}}
{{- if or $.IsHome $.IsSection -}}
{{- $pages = $pctx.RegularPages -}}
{{- else -}}
{{- $pages = $pctx.Pages -}}
{{- end -}}
{{- $limit := .Site.Config.Services.RSS.Limit -}}
{{- if ge $limit 1 -}}
{{- $pages = $pages | first $limit -}}
{{- end -}}
{{- printf "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>" | safeHTML }}
{{- printf "<?xml-stylesheet type=\"text/xsl\" href=\"%s\"?>" (absURL "rss.xsl") | safeHTML }}
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{{ if eq .Title .Site.Title }}{{ .Site.Title }}{{ else }}{{ with .Title }}{{ . }} on {{ end }}{{ .Site.Title }}{{ end }}</title>
    <link>{{ .Permalink }}</link>
    <description>Recent content {{ if ne .Title .Site.Title }}{{ with .Title }}in {{ . }} {{ end }}{{ end }}on {{ .Site.Title }}</description>
    <generator>Hugo</generator>{{ with .Site.LanguageCode }}
    <language>{{ . }}</language>{{ end }}{{ with .Site.Params.author }}
    <managingEditor>{{ . }}</managingEditor>{{ end }}{{ with .Site.Params.author }}
    <webMaster>{{ . }}</webMaster>{{ end }}{{ with .Site.Copyright }}
    <copyright>{{ . }}</copyright>{{ end }}{{ if not .Date.IsZero }}
    <lastBuildDate>{{ .Date.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</lastBuildDate>{{ end }}
    {{- with .OutputFormats.Get "RSS" -}}
    {{ printf "<atom:link href=%q rel=\"self\" type=%q />" .Permalink .MediaType | safeHTML }}
    {{- end -}}
    {{ range $pages }}
    <item>
      <title>{{ .Title }}</title>
      <link>{{ .Permalink }}</link>
      <pubDate>{{ .Date.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</pubDate>
      {{ with .Site.Params.author }}<author>{{ . }}</author>{{ end }}
      <guid>{{ .Permalink }}</guid>
      <description>{{ .Summary | html }}</description>
    </item>
    {{ end }}
  </channel>
</rss>
```

- [ ] **Step 3: 重建并校验 RSS**

Run:
```bash
cd /Users/ethanhu/Documents/self/my_blog
rm -rf public && /opt/homebrew/bin/hugo 2>&1 | grep -iE "ERROR" || echo "build clean"
echo "=== 样式表指令注入? ==="
grep "xml-stylesheet" public/index.xml
echo "=== rss.xsl 已输出? ==="
ls public/rss.xsl
echo "=== RSS 仍合法(有 channel/item)? ==="
grep -cE "<item>" public/index.xml
```
Expected: build clean;`index.xml` 含 `<?xml-stylesheet type="text/xsl" href=".../rss.xsl"?>`;`public/rss.xsl` 存在;`<item>` 数 > 0 且不含被忽略的 prompts/outline 条目。

- [ ] **Step 4: 浏览器目视确认**

`/opt/homebrew/bin/hugo server -D` 已在运行(或重启它)。浏览器打开 http://localhost:1313/index.xml。
Expected: 显示美化的文章列表页(橙色提示条 + 文章卡片 + 日期),而非裸 XML。

- [ ] **Step 5: 提交**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add static/rss.xsl layouts/_default/rss.xml
git commit -m "feat: RSS加XSL样式表,浏览器直开显示美化文章列表"
```

---

## Task 3: 提交设计文档与计划

**Files:**
- 已存在: `docs/superpowers/specs/2026-06-25-fix-archive-rss-design.md`
- 已存在: `docs/superpowers/plans/2026-06-25-fix-archive-rss.md`(本文件)

**Interfaces:**
- Consumes: 无。
- Produces: 文档入库。

- [ ] **Step 1: 提交(spec 已在 brainstorming 阶段提交,仅补提交本计划)**

```bash
cd /Users/ethanhu/Documents/self/my_blog
git add docs/superpowers/plans/2026-06-25-fix-archive-rss.md
git commit -m "docs: 子项目E实施计划"
```

---

## 完成标准(整体)

1. `hugo` 构建无 ERROR,Pages 数较基线下降约 53。
2. 归档页无 `0001` 年份桶;文章列表/搜索/RSS 不含 prompts/outline/README/演讲稿。
3. 浏览器开 `/index.xml` 为美化页;原始 `index.xml` 仍为合法 RSS 2.0 且含 `xml-stylesheet` 指令。
4. 改动分任务提交;文档入库。

## Self-Review(已执行)

- **Spec coverage:** spec 两处改动 → Task 1(ignoreFiles)、Task 2(RSS XSL)逐一对应;Task 3 收尾。无遗漏。
- **Placeholder scan:** 无 TBD;`rss.xsl`、`rss.xml` 给出完整文件内容;`ignoreFiles` 给出精确 old/new;验证步骤含确切命令与预期。
- **Type consistency:** `ignoreFiles` 四条正则在 spec/plan 一致;`rss.xsl` 路径(`static/rss.xsl` → 站点根 `/rss.xsl`)与 `rss.xml` 中 `absURL "rss.xsl"` 引用一致;XSL 取 `title/link/pubDate` 与 `rss.xml` 输出的字段一致。
