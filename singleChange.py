import json
import numpy as np
from scipy.io import savemat

# 讀取JSON文件
with open('241.json', 'r') as file:
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
output_mat_file = 'output_file_path.mat'
savemat(output_mat_file, {
    'image_info': final_structure
})

