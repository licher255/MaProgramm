# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec
from PIL import Image

# -----------------------------
# 1. 准备图片路径与标注
# -----------------------------
img_paths = [
    'cad/cad5-1.png',
    '20250408-Variation-Geo/geo5-1water.png',
    '20250408-Variation-Geo/geo5-1ice.png'
]
top_labels    = ['', 'geo5-1, water', 'geo5-1, ice']
bottom_labels = ['(a)', '(b)', '(c)']

# -----------------------------
# 2. 加载并预处理所有图片
# -----------------------------
raw_images = []
for p in img_paths:
    arr = mpimg.imread(p)
    # 如果是 float，转 uint8
    if arr.dtype in [np.float32, np.float64]:
        arr = (arr * 255).clip(0, 255).astype(np.uint8)
    # 如果有 alpha 通道，丢弃
    if arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]
    raw_images.append(arr)

# 目标高度与宽度，取图片2 的尺寸
target_h, target_w = raw_images[1].shape[:2]

# 对第一张图做等比例缩放＋透明（白底）填充
img0_pil = Image.fromarray(raw_images[0])
orig_w, orig_h = img0_pil.size
scale = target_h / orig_h
new_w = int(orig_w * scale)
img0_resized = img0_pil.resize((new_w, target_h), Image.BILINEAR)

# 如果宽度不足，左右各自填充透明（最后合成白底 RGB）
if new_w < target_w:
    pad_total = target_w - new_w
    pad_left  = pad_total // 2
    pad_right = pad_total - pad_left

    # 先生成透明底
    canvas = Image.new("RGBA", (target_w, target_h), (255,255,255,0))
    canvas.paste(img0_resized.convert("RGBA"), (pad_left, 0))

    # 再合成到白底，得到 RGB
    white_bg = Image.new("RGB", (target_w, target_h), (255,255,255))
    white_bg.paste(canvas, mask=canvas.split()[3])
    proc0 = white_bg
else:
    proc0 = img0_resized.convert("RGB")

# 更新第一张
images = [np.array(proc0), raw_images[1], raw_images[2]]

# -----------------------------
# 3. 创建紧凑 1×3 布局 + colorbar 行
# -----------------------------
fig = plt.figure(figsize=(12, 5), constrained_layout=True)
gs = fig.add_gridspec(
    nrows=2,
    ncols=3,
    height_ratios=[1, 0.03],
    hspace=0.05,
    wspace=0.02
)
axes = [fig.add_subplot(gs[0, i]) for i in range(3)]

# -----------------------------
# 4. 显示 + 顶部文字 + 外下方标签 + 细黑边框
# -----------------------------
for i, ax in enumerate(axes):
    ax.imshow(images[i])
    ax.set_xticks([]); ax.set_yticks([])

    # 仅第2和第3图加细黑边
    if i > 0:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)

    # 内部顶部文字
    if top_labels[i]:
        ax.text(
            0.5, 0.95,
            top_labels[i],
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=12,
            color='black'
        )

    # 外部底部 (a)(b)(c) 标签
    ax.annotate(
        bottom_labels[i],
        xy=(0.5, -0.05),
        xycoords='axes fraction',
        ha='center', va='top',
        fontsize=12,
        color='black'
    )

# -----------------------------
# 5. 构造 colormap 并添加横向 colorbar
# -----------------------------
colors = [
    (1,1,1), (0.5,0.8,1), (0,0,1), (0,0,0.5),
    (0,1,0), (1,1,0), (1,0.5,0), (1,0,0), (0,0,0)
]
cmap = LinearSegmentedColormap.from_list('amp_rainbow', colors, N=256)
vmin_db, vmax_db = -100, 0
lin_vmin = 10**(vmin_db/20)
lin_vmax = 10**(vmax_db/20)
norm = LogNorm(vmin=lin_vmin, vmax=lin_vmax)
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])

cax = fig.add_subplot(gs[1, :])
cbar = fig.colorbar(mappable, cax=cax, orientation='horizontal')

def db_fmt(x, pos):
    if x <= lin_vmin * (1 + 1e-6):
        return "–∞ dB"
    return f"{20 * np.log10(x):.0f} dB"

cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x', which='major', labelsize=12, pad=4)

# -----------------------------
# 6. 保存高分辨率图像
# -----------------------------
#output_dir = '20250408-Variation-Geo/grouped'
#os.makedirs(output_dir, exist_ok=True)
#output_path = os.path.join(output_dir, 'grouped1_123.png')
#fig.savefig(output_path, dpi=300, bbox_inches='tight')

# -----------------------------
# 7. 展示
# -----------------------------
plt.show()
