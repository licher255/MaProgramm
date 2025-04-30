import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import FuncFormatter
import numpy as np

# Load image
img = mpimg.imread('20250408-Variation-Geo/add_patch/geo1-1ice.png')
fig, ax = plt.subplots()
ax.imshow(img)
ax.axis('off')

# Custom colormap as before
colors = [
    (1,1,1), (0.5,0.8,1), (0,0,1), (0,0,0.5),
    (0,1,0), (1,1,0), (1,0.5,0), (1,0,0), (0,0,0)
]
cmap = LinearSegmentedColormap.from_list('amp_rainbow', colors, N=256)

# Create inset_axes for a horizontal bar
cax = inset_axes(ax,
                 width="90%",    # 横条占主图宽度的80%
                 height="2%",    # 高度5%
                 loc='lower center',
                 bbox_to_anchor=(0.01, 0.02, 1, 1),  # (x_center, y_bottom, _, _)
                 bbox_transform=ax.transAxes,
                 borderpad=0)

# Norm for amplitude-ratio dB (20*log10) mapping
vmin_db, vmax_db = -100, 0
lin_vmin = 10**(vmin_db/20)
lin_vmax = 10**(vmax_db/20)
norm = LogNorm(vmin=lin_vmin, vmax=lin_vmax)

mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])

# Draw horizontal colorbar
cbar = fig.colorbar(mappable,
                    cax=cax,
                    orientation='horizontal')

# Formatter for dB labels
def db_fmt(x, pos):
    if x <= lin_vmin * 1.0001:
        return "–∞ dB"
    return f"{20 * np.log10(x):.0f} dB"

cbar.ax.xaxis.set_major_formatter(FuncFormatter(db_fmt))
cbar.ax.minorticks_off()
# 1. 告诉 x 轴把刻度线放在上面
cbar.ax.xaxis.set_ticks_position('top')

# 2. 把刻度标签也放在上面
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(axis='x',       # 针对 x 轴
                   which='major',  # 只针对主刻度
                   labelsize=12,
                   labeltop=True,  # 标签放在顶部
                   labelbottom=False,
                   top=True,       # 刻度线放在顶部
                   bottom=False,
                   pad=4)          # 标签与 colorbar 之间的距离
plt.tight_layout()
plt.show()
