# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec

# -----------------------------
# 1. 准备图片路径与标注
# -----------------------------
img_paths = [
    'cad/cad6-1.png',
    '20250409-Variation-LuftOrderOhne/label/Water-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/AlIce-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/BiSn-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/Gallium-airDefact.png',
    '20250409-Variation-LuftOrderOhne/label/Ice-airdefect.png',
    '20250409-Variation-LuftOrderOhne/label/Lead-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/Rexolite-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/Wax-airDefect.png',
    '20250409-Variation-LuftOrderOhne/label/Zinc-airDefect.png'
]
top_labels = [
    '', 
    'Water', 
    'Al-Ice-Comp.', 
    'BiSn',
    'Gallium', 
    'Ice', 
    'Lead', 
    'Rexolite',
    'Wax', 
    'Zinc'
]
bottom_labels = [f'({chr(ord("a")+i)})' for i in range(len(img_paths))]

# -----------------------------
# 2. 加载并预处理所有图片
# -----------------------------
images = []
for p in img_paths:
    arr = mpimg.imread(p)
    if arr.dtype.kind == 'f':
        arr = (arr * 255).clip(0, 255).astype(np.uint8)
    if arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]
    images.append(arr)

# -----------------------------
# 3. 构造 colormap + 归一化
# -----------------------------
colors = [
    (1,1,1), (0.5,0.8,1), (0,0,1), (0,0,0.5),
    (0,1,0), (1,1,0), (1,0.5,0), (1,0,0), (0,0,0)
]
cmap = LinearSegmentedColormap.from_list('amp_rainbow', colors, N=256)
vmin_db, vmax_db = -100, 0
lin_vmin = 10 ** (vmin_db / 20)
lin_vmax = 10 ** (vmax_db / 20)
norm = LogNorm(vmin=lin_vmin, vmax=lin_vmax)

def db_fmt(x, pos):
    if x <= lin_vmin * (1 + 1e-6):
        return "–∞ dB"
    return f"{20 * np.log10(x):.0f} dB"

# -----------------------------
# 4. 用 GridSpec 创建 7×3 布局（4 行图 + 2 空白行 + 1 行 colorbar）
# -----------------------------
# 定义每段的相对高度（权重）
first_row_h   = 1.3   # 第1行大图
space12_h     = 0.1    # 第1->第2行间距
mid_rows_h    = 1.0    # 第2-4行小图
space45_h     = 0.11    # 第4->第5行间距
cbar_h        = 0.05    # 第5行 colorbar

fig = plt.figure(figsize=(12, 14), constrained_layout=False)
gs = gridspec.GridSpec(
    nrows=7, ncols=3,
    height_ratios=[
        first_row_h,
        space12_h,
        mid_rows_h, mid_rows_h, mid_rows_h,
        space45_h,
        cbar_h
    ],
    hspace=0, wspace=0.01,
    bottom=0.01, top=0.99, left=0.01, right=0.99
)

# 第1行：跨3列的主图
ax0 = fig.add_subplot(gs[0, :])
ax0.imshow(images[0])
ax0.set_xticks([]); ax0.set_yticks([])
ax0.text(0.02, 0.98, top_labels[0], transform=ax0.transAxes,
         ha='left', va='top', fontsize=14)
ax0.annotate(bottom_labels[0], xy=(0.5, -0.05), xycoords='axes fraction',
         ha='center', va='top', fontsize=14)
for spine in ax0.spines.values():
    spine.set_visible(False)
    spine.set_edgecolor('black')
    spine.set_linewidth(0.5)

# 第2-4行：每行3张小图
axes = [ax0]
for row in range(2, 5):
    for col in range(3):
        idx = (row - 2) * 3 + 1 + col
        ax = fig.add_subplot(gs[row, col])
        ax.imshow(images[idx])
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.01, 0.98, top_labels[idx], transform=ax.transAxes,
                ha='left', va='top', fontsize=14)
        ax.annotate(bottom_labels[idx], xy=(0.5, -0.05), xycoords='axes fraction',
                ha='center', va='top', fontsize=14)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)
        axes.append(ax)

# 第7行：跨3列的 colorbar
cax = fig.add_subplot(gs[6, :])
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cbar = fig.colorbar(mappable, cax=cax, orientation='horizontal')
cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x', which='major', labelsize=12, pad=6)

# -----------------------------
# 5. 保存并展示
# -----------------------------
output_dir = '20250409-Variation-LuftOrderOhne/grouped'
os.makedirs(output_dir, exist_ok=True)
fig.savefig(os.path.join(output_dir, '1_3X3.png'), dpi=300, bbox_inches='tight')
# plt.show()
