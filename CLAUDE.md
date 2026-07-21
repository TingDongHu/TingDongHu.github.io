# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
Personal static blog (mostly Simplified Chinese content) built with Hugo **extended** edition, using the Dream theme v3.13.0. Pushing to `main` triggers GitHub Actions, which builds with `hugo --minify` and deploys to GitHub Pages at https://tingdonghu.github.io/. Content spans four areas: Computer Graphics, C++, LLM/Agent development, and Algorithms/essays.

## Common Commands
| Command | Purpose |
|---------|---------|
| `hugo server -D` | Local dev server with drafts at http://localhost:1313 |
| `hugo` | Build production site into `public/` |
| `python compress_images.py` | **Run before committing new content** — see Content Pipeline below |

The deploy workflow (`.github/workflows/hugo.yml`) pins Hugo to `latest` extended and requires it; the theme's CSS build needs the extended binary.

## Content Authoring

### Directory structure (reorganized 2026-07)
```
content/posts/
  llm/                  ← LLM / Agent / AI编程
  cpp/                  ← C++ 语言与设计模式
  computer-graphics/    ← 图形学 / 3D生成 / 3D视觉
  game-dev/             ← 虚幻引擎 / 游戏设计
  ml/                   ← 机器学习 / 深度学习 / ComfyUI
  algorithms/           ← 算法刷题
  dev-notes/            ← 博客搭建 / 杂项笔记
  essays/               ← 随笔
```

### File naming
- English kebab-case, e.g. `mcp-overview.md`, `unreal-gamemode-gamestate.md`
- No Chinese, spaces, or special characters in filenames

### Front matter (YAML) — follow the existing convention
```yaml
---
title: "【分类】文章标题"        # bracketed category prefix is the house style
date: 2025-12-06T00:00:00+08:00
categories: ["LLM"]               # must match target directory (see below)
tags: ["LLM", "Agent", "MCP"]     # first tag = category tag, then 1-3 technical tags
description: "首段摘要，用于 SEO 和首页卡片"   # consumed by layouts/partials/head.html
cover: "/img/Algorithm.png"       # card image, lives in static/img/
headerImage: "/img/Makima.png"    # banner image
math: true                        # enable per-page MathJax
---
```

Categories ↔ directory mapping:

| Directory | categories value |
|-----------|-----------------|
| `llm/` | `["LLM"]` |
| `cpp/` | `["C++"]` |
| `computer-graphics/` | `["计算机图形学"]` |
| `game-dev/` | `["游戏开发"]` |
| `ml/` | `["机器学习"]` |
| `algorithms/` | `["算法刷题"]` |
| `dev-notes/` | `["开发工具"]` |
| `essays/` | `["随笔"]` |

### Images
Images are served from **Cloudflare R2** CDN, **not** stored in the repo.
- New images: paste/screenshot in Typora → PicGo CLI auto-uploads to R2 → CDN URL inserted
- URL format: `https://pub-500a3a9e99b44ef29efa70fd87011d69.r2.dev/2026-07-20/{md5}.png`
- Do NOT use local relative paths for images
- **When writing with AI**: AI should output `![描述]` with empty path (no URL, no placeholder path). The user adds real images later in Typora.
- Cover/header images still live in `static/img/` (they're theme assets, not post content)

### Math
Math is rendered by MathJax (custom override in `layouts/partials/math.html`), gated by `math: true` in front matter and `math = true` in `hugo.toml`. Goldmark passthrough is enabled for `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, so write LaTeX directly in Markdown without escaping.

### New post workflow
1. `hugo new content posts/<dir>/<name>.md` — generates archetype with skeleton front matter
2. Write in Typora — paste images via PicGo (auto-uploads to R2)
3. Preview: `hugo server -D`
4. Commit and push to `main` → auto-deploys via GitHub Actions

### AI writing prompt
When asking AI to write or edit a post, reference `BLOG-STANDARDS.md` in the project root which contains the full writing convention. The key points are: YAML front matter with bracketed title, English kebab filename, R2 CDN image URLs, MathJax for formulas.

## Deleted content pipeline
`compress_images.py` was **deleted** (images are now on R2, no local compression needed). Don't try to run it. If adding new posts, just write and push — no preprocessing step needed.

## Theme Customization
Do **not** edit `themes/dream-3.13.0/` directly. Override instead:
- `layouts/partials/*.html` — overrides for `head.html` (meta/SEO, loads `css/output.css` built from the theme + `css/custom.css` + Mac-style chroma CSS), `math.html`, `scripts.html`.
- `assets/css/custom.css` — registered via `customCSS` in `hugo.toml`.
- `static/css/chroma-mac.css` + `static/js/chroma-mac.js` — macOS-window-style code blocks (works with Hugo's Chroma highlighter, configured under `[markup.highlight]`, style `monokai`).

Theme uses DaisyUI color schemes: `lightTheme = "emerald"`, `darkTheme = "forest"` in `hugo.toml`.

### Tailwind is pre-compiled — new utility classes silently do nothing
`css/output.css` is a **prebuilt** Tailwind/DaisyUI bundle shipped in the theme; the site build does **not** re-run Tailwind over your markup. So any utility class the theme didn't already use is absent from the CSS. Adding it in an overridden template (e.g. `layouts/_default/single.html`) leaves the class on the element with **no rule behind it** — the layout silently won't change. This bites arbitrary values especially (`grid-cols-[1fr_16rem]`, `max-h-[calc(100vh-2rem)]`), but also plain-but-unused utilities (`min-w-0`, `gap-8`, `lg:top-4`).
- Verify a class actually exists: `grep -o 'min-width:0' public/css/output.min.css` (search the compiled *property*, remember `:`→`\:` in class selectors).
- Fix pattern: put a **stable custom class** on the element in the template, then write **plain CSS** in `static/css/custom.css` (loaded last, always applies). The article/TOC two-column layout (`.dream-post-layout` / `.dream-post-toc`, with `min-width:0` on the article column to stop long titles stretching the `1fr` track) is done exactly this way.
- Local preview gotcha: don't run a production `hugo` build (`rm -rf public && hugo`) while `hugo server` is live — it desyncs the dev server and `/css/output.css` 404s, dropping all CSS. Use one or the other.
