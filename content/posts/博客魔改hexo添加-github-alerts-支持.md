---
title: 【博客魔改】Hexo添加 Github alerts 支持
date: 2025-12-03T00:00:00+08:00
categories: ["Hexo博客"]
tags: ["blog", "css", "javascript", "markdown", "GitHub", "Alerts"]
description: "在Hexo博客中，通过更换Markdown渲染器为markdown-it并添加自定义解析脚本，即可便捷地使用类似[!NOTE]的语法创建GitHub风格的Alerts提示框。"
cover: "/img/BlogMakeover.png"
headerImage: "/img/Raythy.png"
math: true
--- 

 
> [!TIP]
>
> 一直很喜欢 Github 上的 [Alerts](https://github.com/orgs/community/discussions/16925)书写格式，非常简洁快捷，比hexo各类主题带的外挂标签方便很多，然后发现现在用的 hexo 主题并不支持解析该格式的语法。

给个示例：

```markdown
> [!NOTE]
> 这是一个注意事项提示框。这种提示框通常用于展示一般性的提示信息。
```

通过简单的引用加调用预设语法既可以写出好看的外挂标签的效果：

> [!note]
>
> 这是一个注意事项提示框。这种提示框通常用于展示一般性的提示信息。

参考[Hexo 美化：添加 Github alerts 支持 | Dogxi 的狗窝](https://blog.dogxi.me/hexo-github-alerts/)的博客做了一点魔改，在此记录一下，方便自己后续潜移修改。

## 配置步骤

### 1. 更换 Markdown 渲染器

Hexo 默认的 `marked`渲染器不支持此语法，需要更换为 `markdown-it`：

```bash
# 卸载默认渲染器
npm uninstall hexo-renderer-marked --save

# 安装 markdown-it 渲染器
npm install hexo-renderer-markdown-it --save
```

### 2. 创建解析脚本

在 Hexo 根目录创建脚本文件：`scripts/github-alerts.js`

```javascript
// GitHub Alerts 解析脚本
hexo.extend.filter.register('markdown-it:renderer', function (md) {
  md.core.ruler.after('block', 'github-alert', function (state) {
    const tokens = state.tokens
    for (let i = 0; i < tokens.length; i++) {
      if (tokens[i].type === 'blockquote_open') {
        // 找到 blockquote 的内容
        let j = i + 1
        // 只处理第一个段落
        if (
          tokens[j] &&
          tokens[j].type === 'paragraph_open' &&
          tokens[j + 1] &&
          tokens[j + 1].type === 'inline'
        ) {
          let content = tokens[j + 1].content.trim()
          // 兼容 [!NOTE]、[!NOTE]<br>、[!NOTE]\n
          const match = content.match(
            /^\[!(NOTE|WARNING|TIP|IMPORTANT|CAUTION|INFO|SUCCESS|ERROR)\][\s:：-]*(.*)$/i,
          )
          if (match) {
            const alertType = match[1].toLowerCase()
            let restContent = match[2].trim()

            // 给 blockquote_open 加 class
            let className = tokens[i].attrGet('class') || ''
            className += (className ? ' ' : '') + `alert alert-${alertType}`
            tokens[i].attrSet('class', className)

            if (restContent) {
              // [!NOTE] 和内容在同一行
              tokens[j + 1].content = restContent
            } else {
              // [!NOTE] 单独一行，移除该段
              tokens.splice(j, 3)
            }
          }
        }
      }
    }
  })
})
```

### 3. 创建样式文件

在 `source/css/github-alerts.css`创建样式文件：

```css
/* GitHub Alerts 样式 */
.alert {
  position: relative;
  margin: 1.5rem 0;
  padding: 1rem 1.5rem;
  border-left: 4px solid;
  border-radius: 8px;
  background: var(--card-bg);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.alert::before {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  display: block;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Lato, Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.alert p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

/* 各类型样式 */
.alert-note {
  border-color: #1e88e5;
  background: rgba(30, 136, 229, 0.05);
}
.alert-note::before {
  content: "💡 NOTE";
  color: #1e88e5;
}

.alert-warning {
  border-color: #ff9800;
  background: rgba(255, 152, 0, 0.08);
}
.alert-warning::before {
  content: "⚠️ WARNING";
  color: #ff9800;
}

.alert-tip {
  border-color: #00bcd4;
  background: rgba(0, 188, 212, 0.05);
}
.alert-tip::before {
  content: "💡 TIP";
  color: #00bcd4;
}

.alert-important {
  border-color: #e91e63;
  background: rgba(233, 30, 99, 0.05);
}
.alert-important::before {
  content: "❗ IMPORTANT";
  color: #e91e63;
}

.alert-caution {
  border-color: #ff5722;
  background: rgba(255, 87, 34, 0.08);
}
.alert-caution::before {
  content: "🔥 CAUTION";
  color: #ff5722;
}

.alert-info {
  border-color: #2196f3;
  background: rgba(33, 150, 243, 0.05);
}
.alert-info::before {
  content: "ℹ️ INFO";
  color: #2196f3;
}

.alert-success {
  border-color: #4caf50;
  background: rgba(76, 175, 80, 0.05);
}
.alert-success::before {
  content: "✅ SUCCESS";
  color: #4caf50;
}

.alert-error {
  border-color: #f44336;
  background: rgba(244, 67, 54, 0.08);
}
.alert-error::before {
  content: "❌ ERROR";
  color: #f44336;
}

/* 暗色模式适配 */
[data-theme="dark"] .alert {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .alert-note {
  background: rgba(30, 136, 229, 0.1);
}

[data-theme="dark"] .alert-warning {
  background: rgba(255, 152, 0, 0.1);
}

[data-theme="dark"] .alert-tip {
  background: rgba(0, 188, 212, 0.1);
}

[data-theme="dark"] .alert-important {
  background: rgba(233, 30, 99, 0.1);
}

[data-theme="dark"] .alert-caution {
  background: rgba(255, 87, 34, 0.1);
}

[data-theme="dark"] .alert-info {
  background: rgba(33, 150, 243, 0.1);
}

[data-theme="dark"] .alert-success {
  background: rgba(76, 175, 80, 0.1);
}

[data-theme="dark"] .alert-error {
  background: rgba(244, 67, 54, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .alert {
    margin: 1rem 0;
    padding: 0.8rem 1rem;
  }
}
```

### 4. 配置 Butterfly 主题

在 `_config.butterfly.yml`中添加 CSS 注入：

```yaml
inject:
  head:
    # 其他已有的CSS注入...
    - <link rel="stylesheet" href="/css/github-alerts.css">
```

### 5. 清理缓存并测试

```bash
hexo clean
hexo g
hexo s
```

创建测试文章验证效果：

```markdown
> [!NOTE]
这是一个注意事项提示框

> [!WARNING]
这是一个警告提示框

> [!TIP]
这是一个技巧提示
```

## 文件结构总结

整体修改的文件结构如下所示：

```
hexo-blog/
├── scripts/
│   └── github-alerts.js          # 解析脚本
├── source/
│   └── css/
│       └── github-alerts.css     # 样式文件
├── _config.butterfly.yml         # 主题配置（注入部分）
└── package.json                  # 依赖项
```

> [!Caution]
>
> 要注意：
>
> 1. **必须先更换渲染器**，否则脚本不会生效
> 2. **脚本文件必须在 `scripts/`目录下**
> 3. **CSS 路径使用 `/css/`而不是绝对路径**
> 4. **每次修改配置后需要执行 `hexo clean`**

效果示例：

> [!NOTE]
>
> 这是一个注意事项提示框。这种提示框通常用于展示一般性的提示信息。

> [!WARNING]
>
> 这是一个警告提示框。这种提示框通常用于警告用户注意潜在的问题。

> [!TIP]
>
> 这是一个提示框。这种提示框通常用于提供有用的小技巧和建议。