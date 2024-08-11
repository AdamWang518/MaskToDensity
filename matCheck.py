import scipy.io as sio
import numpy as np

# 递归函数，用于打印字典的所有键和值
def print_dict(d, indent=0):
    for key, value in d.items():
        print('    ' * indent + str(key) + ":")
        if isinstance(value, dict):
            print_dict(value, indent + 1)
        elif isinstance(value, np.ndarray):
            print('    ' * (indent + 1) + f"Array shape: {value.shape}")
            if value.size < 100:  # 如果数组比较小，直接打印内容
                print('    ' * (indent + 1) + f"Values: {value}")
            else:
                print('    ' * (indent + 1) + f"Array too large to display all values.")
        else:
            print('    ' * (indent + 1) + f"Value: {value}")

# 设置要检查的.mat文件路径
# mat_file_path = 'D:\\Github\\MaskToDensity\\video_1_frame_1.mat'  # 替换为您的.mat文件路径
mat_file_path = 'D:\\Github\\MaskToDensity\\GT_video_3_frame_1.mat'  # 替换为您的.mat文件路径
# 加载.mat文件
mat_data = sio.loadmat(mat_file_path)

# 打印.mat文件的所有内容
print_dict(mat_data)
