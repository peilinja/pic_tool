import xml.etree.ElementTree as ET
import os
import json


def xml_transform_json(xml_path, file, save_path):
    print(os.path.join(xml_path, file))
    # 读取xml文件
    path_file_xml = os.path.join(xml_path, file)
    # 解析读取xml函数
    root = ET.parse(path_file_xml)
    folder = root.find('folder').text
    filename = root.find('filename').text
    path = root.find('path').text
    sz = root.find('size')
    width = int(sz[0].text)
    height = int(sz[1].text)

    # 构建json数据
    data = {}
    data['flags'] = {}
    data['version'] = "4.5.6"
    data["shapes"] = []
    for child in root.findall('object'):  # 找到图片中的所有框
        sub = child.find('bndbox')  # 找到框的标注值并进行读取
        xmin = float(sub[0].text)
        ymin = float(sub[1].text)
        xmax = float(sub[2].text)
        ymax = float(sub[3].text)
        points = [[xmin, ymin], [xmax, ymax]]
        itemData = {'points': []}
        itemData['points'].extend(points)
        name = child.find("name").text
        itemData["flag"] = {}
        itemData["group_id"] = None
        itemData["shape_type"] = "rectangle"
        itemData["label"] = name
        data["shapes"].append(itemData)
    data['imageWidth'] = width
    data['imageHeight'] = height
    data['imageData'] = None
    data['imagePath'] = filename

    filename, extension = os.path.splitext(file)
    jsonName = ".".join([filename, "json"])
    # 写入json
    json_path = os.path.join(save_path, jsonName)
    with open(json_path, "w") as f:
        json.dump(data, f)
    print(json_path, "加载入文件完成...")


if __name__ == '__main__':
    xml_path = r"C:\Users\Administrator\Desktop\planet\data"
    # save_path = r"C:\Users\JoelYang\Desktop\111111\bbox_20230417_gjx"
    save_path = xml_path
    for root, dirs, files in os.walk(xml_path):
        for file in files:
            if not file.endswith(".xml"):
                continue
            xml_transform_json(root, file, save_path)

