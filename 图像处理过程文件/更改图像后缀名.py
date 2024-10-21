# """
#     批量修改文件后缀。
# """

import os
from PIL import Image


def changename(folder_path,orinend,newend):

    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        # 检查文件是否是.png格式
        if filename.endswith(orinend):
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, filename)
            try:
                # 打开图片
                with Image.open(file_path) as img:
                    # 如果图片是RGBA模式，转换为RGB模式
                    # if img.mode == 'RGBA':
                    #     rgb_img = img.convert('RGB')
                    #     print(f" 已修改 RGBA 模式图片 {filename} 为 RGB 模式")
                    # else:
                    #     rgb_img = img
                    # 转换图片格式并保存为.jpg
                    base_filename = os.path.splitext(filename)[0]  # 去掉扩展名
                    new_filename = base_filename + newend  # 添加新的扩展名
                    new_file_path = os.path.join(folder_path, new_filename)
                    img.save(new_file_path, "JPEG")
                # 删除原始文件
                os.remove(file_path)
                print(f" 已修改 {filename} 为 {new_filename}，并删除原始文件")
            except:
                print(f"{filename}异常")
    print("已完成所有后缀替换及RGBA模式替换")

# 指定文件夹路径
folder_path = r'C:\Users\Administrator\Desktop\tirecode'
orinend = (".png",".jpeg")
newend = ".jpg"
changename(folder_path,orinend,newend)
#
# for i in range(2,7):
#     folder_path = r'C:\Users\Administrator\Desktop\分组'
#     folder_path2 = os.path.join(folder_path,f'胎纹尺{i}')
#     changename(folder_path2,orinend,newend)
#修改文件名，替换每个文件开始的’胎码图片‘为’tirecode‘
# import os
# from PIL import Image
# folder_path = r'C:\Users\Administrator\Desktop\exp17\labels'
# for filename in os.listdir(folder_path):
#     if filename.startswith('胎码图片'):
#         file_path = os.path.join(folder_path, filename)
#         new_filename = filename.replace('胎码图片', 'tirecode')
#         new_file_path = os.path.join(folder_path, new_filename)
#         os.rename(file_path, new_file_path)
#         print(f" 已修改 {filename} 为 {new_filename}")