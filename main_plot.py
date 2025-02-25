import json
import numpy as np

from Material import Material
from RT_Cal import RT_Cal
from RT_Plot import RT_Plot

def main():
    # 读取包含材料属性的 JSON 文件
    with open('materials.json', 'r') as file:
        data = json.load(file)

    # 构建一个字典，key 为材料名称（小写），value 为对应的属性
    materials_data = {mat['name'].lower(): mat for mat in data['materials']}

    # 获取 water 和 aluminium 的属性数据
    water_data = materials_data.get('water')
    aluminium_data = materials_data.get('aluminium')

    if not water_data or not aluminium_data:
        print("Required materials (water and aluminium) not found in the JSON database.")
        return None

    # 创建 Material 实例
    water = Material(water_data['density'], water_data['vp'], water_data['vs'])
    aluminium = Material(aluminium_data['density'], aluminium_data['vp'], aluminium_data['vs'])

    # 使用 water 作为入射介质，aluminium 作为透射介质，创建 RT_Cal 实例
    rt_cal = RT_Cal(water, aluminium)
    return rt_cal

if __name__ == '__main__':
    rt_cal = main()
    if rt_cal is None:
        exit(1)
    rt_plot = RT_Plot()

    # 分别获取 P 波和 S 波的临界入射角
    Max_angle_inc_l = rt_cal.calculate_critical_angles()[0]
    Max_angle_inc_s = rt_cal.calculate_critical_angles()[1]

    # 分别生成入射角数组：P 波只取到临界角，S 波取全范围
    angles_l = np.arange(0, Max_angle_inc_l+0.1, 0.1)
    angles_s = np.arange(0, Max_angle_inc_s, 0.1)

    # 分别计算能量系数
    intensities_L = [rt_cal.calculate_intensity_coef(angle)[0] for angle in angles_l]
    intensities_S = [rt_cal.calculate_intensity_coef(angle)[1] for angle in angles_s]

    # 修改画图函数，使其支持两个 x 数组
    rt_plot.plot_intensity(angles_l, intensities_L, angles_s, intensities_S)
