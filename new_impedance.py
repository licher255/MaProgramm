import json
import math

# 定义 Material 类
class Material:
    def __init__(self, name, density, vp, vs):
        self.name = name
        self.density = density
        self.vp = vp
        self.vs = vs

def main():
    # 读取材料数据
    with open('materials.json', 'r') as file:
        data = json.load(file)

    # 构建材料对象列表
    materials = [Material(mat['name'], float(mat['density']), float(mat['vp']), (mat['vs'])) for mat in data['materials']]

    # 找出 Aluminium 的 density 和 vs
    aluminium = next(mat for mat in materials if mat.name.lower() == 'aluminium')
    vs_al = aluminium.vs
    density_al = aluminium.density

    # 计算 "声阻抗距离"（欧氏距离）
    distance_list = []
    for mat in materials:
        if mat.name.lower() == 'aluminium':
            continue
        distance = math.sqrt((vs_al - mat.vp) ** 2 + (density_al - mat.density) ** 2)
        distance_list.append((mat.name, distance))

    # 排序：距离从小到大
    distance_list.sort(key=lambda x: x[1])

    # 打印结果（常规数字格式）
    print("\n与 Aluminium 的声阻抗距离（从小到大）：")
    for name, dist in distance_list:
        print(f"{name}: 距离 = {dist:,.2f}")

if __name__ == "__main__":
    main()
