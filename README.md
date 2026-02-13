
   # 🚀 Shimizu Tou's Blog Source

   Hi,欢迎来到我的个人博客源码仓库！

---

   ## 📖 核心专栏

   * **计算机图形学 (Graphics)**: 记录 **Games101** 学习笔记，从光栅化到光线追踪的渲染实践。
   * **C++ 技术栈 (Cpp)**: 探索 C++ 底层原理、高性能编程、工程实践及内存管理。
   * **Agent 开发范式 (LLM & Agents)**: 关注大模型驱动的智能体开发实践、Prompt Engineering 与 RAG 架构。
   * **算法与随笔 (Algo & Thoughts)**: 记录日常开发中的算法沉淀与技术生活感悟。

---

   ## 🔗 快速访问

   * **在线博客地址**: [ShimizuTou'Blog](tingdonghu.github.io)
   * **联系作者**: [2680957536@qq.com]

---

   ## 🛠️ 技术架构

| 模块 | 技术选型 |
| :--- | :--- |
| **静态生成器** | [Hugo](https://gohugo.io/) |
| **主题** | [Dream](https://github.com/g1eny0ung/hugo-theme-dream) (Magical & Clean) |
| **部署方案** | GitHub Actions + GitHub Pages |
| **自动化工具** | `hugo_standardizer.py` (路径标准化与高保真压缩脚本) |

---

   ## 💻 本地开发环境配置

   如果你想在本地预览或参与贡献，请确保已安装 **Hugo (Extended 版)**。

   ### 1. 克隆仓库
   ```bash
   git clone [https://github.com/TingDongHu/TingDongHu.github.io.git](https://github.com/TingDongHu/TingDongHu.github.io.git)
   cd TingDongHu.github.io
   ```

   ### 2. 本地实时预览

   ```bash
   # 启动 Hugo 本地服务器，包含草稿内容预览
   hugo server -D
   ```

   访问地址: `http://localhost:1313`

   ### 3. 发布前准备 (重要)

   为了解决 Linux 服务器（GitHub Pages）的大小写敏感及特殊字符导致的图片 404 问题，**推送前必须运行标准化脚本**：

   ```bash
   # 执行路径标准化、链接修复及图片高保真压缩
   python hugo_standardizer.py
   ```

---

   ## 📂 仓库目录结构

   ```text
   .
   ├── content/posts/           # 博客文章源文件 (.md) 及图片资源
   ├── hugo_standardizer.py     # 核心自动化脚本
   ├── themes/dream/            # Dream 主题子模块
   ├── hugo.toml                # Hugo 全局配置文件
   └── .github/workflows/       # GitHub Actions 自动部署脚本
   ```

---

   ## 🚀 创作流 (Workflow)

   1. 在 `content/posts/` 下创建 `文章名.md` 和 `同名文件夹/` (存放图片)。
   2. 使用 Markdown 编写内容。
   3. git add. 自动运行 `python hugo_standardizer.py` **一键洗稿**（自动处理路径符号、小写化及图片压缩）。
   4. 执行 `git add .`、`git commit` 并推送至 `main` 分支。
   5. **GitHub Actions** 会自动触发构建并在 1 分钟内完成在线更新。

---

