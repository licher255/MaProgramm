import numpy as np
import matplotlib.pyplot as plt

# 设置调试开关
DEBUG = True

# 定义介质参数（单位：SI）
# 水 (介质1)
rho1 = 1000.0            # 水的密度 (kg/m^3)
cP1 = 1480.0             # 水中长波速 (m/s)
# 为模拟液体中剪切波无法传播，使用一个非常小且复数的剪切波速
cS1 = 0.0013 + 0.0013j    # (m/s)

# 铝 (介质2)
rho2 = 2700.0            # 铝的密度 (kg/m^3)
cP2 = 6420.0             # 铝中长波速 (m/s)
cS2 = 3040.0             # 铝中剪切波速 (m/s)

def compute_coefficients(theta_deg):
    """
    给定入射角 (单位：°，对应水中 P 波入射角)，计算：
      - 长波反射系数 R_P
      - 剪切波反射系数 R_S
      - 长波透射系数 T_P
      - 剪切波透射系数 T_S
    以及对应的功率（能量）系数：
      - R_P^(pot), R_S^(pot), T_P^(pot), T_S^(pot)
      
    对于水固界面，当入射角接近 0° 时，采用闭式解计算（忽略水侧剪切波部分）。
    """
    
    theta_P1 = np.deg2rad(theta_deg)
    
    # 根据 Snell 定律计算各模式的传播角度：
    # 介质1中 P 波：θ_P1 就是入射角
    # 介质2中 P 波： sinθ_P2 = (cP2/cP1)*sinθ_P1
    arg_P2 = (cP2 / cP1) * np.sin(theta_P1)
    theta_P2 = np.arcsin(arg_P2 + 0j)  # 保证超过 1 时获得复数解
    
    # 介质1中剪切波（液体中不传播，采用复数模拟）：θ_S1 = arcsin((cS1/cP1)*sinθ_P1)
    arg_S1 = (cS1 / cP1) * np.sin(theta_P1)
    theta_S1 = np.arcsin(arg_S1)
    
    # 介质2中剪切波： sinθ_S2 = (cS2/cP1)* sinθ_P1
    arg_S2 = (cS2 / cP1) * np.sin(theta_P1)
    theta_S2 = np.arcsin(arg_S2 + 0j)
    
    # 构造文献中式 (1) 的 4×4 系数矩阵 A 和右侧向量 b
    A = np.zeros((4, 4), dtype=complex)
    # 第一行：
    A[0,0] = np.sin(theta_P1)/(rho1*cP1)
    A[0,1] = np.cos(theta_S1)/(rho1*cS1)
    A[0,2] =  -np.sin(theta_P2)/(rho2*cP2)
    A[0,3] =  np.sin(theta_S2)/(rho2*cS2)
    
    # 第二行：
    A[1,0] = np.cos(theta_P1)/(rho1*cP1)
    A[1,1] = -np.sin(theta_S1)/(rho1*cS1)
    A[1,2] = np.cos(theta_P2)/(rho2*cP2)
    A[1,3] = np.sin(theta_S2)/(rho2*cS2)
    # 第三行：
    A[2,0] = -np.cos(2*theta_S1)
    A[2,1] = np.sin(2*theta_S1)
    A[2,2] = np.cos(2*theta_S2)
    A[2,3] = np.sin(2*theta_S2)

    # 第四行：
    A[3,0] = np.sin(2*theta_P1)/(cP1**2/cS1**2)
    A[3,1] = np.cos(2*theta_S1)
    A[3,2] = np.sin(2*theta_P2)/(cP1**2/cS2**2)
    A[3,3] =  -np.cos(2*theta_S2)

    
    # 右侧向量 b
    b = np.array([
         -np.sin(theta_P1)/(rho1*cP1),
          np.cos(theta_P1)/(rho1*cP1),
          np.cos(2*theta_S1),
          np.sin(2*theta_P1)/(cP1**2/cS1**2)
    ], dtype=np.complex128)

    # 调试打印部分（选择在 θ≈0°, 30°, 60° 处打印）
    if DEBUG and (np.abs(theta_deg - 0) < 1e-3 or np.abs(theta_deg - 30) < 1e-3 or np.abs(theta_deg - 60) < 1e-3):
        print("====================================================")
        print(f"入射角 thetaP1 = {theta_P1} (弧度), {theta_deg} (°)")
        print("矩阵 A:")
        print(A)
        print("向量 b:")
        print(b)
        condA = np.linalg.cond(A)
        print(f"矩阵 A 的条件数: {condA:e}")
    
    # 求解欠定系统：采用最小二乘法求最小范数解
    X = np.linalg.solve(A, b)
    R_P, R_S, T_P, T_S = X
    
    if DEBUG and (np.abs(theta_deg - 30) < 1e-3 or np.abs(theta_deg - 60) < 1e-3):
        print("求解得到的系数:")
        print(f"R_P = {R_P}")
        print(f"R_S = {R_S}")
        print(f"T_P = {T_P}")
        print(f"T_S = {T_S}")
    
    # 定义各模式在各介质中的角阻抗（式 (3)）
    Z_P1 = (cP1 * rho1) / np.cos(theta_P1)
    Z_P2 = (cP2 * rho2) / np.cos(theta_P2)
    Z_S1 = (cS1 * rho1) / np.cos(theta_S1)
    Z_S2 = (cS2 * rho2) / np.cos(theta_S2)
    
    # 根据式 (2) 计算功率（能量）系数
    RP_pot = - R_P * np.conj(R_P)
    RP_pot = np.real(RP_pot)
    
    RS_pot = - R_S * np.conj(R_S) * ( np.real(1/np.conj(Z_S1)) / np.real(1/np.conj(Z_P1)) )
    RS_pot = np.real(RS_pot)
    
    TP_pot = T_P * np.conj(T_P) * ( np.real(1/np.conj(Z_P2)) / np.real(1/np.conj(Z_P1)) )
    TP_pot = np.real(TP_pot)
    
    TS_pot = - T_S * np.conj(T_S) * ( np.real(1/np.conj(Z_S2)) / np.real(1/np.conj(Z_P1)) )
    TS_pot = np.real(TS_pot)
    
    return R_P, R_S, T_P, T_S, RP_pot, RS_pot, TP_pot, TS_pot

