# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

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

### Post structure
Each post is a single Markdown file in `content/posts/<topic>/` plus a **sibling directory of the same base name** holding its images. Images are referenced with a relative path from the markdown file, e.g. `![alt](排序算法基础/image.png)`. This works because `hugo.toml`'s `[module]` block mounts `content` → `static`, so the content tree is served at the site root.

### Front matter (YAML) — follow the existing convention
```yaml
---
title: 【分类】文章标题        # bracketed category prefix is the house style
date: 2025-12-06T00:00:00+08:00
categories: ["算法刷题"]
tags: ["排序算法", "快排"]
description: "首段摘要，用于 SEO 和首页卡片"   # consumed by layouts/partials/head.html
cover: "/img/Algorithm.png"      # card image, lives in static/img/
headerImage: "/img/Makima.png"   # banner image
math: true                       # enable per-page MathJax
---
```
After the closing `---`, posts typically open with a `---` horizontal rule, a summary paragraph, then a `<!--more-->` truncation marker for the homepage excerpt. Topic-themed cover/header images already exist in `static/img/` — reuse them rather than adding new ones.

### Math
Math is rendered by MathJax (custom override in `layouts/partials/math.html`), gated by `math: true` in front matter and `math = true` in `hugo.toml`. Goldmark passthrough is enabled for `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, so write LaTeX directly in Markdown without escaping.

## Content Pipeline: `compress_images.py`
Run this after adding/editing posts and **before committing**. It performs three passes over `content/posts/`:
1. **Rename** top-level post dirs and `.md` files via `sanitize_name()`: lowercase, spaces/underscores → `-`, strips `【】()[]（）：:！!？?`. Records a name map.
2. **Repair links** — rewrites image paths inside every `.md` to match renamed folders, and lowercases `.JPG/.JPEG/.PNG` extensions.
3. **Compress** images (walks all subdirs): downscales to max width 2560px and re-encodes JPEG q80 / PNG optimized, but **only for files > 4 MB** (`MIN_SIZE_KB`).

Gotchas:
- The rename pass uses `os.listdir` (top level only); only the link-repair map covers nested names. New posts with CJK/bracketed names **will be renamed**, so commit the post and run this script together to avoid stale links.
- Editing markdown produces LF line endings — recent history shows CRLF caused Typora/YAML front-matter rendering issues, so keep files Unix-LF.

`temp_replace.py` and `batch-all.json` are one-off/ad-hoc tooling (a past link fixup script with a hardcoded Windows path, and an image-generation batch manifest); they are not part of the normal flow.

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
