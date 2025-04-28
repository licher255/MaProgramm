import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from RT_Cal_v2 import RT_Cal_v2  # 假设你的新类叫 RT_Cal_v2

class RT_Plot:
    def __init__(self):
        plt.style.use('default')

    def plot_intensity(self, rt_cal: RT_Cal_v2, material1, material2, resolution=0.1):
        # 1. 临界入射角
        max_angle_inc_l, max_angle_inc_s = rt_cal.calculate_critical_angles()

        # 2. 角度数组
        angles_l = np.arange(0, max_angle_inc_l + resolution, resolution)
        angles_s = np.arange(0, max_angle_inc_s + resolution, resolution)

        # 3. 计算透射 P 波 和 T 波（即新算法的 'T_P' 和 'T_S'）
        intensities_L = [
            rt_cal.calculate_intensity_coef(angle)['T_P']
            for angle in angles_l
        ]
        intensities_S = [
            rt_cal.calculate_intensity_coef(angle)['T_S']
            for angle in angles_s
        ]

        # 4. 绘图
        title = f"{material1.name.title()}/{material2.name.title()}"
        plt.figure(figsize=(6, 5))
        plt.plot(angles_l, intensities_L, linestyle='-', linewidth=2, label=r'$T^I_L$')
        plt.plot(angles_s, intensities_S, linestyle='--', linewidth=2, label=r'$T^I_S$')

        plt.xlim(0, 90)
        plt.ylim(0, 1.0)
        plt.xlabel(r'Incidence Angle $\theta$ (°)', fontsize=12)
        plt.ylabel(r'Transmission Intensity Coefficient $\frac{I}{I_{inc}}$', fontsize=12)
        plt.title(title, fontsize=14)
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_material_bars(self, interface2, materials_list, n_segments=100):
        group_width = 0.4
        bar_width = group_width / 8.0

        fig, ax = plt.subplots(figsize=(6, 6))
        num_materials = len(materials_list)
        group_positions = np.arange(num_materials) * group_width + group_width/2

        cmap_p = plt.cm.rainbow
        cmap_s = plt.cm.rainbow
        p_bar_patch = None
        s_bar_patch = None

        for i, material in enumerate(materials_list):
            rt_cal = RT_Cal_v2(material, interface2)
            crit_L, crit_S = rt_cal.calculate_critical_angles()

            # 左侧 P 波条
            x_left = group_positions[i] - bar_width
            y_vals_L = np.linspace(0, crit_L, n_segments + 1)
            for j in range(n_segments):
                y0, y1 = y_vals_L[j], y_vals_L[j+1]
                mid = (y0 + y1)/2
                I_p = rt_cal.calculate_intensity_coef(mid)['T_P']
                rect = Rectangle((x_left, y0), bar_width, y1-y0,
                                 facecolor=cmap_p(I_p), edgecolor=None)
                ax.add_patch(rect)
            ax.add_patch(Rectangle((x_left, 0), bar_width, crit_L,
                                   edgecolor='black', facecolor='none', lw=1))
            ax.text(x_left+bar_width/2, crit_L, 'P', ha='center', va='bottom', color='red')

            # 右侧 S 波条
            x_right = group_positions[i]
            y_vals_S = np.linspace(0, crit_S, n_segments + 1)
            for j in range(n_segments):
                y0, y1 = y_vals_S[j], y_vals_S[j+1]
                mid = (y0 + y1)/2
                I_s = rt_cal.calculate_intensity_coef(mid)['T_S']
                rect = Rectangle((x_right, y0), bar_width, y1-y0,
                                 facecolor=cmap_s(I_s), edgecolor=None)
                ax.add_patch(rect)
            ax.add_patch(Rectangle((x_right, 0), bar_width, crit_S,
                                   edgecolor='black', facecolor='none', lw=1))
            ax.text(x_right+bar_width/2, crit_S, 'S', ha='center', va='bottom', color='blue')

            # 准备图例样本
            if p_bar_patch is None:
                p_bar_patch = Rectangle((0,0),1,1,facecolor=cmap_p(0.5),edgecolor='black')
            if s_bar_patch is None:
                s_bar_patch = Rectangle((0,0),1,1,facecolor=cmap_s(0.5),edgecolor='black')

        # 坐标与标签
        ax.set_xticks(group_positions)
        ax.set_xticklabels([m.name for m in materials_list])
        ax.set_xlabel('Interface 1 Materials')
        ax.set_ylabel('Incidence Angle (°)')
        ax.set_title('Critical Angles with Transmission Intensity Gradient', pad=10)
        # ax.legend([p_bar_patch, s_bar_patch], ['P-wave', 'S-wave'])

        ax.set_xlim(-bar_width, num_materials*group_width)
        ax.set_ylim(0, 90)
        ax.grid(False)
        plt.show()
