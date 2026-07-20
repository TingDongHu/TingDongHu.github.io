---
title: "【计算机图形学】双树遍历与自碰撞：BVH 加速的穿插检测体系"
date: 2026-06-04T00:00:00+08:00
categories: ["计算机图形学"]
tags: ["计算机图形学", "3D验证", "BVH"]
description: "BVH 双树遍历实现穿插检测（O(n²) → O(n log n)），自碰撞检测的核心原理与实现。"
cover: "/img/ComputerGraphics.png"
headerImage: "/img/Makima.png"
math: true
---


> BVH 树不只能加速射线查询——当两棵 BVH 树同时遍历时，它把"两个模型有没有穿插"从 O(n²) 降到 O(n log n)。而自碰撞检测的核心巧妙之处在于：同一棵树的左右子树互检，递归下去就能覆盖所有三角面对。

## 为什么需要这个？

前面学了 BVH 树的构建和射线查询加速，但 3D 几何验证的核心场景不只是"一个点在不在模型内部"，更常见的是：**两个模型有没有穿插？模型自己有没有穿插？**

这两个问题的暴力解法都是 O(n²)——10 万面的模型，两两检查就是 100 亿次。BVH 的层级包围盒结构天然适合做这件事：大部分三角面对在高层就被 AABB 排除了，实际需要精确检查的只有极少数。

> 💡 *我当时的问题："BVH 是找到最近的节点就停吗？"——把射线查询（找最近交点）和面-面检测（找有没有任何交点）混在一起了。这是两个不同的任务，BVH 对两者都能加速，但遍历逻辑不同。*

## 核心概念

### 双树遍历：两个 BVH 树同时走

两个模型各有一棵 BVH 树，从根节点开始同时往下走。每一步检查两个节点的 AABB 是否重叠：

```python
def aabb_overlap(boxA, boxB):
    """两个AABB是否重叠（三轴都要有交集）
    boxA, boxB: (min_xyz, max_xyz) 各为 np.array shape [3]
    """
    for i in range(3):  # x, y, z
        if boxA[1][i] < boxB[0][i] or boxB[1][i] < boxA[0][i]:
            return False
    return True
```

AABB 永远是三维的，不管构建 BVH 时用哪个轴切分。切分轴只决定"怎么把三角面分成两组"，但每个节点的包围盒是包裹所有三角面的最小三维盒子。

> 🧭 *引导过程：用户问"如果两个几何体的划分坐标不同怎么办？"——这是一个很好的直觉，但 AABB 的三维属性让它不影响重叠检测。划分轴是构建策略，AABB 是查询工具，两者解耦。*

### 三种递归情况

双树遍历的递归逻辑有三种情况，取决于当前两个节点的类型：

```python
def intersect_bvh(nodeA, nodeB):
    """双树遍历：检测两个BVH树所代表的几何体是否相交"""
    # 第1步：AABB不重叠 → 剪枝
    if not aabb_overlap(nodeA.aabb, nodeB.aabb):
        return False

    # 第2步：都是叶子 → 实际检查三角面
    if is_leaf(nodeA) and is_leaf(nodeB):
        return check_triangle_pairs(nodeA.triangles, nodeB.triangles)

    # 第3步：递归（三种情况）
    # 情况1：都有子节点 → 4种组合
    if not is_leaf(nodeA) and not is_leaf(nodeB):
        if intersect_bvh(nodeA.left, nodeB.left): return True
        if intersect_bvh(nodeA.left, nodeB.right): return True
        if intersect_bvh(nodeA.right, nodeB.left): return True
        if intersect_bvh(nodeA.right, nodeB.right): return True
        return False

    # 情况2：A是叶子，B不是 → A和B的子节点分别比
    if is_leaf(nodeA):
        if intersect_bvh(nodeA, nodeB.left): return True
        if intersect_bvh(nodeA, nodeB.right): return True
        return False

    # 情况3：B是叶子，A不是 → B和A的子节点分别比
    if intersect_bvh(nodeA.left, nodeB): return True
    if intersect_bvh(nodeA.right, nodeB): return True
    return False
```

> ⚡ *踩坑记录：最初只写了"4种组合"的情况，测试发现永远返回 False。原因是测试数据中一个模型只有 2 个面（叶子节点），另一个模型有 3 个面（内部节点），叶子节点没有 left/right 子节点，4 种组合全部跳过。必须处理"一叶一内部"的不对称情况。*

