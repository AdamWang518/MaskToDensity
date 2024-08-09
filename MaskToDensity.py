import os
import json
import numpy as np
import cv2
from scipy.io import savemat

# 设置输入和输出文件夹路径
input_folder = '/path/to/json_folder'  # 替换为包含JSON文件的文件夹路径
output_folder = '/path/to/output_folder'  # 替换为保存.mat文件的文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有JSON文件
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        json_path = os.path.join(input_folder, filename)
        
        # 读取JSON文件
        with open(json_path) as f:
            labelme_data = json.load(f)
        
        # 自动设置图像大小
        image_height = labelme_data.get('imageHeight', 1024)  # 默认值1024，如果没有该字段
        image_width = labelme_data.get('imageWidth', 1024)    # 默认值1024，如果没有该字段
        image_shape = (image_height, image_width)

        # 创建空的遮罩图像
        mask = np.zeros(image_shape, dtype=np.uint8)

        # 遍历所有多边形并填充遮罩
        for shape in labelme_data['shapes']:
            polygon_points = np.array(shape['points'], dtype=np.int32)
            cv2.fillPoly(mask, [polygon_points], color=255)

        # 生成密度图
        density_map = cv2.GaussianBlur(mask, (15, 15), sigmaX=4, sigmaY=4)

        # 提取所有非零点的坐标
        locations = np.column_stack(np.where(density_map > 0))

        # 对于每个点，指定一个计数值（例如，每个点对应一个“人”）
        counts = density_map[density_map > 0]

        # 构建 image_info 结构
        image_info_struct = np.array([(locations, counts)], dtype=[('location', 'O'), ('number', 'O')])

        # 生成输出文件名
        output_filename = 'GT_' + os.path.splitext(filename)[0] + '.mat'
        output_path = os.path.join(output_folder, output_filename)

        # 保存为.mat文件
        savemat(output_path, {'image_info': image_info_struct})

        print(f'Converted {filename} to {output_filename}')
