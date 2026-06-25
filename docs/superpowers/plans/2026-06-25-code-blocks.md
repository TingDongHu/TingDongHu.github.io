# 实施计划:代码块方案重做(子项目 G)

- 日期:2026-06-25
- 分支:`feature/code-blocks`(已建,基于 main)
- Spec:`docs/superpowers/specs/2026-06-25-code-blocks-design.md`
- 执行偏好:subagent-driven(cavecrew-builder 单文件改),改完本地 `hugo server` 微调,验证后提交。

## 前置状态

- 当前分支 `feature/code-blocks`,工作区 main 干净(仅 `content/posts/3dgenai/` 未跟踪,与本项目无关,勿提交)。
- 相关文件均已核实(见 spec「关键事实」)。
- ⚠️ 本地预览铁律:勿在 `hugo server` 运行时跑生产 `hugo`/`rm -rf public`,会致 `/css/output.css` 404 全站丢样式(见 memory `hugo-server-vs-production-build`)。预览用 `hugo server -D` 一种即可。

## 阶段 1:render hook(组件 1)

**文件:** 新建 `layouts/_default/_markup/render-codeblock.html`

**步骤:**
1. 写 hook,输出 spec「组件 1」的结构:`.code-block[data-lang]` > `.code-block__bar`(三色点 + `.code-block__lang` + 三按钮 wrap/copy/fold,`data-act`) + `.code-block__body`(`transform.Highlight (trim .Inner "\n") (.Type | default "text") "lineNos=false"`)。
2. 语言名 `{{ $lang := .Type | default "text" }}`,用于 `data-lang` 与标签文本。

**验证:** `hugo server -D` 起站,打开任一含代码的文章 → 看到 `.code-block` 包裹(F12),代码单列无行号,语法高亮在(配色此时可能未对,阶段 3 修)。math/mermaid 块仍正常(各自 hook 优先)。

## 阶段 2:JS 重写(组件 2)

**文件:** 重写 `static/js/chroma-mac.js`(整文件覆盖)

**步骤:**
1. 删旧三色点注入 + 旧复制逻辑。
2. 事件委托:`document.addEventListener('click', ...)`,按 `e.target.closest('[data-act]')` 的 `data-act` 分发:
   - `copy`:`closest('.code-block')` → `.code-block__body` `textContent` → `navigator.clipboard.writeText`;按钮文案临时"已复制"。
   - `wrap`:toggle `.code-block__body` 的 `is-wrap` 类;按钮态可切文案。
   - `fold`:toggle `.code-block` 的 `is-folded` 类;按钮文案折叠↔展开。
3. `DOMContentLoaded`:遍历 `.code-block`,`.code-block__body.scrollHeight > 480` 则加 `is-folded`(并把 fold 按钮文案设为"展开")。

**验证:** 复制不带行号/按钮字;长块默认折叠;点按钮三功能均生效。

## 阶段 3:CSS 重写(组件 3)

**文件:** 重写 `static/css/chroma-mac.css`(整文件覆盖)

**步骤:**
1. `.code-block` 容器 + `.code-block__bar` 头栏 + 三色点(复用 `.dot-red/-yellow/-green`)+ `.code-block__lang` + `.code-block__btn`。
2. `.code-block__body { overflow-x:auto }` + 内部 `.chroma/pre/code` 透明背景、padding、Fira Code 14px/1.6。
3. `.is-wrap pre, .is-wrap code { white-space:pre-wrap; word-break:break-word }`。
4. `.is-folded .code-block__body { max-height:300px; overflow:hidden }` + `::after` 渐隐遮罩。
5. One Dark 调色 token(`.k/.kd/.kr/.s*/.c*/.nf/.nc/.kt/.m*/.o/.p/.n*`)作用于 `.code-block__body .chroma`(从 custom.css 迁来)。

**验证:** 配色为 One Dark;头栏好看;折叠渐隐自然;折行/横滚切换正常。

## 阶段 4:清死代码(组件 4)

**文件:** `static/css/custom.css`

**步骤:**
1. 删第 1–130 行(旧 `.highlight`/Mac 表格/三色点/One Dark 整段)。
2. 删第 156–157 行(`.highlight{width:100%}` 补丁及其注释块)。
3. **保留**第 132 行起的 prose 紧凑排版 + 两列布局(子项目 F,勿动)。

**验证:** `grep -n 'mac-dots\|lntd\|\.highlight' static/css/custom.css` 无残留;`hugo server` 页面代码块仍正常(说明全靠新 chroma-mac.css)。

## 阶段 5:本地微调 + 全量验证

1. 逐项过 spec「验证方式」清单(长块折叠、复制干净、横滚/折行、math/mermaid 未波及、窄屏)。
2. 微调:折叠阈值(480px)、`max-height`(300px)、渐隐高度、头栏间距、按钮观感。
3. 停 `hugo server` 后单独跑一次 `rm -rf public && hugo` 确认生产构建无 ERROR/无新增警告(**勿与 server 并行**)。

## 阶段 6:提交

- `git add layouts/_default/_markup/render-codeblock.html static/js/chroma-mac.js static/css/chroma-mac.css static/css/custom.css docs/superpowers/`
- commit(normal 中文 message):`feat: 代码块改用 render hook 组件(折叠/软折行/复制/语言标签,去行号)`
- **不提交** `content/posts/3dgenai/`。
- 暂不合并 main(等用户验收)。

## 回滚

删 `layouts/_default/_markup/render-codeblock.html`;`git checkout feature/code-blocks -- static/js/chroma-mac.js static/css/chroma-mac.css static/css/custom.css`(或回 main)。
