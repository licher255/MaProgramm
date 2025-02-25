import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from RT_Cal import RT_Cal
class RT_Plot:
    def __init__(self):
        # 尝试使用 seaborn 样式，如果不可用则使用默认样式
        plt.style.use('default')

    def plot_intensity(self, angles_l, intensity_L, angles_s, intensity_S):
        plt.figure(figsize=(8, 6))
        plt.plot(angles_l, intensity_L, marker='o', linestyle='-', label='P wave relative intensity')
        plt.plot(angles_s, intensity_S, marker='s', linestyle='-', label='S wave relative intensity')
        plt.xlabel(r'Incidence angle $\theta$ (°)')
        plt.ylabel(r'Relative intensity $\frac{I}{I_0}$ (%)')
        plt.title('Water/aluminium')
        plt.legend()
        plt.grid(True)
        plt.show()
    def plot_material_bars(self, interface2, materials_list, n_segments=100):
        """
        绘制柱状图：
        横坐标为界面1材料的名称，每个材料对应两个柱状图，
        左边柱高度为 P 波临界入射角（crit_L），右边柱高度为 S 波临界入射角（crit_S）。
        柱内部以梯度色填充，梯度由入射角下计算得到的能量系数决定。

        参数:
            interface2: Material 类实例，表示界面2（例如 aluminium）
            materials_list: list，包含多个 Material 类实例，表示界面1材料（例如 water、ice、plexiglass）
            n_segments: int，柱内部梯度细分段数（默认100）
        """
        group_width = 0.8
        bar_width = group_width / 3.0

        fig, ax = plt.subplots(figsize=(10, 6))
        num_materials = len(materials_list)
        group_positions = np.arange(num_materials)
        
        # 选用 colormap
        cmap = plt.cm.hot

        p_bar_patch = None
        s_bar_patch = None

        for i, material in enumerate(materials_list):
            # 根据当前材料与界面2构造 RT_Cal 实例
            rt_cal = RT_Cal(material, interface2)
            crits = rt_cal.calculate_critical_angles()
            # 如果返回 None，则赋值为 0
            crit_L = crits[0] if crits[0] is not None else 0
            crit_S = crits[1] if crits[1] is not None else 0

            x_left = group_positions[i] - bar_width / 2.0
            x_right = group_positions[i] + bar_width / 2.0

            # 绘制 P 波柱（左柱）
            y_vals_L = np.linspace(0, crit_L, n_segments + 1)
            for j in range(n_segments):
                y0 = y_vals_L[j]
                y1 = y_vals_L[j + 1]
                y_mid = (y0 + y1) / 2.0
                intensity_L = rt_cal.calculate_intensity_coef(y_mid)[0]
                # intensity_L 应在 [0, 1] 范围内，否则需要归一化
                color = cmap(intensity_L)
                rect = Rectangle((x_left, y0), bar_width, y1 - y0,
                                 facecolor=color, edgecolor=None)
                ax.add_patch(rect)
            outline_L = Rectangle((x_left, 0), bar_width, crit_L,
                                  edgecolor='black', facecolor='none', lw=1)
            ax.add_patch(outline_L)

            # 绘制 S 波柱（右柱）
            y_vals_S = np.linspace(0, crit_S, n_segments + 1)
            for j in range(n_segments):
                y0 = y_vals_S[j]
                y1 = y_vals_S[j + 1]
                y_mid = (y0 + y1) / 2.0
                intensity_S = rt_cal.calculate_intensity_coef(y_mid)[1]
                color = cmap(intensity_S)
                rect = Rectangle((x_right, y0), bar_width, y1 - y0,
                                 facecolor=color, edgecolor=None)
                ax.add_patch(rect)
            outline_S = Rectangle((x_right, 0), bar_width, crit_S,
                                  edgecolor='black', facecolor='none', lw=1)
            ax.add_patch(outline_S)

            # 构造图例的 dummy patch（仅构造一次）
            if p_bar_patch is None:
                p_bar_patch = Rectangle((0, 0), 1, 1, facecolor=cmap(0.5), edgecolor='black', lw=1)
            if s_bar_patch is None:
                s_bar_patch = Rectangle((0, 0), 1, 1, facecolor=cmap(0.5), edgecolor='black', lw=1)

        # 设置横坐标标签
        material_names = [material.name for material in materials_list]
        ax.set_xticks(group_positions)
        ax.set_xticklabels(material_names)
        ax.set_xlabel('Interface 1 Materials')
        ax.set_ylabel('Incidence angle (°)')
        ax.set_title('Critical incidence angles with gradient-filled bars')
        ax.legend([p_bar_patch, s_bar_patch], ['P wave', 'S wave'])
        
        # 设置 y 轴范围（取所有材料中最大的 crit_S）
        max_crit_S = max([RT_Cal(material, interface2).calculate_critical_angles()[1] or 0
                          for material in materials_list])
        ax.set_ylim(0, max_crit_S * 1.1)
        
        ax.grid(True)
        plt.show()