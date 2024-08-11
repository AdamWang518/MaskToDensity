import os
import json
import numpy as np
from scipy.io import savemat
from PIL import Image

def json_to_mat(json_file_path, image_path, output_mat_path):
    """
    將 JSON 標註格式轉換為指定的 MAT 格式，確保與提供的格式一致。
    
    參數:
    - json_file_path: JSON 檔案的路徑。
    - image_path: 影像檔案的路徑（用來獲取其大小）。
    - output_mat_path: 儲存輸出的 MAT 檔案路徑。
    """
    # 讀取影像以獲取其大小
    with Image.open(image_path) as img:
        image_size = img.size  # (寬度, 高度)

    # 讀取 JSON 標註
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # 從 JSON 中提取所有點位資料
    locations = []
    for shape in data['shapes']:
        for point in shape['points']:
            locations.append(point)  # 提取所有點位並加入到 locations 陣列中
    locations = np.array(locations, dtype='float32')

    # 確保資料結構正確以便保存為 MAT 檔案
    number_array = np.array([[len(locations)]], dtype=np.uint8)

    # 創建具有三層結構且正確數據類型的結構陣列
    struct_array = np.array([[(locations, number_array)]],
                            dtype=[('location', 'O'), ('number', 'O')])
    image_info = np.empty((1, 1), dtype=object)
    image_info[0, 0] = struct_array

    # 保存為 MAT 檔案並確保結構正確
    mat_data = {'image_info': image_info}
    savemat(output_mat_path, mat_data)

def process_folder(folder_path):
    """
    處理資料夾中的所有 JSON 和影像檔案，將它們轉換為 MAT 檔案。
    
    參數:
    - folder_path: 資料夾路徑。
    """
    # 獲取資料夾中的所有檔案
    files = os.listdir(folder_path)
    
    # 過濾出 JSON 檔案
    json_files = [f for f in files if f.endswith('.json')]
    
    # 逐一處理每個 JSON 檔案
    for json_file in json_files:
        # 構建完整的檔案路徑
        json_file_path = os.path.join(folder_path, json_file)
        
        # 對應的影像檔案名稱
        image_file = json_file.replace('.json', '.jpg')
        image_file_path = os.path.join(folder_path, image_file)
        
        # 輸出的 MAT 檔案名稱，加上 GT_ 前綴
        output_mat_file = 'GT_' + json_file.replace('.json', '.mat')
        output_mat_path = os.path.join(folder_path, output_mat_file)
        
        # 執行轉換
        json_to_mat(json_file_path, image_file_path, output_mat_path)
        print(f"已處理並轉換: {json_file} 為 {output_mat_file}")

# 使用範例
folder_path = 'D:\\Github\\MaskToDensity\\Net\\Label_finish\\'  # 替換為你的資料夾路徑
process_folder(folder_path)
