---
illustration_id: 04
type: infographic
style: vector-illustration
palette: macaron
---

# 渲染管线双路径

## Layout
Split layout: left half shows "光栅化管线 Rasterization" as a 5-step horizontal flow; right half shows "光线追踪 Ray Tracing" as a recursive ray diagram with the rendering equation below. A dividing line in the middle. Title "渲染" at top center.

## ZONES
- **Title Zone**: Top center, "渲染管线" in large handwritten font with a small lightbulb icon
- **Left Half - Rasterization**: 5 connected steps flowing left to right
  - Step 1: "顶点处理" — show MVP transform boxes
  - Step 2: "图元装配" — show triangle assembly from vertices
  - Step 3: "光栅化" — show triangle filling pixels with edge function
  - Step 4: "片元着色" — show texture sampling with UV coordinates
  - Step 5: "深度测试" — show Z-buffer with depth values
- **Right Half - Ray Tracing**: Camera at top, rays going down into scene
  - Primary ray from camera through pixel
  - Reflect ray bouncing off surface
  - Shadow ray pointing to light source
  - Rendering equation displayed below in a box
- **Bottom Zone**: Small comparison tags: "光栅化: 实时 GPU" vs "光线追踪: 离线 物理正确"

## LABELS
- **Left Labels**: "v_clip = P·V·M·v", "M 模型 / V 视图 / P 投影", "E₀₁(p) 叉积判内", "λ₀+λ₁+λ₂=1 重心坐标", "Mipmap LOD", "Z-buffer深度测试", "α混合: C_out = α·C_src + (1-α)·C_dst"
- **Right Labels**: "Primary Ray 主光线", "Reflect 反射", "Shadow 阴影", "Refract 折射(Snell)", "渲染方程:", "L_o = L_e + ∫f_r·L_i·cosθ dω", "f_r = F·G·D / (4·cos·cos)", "F=Fresnel G=遮蔽 D=NDF", "Monte Carlo采样"
- **Bottom Tags**: "Rasterization: 实时 GPU管线" in Macaron Blue, "Ray Tracing: 物理正确 路径追踪" in Lavender
- **PBR Callout**: "PBR分离: Albedo / Roughness / Metallic / Normal"

## COLORS
- Background: Warm Cream (#F5F0E8)
- Left half background: very light Macaron Blue (#A8D8EA at 10% opacity effect via lighter tint)
- Right half background: very light Lavender (#D5C6E0 at 10% opacity effect via lighter tint)
- Rasterization steps: alternating Macaron Blue (#A8D8EA) and Mint (#B5E5CF) boxes
- Ray tracing rays: Mustard Yellow (#F2CC8F) for primary, Macaron Blue (#A8D8EA) for reflect, Peach (#FFD5C2) for shadow
- Triangle/surface elements: Macaron Blue (#A8D8EA) fill
- Light source icon: Mustard Yellow (#F2CC8F)
- Rendering equation box: Peach (#FFD5C2) border
- Key formulas: Coral Red (#E8655A)
- PBR callout: Mint (#B5E5CF) background

## STYLE
Flat vector illustration. Clean black outlines on all elements. Step boxes are rounded rectangles with icons inside. Rays are clean lines with arrowheads. Camera is a simplified rectangle with lens. Light source is a circle with rays. Surface is a wavy line. Small decorative dots. No gradients. Keywords in bold handwritten-style font.

## ASPECT
16:9 landscape

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
