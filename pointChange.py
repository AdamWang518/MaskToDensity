import json
import numpy as np
from scipy.io import savemat
from PIL import Image

def json_to_mat(json_file_path, image_path, output_mat_path):
    """
    Convert JSON annotation format to the specified MAT format, ensuring consistency with the provided format.
    
    Parameters:
    - json_file_path: Path to the JSON format file.
    - image_path: Path to the image file (to read its size).
    - output_mat_path: Path to save the output MAT file.
    """
    # Read the image to get its size
    with Image.open(image_path) as img:
        image_size = img.size  # (width, height)

    # Read JSON annotations
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract point locations from JSON
    locations = np.array([shape['points'][0] for shape in data['shapes']], dtype='float32')

    # Ensure correct data structuring for MAT file
    number_array = np.array([len(locations)], dtype=np.uint8)

    # Create the nested structure with the three layers and correct dtype
    struct_array = np.array([[(locations, number_array)]],
                            dtype=[('location', 'O'), ('number', 'O')])
    image_info = np.empty((1, 1), dtype=object)
    image_info[0, 0] = struct_array

    # Save to MAT file with proper structure
    mat_data = {'image_info': image_info}
    savemat(output_mat_path, mat_data)

# Example usage
json_file_path = 'video_1_frame_1.json'
image_path = 'video_1_frame_1.jpg'  # The path to the image file
output_mat_path = 'video_1_frame_1.mat'

json_to_mat(json_file_path, image_path, output_mat_path)
