# """
#     检查训练集文件夹里jpg和json文件是否成对，成对则移动至目标文件夹内。
# """

import os
import shutil

def move_paired_files(src_dir, dst_dir, extensions):
    # 确保目标目录存在，如果不存在则创建
    os.makedirs(dst_dir, exist_ok=True)

    # 用于记录已经找到配对的文件，防止重复移动
    paired_files = set()

    # 遍历源目录中的所有文件
    for filename in os.listdir(src_dir):
        # 获取文件的完整路径
        file_path = os.path.join(src_dir, filename)

        # 检查文件是否是文件（而不是目录）并且具有指定的扩展名之一
        if os.path.isfile(file_path) and os.path.splitext(filename)[1] in extensions:
            # 获取不带扩展名的文件名
            base_name = os.path.splitext(filename)[0]

            # 检查是否存在对应的文件
            for ext in extensions:
                if ext != os.path.splitext(filename)[1]:
                    pairing_file = f"{base_name}{ext}"
                    pairing_file_path = os.path.join(src_dir, pairing_file)

                    # 如果找到对应的文件并且这对文件还没有被移动过
                    if os.path.exists(pairing_file_path) and (base_name, ext) not in paired_files:
                        # 移动文件对到目标目录
                        shutil.move(file_path, dst_dir)
                        shutil.move(pairing_file_path, dst_dir)

                        # 记录这对文件已经被移动过
                        paired_files.add((base_name, ext))
                        print(f"Moved {filename} and {pairing_file} to {dst_dir}")
                        break  # 已经找到配对文件，跳出循环
    print('Finished')

# 设置源目录和目标目录
src_dir = r'C:\Users\Administrator\Desktop\template5'
dst_dir = r'C:\Users\Administrator\Desktop\gasmeter'

#确保输出文件夹存在，不存在则创建
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# 设置要查找的文件扩展名列表
extensions = ['.jpg', '.json']

# 调用函数来移动匹配的文件
move_paired_files(src_dir, dst_dir, extensions)