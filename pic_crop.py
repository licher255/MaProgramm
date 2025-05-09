import os
from PIL import Image

# —— 输入路径 —— 
input_path = r"20250507-Variation-3D Stoff-closedDefect\original\StainlessSteel347\StainlessSteel347-Zinc.png"

# —— 根据 input_path 构造 crop 目录和 output_path —— 
base_dir    = os.path.dirname(input_path)                # e.g. "20250507-Variation-Geo-closedDefect\original"
parent_dir  = os.path.dirname(base_dir)                  # e.g. "20250507-Variation-Geo-closedDefect"
crop_dir    = os.path.join(parent_dir, "crop")           # e.g. "...closedDefect\crop"
os.makedirs(crop_dir, exist_ok=True)                     # 如果不存在就创建
file_name   = os.path.basename(input_path)               # e.g. "geo1-3ice.png"
output_path = os.path.join(crop_dir, file_name)          # 最终输出路径

# —— 中心点裁剪参数 —— 
center_x, center_y = 390,350
width, height     = 400,230

# 计算 left, upper, right, lower
half_w = width  // 2  
half_h = height // 2
left   = center_x - half_w
upper  = center_y - half_h
right  = center_x + half_w
lower  = center_y + half_h
box    = (left, upper, right, lower)

# 打开、裁剪并保存
img     = Image.open(input_path)
cropped = img.crop(box)
cropped.save(output_path)

print(f"已保存：{output_path}")
