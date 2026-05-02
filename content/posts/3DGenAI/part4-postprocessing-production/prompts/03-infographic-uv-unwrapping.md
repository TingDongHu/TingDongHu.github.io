---
illustration_id: 03
type: infographic
style: vector-illustration
palette: macaron
---

UV展开数学原理 - Infographic View

STEP 1: 3D表面 (3D Surface)
- 输入: 三角网格M = (V, F)
- 目标: 寻找映射 φ: M → [0,1]²
- 约束: 畸变最小化

STEP 2: 接缝切割 (Seam Cutting)
- 选择切割线: 沿特征边/曲率高处
- 切割后: 流形可展开为拓扑圆盘
- 关键: 切割线选择影响畸变分布
- 自动方法: 基于最短路径/最小生成树

STEP 3: 展开扁平化 (Flattening)
- LSCM (最小二乘保角映射):
  最小化角度畸变 E = Σ|∂u/∂x - ∂v/∂y|² + |∂u/∂y + ∂v/∂x|²
  Cauchy-Riemann方程满足时畸变为零
- ABF++ (基于角度):
  优化三角形内角, 约束: 内角和=π, 顶点环绕角和=2π
- 畸变量度:
  面积畸变: σ₁σ₂ (Jacobian行列式, 偏离1=拉伸/压缩)
  角度畸变: σ₁/σ₂ (偏离1=扭曲, =1为保角)

STEP 4: [0,1]²纹理空间打包 (Packing)
- UV岛排列在[0,1]²纹理空间
- texel密度一致性: 确保不同UV岛的纹理分辨率均匀
- UV利用率: >75%纹理空间被有效使用
- 避免: 重叠、镜像翻转、边界接缝

ARROW FLOW: 3D表面 → 接缝切割 → 扁平展开 → 纹理空间打包

ANNOTATIONS:
- 展开前后对比: 3D弯曲表面 vs 2D平面UV岛
- 畸变热力图: 绿色=低畸变, 红色=高畸变

Flat vector infographic with horizontal flow. Clean sequential layout.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Blue (#A8D8EA) for 3D surface, Mint (#B5E5CF) for cutting, Lavender (#D5C6E0) for flattening, Peach (#FFD5C2) for packing, Coral Red (#E8655A) for distortion formulas, Mustard Yellow (#F2CC8F) for quality thresholds (75%)
ELEMENTS: Horizontal 4-stage pipeline, mini 3D→2D transformation diagram in step 3, UV island layout diagram in step 4, distortion heat map legend, formula cards for LSCM/ABF++
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
