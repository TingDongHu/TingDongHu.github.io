---
title: 【ComfyUI】批量生成自动化
date: 2025-12-01T00:00:00+08:00
categories: ["ComfyUI"]
tags: ["Diffusion", "AIGC", "AI绘画", "python", "ComfyUI", "AP"]
description: "为解决YOLO项目数据不足问题，作者通过ComfyUI导出工作流API并编写Python脚本，实现了本地批量图片的自动化增强，高效生成了一一对应的训练图像数据。"
cover: "/img/ArtificialIntelligence.png"
headerImage: "/img/GeCML.png"
math: true
---

作者针对YOLO项目数据不足的问题，利用ComfyUI进行数据增强。由于官方批量功能不适用，他通过导出工作流API并编写Python脚本，实现了本地批量图片的自动化处理，高效生成训练所需的一对一对应图像数据。 



之前玩一个yolo项目的时候碰上了数据不足训练结果很差的问题，刚好现在AI生图这么发达，而自己之前有摸索过一点使用ComfyUI生图的工作流，索性开始用ComfyUI开始造数据。ComfyUI本身是支持多批次生成功能的。设置次数后可以反复运行该工作流，但是官方提供的这个更多是面向同一提示词、不同随机种子抽卡情况的。

![image-20251201204323062](%E3%80%90ComfyUI%E3%80%91I2I%E6%89%B9%E9%87%8F%E7%94%9F%E6%88%90%E8%87%AA%E5%8A%A8%E5%8C%96/image-20251201204323062.png)

我造数据需要的工况则是：

> N张图片经过工作流处理生成N张图片,每对图片一一对应

显然和官方提供的方法不太匹配，中间也找了几篇博客，有的是提供了批量加载图片节点，配合工作流的一个循环（LoopStart和LoopEnd）去实现的，个人尝试了一下发现其限制很大，每次限制加载100张，而且循环的逻辑很难用，还会出现重复加载的问题，只能算是面向非程序人员的解决方案了。

