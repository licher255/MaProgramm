import matplotlib.pyplot as plt

class RT_Plot:
    def __init__(self):
        # 尝试使用 seaborn 样式，如果不可用则使用默认样式
        plt.style.use('default')

    def plot_intensity(self, angles, intensity_L, intensity_S):
        """
        绘制入射角与P波、S波透射能量系数的关系图

        参数:
            angles: 入射角（单位：度）的列表
            intensity_L: 对应的P波透射能量系数列表
            intensity_S: 对应的S波透射能量系数列表
        """
        plt.figure(figsize=(8, 6))
        plt.plot(angles, intensity_L, marker='o', linestyle='-', label='P wave relative intensity')
        plt.plot(angles, intensity_S, marker='s', linestyle='-', label='S wave relative intensity')
        plt.xlabel(r'Incidence angle $\theta$ (°)')
        plt.ylabel(r'Relative intensity $\frac{I}{I_0}$ (%)')
        plt.title('Water/aluminium')
        plt.legend()
        plt.grid(True)
        plt.show()
