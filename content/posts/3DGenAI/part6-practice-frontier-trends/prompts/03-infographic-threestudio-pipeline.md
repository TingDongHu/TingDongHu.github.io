---
illustration_id: 03
type: infographic
style: vector-illustration
palette: macaron
---

threestudio解耦生成管线 - Infographic View

INPUT: 文本/图像 (Text/Image)

MODULE 1: PromptProcessor (提示处理)
- 输入: "a hamburger" / 参考图像
- CLIP文本编码 → 文本嵌入
- 支持: 加权提示 "the hamburger::5, blurry::-2"
- 输出: prompt_utils (含conditional/unconditional嵌入)

MODULE 2: Guidance (2D扩散先验)
- StableDiffusionGuidance: SD 1.5/2.1
  * SDS损失: w(t)·(ε_φ - ε)
  * CFG scale: 100 (SDS) / 7.5 (VSD)
- DeepFloydGuidance: DeepFloyd IF (更高质量)
- Zero123Guidance: 单视图条件生成
- 接口: (rgb, prompt_utils) → {loss_sds, ...}
- 关键: 扩散模型冻结, 仅提供梯度信号

MODULE 3: Geometry (3D表示)
- ImplicitVolume: NeRF密度场
- GaussianSplatting: 3D高斯泼溅
- Mesh: 显式网格+可微光栅化
- 输出: 可渲染3D表示

MODULE 4: System (训练策略)
- DreamFusion: SDS + 单一优化
- Magic3D: 两阶段粗到精
- ProlificDreamer: VSD (变分分数蒸馏)
- Fantasia3D: 几何与材质解耦

DESIGN PATTERN: System = Geometry + Guidance + PromptProcessor
- 修改geometry_type: NeRF ↔ 3DGS ↔ Mesh
- 修改guidance_type: SDS ↔ VSD ↔ Zero123
- 无需修改Python代码!

PIPELINE FLOW:
文本/图像 → PromptProcessor → Guidance(梯度) → Geometry(3D表示) → 渲染
                ↑                      ↓
                └─────── System ────────┘

Flat vector infographic with horizontal modular pipeline. Clear component separation.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Peach (#FFD5C2) for PromptProcessor, Lavender (#D5C6E0) for Guidance, Blue (#A8D8EA) for Geometry, Mint (#B5E5CF) for System, Coral Red (#E8655A) for design pattern and swap arrows, Mustard Yellow (#F2CC8F) for YAML config emphasis
ELEMENTS: Horizontal pipeline with 4 main modules, swap arrows between modules (showing replaceability), YAML config card showing geometry_type/guidance_type switches, System wrapper around modules, frozen model icon (snowflake) on Guidance
ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs. Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image. Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords. Language: Chinese.
