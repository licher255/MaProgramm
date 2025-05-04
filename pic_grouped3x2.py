# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec

# -----------------------------
# 1. 准备图片路径与标签
# -----------------------------
base_dir   = '20250408-Variation-Geo/label'
nums       = ['1', '2', '3']
types      = ['ice', 'water']        # 列顺序：ice 在第一列，water 在第二列
out_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# -----------------------------
# 2. 创建 Figure + GridSpe6
# -----------------------------
fig = plt.figure(figsize=(6, 8), constrained_layout=True)
# 4 行 2 列：前三行为图像，第四行为 colorbar
gs = fig.add_gridspec(
    nrows=4,
    ncols=2,
    height_ratios=[1, 1, 1, 0.05],
    hspace=0.001,
    wspace=0.001
)

# 前三行图像子轴
axes = [
    [fig.add_subplot(gs[i, j]) for j in range(2)]
    for i in range(3)
]

# -----------------------------
# 3. 绘制子图、添加标题 & 标签
# -----------------------------
for i, num in enumerate(nums):        # 行：1,2,3
    for j, typ in enumerate(types):   # 列：ice, water
        idx = i*2 + j
        ax = axes[i][j]

        # 读图并显示
        fname = os.path.join(base_dir, f'geo1-{num}{typ}.png')
        img   = mpimg.imread(fname)
        ax.imshow(img, aspect='equal')  # 保持图像原始宽高比

        # 隐藏坐标刻度，仅保留细边框
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)

        # 内部顶部文字：例如 "geo1-1, ice"
        ax.text(
            0.5, 0.96,
            f"geo1-{num}, {typ}",
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=12, color='black'
        )

        # 轴外下方标签 (a)-(f)
        ax.set_xlabel(
            out_labels[idx],
            fontsize=12, labelpad=4, color='black'
        )

# -----------------------------
# 4. 构造 colormap 和 LogNorm
# -----------------------------
colors = [
    (1,1,1), (0.5,0.8,1), (0,0,1), (0,0,0.5),
    (0,1,0), (1,1,0), (1,0.5,0), (1,0,0), (0,0,0)
]
cmap       = LinearSegmentedColormap.from_list('amp_rainbow', colors, N=256)
vmin_db    = -100
vmax_db    = 0
lin_vmin   = 10**(vmin_db/20)
lin_vmax   = 10**(vmax_db/20)
norm       = LogNorm(vmin=lin_vmin, vmax=lin_vmax)
mappable   = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])

# -----------------------------
# 5. 底部 colorbar（跨 2 列）
# -----------------------------
cax = fig.add_subplot(gs[3, :])
cbar = fig.colorbar(
    mappable,
    cax=cax,
    orientation='horizontal'
)

def db_fmt(x, pos):
    if x <= lin_vmin * (1 + 1e-6):
        return "–∞ dB"
    return f"{20 * np.log10(x):.0f} dB"

cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x', which='major', labelsize=12, pad=6)

# -----------------------------
# 6. 显示并保存
# -----------------------------
#plt.show()

output_dir = '20250408-Variation-Geo/grouped'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'grouped1_123.png')
fig.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved figure to {output_path}")
