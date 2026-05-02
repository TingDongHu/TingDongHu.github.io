---
illustration_id: 03
type: infographic
style: vector-illustration
palette: macaron
---

# 多视图几何与对极约束

## Layout
Three-panel layout: left panel shows pinhole camera model (world→camera→image), center panel shows epipolar geometry (two cameras + 3D point + epipolar lines), right panel shows SfM/MVS pipeline steps. Title "多视图几何" at top.

## ZONES
- **Title Zone**: Top center, "多视图几何" in large handwritten font with small camera icon
- **Left Panel - Camera Model**: Pinhole camera with 3D point X_w, projection through camera center to image plane
  - Show world coordinate frame and camera coordinate frame
  - Highlight the projection pipeline: X_w → [R|t] → X_c → K → (u,v)
- **Center Panel - Epipolar Geometry**: Two camera icons on left and right, a 3D point X above, baseline connecting two cameras
  - Epipolar plane shown as a light shaded triangle
  - Epipolar lines on both image planes
  - Epipolar points e₁, e₂ marked
- **Right Panel - SfM Pipeline**: Vertical flow of 4 steps
  - Step 1: "特征提取 SIFT/SuperPoint"
  - Step 2: "特征匹配 + RANSAC"
  - Step 3: "增量式SfM 五点法→PnP→BA"
  - Step 4: "MVS稠密重建 NCC深度图→融合"

## LABELS
- **Left Panel**: "针孔相机模型", "X_w 世界坐标", "X_c = R·X_w + t", "x ~ K·X_c", "内参 K" (with 3x3 matrix icon), "外参 [R|t]", "f_x, f_y 焦距", "(c_x, c_y) 主点"
- **Center Panel**: "对极几何", "基线 Baseline", "对极平面", "对极点 e₁ e₂", "对极线 l₁ l₂", "x₂ᵀFx₁ = 0", "F = K₂⁻ᵀEK₁⁻¹", "E = [t]_×R"
- **Right Panel**: "COLMAP Pipeline", "五点法→E→(R,t)", "三角化", "BA: min Σ‖x - P·X‖²", "NCC深度估计", "Poisson重建"
- **Bottom Callout**: "Janus问题: SDS缺乏对极约束 x₂ᵀFx₁=0" in Coral Red (#E8655A) box

## COLORS
- Background: Warm Cream (#F5F0E8)
- Left panel frame: Macaron Blue (#A8D8EA)
- Center panel frame: Lavender (#D5C6E0)
- Right panel frame: Mint (#B5E5CF)
- Camera icons: Macaron Blue (#A8D8EA) fill
- 3D point X: Coral Red (#E8655A) dot
- Baseline: Mustard Yellow (#F2CC8F) thick line
- Epipolar plane: Peach (#FFD5C2) semi-transparent fill
- Epipolar lines: Coral Red (#E8655A) dashed lines
- Pipeline arrows: Macaron Blue (#A8D8EA)
- Key formulas: Coral Red (#E8655A)
- Janus callout box: Peach (#FFD5C2) background with Coral Red (#E8655A) border

## STYLE
Flat vector illustration. Clean black outlines on all elements. Simplified camera icons (rectangles with lens circles). Geometric shapes for 3D points and coordinate frames. Dashed lines for epipolar lines. Small decorative dots. No gradients. Keywords in bold handwritten-style font, formulas in clean sans-serif.

## ASPECT
16:9 landscape

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
