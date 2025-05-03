from PIL import Image

# —— 输入／输出路径 —— 
input_path  = r"20250411-Variation-3D Stoff\StainSteel347\Steel347-Zinc.png"
output_path = r"20250411-Variation-3D Stoff\crop\Steel347-Zinc.png"

# —— 中心点裁剪参数 —— 
# center_x, center_y 表示裁剪框中心在原图中的坐标 (px)
# width, height 表示裁剪框的宽度和高度 (px)
center_x, center_y = 390, 360
width, height     = 400, 230

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

