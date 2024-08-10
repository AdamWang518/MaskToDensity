import json
import numpy as np
from scipy.io import savemat
import os

# 定義JSON文件所在的資料夾路徑
json_folder_path = 'D:\\Github\\MaskToDensity\\'
mat_folder_path = 'D:\\Github\\MaskToDensity\\'

# 遍歷資料夾中的所有JSON文件
for filename in os.listdir(json_folder_path):
    if filename.endswith('.json'):
        json_path = os.path.join(json_folder_path, filename)
        mat_filename = 'GT_' + filename.replace('.json', '.mat')
        mat_path = os.path.join(mat_folder_path, mat_filename)

        # 讀取JSON文件
        with open(json_path, 'r') as file:
            data = json.load(file)

        # 提取多邊形點
        shapes = data['shapes']
        structured_array = []

        for shape in shapes:
            points = np.array(shape['points'], dtype=np.float64)
            point_count = np.array([[len(points)]], dtype=np.uint8)  # 使用點的數量
            structured_array.append((points, point_count))

        # 根據目標格式建立結構
        structured_data = np.array([structured_array], dtype=[('location', 'O'), ('number', 'O')])

        # 封裝到最終數據結構中，並符合特定的嵌套格式
        final_structure = np.array([[structured_data]])

        # 保存到.mat檔案
        savemat(mat_path, {'image_info': final_structure})

# 確認處理完畢
print("所有JSON文件已轉換為MAT檔案，並以 'GT_原檔名.mat' 格式命名。")
