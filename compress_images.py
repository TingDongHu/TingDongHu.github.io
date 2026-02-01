import os
import sys
import tempfile
from PIL import Image

# --- 配置区 ---
MAX_WIDTH = 2560      # 2K 分辨率
QUALITY = 85          # 高保真质量
MIN_SIZE_KB = 3000    # 阈值：小于 3MB 的图片不重复压缩
EXTENSIONS = ('.jpg', '.jpeg', '.png')

def process_image(file_path):
    try:
        # --- 第一阶段：命名标准化 (所有的图必须先过这一关) ---
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        lower_name = base_name.lower()
        current_path = file_path

        if base_name != lower_name:
            new_path = os.path.join(dir_name, lower_name)
            
            # Windows 特有逻辑：A.JPG 改 a.jpg 有时会报错
            # 我们通过一个中转名来强制重命名
            temp_name = os.path.join(dir_name, f"temp_{base_name}")
            os.rename(current_path, temp_name)
            os.rename(temp_name, new_path)
            
            current_path = new_path
            print(f"  [重命名] {base_name} -> {lower_name}")

        # --- 第二阶段：体积判定 (基于标准化后的路径) ---
        original_size = os.path.getsize(current_path)
        
        # 如果体积已经很小，直接结束（此时已完成重命名）
        if original_size < MIN_SIZE_KB * 1024:
            return True

        # --- 第三阶段：压缩处理 ---
        img = Image.open(current_path)
        needs_compression = False
        
        # 判定是否需要调整尺寸
        if img.width > MAX_WIDTH:
            needs_compression = True
        
        # 即使尺寸不超，如果体积很大且没被压缩过，也建议过一遍优化
        if original_size > MIN_SIZE_KB * 1024:
            needs_compression = True

        if needs_compression:
            ext = os.path.splitext(current_path)[1].lower()
            
            # 调整尺寸
            if img.width > MAX_WIDTH:
                height = int((MAX_WIDTH / img.width) * img.height)
                img = img.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)

            # 保存覆盖
            if ext in ('.jpg', '.jpeg'):
                img.save(current_path, "JPEG", optimize=True, quality=QUALITY, subsampling=0, progressive=True)
            elif ext == '.png':
                img.save(current_path, "PNG", optimize=True)

            new_size = os.path.getsize(current_path)
            print(f"  [优化] {lower_name}: {original_size//1024}KB -> {new_size//1024}KB")
        
        return True

    except Exception as e:
        print(f"  [失败] {file_path}: {e}")
        return False

if __name__ == "__main__":
    # 获取 Git Hook 传进来的文件列表
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 手动运行模式：扫描 content 目录
    if not files:
        for root, _, filenames in os.walk('./content/posts/'):
            for filename in filenames:
                if filename.lower().endswith(EXTENSIONS):
                    files.append(os.path.join(root, filename))

    for f in files:
        if os.path.exists(f):
            process_image(f)