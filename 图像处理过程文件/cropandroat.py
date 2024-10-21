import cv2
import numpy as np
import os
import math

# 设置图片标签文件夹及输出文件夹的路径

images_folder = r'C:\Users\Administrator\Desktop\tirecode'
labels_folder = r'C:\Users\Administrator\Desktop\labels'
output_folder = r'C:\Users\Administrator\Desktop\tirecode2'
# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历labels文件夹中的txt文件
import os
import cv2
import numpy as np


def calculate_angle(points):
  # 计算矩形框长边的方向向量
  diff1 = np.subtract(points[2:4], points[:2])  # vector from x1,y1 to x2,y2
  diff2 = np.subtract(points[6:8], points[4:6])  # vector from x3,y3 to x4,y4
  # 计算水平方向向量
  horizontal_vector = (1, 0)
  # 计算两个向量的点积
  dot_product = np.dot(diff1, horizontal_vector)
  # 计算两个向量的模长
  magnitude1 = np.linalg.norm(diff1)
  magnitude2 = np.linalg.norm(horizontal_vector)
  # 计算余弦值
  cos_theta = dot_product / (magnitude1 * magnitude2)
  # 计算角度
  theta = math.acos(cos_theta)
  return theta

# 遍历labels文件夹中的txt文件
for filename in os.listdir(labels_folder):
    if filename.endswith('.txt'):
        # 读取txt文件并解析坐标
        coords_list = []  # 初始化坐标列表，用来存储所有坐标集
        with open(os.path.join(labels_folder, filename), 'r') as f:
            for line in f:
                content = line.strip().split()
                label = int(content[0])
                coords = [float(c) for c in content[1:]]
                angle = calculate_angle(coords)
                # 将弧度转换为角度
                angle_in_degrees = math.degrees(angle)
                angle_deg= angle_in_degrees -90
                # 检查当前行的坐标数量是否正确
                if len(coords) != 8:
                    print(f"Invalid coordinates in {filename}")
                    continue

                coords_list.append((label, coords,angle_deg))  # 将坐标集和标签一起存储

        # 提取图片文件名（假设txt文件名和图片文件名相似）
        image_filename = filename.replace('.txt', '.jpg')  # 或使用其他图片格式，如.png
        image_path = os.path.join(images_folder, image_filename)

        # 检查图片文件是否存在
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue

        # 加载图片
        image = cv2.imread(image_path)

        # 对每个坐标集进行处理
        for label, coords, angle_deg in coords_list:
            # 转换坐标到整数（因为OpenCV操作需要整数坐标）
            pts = np.array(coords, dtype=np.int32).reshape((-1, 1, 2))

            # 获取四边形的掩码
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [pts], (255, 255, 255))

            # 应用掩码到图片上
            cropped_image = cv2.bitwise_and(image, image, mask=mask)

            # 去除掩码区域外的黑色边框
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:  # 确保找到轮廓
                x, y, w, h = cv2.boundingRect(contours[0])
                cropped_image = cropped_image[y:y+h, x:x+w]
            # 获取图像尺寸
            height, width = cropped_image.shape[:2]
            # 定义旋转中心为图像中心
            center = (width // 2, height // 2)
            # 获取旋转矩阵
            M = cv2.getRotationMatrix2D(center, angle_deg, 1)
            # 计算旋转后图像的四个角点的坐标
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            # 新的边界框的宽度和高度
            nW = int((height * sin) + int(width * cos))
            nH = int((height * cos) + int(width * sin))
            #考虑平移
            M[0, 2] += (nW / 2) - center[0]
            M[1, 2] += (nH / 2) - center[1]
            # 将旋转后的图像绘制到背景图像上
            rotated_img = cv2.warpAffine(cropped_image, M, (nW, nH))
            # 保存裁剪后的图片
            output_path = os.path.join(output_folder, str(label), image_filename)
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            cv2.imwrite(output_path, rotated_img)
            print(f"rotated Cropped image saved to {output_path}")
print("ALL CROPPED")

# #批量删除img_folder内文件名的前四个字符
# import os
# for filename in os.listdir(images_folder):
#     if filename.endswith('.jpg'):
#         new_filename = filename[4:]
#         os.rename(os.path.join(images_folder, filename), os.path.join(images_folder, new_filename))