为什么是 4 种组合？因为二叉 BVH 每个节点有 2 个子节点，两棵树对比就是 2×2=4。如果用 8 叉 BVH（GPU 优化常用），就是 8×8=64 种组合。这是**宽度 vs 深度**的工程权衡。

### 早停优化

如果目标只是"有没有穿插"（不需要找全部交点），找到一对相交的三角面就可以立即返回 True：

```python
def check_triangle_pairs(trisA, trisB):
    """两组三角面是否有相交（AABB重叠近似）"""
    for triA in trisA:
        for triB in trisB:
            boxA = (np.min(triA, axis=0), np.max(triA, axis=0))
            boxB = (np.min(triB, axis=0), np.max(triB, axis=0))
            if aabb_overlap(boxA, boxB):
                return True  # 早停：找到一个就返回
    return False
```

### 自碰撞检测：同一棵树的左右互检

自碰撞检测的核心问题是：只有一个模型，只有一棵 BVH 树，怎么检查"自己和自己有没有穿插"？

答案是：**从根节点开始，只比较左右子树**。

```python
def self_intersect(node):
    """自碰撞检测：检查同一棵BVH树内部是否有三角面相交"""
    # 1. 左子树内部有没有自碰撞？
    if not is_leaf(node.left):
        self_intersect(node.left)
    # 2. 右子树内部有没有自碰撞？
    if not is_leaf(node.right):
        self_intersect(node.right)
    # 3. 左子树 vs 右子树有没有碰撞？
    intersect_bvh(node.left, node.right)
```

为什么只比较左右子树？因为 BVH 构建时左右子树是按空间切分的，它们代表模型的不同区域。递归下去，最终会覆盖所有"不同区域"的三角面对。

> 🧭 *引导过程：用户提出了一个深刻的问题——"BVH 按空间划分，重叠的部分会被分到一块，这样的检测有意义吗？"答案是：即使交叉的三角面在某一层被分到同一棵子树，递归到更深层时它们一定会被分到不同的叶子节点。BVH 的递归切分保证了任意两个三角面最终都会在某一层的"左 vs 右"比较中被检查到。*

## 任务对比：射线-面 vs 面-面

BVH 加速的两种典型任务：

| 任务 | 输入 | 输出 | BVH 遍历方式 |
|------|------|------|-------------|
| 点在模型内？ | 射线 + mesh | 所有交点（奇偶判定） | 单树遍历，找所有命中节点 |
| 两个模型穿插？ | mesh A + mesh B | 有没有任何交点 | 双树遍历，AABB 剪枝 + 早停 |
| 模型自碰撞？ | mesh | 有没有任何交点 | 左右子树互检 + 递归 |

三者共享同一套 AABB 重叠检测和三角面对检查逻辑，区别在于遍历策略。

## 完整验证流程回顾

阶段 2 学习的 6 个概念构成了 3D 几何验证的完整工具链：

```
模型完整吗？ → 水密性检测（找边界边）
    ↓
法线对不对？ → 法线一致性（质心法 / 绕序传播 / 射线种子）
    ↓
自己有没有穿插？ → 自碰撞检测（BVH 左右互检）
    ↓
和其他模型有没有穿插？ → 穿插检测（射线奇偶 + 面-面相交）
    ↓
所有检测都可以用 BVH 加速
```

依赖关系：水密性 → 法线一致性（需要水密才能传播）→ 穿插检测（需要正确法线才能判断内外）。

## 常见误区

- **"BVH 找到最近节点就停"**：那是射线追踪的优化。面-面检测需要找"有没有任何交点"，不是"最近交点"
- **"4 种组合就够了"**：只适用于两棵树都是内部节点的情况。遍历过程中经常出现"一叶一内部"，需要 2 种组合
- **"自碰撞直接套双树遍历"**：不能用同一棵树的同一个节点和自己比，只能比较兄弟子树
- **"AABB 重叠 = 三角面相交"**：AABB 重叠只是必要条件，不是充分条件。重叠了还需要精确的面-面检测

## 延伸阅读

- [BVH Traversal — PBRT](https://pbrt.org/chapters/pbrt_chapter4.pdf) — 物理渲染器中的 BVH 遍历实现，包含 SAH 优化
- [Self-Collision Detection for Deformable Meshes — Bridson et al.](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2003-collisioncloth.pdf) — 布料自碰撞检测的经典论文
- [trimesh 文档 — Collision](https://trimesh.org/trimesh.collision.html) — trimesh 碰撞检测 API

---
*基于 2026-06-04 学习 session 生成 · 时长 45 分钟 · 阶段2完成*
