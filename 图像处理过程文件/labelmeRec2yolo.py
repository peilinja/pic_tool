# """
#     labelme标注的矩形json数据集批量转换为yolo格式。
#     需要指定label_dict = {"1": 1, "2": 2,"3":3,"4":4} #标签字典 “”内与labelme保持一致，值按需调整。**yolov5需要标签从0开始
#                                                                                    eg：{"test":0}就是将labelme中标注为test的标签转换为0
#     input_folder = r'C:\Users\Administrator\Desktop\rec' #源文件夹
#     output_folder = r'C:\Users\Administrator\Desktop\rec' #输出文件夹
# """

import json
import os

def convert_labelme_to_yolo(json_path, txt_path, label_dict):
    with open(json_path, 'r') as file:
        data = json.load(file)

    image_width = data['imageWidth']
    image_height = data['imageHeight']

    with open(txt_path, 'w') as file:
        for shape in data['shapes']:
            label = shape['label']
            points = shape['points']
            x_min, y_min = points[0]
            x_max, y_max = points[1]

            x_center = (x_min + x_max) / 2 / image_width
            y_center = (y_min + y_max) / 2 / image_height
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height

            class_id = label_dict[label]
            file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    print(f'finish {json_path} to yolo.')

def batch_convert(input_folder, output_folder, label_dict):
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            json_path = os.path.join(input_folder, file_name)
            txt_path = os.path.join(output_folder, file_name.replace('.json', '.txt'))
            convert_labelme_to_yolo(json_path, txt_path, label_dict)

def create_label_file(label_dict, output_path):
    sorted_labels = [label for label, _ in sorted(label_dict.items(), key=lambda item: item[1])]

    with open(output_path, 'w') as file:
        for label in sorted_labels:
            file.write(f"{label}\n")

if __name__ == '__main__':
    # Example usage
    label_dict = {"0": 0, "1": 1,"2":1,"3":3}
    input_folder = r'C:\Users\Administrator\Desktop\1'
    output_folder = r'C:\Users\Administrator\Desktop\1'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    batch_convert(input_folder, output_folder, label_dict)
    # 生成lableme.txt文件，按照label_dict的值从小到大排列，一个类别1行
    labeltxt_name = 'yolo-label.txt'
    labeltxt_path = os.path.join(output_folder,labeltxt_name)
    create_label_file(label_dict,labeltxt_path)