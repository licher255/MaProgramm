import json
import matplotlib.pyplot as plt
from Material import Material

def main():
    # 读取包含材料属性的 JSON 文件
    with open('materials.json', 'r') as file:
        data = json.load(file)
    
    # 获取所有材料的数据
    materials = [Material(mat['name'], mat['density'], mat['vp'], mat['vs']) for mat in data['materials']]
    
    # 提取密度和 vp 数据
    densities = [mat.density for mat in materials]
    vp_values = [mat.vp for mat in materials]
    names = [mat.name for mat in materials]
    
    # 绘制散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(densities, vp_values, color='b', marker='o')
    
    # 标注每个点
    for i, name in enumerate(names):
        #plt.text(densities[i], vp_values[i] + 0.02 * max(vp_values), name, fontsize=8, verticalalignment='bottom', horizontalalignment='left')
        plt.text(densities[i]+500, vp_values[i]-80, name, fontsize=8, verticalalignment='bottom', horizontalalignment='left')
    # 设置图表标签
    plt.xlabel(r'Density ($kg/m^3$)')
    plt.ylabel(r'L wave speed ($m/s$)')
    plt.xlim (0,30000) 
    plt.title('Density-sound velocity/logitudinal characteristic')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
