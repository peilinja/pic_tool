# """
#     语义分割训练及图像增强（需要mask和原图均为png）
#     aug函数生成的增强mask和增强原图保存在orinpath的output子文件夹内
#     批量运行后进行分离；
#     mask文件开头为“_groundtruth_”
#     原图文件开头为“testjpg_original_”
#        流程：   1.转png；2.图像增强；3.改名+原图改回jpg
# """
import os
import Augmentor
import shutil

# 修改文件后缀名
def changename(folder_path,orinend,newend):
    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        # 检查文件是否是.png格式
        if filename.endswith(orinend):
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, filename)
            try:
                base_filename = os.path.splitext(filename)[0]  # 去掉扩展名
                new_filename = base_filename + newend  # 添加新的扩展名
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)
                # print(f" 已修改 {filename} 为 {new_filename}，并删除原始文件")
            except:
                print(f"修改时{filename}发生异常，未能修改成功")
    print(f"All done folder {folder_path} file {orinend} to {newend}")

# 图像增强
def aug(orinpath,maskpath,n):
    # 确定原始图像存储路径以及掩码文件存储路径
    p = Augmentor.Pipeline(orinpath)
    p.ground_truth(maskpath)
    # 图像旋转： 按照概率0.8执行，最大左旋角度10，最大右旋角度10
    p.rotate(probability=0.8, max_left_rotation=15, max_right_rotation=15)
    # 图像左右互换： 按照概率0.5执行
    p.flip_left_right(probability=0.5)
    #随即翻转
    p.flip_random(probability=1)
    # 图像放大缩小： 按照概率0.8执行，面积为原始图0.85倍
    p.zoom_random(probability=0.3, percentage_area=0.85)
    # 最终扩充的数据样本数
    p.sample(n)

# 获取原图（转png后）数量
def count_n(orinpath):
    png_files = [entry for entry in os.listdir(orinpath) if entry.endswith('.png')]
    count = len(png_files)
    return count

#移动已moveconclude开头的文件
def moveaugfile(moveconclude,fromfolder,tofolder):
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(fromfolder):
        # 检查文件名是否以'_groundtruth_'开头
        if filename.startswith(moveconclude):
            # 构建源文件的完整路径和目标文件的完整路径
            source_path = os.path.join(fromfolder, filename)
            destination_path = os.path.join(tofolder, filename)
            # 移动文件
            shutil.move(source_path, destination_path)
            #print(f"Moved {filename} to {tofolder}")
    print(f"All files starting with {moveconclude} have been moved to the 'mask' folder.")

#文件重命名（取第一个.之后的文件名为新文件名）
def changeaugfilename(folder):
    for filename in os.listdir(folder):
        # 原始文件名
        original_filename = filename
        # 找到第一个点的位置
        first_dot_index = original_filename.find('.')
        # 如果找到了点，则截取第一个点之后的所有内容作为新文件名
        if first_dot_index != -1:
            new_filename = original_filename[first_dot_index + 1:]
        else:
            print("No dot found in the filename.")
        # 完整路径
        source_path = os.path.join(folder,filename)
        target_path = os.path.join(folder,new_filename)
        # 重命名文件
        try:
            os.rename(source_path, target_path)
        except Exception as e:
            print(f"Error renaming file: {e}")
    print(f"All done rename folder {folder}")

# 批量
# 设置文件夹
orinpath = r"C:\Users\Administrator\Desktop\gas_orin"
maskpath = r"C:\Users\Administrator\Desktop\gas_seg"
augoutput_path = os.path.join(orinpath,'output')
maskaug_save = r"C:\Users\Administrator\Desktop\SegmentationAUG"
orinaug_save = r"C:\Users\Administrator\Desktop\orinAUG"

# 确保目标文件夹存在，如果不存在则创建它
if not os.path.exists(maskaug_save):
    os.makedirs(maskaug_save)

if not os.path.exists(orinaug_save ):
    os.makedirs(orinaug_save )

# 原图jpg改png
changename(orinpath,'.jpg','.png')
# 设置增强数量为原图10倍
n = count_n(orinpath)*5
# 图像增强处理
aug(orinpath,maskpath,n)
#移动增强后原图及mask图
moveaugfile('_groundtruth_',augoutput_path,maskaug_save)
orinfilename = os.path.basename(orinpath)
moveaugfile(orinfilename,augoutput_path,orinaug_save)
#重命名增强图
changeaugfilename(maskaug_save)
changeaugfilename(orinaug_save)
#修改增强后原图至jpg
changename(orinaug_save,'.png','.jpg')

#删除原图文件加内的output子文件夹，改回jpg
if os.path.exists(augoutput_path):
    # 递归删除文件夹及其内容
    shutil.rmtree(augoutput_path)
    print(f"The '{augoutput_path}' folder and its contents have been deleted.")
else:
    print(f"The '{augoutput_path}' folder does not exist.")
changename(orinpath,'.png','.jpg')