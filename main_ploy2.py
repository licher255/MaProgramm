import json
  
from Material import Material
from RT_Plot import RT_Plot

def main():
    # 读取包含材料属性的 JSON 文件
    with open('materials.json', 'r') as file:
        data = json.load(file)

    # 构建一个字典，key 为材料名称（小写），value 为对应的属性
    materials_data = {mat['name'].lower(): mat for mat in data['materials']}

    # 获取 water, ice, plexiglass, aluminium 的属性数据
    water_data = materials_data.get('water')
    ice_data = materials_data.get('ice')
    plexiglass_data = materials_data.get('plexiglass')
    aluminium_data = materials_data.get('aluminium')

    # 创建 Material 实例
    water = Material(water_data['name'],water_data['density'], water_data['vp'], water_data['vs'])
    ice = Material(ice_data['name'],ice_data['density'], ice_data['vp'], ice_data['vs'])
    plexiglass = Material(plexiglass_data['name'],plexiglass_data['density'], plexiglass_data['vp'], plexiglass_data['vs'])
    aluminium = Material(aluminium_data['name'],aluminium_data['density'], aluminium_data['vp'], aluminium_data['vs'])
    
    # 使用 aluminium 作为界面2材料，
    # water, ice, plexiglass 作为界面1材料
    rt_plot = RT_Plot()
    rt_plot.plot_material_bars(aluminium, [water, ice, plexiglass])
    
if __name__ == '__main__':
    main()
