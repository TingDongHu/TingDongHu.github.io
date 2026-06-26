# 子项目 C:3D GenAI 六部曲 git 归位 — 设计文档

## 背景

3D GenAI 六部曲（part1–part6）系列文章**已在线上发布**:

- `origin/main` 跟踪 `content/posts/3DGenAI/`(大写,91 个文件),提交于 `92095df`
- 线上 `https://tingdonghu.github.io/posts/3dgenai/part1-...` 返回 200(Hugo 生成的 URL 本就是小写)

但本地工作区存在长期未解决的混乱,需要一次性归位。

## 问题清单

### 1. 大小写碰撞(核心)

- git 索引 / HEAD 跟踪 `content/posts/3DGenAI/`(大写)
- 磁盘实际是 `content/posts/3dgenai/`(小写,被 `compress_images.py` 的 `sanitize_name()` 改过)
- macOS 大小写不敏感文件系统 → git 永久报 `M content/posts/3DGenAI/*` + `?? content/posts/3dgenai/`
- 危险:误 `git checkout` 大写重影路径会用旧 blob 覆盖磁盘真实文件(已有踩坑记录)
- 这是此前定下"不提交 content/posts/3dgenai/"规则的根本原因——怕在其他子项目里误操作

### 2. 未提交的新内容

- 磁盘小写版 `part*.md` 有 2026-06-25 的新编辑(每篇小幅 diff),从未提交
- 线上仍是旧版

### 3. 生成脚手架混在 content 下

- 39 个 `prompts/*.md`(配图生成提示词)
- 6 个 `outline.md`(各部分大纲)
- 1 个 `batch.json`(图片生成批处理清单)
- 1 个 `README.md`
- 空目录 `3DGenAIimg/`
- `.DS_Store`
- 这些是 AI 配图生成的输入物,不渲染成页面(实测访问返回 404),但污染仓库

### 4. 图片偏重

- 38 张 PNG,共 26MB,每张约 700KB,尺寸 1376×768(信息图,含文字)
- `compress_images.py` 阈值是 4MB,碰不到这些

## 决策(已与用户确认)

| 维度 | 决策 |
|------|------|
| 核心目标 | 完整重构(一次做透) |
| 脚手架 | **直接删除**(prompts / outline / batch.json / README / 3DGenAIimg / .DS_Store) |
| 图片压缩 | **pngquant 量化压缩**(8-bit 调色板,保尺寸,文字清晰,~70% 减) |
| 大小写 | 大写 `3DGenAI` → 小写 `3dgenai` git 归一 |

## 方案

### 核心:大小写归一(安全两步法)

磁盘本就是小写,索引是大写,两版内容几乎一致。用纯索引操作完成切换,**不触碰磁盘**,因此零 checkout 风险:

```bash
git rm -r --cached content/posts/3DGenAI   # 仅从索引删大写重影,--cached 不动磁盘
git add content/posts/3dgenai              # 加入小写磁盘文件(已最新 + 压缩 + 清理)
```

git 会自动把 `3DGenAI/x` → `3dgenai/x` 识别为 rename。此步同时纳入新内容(因为 add 的是当前磁盘)。

### 执行顺序

1. 创建分支 `feature/3dgenai`
2. `brew install pngquant`
3. 删脚手架(磁盘):39 prompts + 6 outline.md + batch.json + README.md + 空 3DGenAIimg/ + .DS_Store
4. pngquant 压缩 38 张 PNG(原地,保尺寸)
5. 抽查压缩后文字清晰度
6. 索引归一(上面两步 git 命令)
7. `.DS_Store` 加进全局 `.gitignore`
8. 验证:`git status` 无 ghost 噪声、本地 build 通过、六部曲页面图片正常
9. 提交 → PR → 合并(触发部署,线上更新为新版)

## 验收标准

- `git status` 中 `content/posts/3DGenAI/`(大写)条目完全消失,只剩小写或干净
- `git ls-files | grep 3DGenAI`(大写)返回空,`grep 3dgenai`(小写)返回 ~44 个(md + 压缩图,无脚手架)
- 本地 `hugo` 生产构建无 error
- 六部曲 6 篇页面正文图片全部正常加载,文字清晰
- 仓库内不再有 prompts / outline.md / batch.json / README.md / .DS_Store(3dgenai 下)
- 图片总体积显著下降(目标 26MB → 10MB 内)

## 风险与边界

- **pngquant 有损**:量化后逐张抽查信息图文字是否糊;不可接受则该张回退原图或降低压缩率
- **误伤其他路径**:`git rm --cached` 严格限定 `content/posts/3DGenAI`,操作后核对 staged 列表只含 3dgenai 相关
- **不碰其他重影**:全程不动 `content/posts/` 下其他大小写重影路径(留给子项目 D)
- **分支隔离**:全程在 `feature/3dgenai`,不直接推 main

## 不在范围内

- 其他 507 个大小写重影路径的清理(子项目 D)
- 六部曲正文内容的实质性改写(只做归位,不改文字)
- 系列文章的 SEO / 导航 / 分类页优化
