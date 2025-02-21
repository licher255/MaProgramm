import json
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
    # 从 main() 中获得 RT_Cal 实例
    rt_cal = main()
    if rt_cal is None:
        exit(1)
    
    # 实例化画图类
    rt_plot = RT_Plot()
    
    # 定义入射角范围，比如 0 到 85 度，每隔 5 度计算一次
    angles = list(range(0, 90, 5))
    intensities_L = []
    intensities_S = []
    
    # 遍历各入射角，计算对应的能量系数
    for angle in angles:
        T_intensity_L, T_intensity_S = rt_cal.calculate_intensity_coef(angle)
        intensities_L.append(T_intensity_L)
        intensities_S.append(T_intensity_S)
    
    # 调用画图方法，绘制图形
    rt_plot.plot_intensity(angles, intensities_L, intensities_S)
