import os
import shutil
# from random import sample
#
# def split_images(source_folder, train_folder, test_folder, ratio=0.3):
#     """
#     将源文件夹内的图片按指定比例分为训练集和测试集。
#
#     :param source_folder: 源图片文件夹路径
#     :param train_folder: 训练集目标文件夹路径
#     :param test_folder: 测试集目标文件夹路径
#     :param ratio: 训练集占总数据的比例，默认为0.3
#     """
#     # 确保目标文件夹存在
#     os.makedirs(train_folder, exist_ok=True)
#     os.makedirs(test_folder, exist_ok=True)
#
#     # 获取源文件夹内所有图片的路径
#     images = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
#
#     # 根据比例计算训练集和测试集的大小
#     train_size = int(len(images) * ratio)
#     test_size = len(images) - train_size
#
#     # 随机选择训练集和测试集的图片
#     train_images = sample(images, train_size)
#     test_images = [img for img in images if img not in train_images]
#
#     # 复制图片到相应的文件夹
#     for img_path in train_images:
#         shutil.copy(img_path, train_folder)
#     for img_path in test_images:
#         shutil.copy(img_path, test_folder)
#
#     print(f"分割完成，训练集有{train_size}张图片，测试集有{test_size}张图片。")
#
# # 示例用法
# source_folder = r'D:\气压表\气压表_分类\data'  # 源图片文件夹路径
# train_folder = r'C:\Users\Administrator\Desktop\train\imgs'          # 训练集目标文件夹路径
# test_folder = r'C:\Users\Administrator\Desktop\test\imgs'            # 测试集目标文件夹路径
# split_images(source_folder, train_folder, test_folder)

def copy_corresponding_txt_files(train_folder, test_folder, labels_folder, train_label_folder, test_label_folder):
    """
    根据图片文件夹中的文件名，从labels文件夹复制对应的txt文件到训练集和测试集的标签文件夹。

    :param train_folder: 训练图片文件夹路径
    :param test_folder: 测试图片文件夹路径
    :param labels_folder: 标签文件（txt）所在文件夹路径
    :param train_label_folder: 训练集标签文件夹路径
    :param test_label_folder: 测试集标签文件夹路径
    """
    # 确保目标文件夹存在
    os.makedirs(train_label_folder, exist_ok=True)
    os.makedirs(test_label_folder, exist_ok=True)

    # 获取训练集和测试集图片的文件名（不含后缀）
    train_images_names = {os.path.splitext(os.path.basename(f))[0] for f in os.listdir(train_folder)}
    test_images_names = {os.path.splitext(os.path.basename(f))[0] for f in os.listdir(test_folder)}

    # 复制对应的.txt文件到训练集和测试集的标签文件夹
    for name in train_images_names:
        src_txt = os.path.join(labels_folder, f"{name}.txt")
        if os.path.exists(src_txt):
            dst_txt = os.path.join(train_label_folder, f"{name}.txt")
            shutil.copy(src_txt, dst_txt)

    for name in test_images_names:
        src_txt = os.path.join(labels_folder, f"{name}.txt")
        if os.path.exists(src_txt):
            dst_txt = os.path.join(test_label_folder, f"{name}.txt")
            shutil.copy(src_txt, dst_txt)

    print("标签文件复制完成。")


# 示例用法
train_folder = r'C:\Users\Administrator\Desktop\train\imgs'
test_folder = r'C:\Users\Administrator\Desktop\test\imgs'
labels_folder = r'D:\气压表\气压表_分类\labels'  # 标签（txt）文件所在文件夹路径
train_label_folder = r'C:\Users\Administrator\Desktop\train\labels'  # 训练集标签文件夹路径
test_label_folder = r'C:\Users\Administrator\Desktop\test\labels'  # 测试集标签文件夹路径

copy_corresponding_txt_files(train_folder, test_folder, labels_folder, train_label_folder, test_label_folder)
