import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np

# 设置要检查的.mat文件路径
mat_file_path = '/path/to/output_folder/GT_filename.mat'  # 替换为您的.mat文件路径

# 加载.mat文件
mat_data = sio.loadmat(mat_file_path)

# 从.mat文件中提取密度图信息
image_info = mat_data['image_info']
locations = image_info['location'][0, 0]
counts = image_info['number'][0, 0]

# 创建空白图像，用于显示密度图
image_shape = (1024, 1024)  # 根据实际图像大小设置，或者从.mat文件中读取
density_map = np.zeros(image_shape, dtype=np.float32)

# 将点和计数值绘制到图像上
for (y, x), count in zip(locations, counts):
    density_map[int(y), int(x)] = count

# 显示密度图
plt.imshow(density_map, cmap='hot')
plt.colorbar()
plt.title('Density Map')
plt.show()