![Load Images For Loop文章图片](https://uinodes.com/_next/image?url=%2Fimg%2Fplugins%2FComfyUI-Easy-Use%2Fcompressed%2FLGQn8E9iXbgQMmp3dnQx5Y.webp&w=3840&q=75)

还有些方法就是使用第三方的平台或者插件等调用API，该方法的解决问题是很不错的。这里留一个链接方便以后查找[快速开始 - EasyAI在线文档](https://doc.51easyai.com/getting-started/quickstart)。但是感觉我就很简单一个需求，完全没必要用这么复杂的东西，索性自己配合GPT整理了一个脚本，用于本地的Image2Image的工作流批量运行.

### ComfyUI导出工作流为API

要注意在保存导出为API之前，工作流中的预览图片节点要尽量去除，节省算力，同时要保证该工作流是确实可用的，可以运行出图的。

![image-20251201210839690](%E3%80%90ComfyUI%E3%80%91I2I%E6%89%B9%E9%87%8F%E7%94%9F%E6%88%90%E8%87%AA%E5%8A%A8%E5%8C%96/image-20251201210839690.png)

导出后可以得到一个.json后缀的文件，就是可以用于python脚本中API调用的文件了。

### 配置脚本运行

脚本如下，其本质上是一个"ComfyUI远程控制器"，省去了自己一个一个配置参数的麻烦。

使用的时候只需要程序头部的输入输出路径进行配置，把导出的comfyUI工作流配置好即可，程序就可以自动的对输入路径的全部照片进行处理，如果你的显存足够大，觉得同时跑多批次也没问题，那推荐再开一个多线程加载。

```python
#!/usr/bin/env python3
"""
ComfyUI 极简批量图片处理脚本
将工作流JSON和所有配置参数集中在代码头部，开箱即用
"""

import requests
import json
import os
import time
import glob
from pathlib import Path

# ===================== 用户配置区域 =====================
# 注意：所有路径建议使用原始字符串（前面加r）避免转义问题

# 1. 输入输出设置
INPUT_FOLDER = r"D:\CutRes\buzzer"       # 输入图片文件夹路径
OUTPUT_FOLDER = r"D:\inCutRes\buzzer"    # 输出文件夹路径
WORKFLOW_FILE = "api_workflow.json"      # ComfyUI导出的工作流JSON文件

# 2. ComfyUI服务器设置
COMFYUI_SERVER = "http://127.0.0.1:8188" # ComfyUI服务器地址
TIMEOUT = 60                             # 单张图片最大处理等待时间(秒)
RETRY_TIMES = 3                          # 失败重试次数

# 3. 图片处理设置
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')  # 支持的图片格式
OVERWRITE_EXISTING = False               # 是否覆盖已存在的输出文件

# 4. 动态参数设置 (根据你的工作流节点参数调整)
CUSTOM_PARAMETERS = {
    # 示例参数（根据你的工作流实际参数名修改）：
    # "denoise": 0.7,
    # "steps": 20,
    # "cfg_scale": 7.5,
    # "seed": -1,
}

# ===================== 主程序 =====================
def main():
    # 初始化检查
    print("="*50)
    print("ComfyUI 批量图片处理器")
    print(f"输入目录: {INPUT_FOLDER}")
    print(f"输出目录: {OUTPUT_FOLDER}")
    print("="*50)
    
    # 检查文件夹是否存在
    if not os.path.isdir(INPUT_FOLDER):
        print(f"错误：输入文件夹不存在 {INPUT_FOLDER}")
        return
    
    # 确保输出文件夹存在
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # 加载工作流
    try:
        with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        print(f"✅ 成功加载工作流文件: {WORKFLOW_FILE}")
    except Exception as e:
        print(f"❌ 加载工作流文件失败: {e}")
        return
    
    # 获取图片列表
    image_files = [
        f for f in glob.glob(os.path.join(INPUT_FOLDER, "*.*")) 
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]
    
    if not image_files:
        print(f"⚠️ 没有找到支持的图片文件（扩展名: {IMAGE_EXTENSIONS}）")
        return
    
    print(f"找到 {len(image_files)} 张待处理图片")
    
    # 处理每张图片
    success_count = 0
    for i, img_path in enumerate(image_files, 1):
        img_name = os.path.basename(img_path)
        print(f"\n[{i}/{len(image_files)}] 正在处理: {img_name}")
        
        # 检查输出是否已存在
        output_exists = any(glob.glob(os.path.join(OUTPUT_FOLDER, f"*{os.path.splitext(img_name)[0]}*")))
        if output_exists and not OVERWRITE_EXISTING:
            print(f"⏩ 跳过（输出文件已存在）")
            continue
        
        # 带重试机制的图片处理
        for attempt in range(1, RETRY_TIMES + 1):
            try:
                # 上传图片
                with open(img_path, "rb") as f:
                    files = {'image': (img_name, f, 'image/png')}
                    upload_response = requests.post(
                        f"{COMFYUI_SERVER}/upload/image", 
                        files=files,
                        timeout=10
                    )
                    upload_response.raise_for_status()
                
                # 准备工作流
                current_workflow = json.loads(json.dumps(workflow))  # 深拷贝
                
                # 替换图片文件名
                for node_id, node in current_workflow.items():
                    if node.get("class_type") == "LoadImage":
                        current_workflow[node_id]["inputs"]["image"] = img_name
                
                # 替换自定义参数
                for param_name, param_value in CUSTOM_PARAMETERS.items():
                    for node_id, node in current_workflow.items():
                        if param_name in node.get("inputs", {}):
                            current_workflow[node_id]["inputs"][param_name] = param_value
                
                # 提交任务
                response = requests.post(
                    f"{COMFYUI_SERVER}/prompt", 
                    json={"prompt": current_workflow},
                    timeout=10
                )
                response.raise_for_status()
                prompt_id = response.json()["prompt_id"]
                
                # 等待处理完成
                for wait_time in range(TIMEOUT):
                    time.sleep(1)
                    
                    history = requests.get(
                        f"{COMFYUI_SERVER}/history/{prompt_id}",
                        timeout=10
                    ).json()
                    
                    if prompt_id in history:
                        # 保存输出图片
                        outputs = history[prompt_id].get("outputs", {})
                        for node_output in outputs.values():
                            if "images" in node_output:
                                for img in node_output["images"]:
                                    output_filename = f"{os.path.splitext(img_name)[0]}_{img['filename']}"
                                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                                    
                                    image_data = requests.get(
                                        f"{COMFYUI_SERVER}/view",
                                        params={
                                            "filename": img["filename"],
                                            "subfolder": img.get("subfolder", ""),
                                            "type": img.get("type", "output")
                                        },
                                        timeout=10
                                    ).content
                                    
                                    with open(output_path, "wb") as f:
                                        f.write(image_data)
                                    print(f"✅ 保存: {output_filename}")
                        
                        success_count += 1
                        break
                else:
                    print(f"⚠️ 处理超时（{TIMEOUT}秒）")
                    continue
                
                break  # 处理成功，跳出重试循环
            
            except Exception as e:
                print(f"⚠️ 尝试 {attempt}/{RETRY_TIMES} 失败: {str(e)}")
                if attempt == RETRY_TIMES:
                    print(f"❌ 放弃处理: {img_name}")
                time.sleep(2)
    
    # 打印摘要
    print("\n" + "="*50)
    print(f"处理完成！成功 {success_count}/{len(image_files)} 张图片")
    print(f"输出目录: {OUTPUT_FOLDER}")
    print("="*50)

if __name__ == "__main__":
    main()
```

> [!IMPORTANT]
>
> 要注意使用的时候需要确保：
>
> - ComfyUI正在运行且可访问，因为该进程将直接作为服务端
>
> - 地址端口正确（默认127.0.0.1:8188）
>
> - 没有其他任务在排队

![image-20251201210952597](%E3%80%90ComfyUI%E3%80%91I2I%E6%89%B9%E9%87%8F%E7%94%9F%E6%88%90%E8%87%AA%E5%8A%A8%E5%8C%96/image-20251201210952597.png)

如此就可以交给该脚本线性的处理我配置文件夹中所有的图片且不会出现加载重复的问题了，而我本人就可以安心睡大觉去了!