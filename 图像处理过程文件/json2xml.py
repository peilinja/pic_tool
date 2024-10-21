# -*- coding: utf-8 -*-
import numpy as np
import json
from lxml import etree
import os
from tqdm import tqdm


class ReadJson(object):
    '''
    读取json文件，获取相应的标签信息
    '''

    def __init__(self, json_path):
        self.json_data = json.load(open(json_path, encoding="utf-8"))
        self.filename = self.json_data['imagePath']
        self.width = self.json_data['imageWidth']
        self.height = self.json_data['imageHeight']

        self.coordis = []
        # 构建坐标
        self.process_shapes()

    def process_shapes(self):
        for single_shape in self.json_data['shapes']:
            if single_shape['shape_type'] == "rectangle":
                bbox_class = single_shape['label']
                xmin = single_shape['points'][0][0]
                ymin = single_shape['points'][0][1]
                xmax = single_shape['points'][1][0]
                ymax = single_shape['points'][1][1]
                self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])
            elif single_shape['shape_type'] == 'polygon':
                bbox_class = single_shape['label']
                temp_points = single_shape['points']
                temp_points = np.array(temp_points)
                xmin, ymin = temp_points.min(axis=0)
                xmax, ymax = temp_points.max(axis=0)
                self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])
            else:
                print("shape type error, shape_type not in ['rectangle', 'polygon']")

    def get_width_height(self):
        return self.width, self.height

    def get_filename(self):
        return self.filename

    def get_coordis(self):
        return self.coordis


class labelimg_Annotations_xml:
    def __init__(self, folder_name, filename, path, database="Unknown"):
        self.root = etree.Element("annotation")
        child1 = etree.SubElement(self.root, "folder")
        child1.text = folder_name
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename
        child3 = etree.SubElement(self.root, "path")
        child3.text = path
        child4 = etree.SubElement(self.root, "source")
        child5 = etree.SubElement(child4, "database")
        child5.text = database

    def set_size(self, width, height, channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(width)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "channel")
        channeln.text = str(channel)

    def set_segmented(self, seg_data=0):
        segmented = etree.SubElement(self.root, "segmented")
        segmented.text = str(seg_data)

    def set_object(self, label, x_min, y_min, x_max, y_max,
                   pose='Unspecified', truncated=0, difficult=0):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        posen = etree.SubElement(object, "pose")
        posen.text = pose
        truncatedn = etree.SubElement(object, "truncated")
        truncatedn.text = str(truncated)
        difficultn = etree.SubElement(object, "difficult")
        difficultn.text = str(difficult)
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(x_min)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(y_min)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(x_max)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(y_max)

    def savefile(self, filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')


def json_transform_xml(json_path, xml_path):
    json_anno = ReadJson(json_path)
    width, height = json_anno.get_width_height()
    channel = 3
    filename = json_anno.get_filename()
    coordis = json_anno.get_coordis()

    anno = labelimg_Annotations_xml('JPEGImages', filename, 'JPEGImages')
    anno.set_size(width, height, channel)
    anno.set_segmented()
    for data in coordis:
        x_min, y_min, x_max, y_max, label = data
        anno.set_object(label, int(x_min), int(y_min), int(x_max), int(y_max))
    anno.savefile(xml_path)


if __name__ == "__main__":
    '''
        目前只能支持 json中 rectangle 和 polygon 两种模式的转换，其中 polygon 的转换方式为，替换成最小外接矩形的左上角和右下角坐标
    '''
    root_json_dir = r"C:\Users\Administrator\Desktop\planet\data"
    # root_save_xml_dir = r"\\SHARE\public\Time_Plus\traindata\bbox\tiaoshui3m\20230418_zxl"
    root_save_xml_dir = root_json_dir
    for json_filename in tqdm(os.listdir(root_json_dir)):
        if not json_filename.endswith(".json"):
            continue
        json_path = os.path.join(root_json_dir, json_filename)
        save_xml_path = os.path.join(root_save_xml_dir, json_filename.replace(".json", ".xml"))
        json_transform_xml(json_path, save_xml_path)

