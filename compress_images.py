import os
import sys
from PIL import Image

# 1. 这里的参数是保住画质的关键
MAX_WIDTH = 3840  # 允许 4K 分辨率，确保放大后的细节
QUALITY = 85      # 85 是画质与体积的“黄金分割点”，几乎看不出区别
EXTENSIONS = ('.jpg', '.jpeg', '.png')

def compress_image(file_path):
    try:
        original_size = os.path.getsize(file_path)
        img = Image.open(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        # 如果图片超过 4K，才进行等比缩小，否则保留原大
        if img.width > MAX_WIDTH:
            height = int((MAX_WIDTH / img.width) * img.height)
            img = img.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)

        # 针对不同格式采取不同的“保真”策略
        if ext in ('.jpg', '.jpeg'):
            # subsampling=0 确保颜色不失真，progressive 增强加载体验
            img.save(file_path, "JPEG", optimize=True, quality=QUALITY, subsampling=0, progressive=True)
        elif ext == '.png':
            # PNG 采用无损压缩优化
            img.save(file_path, "PNG", optimize=True)

        new_size = os.path.getsize(file_path)
        ratio = (1 - new_size / original_size) * 100
        print(f"  [优化] {os.path.basename(file_path)}: 瘦身 {ratio:.1f}% ({original_size//1024}KB -> {new_size//1024}KB)")
        return True
    except Exception as e:
        print(f"  [失败] {file_path}: {e}")
        return False

if __name__ == "__main__":
    # 获取 Git 传入的或手动扫描的文件
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        for root, _, filenames in os.walk('./content/posts/'):
            for filename in filenames:
                if filename.lower().endswith(EXTENSIONS):
                    files.append(os.path.join(root, filename))

    for f in files:
        compress_image(f)