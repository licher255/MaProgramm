import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from RT_Cal import RT_Cal
class RT_Plot:
    def __init__(self):
        plt.style.use('default')


    def plot_intensity(self, rt_cal, material1, material2, resolution=0.1):
        # 计算临界入射角
        max_angle_inc_l, max_angle_inc_s = rt_cal.calculate_critical_angles()

        # 根据分辨率生成角度数组
        angles_l = np.arange(0, max_angle_inc_l + resolution, resolution)
        angles_s = np.arange(0, max_angle_inc_s, resolution)

        # 根据每个角度计算对应的反射系数
        intensities_L = [rt_cal.calculate_intensity_coef(angle)[0] for angle in angles_l]
        intensities_S = [rt_cal.calculate_intensity_coef(angle)[1] for angle in angles_s]

        # 使用材料名称作为图的标题（例如 water/aluminium）
        title = f"{material1.name.lower()}/{material2.name.lower()}"

        # 绘图
        plt.figure(figsize=(6, 5))
        plt.xlim(0, 90)
        plt.ylim(0, 1)
        plt.plot(angles_l, intensities_L, marker='', linestyle='-', label='P wave relative intensity')
        plt.plot(angles_s, intensities_S, marker='', linestyle='-', label='S wave relative intensity')

        plt.xlabel(r'Incidence angle $\theta$ (°)')
        plt.ylabel(r'Relative intensity $\frac{I}{I_0}$ (%)')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()


    def plot_material_bars(self, interface2, materials_list, n_segments=100):
        group_width = 0.4
        bar_width = group_width / 8.0

        fig, ax = plt.subplots(figsize=(6, 6))
        num_materials = len(materials_list)
        group_positions = np.arange(num_materials) * group_width + group_width/2

        cmap_p = plt.cm.plasma
        cmap_s = plt.cm.plasma
        p_bar_patch = None
        s_bar_patch = None

        for i, material in enumerate(materials_list):
            rt_cal = RT_Cal(material, interface2)
            crits = rt_cal.calculate_critical_angles()
            crit_L = crits[0] if crits[0] is not None else 0
            crit_S = crits[1] if crits[1] is not None else 0

            x_left = group_positions[i] - bar_width
            x_right = group_positions[i]

            y_vals_L = np.linspace(0, crit_L, n_segments + 1)
            for j in range(n_segments):
                y0 = y_vals_L[j]
                y1 = y_vals_L[j + 1]
                y_mid = (y0 + y1) / 2.0
                intensity_L = rt_cal.calculate_intensity_coef(y_mid)[0]
                color = cmap_p(intensity_L)
                rect = Rectangle((x_left, y0), bar_width, y1 - y0,
                                 facecolor=color, edgecolor=None)
                ax.add_patch(rect)
            outline_L = Rectangle((x_left, 0), bar_width, crit_L,
                                  edgecolor='black', facecolor='none', lw=1)
            ax.add_patch(outline_L)


            y_vals_S = np.linspace(0, crit_S, n_segments + 1)
            for j in range(n_segments):
                y0 = y_vals_S[j]
                y1 = y_vals_S[j + 1]
                y_mid = (y0 + y1) / 2.0
                intensity_S = rt_cal.calculate_intensity_coef(y_mid)[1]
                color = cmap_s(intensity_S)
                rect = Rectangle((x_right, y0), bar_width, y1 - y0,
                                 facecolor=color, edgecolor=None)
                ax.add_patch(rect)
            outline_S = Rectangle((x_right, 0), bar_width, crit_S,
                                  edgecolor='black', facecolor='none', lw=1)
            ax.add_patch(outline_S)

            ax.text(x_left + bar_width/2, crit_L, 'L', ha='center', va='bottom', fontsize=10, color='red')
            ax.text(x_right + bar_width/2, crit_S, 'T', ha='center', va='bottom', fontsize=10, color='blue')


            if p_bar_patch is None:
                p_bar_patch = Rectangle((0, 0), 1, 1, facecolor=cmap_p(0.5), edgecolor='black', lw=1)
            if s_bar_patch is None:
                s_bar_patch = Rectangle((0, 0), 1, 1, facecolor=cmap_s(0.5), edgecolor='black', lw=1)

        material_names = [material.name for material in materials_list]
        ax.set_xticks(group_positions)
        ax.set_xticklabels(material_names)
        ax.set_xlabel('Interface 1 Materials')
        ax.set_ylabel('Incidence angle (°)')
        ax.set_title('Critical incidence angles with gradient-filled bars', y=1.05, pad=5)
        #ax.legend([p_bar_patch, s_bar_patch], ['L wave', 'T wave'])

        ax.set_xlim(0, num_materials * group_width)
        ax.set_ylim(0, 90)
        ax.grid(False)
        plt.show()