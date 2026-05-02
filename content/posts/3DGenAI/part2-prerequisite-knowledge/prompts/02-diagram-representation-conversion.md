---
illustration_id: 02
type: diagram
style: vector-illustration
palette: macaron
---

# 表示转换链

## Layout
Circular/rotational diagram with five nodes (Mesh, Voxel, PointCloud, SDF, NeRF) arranged in a pentagon layout. Directed arrows between nodes labeled with the conversion algorithm name. Center area contains a small decorative 3D object silhouette.

## ZONES
- **Center Zone**: Small decorative silhouette of a 3D bunny/teapot shape in light outline
- **Node Mesh**: Top, with triangulated surface icon
- **Node Voxel**: Upper-right, with cube grid icon
- **Node PointCloud**: Lower-right, with scattered dots icon
- **Node SDF**: Lower-left, with contour lines icon
- **Node NeRF**: Upper-left, with camera ray icon
- **Arrow Zone**: Curved arrows between nodes with algorithm labels

## LABELS
- **Mesh → PointCloud**: "均匀采样 / FPS", sublabel "按面积加权 P(T)=A_T/A_total"
- **PointCloud → Mesh**: "Poisson重建", sublabel "ΔF = ∇·V (泊松方程)", second arrow "Ball-Pivoting BPA"
- **SDF → Mesh**: "Marching Cubes", sublabel "256种→15种配置 查表"
- **Mesh → SDF**: "扫描转换 + BVH", sublabel "射线投射判内外 O(log F)"
- **PointCloud → SDF**: "PCA法向→符号分配", sublabel "v₃=法向方向"
- **NeRF → SDF**: "VolSDF / UNISURF", sublabel "σ = Ψ_β(f(x))"
- **SDF → Voxel**: "离散采样", sublabel "f[i,j,k]网格化"
- **Voxel → SDF**: "体素→连续场", sublabel "三线性插值"
- **Mesh tag**: "最终交付格式 GPU光栅化"
- **PointCloud tag**: "生成最简单 无拓扑约束"

## COLORS
- Background: Warm Cream (#F5F0E8)
- Mesh node: Macaron Blue (#A8D8EA) fill
- Voxel node: Mint (#B5E5CF) fill
- PointCloud node: Lavender (#D5C6E0) fill
- SDF node: Peach (#FFD5C2) fill
- NeRF node: Mustard Yellow (#F2CC8F) fill
- Arrow lines: dark grey with colored arrowheads matching destination node
- Algorithm labels on arrows: Coral Red (#E8655A) for key names, black for sublabels
- Center silhouette: light Macaron Blue (#A8D8EA) outline

## STYLE
Flat vector illustration. Clean black outlines on all node circles/rounded-rectangles. Curved arrows with clean arrowheads. Algorithm names in bold handwritten-style font, sublabels in smaller clean font. Geometric simplified icons inside each node. Decorative small geometric shapes (triangles, circles) near arrows. No gradients.

## ASPECT
16:9 landscape

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
