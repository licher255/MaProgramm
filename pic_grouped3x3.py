# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec

# -----------------------------
# 1. 准备图片路径与标注（这里只取前9张）
# -----------------------------
img_paths = [
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Water.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-AlIce.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-BiSn.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Gallium.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Ice.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Lead.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Rexolite.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Wax.png',
    '20250507-Variation-3D Stoff-closedDefect\label\Al-Zinc.png',
]
top_labels = [
    'Water',
    '$Al_2O_3-Ice-Comp.$',
    'BiSn',
    'Gallium',
    'Ice',
    'Lead',
    'Rexolite',
    'Wax',
    'Zinc',
]
bottom_labels = [f'({chr(ord("a")+i)})' for i in range(9)]

# -----------------------------
# 2. 加载并预处理所有图片
# -----------------------------
images = []
for p in img_paths:
    arr = mpimg.imread(p)
    if arr.dtype.kind == 'f':
        arr = (arr * 255).clip(0,255).astype(np.uint8)
    if arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]
    images.append(arr)

# -----------------------------
# 3. 构造 colormap + 归一化（保持不变）
# -----------------------------
colors = [
    (1,1,1),(0.5,0.8,1),(0,0,1),(0,0,0.5),
    (0,1,0),(1,1,0),(1,0.5,0),(1,0,0),(0,0,0)
]
cmap    = LinearSegmentedColormap.from_list('amp_rainbow', colors, N=256)
vmin_db, vmax_db = -100, 0
lin_vmin = 10**(vmin_db/20)
lin_vmax = 10**(vmax_db/20)
norm    = LogNorm(vmin=lin_vmin, vmax=lin_vmax)
def db_fmt(x, pos):
    if x <= lin_vmin*(1+1e-6):
        return "–∞ dB"
    return f"{20*np.log10(x):.0f} dB"

# -----------------------------
# 4. 用 GridSpec 创建 5×3 布局（3 行图 + 1 行空白间隔 + 1 行 colorbar）
fig = plt.figure(figsize=(12, 9), constrained_layout=False)
gap = 0.1  # 这里调节第三行和 colorbar 之间的距离比例，自己试不同值
gs = gridspec.GridSpec(
    nrows=5, ncols=3,
    height_ratios=[1, 1, 1, gap, 0.05],  # 增加了第四行作为空白
    hspace=0.05, wspace=0.01,
    bottom=0.01, top=0.99, left=0.01, right=0.99
)

# 前 3 行放 9 张图（和原来一致，只改行索引到 0–2）
for i in range(3):
    for j in range(3):
        idx = i*3 + j
        ax = fig.add_subplot(gs[i, j])
        ax.imshow(images[idx])
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.01, 0.99, top_labels[idx],
                transform=ax.transAxes, ha='left', va='top',
                fontsize=12)
        ax.annotate(bottom_labels[idx],
                    xy=(0.5, -0.05), xycoords='axes fraction',
                    ha='center', va='top', fontsize=12)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.5)

# 第 4 行（索引 3）留空，不需要任何 subplot

# 第 5 行（索引 4）跨 3 列放 colorbar
cax = fig.add_subplot(gs[4, :])
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cbar = fig.colorbar(mappable, cax=cax, orientation='horizontal')
cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x', which='major', labelsize=12, pad=4)
# -----------------------------
# 5. 保存并展示
# -----------------------------
output_dir = '20250507-Variation-3D Stoff-closedDefect/grouped'
os.makedirs(output_dir, exist_ok=True)
fig.savefig(os.path.join(output_dir, '3x3_Al'),
            dpi=300, bbox_inches='tight')
# plt.show()
