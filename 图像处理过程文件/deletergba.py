# """
#     删除目标文件夹内labelme无法打开导致崩溃闪退的RGBA格式的图片。
# """

import os
from PIL import Image

def is_rgba(image_path):
    """
    检查图片是否为RGBA格式
    """
    try:
        with Image.open(image_path) as img:
            return img.mode == 'RGBA'
    except Exception:
        return False

def delete_rgba_images(folder_path):
    """
    删除文件夹中所有RGBA格式的图片
    """
    if not os.path.isdir(folder_path):
        print(f"文件夹 '{folder_path}' 不存在")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 添加更多格式如果需要
                file_path = os.path.join(root, file)
                print('读取到',file)
                if is_rgba(file_path):
                    try:
                        os.remove(file_path)
                        print(f"已删除 {file_path}")
                    except Exception as e:
                        print(f"无法删除 {file_path}: {e}")
    print("已完成RGBA格式图片的清理。")

# 使用示例
delete_rgba_images(r'D:\0409')