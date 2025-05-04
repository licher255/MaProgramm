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
# 假设你一共有 10 张图
img_paths = [
    'cad/cad6-1.png',
    '20250409-Variation-LuftOrderOhne\label\Water-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\AlIce-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\BiSn-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\Gallium-airDefact.png',
    '20250409-Variation-LuftOrderOhne\label\Ice-airdefect.png',
    '20250409-Variation-LuftOrderOhne\label\Lead-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\Rexolite-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\Wax-airDefect.png',
    '20250409-Variation-LuftOrderOhne\label\Zinc-airDefect.png'
]
top_labels    = [
    'geo6-1', 
    'geo6-1, water', 
    'geo6-1, Al-Ice',
    'geo6-1, BiSn', 
    'geo6-1, Gallium', 
    'geo6-1, Ice ',
    'geo6-1, Lead', 
    'geo6-1, Rexolite', 
    'geo6-1, Wax',
    'geo6-1, Zinc'
]
bottom_labels = [f'({chr(ord("a")+i)})' for i in range(len(img_paths))]

# -----------------------------
# 2. 加载并预处理所有图片
# -----------------------------
images = []
for p in img_paths:
    arr = mpimg.imread(p)
    # 如果是 float，转 uint8
    if arr.dtype.kind == 'f':
        arr = (arr*255).clip(0,255).astype(np.uint8)
    # 丢弃 alpha 通道
    if arr.ndim==3 and arr.shape[2]==4:
        arr = arr[:,:,:3]
    images.append(arr)

# -----------------------------
# 3. 构造 colormap + 归一化
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
# 4. 用 GridSpec 创建 6×2 布局（5 行图 + 1 行 colorbar）
# -----------------------------
fig = plt.figure(figsize=(12, 24), constrained_layout=False)
gs = gridspec.GridSpec(
    nrows=6, ncols=2,
    height_ratios=[1]*5 + [0.05],  # 最下面一行高度很小，只放 colorbar
    hspace=0.05, wspace=0.01,
    bottom=0.05, top=0.98, left=0.05, right=0.98
)

# 前 5 行放 10 张图
axes = []
for i in range(5):
    for j in range(2):
        ax = fig.add_subplot(gs[i, j])
        idx = i*2 + j
        ax.imshow(images[idx])
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.2, 0.99, top_labels[idx], transform=ax.transAxes,
                ha='center', va='top', fontsize=12, color='black')
        ax.annotate(bottom_labels[idx],
                    xy=(0.5, -0.05), xycoords='axes fraction',
                    ha='center', va='top', fontsize=12, color='black')
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)
        axes.append(ax)

# 最下面一行跨两列放 colorbar
cax = fig.add_subplot(gs[5, :])
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cbar = fig.colorbar(mappable, cax=cax, orientation='horizontal')
cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
cbar.ax.xaxis.set_ticks_position('top')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x', which='major', labelsize=12, pad=4)
# -----------------------------
# 6. 保存并展示
# -----------------------------
output_dir = '20250409-Variation-LuftOrderOhne\grouped'
os.makedirs(output_dir, exist_ok=True)
fig.savefig(os.path.join(output_dir, '2x5_with_colormap.png'), dpi=300, bbox_inches='tight')
#plt.show()
