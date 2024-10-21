# """
#     检查a文件夹内的数据与b（或更多）文件夹内是否重复，删除a文件夹中重复数据。
# """

import os
import shutil

# 替换成您实际的文件夹路径
folder_a = r'D:\0409'
folder_b = r'C:\Users\Administrator\Desktop\气压表图\0409'
#folder_c = r'C:\Users\Administrator\Desktop\rec'

# 获取A文件夹内的所有文件basename
files_in_a = os.listdir(folder_a)

# 遍历A文件夹中的文件
for filename in files_in_a:
    # 构建文件的完整路径
    file_path_a = os.path.join(folder_a, filename)

    # 如果文件是真正的文件（而不是文件夹）
    if os.path.isfile(file_path_a):
        # 检查basename是否在B文件夹或C文件夹内
        file_exists_in_b = os.path.exists(os.path.join(folder_b, filename))
        #file_exists_in_c = os.path.exists(os.path.join(folder_c, filename))

        # 如果文件在B或C文件夹中存在
        if file_exists_in_b: # or file_exists_in_c:
            # 从A文件夹中删除该文件
            try:
                os.remove(file_path_a)
                print(f"Deleted file: {filename}")
            except OSError as e:
                print(f"Error: {e.strerror} when deleting {filename}")

print("Process completed.")