# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec
import matplotlib.patheffects as patheffects

# -----------------------------
# 1. 准备图片路径与标签
# -----------------------------
base_dir = '20250408-Variation-Geo/add_patch'
nums   = ['1', '2', '3']
types  = ['water', 'ice']
out_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# -----------------------------
# 2. 创建 Figure + GridSpec（超紧凑）
# -----------------------------
fig = plt.figure(figsize=(12, 8), constrained_layout=True)
gs = fig.add_gridspec(
    nrows=3,
    ncols=3,
    height_ratios=[1, 1, 0.05],
    hspace=0.02,
    wspace=0.02
)

# 前两行：3×2 子图
axes = [[fig.add_subplot(gs[i, j]) for j in range(3)] for i in range(2)]

# -----------------------------
# 3. 绘制子图、添加内部顶部文字 + 外部底部标签 + 细黑边框
# -----------------------------
for i, typ in enumerate(types):
    for j, num in enumerate(nums):
        idx = i*3 + j
        ax = axes[i][j]

        # 读图并显示
        fname = os.path.join(base_dir, f'geo4-{num}{typ}.png')
        img = mpimg.imread(fname)
        ax.imshow(img)

        # 隐藏刻度，仅保留薄边框
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)

        # 内部顶部文字：例如 "geo1-1, ice"
        title_txt = f"geo4-{num}, {typ}"
        ax.text(
            0.5, 0.96,
            title_txt,
            transform=ax.transAxes,
            ha='center',
            va='top',
            fontsize=12,
            fontweight='light',
            color='black',
        )

        # 轴外下方标签 (a)-(f)
        ax.set_xlabel(
            out_labels[idx],
            fontsize=12,
            fontweight='normal',
            labelpad=2,
            color='black'
        )

# -----------------------------
# 4. 构造 colormap 和 LogNorm
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

# -----------------------------
# 5. 第三行：横向 colorbar（跨 3 列）
# -----------------------------
cax = fig.add_subplot(gs[2, :])
cbar = fig.colorbar(mappable,
                    cax=cax,
                    orientation='horizontal')

def db_fmt(x, pos):
    if x <= lin_vmin * (1 + 1e-6):
        return "–∞ dB"
    return f"{20 * np.log10(x):.0f} dB"

cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x',
                    which='major',
                    labelsize=12,
                    pad=4)

# -----------------------------
# 6. 显示
# -----------------------------
plt.show()
# -----------------------------
# 7. 保存高分辨率图片
# -----------------------------
output_dir = '20250408-Variation-Geo/grouped'
os.makedirs(output_dir, exist_ok=True)  # 如果不存在则创建文件夹

output_path = os.path.join(output_dir, 'grouped4_123.png')
fig.savefig(output_path, dpi=300, bbox_inches='tight')