# 建立入射角度数组（0° 到 90°）
angles = np.linspace(0, 90, 181)  # 每 0.25°采样一次

# 初始化存储各功率系数的列表
RPp_list = []  # 长波反射功率系数
RSp_list = []  # 剪切波反射功率系数
TPp_list = []  # 长波透射功率系数
TSp_list = []  # 剪切波透射功率系数

# 循环计算各角度下的系数
for ang in angles:
    try:
        R_P, R_S, T_P, T_S, RP_pot, RS_pot, TP_pot, TS_pot = compute_coefficients(ang)
    except Exception as e:
        print(f"计算角 {ang}° 时出错：{e}")
        RP_pot = RS_pot = TP_pot = TS_pot = 0
    RPp_list.append(RP_pot)
    RSp_list.append(RS_pot)
    TPp_list.append(TP_pot)
    TSp_list.append(TS_pot)

# 计算总能量（反射+透射），理论上应接近 1
total_power = np.array(RPp_list) + np.array(TPp_list) + np.array(TSp_list)

# 绘制功率系数曲线
plt.figure(figsize=(8,6))
plt.plot(angles, RPp_list, label=r'$R_P^{(pot)}$')
plt.plot(angles, TPp_list, label=r'$T_P^{(pot)}$')
plt.plot(angles, TSp_list, label=r'$T_S^{(pot)}$')
plt.plot(angles, total_power, label='Total Power', linestyle='--', color='grey')
plt.xlabel("")
plt.ylabel("")
plt.title("Water Aluminum")
plt.legend()
plt.grid(True)
plt.ylim(0, 1.1)
plt.show()
