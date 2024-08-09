import os
import json
import numpy as np
from scipy.io import savemat
from PIL import Image, ImageDraw

def convert_json_to_mat(json_folder, mat_folder, image_size):
    if not os.path.exists(mat_folder):
        os.makedirs(mat_folder)

    for json_file in os.listdir(json_folder):
        if json_file.endswith(".json"):
            json_path = os.path.join(json_folder, json_file)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 创建一个空的二值图像，用于保存遮罩
            mask = Image.new('L', (image_size[0], image_size[1]), 0)
            draw = ImageDraw.Draw(mask)

            for shape in data['shapes']:
                if shape['shape_type'] == 'polygon':
                    polygon = [tuple(point) for point in shape['points']]
                    draw.polygon(polygon, outline=1, fill=1)

            # 将遮罩转换为numpy数组
            mask_np = np.array(mask)

            # 创建符合你提供的结构的数据
            image_info = np.array([[(mask_np, np.array([[234]], dtype=np.uint8))]], dtype=[('location', 'O'), ('number', 'O')])

            # 保存为.mat文件
            mat_file_name = 'GT_'+os.path.splitext(json_file)[0] + '.mat'
            mat_path = os.path.join(mat_folder, mat_file_name)
            savemat(mat_path, {'image_info': image_info})

            print(f"{mat_file_name} 已保存.")

json_folder = "D:\\Github\\MaskToDensity\\"  # 替换为你的json文件夹路径
mat_folder = "D:\\Github\\MaskToDensity\\"  # 替换为你想保存mat文件的路径
image_size = (1920, 1080)  # 替换为你的图像尺寸

convert_json_to_mat(json_folder, mat_folder, image_size)
