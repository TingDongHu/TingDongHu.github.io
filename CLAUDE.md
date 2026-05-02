# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This is a personal static blog built with Hugo (extended edition), using the Dream theme v3.13.0. Deployed automatically to GitHub Pages via GitHub Actions when commits are pushed to the `main` branch.

## Common Commands
| Command | Purpose |
|---------|---------|
| `hugo server -D` | Start local development server with draft content preview, accessible at http://localhost:1313 |
| `hugo` | Build production static site to the `public/` directory |
| `python compress_images.py` | **Must run before committing new content**: Normalizes file/folder names (lowercase, special character removal), fixes internal Markdown links, and compresses images to avoid 404 issues on GitHub Pages and reduce file sizes |

## Key File Locations
- `content/posts/`: All blog post Markdown files and associated image assets (each post has a matching directory for images)
- `hugo.toml`: Global Hugo configuration file
- `compress_images.py`: Core automation script for content normalization
- `.github/workflows/hugo.yml`: GitHub Actions deployment workflow
- `themes/dream-3.13.0/`: Dream theme source code (avoid modifying directly, use overrides in `layouts/` and `assets/` when possible)
- `layouts/`: Custom Hugo template overrides
- `assets/`: Custom CSS/JS assets
- `static/`: Static assets (images, fonts, etc.) served at the root URL

## Important Notes
- All new posts should be created in `content/posts/` with a Markdown file and matching directory for images
- Always run `python compress_images.py` before committing new content to fix path issues and compress images
- Commits to the `main` branch trigger automatic deployment to https://tingdonghu.github.io/
- The blog focuses on 4 core content areas: Computer Graphics, C++ development, LLM/Agent development, and Algorithms/Technical Essays