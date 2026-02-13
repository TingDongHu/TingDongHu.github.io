import os
import sys
import re
from PIL import Image

# --- 配置区 ---
MAX_WIDTH = 2560      # 2K 分辨率
QUALITY = 80          # 高保真质量
MIN_SIZE_KB = 4000    # 阈值：小于 4MB 的图片不重复压缩
EXTENSIONS = ('.jpg', '.jpeg', '.png')
TARGET_DIR = './content/posts/'

# 统计数据
stats = {
    "folders_fixed": 0,
    "md_files_fixed": 0,
    "links_repaired": 0,
    "images_compressed": 0,
    "total_saved_kb": 0
}

def sanitize_name(name):
    """
    Hugo 规范化逻辑：变小写、空格转中划线、剔除括号及特殊符号
    """
    name = name.lower().replace(" ", "-").replace("_", "-")
    # 剔除 【 】 ( ) [ ] （ ） : ： ! ! ? ?
    name = re.sub(r'[【】\(\)\[\]（）：:！!？\?]', '', name)
    # 合并连续中划线并去除首尾
    return re.sub(r'-+', '-', name).strip("-")

def safe_rename(full_path, is_folder=False):
    """
    Windows 兼容重命名逻辑
    """
    dir_name = os.path.dirname(full_path)
    old_name = os.path.basename(full_path)
    
    # 保持后缀，仅处理主文件名
    if not is_folder and old_name.endswith('.md'):
        name_part, ext_part = old_name[:-3], ".md"
    elif not is_folder:
        name_part, ext_part = os.path.splitext(old_name)
    else:
        name_part, ext_part = old_name, ""

    new_name = sanitize_name(name_part) + ext_part.lower()

    if old_name != new_name:
        new_path = os.path.join(dir_name, new_name)
        temp_path = os.path.join(dir_name, f"temp_fix_{hash(old_name)}")
        try:
            os.rename(full_path, temp_path)
            os.rename(temp_path, new_path)
            return new_path, True
        except Exception as e:
            print(f"  [重命名失败] {old_name}: {e}")
            return full_path, False
    return full_path, False

def compress_image(file_path):
    """
    执行图片压缩
    """
    try:
        size = os.path.getsize(file_path)
        if size < MIN_SIZE_KB * 1024: return
        img = Image.open(file_path)
        if img.width > MAX_WIDTH or size > MIN_SIZE_KB * 1024:
            if img.width > MAX_WIDTH:
                h = int((MAX_WIDTH / img.width) * img.height)
                img = img.resize((MAX_WIDTH, h), Image.Resampling.LANCZOS)
            
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ('.jpg', '.jpeg'):
                img.save(file_path, "JPEG", optimize=True, quality=QUALITY, subsampling=0, progressive=True)
            elif ext == '.png':
                img.save(file_path, "PNG", optimize=True)
            
            new_size = os.path.getsize(file_path)
            stats["images_compressed"] += 1
            stats["total_saved_kb"] += (size - new_size) // 1024
    except Exception as e:
        print(f"  [压缩失败] {os.path.basename(file_path)}: {e}")

if __name__ == "__main__":
    print(">>>> 正在启动全量重构与同步程序...")
    
    # 用于记录路径映射： { "旧名": "新名" }
    path_map = {}

    # 1. 物理重命名阶段
    all_items = os.listdir(TARGET_DIR)
    
    # 先处理文件夹和 .md 文件
    for item in all_items:
        full_path = os.path.join(TARGET_DIR, item)
        is_dir = os.path.isdir(full_path)
        is_md = item.endswith('.md')
        
        if is_dir or is_md:
            new_path, renamed = safe_rename(full_path, is_folder=is_dir)
            if renamed:
                old_pure_name = item[:-3] if is_md else item
                new_pure_name = os.path.basename(new_path)[:-3] if is_md else os.path.basename(new_path)
                path_map[old_pure_name] = new_pure_name
                
                if is_dir: stats["folders_fixed"] += 1
                else: stats["md_files_fixed"] += 1
                print(f"  [物理重命名] {item} -> {os.path.basename(new_path)}")

    # 2. 内容修复阶段 (Sync Links)
    print("\n>>>> 正在修复 Markdown 内部引用...")
    for item in os.listdir(TARGET_DIR):
        if item.endswith('.md'):
            md_path = os.path.join(TARGET_DIR, item)
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            # 修复图片链接中的文件夹名和文件名
            for old_p, new_p in path_map.items():
                # 替换形如 (Folder/Image.JPG) 的路径文字
                new_content = new_content.replace(f"({old_p}/", f"({new_p}/")
                new_content = new_content.replace(f"/{old_p}/", f"/{new_p}/")
            
            # 额外处理：将所有图片后缀强转小写进行匹配
            new_content = re.sub(r'\.(JPG|JPEG|PNG)', lambda m: m.group(0).lower(), new_content)

            if new_content != content:
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                stats["links_repaired"] += 1
                print(f"  [内容修复] {item} 内部链接已同步")

    # 3. 图片压缩阶段
    print("\n>>>> 正在执行图片标准化及压缩...")
    for root, _, filenames in os.walk(TARGET_DIR):
        for f in filenames:
            if f.lower().endswith(EXTENSIONS):
                # 即使是子文件夹里的图片名，也顺手变小写
                full_img_path = os.path.join(root, f)
                new_img_path, renamed = safe_rename(full_img_path, is_folder=False)
                compress_image(new_img_path)

    # 汇总报告
    print("\n" + "="*45)
    print(f"报告: 文件夹更名:{stats['folders_fixed']} | 文章更名:{stats['md_files_fixed']}")
    print(f"报告: 链接同步:{stats['links_repaired']} 篇 | 图片压缩:{stats['images_compressed']} 张")
    print(f"报告: 节省空间: {stats['total_saved_kb']} KB")
    print("="*45 + "\n")