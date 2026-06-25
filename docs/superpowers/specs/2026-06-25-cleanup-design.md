# 设计文档:工程清理(子项目 D)

- 日期:2026-06-25
- 状态:已确认,待实施
- 分支:建议新建 `feature/cleanup`(基于 H 合并后的 main)
- 所属:博客样式优化子项目 D(工程债清理)

## 背景与目的

子项目 H(标签治理)实施时暴露出 repo 的 git 大小写幻影问题:索引里有大量大写重复路径,macOS(大小写不敏感)磁盘只有一份小写真实文件。`git status`/`git diff` 文件数虚高,且 `git checkout` 大写路径会用旧 blob 覆盖磁盘真实文件(H 实施中曾因此翻车,audit 49→67 后重跑 apply 恢复)。

诉求:消除大小写幻影 + 顺手清理工程债,使 repo 在大小写敏感环境(GitHub Actions CI)也干净一致。

## 决策(已与用户确认)

- **核心:清 9 个安全域的大写幻影索引项**(507 文件),`git rm --cached`(只删索引、不碰磁盘小写真实文件)。
- **3DGenAI(91 文件)不动** —— 牵涉子项目 C(3dgenai 重构),且磁盘 `3dgenai/` 未跟踪;本次范围外。
- **工作区 24 个幻影域残留改动**:随 `git rm --cached` 一并清掉(小写真实版已在 H 提交)。
- **删废弃脚本**:`temp_replace.py`、`batch-all.json`。保留 `compress_images.py`/`retag.py`/`tag-map.json`。
- **补 .gitignore**:加 `.pytest_cache/`。
- **清空目录**:删空的 content 目录(如 `c++learncppdate`)。低优先,可选。
- **大写路径历史断点可接受**(自用博客)。
- ⚠️ **全程不 checkout、不动磁盘文件**;保持 `core.ignorecase=false` 以精确定位大写路径。

## 关键事实(已核实)

- `core.ignorecase=false`;macOS HFS+ 大小写不敏感 → 同一磁盘文件可被 git 以两种大小写路径跟踪。
- 幻影分布(git 有、磁盘 `os.listdir('content/posts')` 无的顶层域),共 **598 幻影文件**:
  - **9 个安全域(507 文件)**:`3DComputerVison`(4)、`AI编程`(1)、`Agent`(75)、`C++`(1)、`ComfyUI`(3)、`Games101笔记`(3)、`Hexo博客`(2)、`LLM`(1)、`MultiplayerCourse`(2)… 经核实每个幻影文件都有对应小写真实路径(删索引不丢内容)。
  - **3DGenAI(91 文件)**:无小写真实对应(磁盘 `3dgenai/` 未被 git 跟踪)。本次**不动**。
- 安全域幻影 blob 多为旧内容(如 Agent/agent 75 对中 67 同、8 个不同——不同的正是 H 标签改写动过的,小写真实版才是当前内容)。
- 磁盘真实顶层域全小写(18 个)。
- 工作区现 ~41 改动:大部分是幻影域路径(H 的 apply 改了磁盘文件,git 经大写路径也"看到"改动);其中 3DGenAI 6 个 + 3dcomputervison 等。
- 废弃脚本(CLAUDE.md 已标 ad-hoc):`temp_replace.py`(硬编码 `F:\Hugo_Blog\...` Windows 路径,移图引用一次性)、`batch-all.json`(3DGenAI 配图生成清单)。
- `.gitignore` 已忽略 public/、resources/、.venv/、__pycache__/、.DS_Store 等;**未显式忽略 `.pytest_cache/`**(H 跑 pytest 产生)。
- 空目录(部分):`content/posts/c++/c++learncppdate`、`content/posts/侯捷面向对象/c++复数类与字符串类` 等。

## 范围

### 包含
1. 写 `cleanup_case_dups.py`(或一次性脚本)—— 列出 9 个安全域的大写幻影索引路径,`git rm --cached` 移除(不动磁盘)。
2. 删 `temp_replace.py`、`batch-all.json`。
3. `.gitignore` 加 `.pytest_cache/`。
4. 删空 content 目录(可选,低优先)。

### 不包含
- **3DGenAI / 3dgenai**:留子项目 C(3dgenai 重构)。
- 不改 `core.ignorecase`。
- 不动磁盘上的任何真实内容文件(只动 git 索引 + 删废弃脚本/空目录)。
- 不改 `themes/`、不碰文章正文。

## 详细设计

### 组件 1:清大写幻影索引

**判定逻辑**(与 H 实施时一致):
- `disk = set(os.listdir('content/posts'))`(全小写真实域名)。
- 遍历 `git -c core.quotepath=false ls-files content/posts/`,顶层域名 `parts[2] not in disk` 即幻影路径。
- **排除 `3DGenAI`**(本次不动)。
- 其余幻影路径 → `git rm --cached --` 批量移除(分批避免命令行过长;路径含中文/特殊字符须正确转义,用 `-z`/pathspec-from-file 或逐条)。

**安全约束**:
- 只 `git rm --cached`(索引),**绝不** `rm`/`checkout`/`mv` 磁盘文件。
- 执行前 `git status` 确认磁盘小写真实文件完整(H 的标签改动已在 main)。
- 脚本 dry-run 先打印待删清单,人工核对全是大写幻影(无小写真实路径混入)再执行。

### 组件 2:删废弃脚本
- `git rm temp_replace.py batch-all.json`。

### 组件 3:.gitignore
- 追加 `.pytest_cache/`。

### 组件 4:空目录(可选)
- `find content/posts -type d -empty` 列出,确认非脚手架占位后删除。

## 验证方式

1. `git -c core.quotepath=false ls-files content/posts/ | awk -F/ '{print $3}' | sort -u` —— 9 域无大写变体,仅剩 `3DGenAI` 一个已知遗留(留 C)。
2. `git ls-files | sort | uniq -di` —— 大小写冲突仅剩 3DGenAI 相关(其余清零)。
3. `git status` 干净(仅 `?? content/posts/3dgenai/` 未跟踪)。
4. `git diff --cached --stat` —— 删除项全是大写幻影路径 + 两个废弃脚本,无磁盘真实文件被删。
5. `rm -rf public && hugo` 构建无 ERROR、无新增警告(磁盘未动,站点不变);页面数与清理前一致。
6. `temp_replace.py`/`batch-all.json` 已删;`.pytest_cache/` 被忽略。

## 风险与回滚

- 风险:中高。核心是 `git rm --cached` 507 索引项 + 工作区残留。
- 缓解:独立分支;dry-run 核对待删清单;脚本只匹配大写幻影(排除 3DGenAI、排除小写真实);全程不动磁盘。
- ⚠️ 教训(来自 H):`core.ignorecase=false` 下**绝不 checkout 大写幻影路径**(会用旧 blob 覆盖磁盘真实文件)。本次只 rm --cached。
- 回滚:`git reset` 取消未提交的 rm --cached;或 `git checkout HEAD~1 -- .gitignore temp_replace.py batch-all.json` 还原删除项。**注意回滚时同样不要 checkout 大写 content 路径**。

## 后续子项目
- **C**:3dgenai 重构(含把磁盘 `3dgenai/` 正式纳入 git + 清 3DGenAI 大写幻影)。
- **B**:图片优化,待排期。
