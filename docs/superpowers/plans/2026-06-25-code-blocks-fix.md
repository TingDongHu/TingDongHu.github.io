# 修复计划:代码块组件未生效(子项目 G 续)

- 日期:2026-06-25
- 分支:`feature/code-blocks`(承接 commit `d679384`)
- 关联:`docs/superpowers/specs/2026-06-25-code-blocks-design.md`、`docs/superpowers/plans/2026-06-25-code-blocks.md`

## 现象(用户实测)

- 行号已去掉 ✅(新 render hook 的 HTML 生效)。
- 但代码块**无深色头栏**;三色点不可见;语言名 + 三个按钮以**裸文本**形式暴露在正文里。
- 按钮**点不动**,无任何交互(复制/折叠/软折行均无反应)。
- Console:`alpinejs` integrity 校验失败被 block(主题自带,**与代码块无关**);其余为慢网字体 fallback 提示,非错误。

## 根因(已核实)

HTML 是新结构(`.code-block`/`data-act`,curl 服务端确认是真 `<button>` 标签),但 `.code-block` 的 **CSS 没上色、JS 没绑定**。

- 服务端 `static/css/chroma-mac.css` 与 `static/js/chroma-mac.js` curl 出来**都是新版**。
- 矛盾点:HTML 新、CSS/JS 行为旧 ⇒ **浏览器缓存了旧的 `chroma-mac.css` / `chroma-mac.js`**。
- 为何独独这两个文件被缓存:
  - 主题自带 css/js 走 **Hugo asset pipeline**(`resources.Get ... .RelPermalink`,见 `scripts.html:14,21`),输出**带指纹哈希**的文件名(`main.min.<hash>.js`),内容一变文件名就变,缓存天然失效。
  - 而 `chroma-mac.*` 是**裸 `static/` 路径**(`head.html:63` `/css/chroma-mac.css`、`scripts.html:24` `/js/chroma-mac.js`),**无指纹**。浏览器按 URL 缓存,旧版赖着不更新。
  - livereload 只热替了页面 HTML,没强制重取这两个 static 资源。

裸文本+点不动正是「旧 CSS 只认 `.highlight/.mac-dots`、旧 JS 只查 `.lntd`,对新 `.code-block` 结构完全无效」的表现。

## 立即验证根因(零改动)

浏览器 **Cmd+Shift+R 硬刷** `localhost:1313` 一篇含代码块的文章:

- **头栏出现 + 按钮可点** → 确诊纯缓存,核心代码无 bug → 执行阶段 1(根治缓存)。
- **硬刷后仍裸文本/点不动** → 另有真 bug → 跳「附:备用排查」。

> 本计划按「确诊为缓存」主线写;若硬刷后仍异常,先做备用排查再回主线。

## 阶段 1:根治缓存 —— chroma-mac.css/js 改走 asset pipeline 指纹

让两个文件与主题资源一样带哈希指纹,内容一改 URL 即变,浏览器永不吃陈旧缓存。

**步骤:**
1. 移动文件:`static/css/chroma-mac.css` → `assets/css/chroma-mac.css`;`static/js/chroma-mac.js` → `assets/js/chroma-mac.js`(`git mv`)。
2. `layouts/partials/head.html:63` 改为 pipeline + 指纹:
   ```go-html-template
   {{ $chromaCss := resources.Get "css/chroma-mac.css" }}
   {{ if hugo.IsProduction }}{{ $chromaCss = $chromaCss | minify | fingerprint }}{{ end }}
   <link rel="stylesheet" href="{{ $chromaCss.RelPermalink }}" />
   ```
3. `layouts/partials/scripts.html:24` 改为 pipeline + 指纹:
   ```go-html-template
   {{ $chromaJs := resources.Get "js/chroma-mac.js" }}
   {{ if hugo.IsProduction }}{{ $chromaJs = $chromaJs | minify | fingerprint }}{{ end }}
   <script src="{{ $chromaJs.RelPermalink }}" defer></script>
   ```
   - dev(非 IsProduction)不加指纹也无妨:Hugo dev 的 `.RelPermalink` 仍随内容变更触发 livereload 重取;但开发期最稳的是硬刷一次。
   - 顺序保持:`chroma-mac.css` 在 `output.css` 之后加载(覆盖关系不变);`chroma-mac.js` defer。

