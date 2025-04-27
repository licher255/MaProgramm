import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize


def create_custom_rainbow_cmap(colors=None, n_colors=256):
    """创建一个自定义的 rainbow colormap，按给定颜色顺序插值。"""
    if colors is None:
        # 默认颜色序列：白 - 浅蓝 - 蓝 - 绿 - 黄 - 橙 - 红
        colors = ['white', 'cyan', 'blue', 'green', 'yellow', 'orange', 'red']
    return LinearSegmentedColormap.from_list('custom_rainbow', colors, N=n_colors)


def plot_heatmap_db(data_db, cmap, db_max=-16, label='Magnitude (dB)', orientation='horizontal'):
    """
    绘制 dB 值热力图并添加色标注释。
    红色对应最大 dB（db_max），白色对应最小（-inf），在色条底部显示下溢箭头。
    """
    # 将 -inf 掩码，以显示为白色
    data = np.ma.masked_where(np.isneginf(data_db), data_db)
    # 设定 dB 范围：vmin=数据中最小有限值，vmax=db_max
    db_min = data.min()  # 最小有限值
    norm = Normalize(vmin=db_min, vmax=db_max, clip=False)

    plt.figure(figsize=(8, 3) if orientation=='horizontal' else (4, 6))
    im = plt.imshow(data, cmap=cmap, norm=norm, aspect='auto')
    # colorbar 方向和下溢箭头
    cbar = plt.colorbar(im, orientation=orientation, pad=0.2, extend='min')
    cbar.set_label(label)
    plt.xticks([])
    plt.yticks([])
    plt.title(f'Heatmap ({label}), Red = {db_max} dB, White = -inf')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # 示例：模拟 dB 矩阵，部分值为 -inf
    matrix_db = np.random.uniform(-60, -16, size=(10, 10))
    matrix_db[np.random.rand(10, 10) < 0.1] = -np.inf  # 随机置为 -inf

    # 创建自定义 colormap（白→浅蓝→蓝→…→红）
    custom_cmap = create_custom_rainbow_cmap()
    # 绘制热力图示例，红色代表最大 -16 dB，白色代表 -inf
    plot_heatmap_db(matrix_db, custom_cmap, db_max=-16, label='Magnitude (dB)', orientation='horizontal')

    # 如需垂直 colorbar：
    # plot_heatmap_db(matrix_db, custom_cmap, db_max=-16, label='Magnitude (dB)', orientation='vertical')
