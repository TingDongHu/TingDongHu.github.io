import os
import sys
from PIL import Image

# --- 配置区 ---
MAX_WIDTH = 2560      # 2K 分辨率
QUALITY = 85          # 高保真质量
MIN_SIZE_KB = 3000    # 阈值：小于 3MB 的图片不重复压缩 (根据你的要求设定)
EXTENSIONS = ('.jpg', '.jpeg', '.png')

def compress_image(file_path):
    try:
        # --- 1. 强制文件名小写逻辑 (解决 GitHub Pages 404) ---
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        lower_name = base_name.lower()
        
        # 即使图片很小不压缩，也要先确保它是小写的
        if base_name != lower_name:
            new_path = os.path.join(dir_name, lower_name)
            # 如果目标小写文件已存在，先删除（防止 Windows 报错）
            if os.path.exists(new_path) and base_name.lower() == lower_name:
                pass 
            os.rename(file_path, new_path)
            file_path = new_path # 后续逻辑使用新路径
            print(f"  [重命名] {base_name} -> {lower_name}")

        # --- 2. 检查文件大小：如果已经小于阈值，直接跳过压缩 ---
        original_size = os.path.getsize(file_path)
        if original_size < MIN_SIZE_KB * 1024:
            # 如果只是重命名了，我们也返回 True 以便 Git 捕获变化
            return True

        # --- 3. 读取图片并检查分辨率 ---
        img = Image.open(file_path)
        
        # 如果宽度没超标且文件不是巨大，跳过压缩
        if img.width <= MAX_WIDTH and original_size < 1024 * 1024: 
            return True

        # --- 4. 执行压缩逻辑 ---
        ext = os.path.splitext(file_path)[1].lower()

        # 调整尺寸
        if img.width > MAX_WIDTH:
            height = int((MAX_WIDTH / img.width) * img.height)
            img = img.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)

        # 保存文件
        if ext in ('.jpg', '.jpeg'):
            img.save(file_path, "JPEG", optimize=True, quality=QUALITY, subsampling=0, progressive=True)
        elif ext == '.png':
            img.save(file_path, "PNG", optimize=True)

        new_size = os.path.getsize(file_path)
        print(f"  [优化] {os.path.basename(file_path)}: {original_size//1024}KB -> {new_size//1024}KB")
        return True
    except Exception as e:
        print(f"  [失败] {file_path}: {e}")
        return False

if __name__ == "__main__":
    # 获取 Git Hook 传进来的文件列表
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 如果没传参数，说明是手动全量扫描整个 content 目录
    if not files:
        for root, _, filenames in os.walk('./content/posts/'):
            for filename in filenames:
                if filename.lower().endswith(EXTENSIONS):
                    files.append(os.path.join(root, filename))

    for f in files:
        # 过滤掉不存在的文件（有时 Git Hook 传进来的文件可能已被删）
        if os.path.exists(f):
            compress_image(f)