**验证:** `hugo server -D` 后**普通刷新**(非硬刷)文章:查看页面源码,`chroma-mac` 的 href/src 形如 `/css/chroma-mac.min.<hash>.css`;头栏深色出现、三色点在、按钮成形且可点(复制/折叠/软折行三功能生效);长块默认折叠。

## 阶段 2(可选,顺手):修 alpinejs integrity 报错

Console 里 alpinejs 因 `integrity` SHA256 不匹配被 block —— CDN 上 `alpinejs@3` 的内容与主题硬编码的哈希对不上(版本漂移)。代码块功能不依赖 alpine,但既然报错碍眼可顺手处理。

- 定位:`grep -rn 'alpinejs' layouts/ themes/dream-3.13.0/layouts/`。
- 该 `<script ... integrity="sha256-...">` 若在**主题**内 → 用 `layouts/partials/` 覆盖对应 partial,去掉 `integrity`/`crossorigin`,或把 `@3` 钉到具体小版本(如 `@3.14.1`)配对应哈希。
- **不改 `themes/` 源码**(铁律),只在 `layouts/` 覆盖。
- 若该脚本在 `head.html` 里(已被本仓覆盖)→ 直接在覆盖文件里修。
- **判断**:本子项目聚焦代码块。若 alpine 报错涉及主题其他功能、改动面大,**单列子项目**,本次仅记录不动。

**验证:** Console 无 alpine integrity 报错;主题原用到 alpine 的交互(如菜单/搜索)仍正常。

## 阶段 3:本地全量验证

普通刷新走一遍 spec「验证方式」:
- 头栏:三色点 + 居中语言标签 + 右侧三按钮,排版正常不溢出。
- 复制:剪贴板内容**不含行号/按钮文字**;按钮临时显「已复制」。
- 折叠:长块(>480px)默认折叠 + 底部渐隐;点「展开/折叠」切换。
- 软折行:长行默认横滚;点切换 pre-wrap,再点恢复。
- math/mermaid 块外观与改动前一致。
- 窄屏(<768)头栏紧凑、按钮不溢出。
- 停 server 后单独跑一次 `rm -rf public && hugo`,无 ERROR、无新增警告(`.Site.LanguageCode` 既有警告除外)。**勿与 server 并行**。

## 阶段 4:提交

- `git add` 改动:`assets/css/chroma-mac.css`、`assets/js/chroma-mac.js`(由 static 移入)、`layouts/partials/head.html`、`layouts/partials/scripts.html`、(阶段 2 若做)对应 partial、`docs/superpowers/`。
- 确认 `static/css/chroma-mac.css`、`static/js/chroma-mac.js` 已被 `git mv` 删除(无遗留)。
- commit(中文):`fix: chroma-mac.css/js 改走 Hugo asset pipeline 指纹,根治缓存致代码块组件不生效`。
- **不提交** `content/posts/3dgenai/`。
- 暂不合并 main(等用户验收)。

## 附:备用排查(仅当硬刷后仍异常)

按可能性排序:
1. **CSS 选择器没命中** — F12 选中头栏元素,看 `.code-block__bar` 规则有无应用、是否被划掉(specificity/`!important` 之争)。本仓 `chroma-mac.css` 无 `!important`,若被主题某规则压过,给关键规则提级或加 `!important`。
2. **`.code-block__body .chroma` 嵌套对不上** — 实际输出是 `.code-block__body > .highlight > .chroma`(见 commit 内 HTML),调色选择器是 `.code-block__body .chroma`(后代选择器,层级无碍)。确认无误即可。
3. **JS 没执行** — Console 输入 `document.querySelectorAll('[data-act]').length`,>0 说明节点在;再看事件委托是否绑上(本版用 `document` 上 click 委托,理论上对动态/静态节点都生效)。若为 0,是 hook 没渲染(回退看 HTML)。
4. **clipboard 仅 HTTPS/localhost 可用** — `navigator.clipboard` 在 `localhost` 可用、在 `http://` 局域网 IP(`--bind 0.0.0.0` 后用 IP 访问)被禁。验证复制功能请用 `localhost:1313`,勿用 `192.168.x.x:1313`。

## 回滚

- `git mv` 回 `static/`;`git checkout feature/code-blocks -- layouts/partials/head.html layouts/partials/scripts.html`。
