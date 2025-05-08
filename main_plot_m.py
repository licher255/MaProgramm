import json
import os
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})

# 定义 Material 类
class Material:
    def __init__(self, name, density, vp, vs):
        self.name = name
        self.density = density
        self.vp = vp
        self.vs = vs

def plot_hyperbola(constant, label, color):
    x_vals = list(range(500, 30000, 100))
    y_vals = [constant / x if x != 0 else 0 for x in x_vals]
    plt.plot(x_vals, y_vals, linestyle='--', linewidth=1.5, color=color, label=label)


def main():
    # 读取 JSON 数据
    with open('materials.json', 'r') as file:
        data = json.load(file)

    # 创建 Material 实例列表
    materials = [Material(mat['name'], mat['density'], mat['vp'], mat['vs']) for mat in data['materials']]

    # 自定义展示标签
    custom_labels = {
        "al ice composite": "Al-Ice Composite",
        "bi sn": "BiSn",
        "gallium": "Gallium",
        "ice": "Ice",
        "lead": "Lead",
        "water": "Water",
        "wax": "Wax",
        "rexolite": "Rexolite",
        "zinc": "Zinc",
        "aluminium": "Aluminium",
        "stainless steel347": "Stainless Steel347",
        "hastelloy x": "Hastelloy X"
    }

    # 提取绘图所需数据
    densities = [mat.density for mat in materials]
    vp_values = [mat.vp for mat in materials]

    # 设置颜色
    colors = []
    for mat in materials:
        name_lower = mat.name.lower()
        if name_lower == "aluminium":
            colors.append('red')
        elif name_lower == "hastelloy x":
            colors.append('green')
        elif name_lower == "stainless steel347":
            colors.append('orange')
        else:
            colors.append('blue')

    # 绘制散点图
    plt.figure(figsize=(10, 7))
    plt.scatter(densities, vp_values, c=colors, marker='o')

    # 添加文字标签
    for i, mat in enumerate(materials):
        name_key = mat.name.lower()
        label = custom_labels.get(name_key, mat.name.title())
        x, y = mat.density, mat.vp

        # 默认偏移
        dx, dy = 280, -100

        # 调整特定标签位置
        if name_key == "hastelloy x":
            dx, dy = -200, 100
        elif name_key == "stainless steel347":
            dx, dy = -280, -300
        elif name_key == "aluminium":
            dx, dy = 280, -100
        elif name_key == "gallium":
            dx, dy = 0, -250

        plt.text(x + dx, y + dy, label, fontsize=12, verticalalignment='bottom')

    # 添加乘积不变曲线
    for mat in materials:
        name = mat.name.lower()
        if name in ["aluminium", "stainless steel347", "hastelloy x"]:
            C = mat.density * mat.vp
            label = custom_labels[name]
            if name == "aluminium":
                plot_hyperbola(C, f"{label}: Impedance $z$ = {C:.1e}kg/($m^2 s$)", color='red')
            elif name == "hastelloy x":
                plot_hyperbola(C, f"{label}: Impedance $z$ = {C:.1e}kg/($m^2 s$)", color='green')
            elif name == "stainless steel347":
                plot_hyperbola(C, f"{label}: Impedance $z$ = {C:.1e}kg/($m^2 s$)", color='orange')

    # 图表设置
    plt.xlabel(r'Density ($kg/m^3$)')
    plt.ylabel(r'L wave speed ($m/s$)')
    #plt.title('Density vs. Longitudinal Velocity')
    plt.xlim(0, 30000)
    plt.ylim(0, 7000)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    output_dir = 'pic_rec'
    #os.makedirs(output_dir, exist_ok=True)
    #plt.savefig(os.path.join(output_dir, 'impedance.png'), dpi=300, bbox_inches='tight')  # ← 必须在 show() 之前
    #plt.show()
    # ------------------- 计算声阻抗及与Aluminium差值排序 -------------------
    print("\n声阻抗差值（与 hastelloy x 比较，从大到小排序）：")
    # 计算每个材料的声阻抗
    impedance_dict = {mat.name: mat.density * mat.vp for mat in materials}

    # 找出 Aluminium 的声阻抗
    aluminium_impedance = None
    for name, imp in impedance_dict.items():
        if name.lower() == "hastelloy x":
            aluminium_impedance = imp
            break

    # 计算与 Aluminium 的差值
    impedance_diffs = []
    for name, imp in impedance_dict.items():
        if name.lower() != "hastelloy x":
            diff = abs(imp - aluminium_impedance)
            impedance_diffs.append((name, diff))

    # 排序（从大到小）
    impedance_diffs.sort(key=lambda x: x[1], reverse=True)

    # 打印结果
    for name, diff in impedance_diffs:
        print(f"{name}: 差值 = {diff:.2e} kg/(m²·s)")

if __name__ == "__main__":
    main()



