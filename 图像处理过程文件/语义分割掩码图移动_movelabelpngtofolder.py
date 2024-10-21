# """
#     用于语义分割项目：
#     labelme批量转换json至png会将png生成至独立的文件夹内，运行本脚本将独立文件夹内的png数据提取出。
# """

import os
import shutil

# 设置源文件夹和目标文件夹的路径
source_folder = './json2png' #包含png数据的文件夹所在的目录
target_folder = r'C:\Users\Administrator\Desktop\add' #目标目录

# 确保目标文件夹存在，如果不存在则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有子文件夹
for subdir, dirs, files in os.walk(source_folder):
    for file in files:
        # 检查是否是label.png文件
        if file == 'label.png':
            # 获取当前子文件夹的名称
            current_dir = os.path.basename(subdir)
            # 去掉最后的"_json"并添加".png"后缀
            new_name = current_dir.rsplit('_json', 1)[0] + '.png'
            # 构造原文件和目标文件的完整路径
            source_file = os.path.join(subdir, file)
            target_file = os.path.join(target_folder, new_name)
            # 重命名并移动文件
            shutil.move(source_file, target_file)
            print(f"已移动{new_name}")
print("已全部完成")
