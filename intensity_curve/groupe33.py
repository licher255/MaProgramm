import os
import matplotlib.pyplot as plt
from PIL import Image

# 获取当前文件夹下的 Figure_1.png 到 Figure_9.png

# 获取当前脚本文件所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
image_files = [
    os.path.join(script_dir, f"Figure_{i}.png")
    for i in range(1, 10)
]

# 检查文件是否存在
for img in image_files:
    if not os.path.exists(img):
        raise FileNotFoundError(f"未找到文件: {img}")

# 创建 3x3 子图
fig, axes = plt.subplots(3, 3, figsize=(9, 9))

for idx, (ax, img_path) in enumerate(zip(axes.flatten(), image_files)):
    # 读取并显示图片
    img = Image.open(img_path)
    ax.imshow(img)
    ax.axis('off')
    
    # 计算对应的小写字母，并在子图下方添加
    letter = chr(ord('a') + idx)  # a, b, c, ..., i
    ax.text(
        0.5, -0.01,            # 水平方向居中(0.5)，垂直方向稍微往下(-0.05)
        f'({letter})',
        transform=ax.transAxes,
        ha='center', va='top',
        fontsize=12
    )

plt.tight_layout()
# 保存高分辨率大图
out_path = os.path.join(script_dir, 'figure_grouped.png')
plt.savefig(out_path, dpi=300, bbox_inches='tight')

plt.show()
