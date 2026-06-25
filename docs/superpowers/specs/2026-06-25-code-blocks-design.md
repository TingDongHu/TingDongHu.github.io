# 设计文档:代码块方案重做(子项目 G)

- 日期:2026-06-25
- 状态:已确认,待实施
- 分支:`feature/code-blocks`
- 所属:博客样式优化子项目 G(样式问题清单第 3 项)

## 背景与目的

博客自用复习。当前代码块问题(#3):

1. 不能折叠 —— 长代码块占满屏幕,影响阅读流。
2. 横向滚动体验差 —— `lineNumbersInTable=true` 生成两列表格,长行横滚时行号列跟着乱,复制还会混进行号。
3. 可读性差,且现方案是手写散件(`chroma-mac.js` DOM 注入 + 两份 CSS 各改 `.highlight`,重复/打架隐患)。

诉求:用一个干净的"模组"替换手写散件,支持复制、语言标签、折叠/展开、软折行切换。

## 决策(已与用户确认)

- **路线 A:Hugo codeblock render hook(服务端)**。保留 Chroma 服务端高亮(无 FOUC、无运行时依赖),用 render hook 把代码块包成统一组件。否决客户端库(Prism/highlight.js):需关掉 Chroma 改客户端重新高亮 → FOUC + 体积,且折叠在任何方案里都得自定义。
- **功能:** 复制按钮、语言标签、折叠/展开、软折行切换。
- **行号:去掉**(hook 内传 `lineNos=false`,单列布局;横滚/复制最干净)。
- **配色:** 代码块恒为深色(One Dark),不跟随浅色主题——与现状一致,简单。

## 关键事实(已核实)

- Hugo Chroma 服务端高亮:`hugo.toml` `[markup.highlight]` 现为 `lineNos=true`、`lineNumbersInTable=true`、`noClasses=false`(class 模式)、`guessSyntax=true`、`style="monokai"`。
- 现有散件:
  - `layouts/partials/head.html:63` 加载 `/css/chroma-mac.css`。
  - `layouts/partials/scripts.html:24` 加载 `/js/chroma-mac.js`(defer)。
  - `static/css/chroma-mac.css` + `static/css/custom.css` 第 1–130 行**都在改 `.highlight`**(Mac 三色点 + One Dark)。`custom.css` 第 156–157 行另有 `.highlight { width:100% }` 补丁。
- 主题 render hooks:`themes/dream-3.13.0/layouts/_default/_markup/` 含 `render-codeblock-math.html`、`render-codeblock-mermaid.html`(**type 专属,优先级高于通用 hook**),但**无通用 `render-codeblock.html`**。
- `noClasses=false` ⇒ Chroma 输出 class 化 span(`.k/.s/.c/.nf/.nc/.m/.o/.p/.n…`),`custom.css` 第 96–105 行的 One Dark 调色规则对单列布局同样生效。

## 范围

### 包含
1. 新建 `layouts/_default/_markup/render-codeblock.html` —— 通用代码块组件。
2. 重写 `static/js/chroma-mac.js` —— 复制 / 软折行 / 折叠 / 自动折叠,删旧 DOM 注入逻辑。
3. 重写 `static/css/chroma-mac.css` —— `.code-block` 组件样式 + 保留 One Dark 调色 token。
4. 删 `static/css/custom.css` 第 1–130 行(旧 Mac 表格样式)+ 第 156–157 行(`.highlight` 宽度补丁)。
5. 本地 `hugo server` 实时微调(折叠阈值、间距、配色)。

### 不包含
- `hugo.toml` `[markup.highlight]` 的 `lineNos/lineNumbersInTable` 不必改(hook 内显式传 `lineNos=false` 为准);如顺手可设 `lineNos=false` 但非必须。
- 浅色主题代码块配色(YAGNI,恒深色)。
- 其余清单项(标签 #6 → H、about #7 → I)。
- 不改 `themes/dream-3.13.0/` 源码(仅在 `layouts/` 覆盖)。

## 详细设计

### 组件 1:`layouts/_default/_markup/render-codeblock.html`

通用 codeblock render hook,截获所有围栏代码块(math/mermaid 由 type 专属 hook 处理,不受影响)。内部调 `transform.Highlight` 拿单列 Chroma HTML,外包统一结构。

输出结构:
```
<div class="code-block" data-lang="{{ lang }}">
  <div class="code-block__bar">
    <span class="code-block__dots"><i class="dot-red"></i><i class="dot-yellow"></i><i class="dot-green"></i></span>
    <span class="code-block__lang">{{ lang }}</span>
    <span class="code-block__actions">
      <button class="code-block__btn" data-act="wrap">软折行</button>
      <button class="code-block__btn" data-act="copy">复制</button>
      <button class="code-block__btn" data-act="fold">折叠</button>
    </span>
  </div>
  <div class="code-block__body">
    {{ transform.Highlight (trim .Inner "\n") (.Type | default "text") "lineNos=false" }}
  </div>
</div>
```
- 语言名:`.Type`,空则 `text`(`data-lang` 与 `.code-block__lang` 同源)。
- `lineNos=false` 选项确保单列;`noClasses` 沿用全局(class 化,配色靠 CSS)。
- 用 `.Position` 不必;`.Inner` 去首尾换行。

### 组件 2:`static/js/chroma-mac.js`(重写)

事件委托(`document` 上监听 `click`,按 `data-act` 分发),避免逐块绑定。逻辑:
- **copy**:取所在 `.code-block` 的 `.code-block__body` 的 `textContent`(单列无行号,天然干净),`navigator.clipboard.writeText`;成功临时改按钮文案为"已复制"。
- **wrap**:toggle `.code-block__body` 上 `is-wrap` 类(CSS 控制 `white-space: pre-wrap`)。
- **fold**:toggle `.code-block` 上 `is-folded` 类。
- **自动折叠**:`DOMContentLoaded` 时遍历 `.code-block`,若 `.code-block__body` 的 `scrollHeight > 阈值`(初值 ≈480px,约 25 行)则加 `is-folded`,并在折叠态按钮/角标显示行数提示(可选)。
- 删除旧三色点注入与旧复制逻辑(三色点改由 hook 静态输出 + CSS)。

### 组件 3:`static/css/chroma-mac.css`(重写)

- `.code-block`:深色容器(`#282c34`),圆角,阴影,`overflow:hidden`。
- `.code-block__bar`:`#21252b` 头栏,flex 两端对齐;三色点(复用旧 `.dot-red/.dot-yellow/.dot-green`)、语言标签居中或左、按钮组右。
- `.code-block__btn`:低调描边按钮,hover 提亮。
- `.code-block__body`:`overflow-x:auto`;内部 `.chroma/pre/code` 透明背景、`padding`、`font-family: 'Fira Code', Consolas, monospace`、`font-size:14px`、`line-height:1.6`。
- `.code-block__body.is-wrap pre, .is-wrap code { white-space: pre-wrap; word-break: break-word; }`。
- `.code-block.is-folded .code-block__body { max-height: ~300px; overflow:hidden; }` + 底部渐隐遮罩(`::after` 线性渐变)+ 折叠态按钮文案"展开"。
- **One Dark 调色 token**(`.k/.kd/.kr/.s.../.c.../.nf/.nc/.m/.o/.p/.n…`)从 `custom.css` 迁移/保留于此,作用于 `.code-block__body .chroma`。

### 组件 4:清死代码

- `static/css/custom.css` 删第 1–130 行(旧 `.highlight`/Mac 表格/三色点/One Dark)与第 156–157 行(`.highlight{width:100%}`)。**保留**第 132 行起的 prose 紧凑排版与两列布局段(子项目 F 成果,勿动)。

## 验证方式

1. `hugo` 构建无 ERROR、无**新增** deprecation 警告(主题 `baseof.html` 的 `site.LanguageCode` 既有警告除外)。
2. 本地 `hugo server -D` 打开含长代码块的文章(如 games101 / C++ 篇):
   - 头栏显示语言标签 + 三色点 + 三个按钮;
   - 复制 → 剪贴板内容**不含行号**、不含按钮文字;
   - 长代码块(>25 行)**默认折叠**,点折叠按钮可展开/收起;
   - 长行**默认横向滚动**;点"软折行"切换为折行,再点恢复;
   - math 块、mermaid 块外观与改动前一致(未被通用 hook 波及)。
3. 窄屏(<lg)正常:代码块单列全宽,头栏按钮不溢出。
4. 全站无残留旧 `.mac-dots`/表格行号样式。

## 风险与回滚

- 风险:中。render hook 截获**所有**代码块,需确认不破坏 math/mermaid(由 type 专属 hook 优先处理——已核实存在)。
- 调色迁移:`noClasses=false` 的 Chroma class 名需与 CSS 选择器对齐(沿用现有 token,低风险)。
- 自动折叠阈值/渐隐观感靠本地微调。
- 回滚:删 `layouts/_default/_markup/render-codeblock.html`;`git checkout` 还原 `chroma-mac.js`/`chroma-mac.css`/`custom.css`。

## 后续子项目
- **H**:标签治理(#6)。
- **I**:about 重做(#7)。
- 原始 B(图片)/C(3dgenai 重构)/D(工程清理)待排期。
