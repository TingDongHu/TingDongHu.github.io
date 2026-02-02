import os
import sys
from PIL import Image

# --- 配置区 ---
MAX_WIDTH = 2560
QUALITY = 85
MIN_SIZE_KB = 4000
EXTENSIONS = ('.jpg', '.jpeg', '.png')

# 统计数据
stats = {
    "folders_renamed": 0,
    "files_renamed": 0,
    "files_compressed": 0,
    "total_saved_kb": 0
}

def safe_rename_to_lower(full_path, is_folder=False):
    """
    安全地将路径重命名为全小写，并记录统计数据。
    """
    dir_name = os.path.dirname(full_path)
    old_name = os.path.basename(full_path)
    lower_name = old_name.lower()

    if old_name != lower_name:
        new_path = os.path.join(dir_name, lower_name)
        temp_path = os.path.join(dir_name, f"temp_rename_{old_name}")
        try:
            os.rename(full_path, temp_path)
            os.rename(temp_path, new_path)
            
            label = "文件夹" if is_folder else "文件"
            print(f"  [{label}重命名] {old_name} -> {lower_name}")
            
            if is_folder:
                stats["folders_renamed"] += 1
            else:
                stats["files_renamed"] += 1
                
            return new_path, True
        except Exception as e:
            print(f"  [失败] 重命名 {old_name} 时出错: {e}")
            return full_path, False
    return full_path, False

def compress_image(file_path):
    """
    执行图片压缩并记录节省的体积。
    """
    try:
        original_size = os.path.getsize(file_path)
        if original_size < MIN_SIZE_KB * 1024:
            return

        img = Image.open(file_path)
        if img.width > MAX_WIDTH or original_size > MIN_SIZE_KB * 1024:
            ext = os.path.splitext(file_path)[1].lower()
            
            # 缩放逻辑
            if img.width > MAX_WIDTH:
                height = int((MAX_WIDTH / img.width) * img.height)
                img = img.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)
            
            # 保存
            if ext in ('.jpg', '.jpeg'):
                img.save(file_path, "JPEG", optimize=True, quality=QUALITY, subsampling=0, progressive=True)
            elif ext == '.png':
                img.save(file_path, "PNG", optimize=True)

            new_size = os.path.getsize(file_path)
            saved_kb = (original_size - new_size) // 1024
            
            if saved_kb > 0:
                print(f"  [图片压缩] {os.path.basename(file_path)}: {original_size//1024}KB -> {new_size//1024}KB (节省 {saved_kb}KB)")
                stats["files_compressed"] += 1
                stats["total_saved_kb"] += saved_kb
    except Exception as e:
        print(f"  [失败] 压缩 {file_path} 时出错: {e}")

def print_summary():
    """打印最终的处理汇总"""
    print("\n" + "="*40)
    print(" >>> 处理汇总报告 <<<")
    print(f" - 重命名文件夹: {stats['folders_renamed']} 个")
    print(f" - 重命名文件:   {stats['files_renamed']} 个")
    print(f" - 压缩优化图片: {stats['files_compressed']} 张")
    print(f" - 共计节省空间: {stats['total_saved_kb']} KB (~{stats['total_saved_kb']/1024:.2f} MB)")
    print("="*40 + "\n")

if __name__ == "__main__":
    target_dir = './content/posts/'
    git_files = sys.argv[1:] if len(sys.argv) > 1 else []

    if git_files:
        print(">>>> Git Hook 模式: 正在处理暂存区文件...")
        for f in git_files:
            if os.path.exists(f) and f.lower().endswith(EXTENSIONS):
                new_f, _ = safe_rename_to_lower(f, is_folder=False)
                compress_image(new_f)
    else:
        print(">>>> 手动全量模式: 正在扫描路径标准化...")
        # 1. 文件夹处理
        for root, dirs, _ in os.walk(target_dir, topdown=False):
            for d in dirs:
                safe_rename_to_lower(os.path.join(root, d), is_folder=True)

        # 2. 文件处理
        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                if filename.lower().endswith(EXTENSIONS):
                    full_file_path = os.path.join(root, filename)
                    new_file_path, _ = safe_rename_to_lower(full_file_path, is_folder=False)
                    compress_image(new_file_path)

    print_summary()