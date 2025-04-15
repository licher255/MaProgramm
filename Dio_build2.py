import numpy as np
import matplotlib.pyplot as plt

# 使用 np.lib.scimath.arcsin 处理超出 [-1,1] 的情况，返回复数解
asin_complex = np.lib.scimath.arcsin

def compute_coeffs(theta_inc, rho1, cP1, cS1, rho2, cP2, cS2):
    """
    给定长波入射角 theta_inc（单位：弧度）以及两个介质的参数，
    利用文献中的矩阵方程求解反射与透射振幅系数：
      - R_P: 入射长波反射产生的长波振幅系数
      - R_S: 入射长波反射产生的剪切波振幅系数
      - T_P: 透射产生的长波振幅系数
      - T_S: 透射产生的剪切波振幅系数
    所有计算均采用复数运算。
    """
    # 介质1中入射角即为 theta_inc
    theta_P1 = theta_inc
    # 计算水中入射长波的正弦和余弦
    sin_P1 = np.sin(theta_P1)
    cos_P1 = np.cos(theta_P1)
    
    # 根据 Snell 定律计算其他角度（使用复数 arcsin 函数）：
    # 介质2中长波角 (P波)
    arg_P2 = (cP2 / cP1) * sin_P1
    theta_P2 = asin_complex(arg_P2)
    # 介质1中剪切波角（虽然水中剪切波无法传播，但这里采用复数 cS1 近似其衰减特性）
    arg_S1 = (cS1 / cP1) * sin_P1
    theta_S1 = asin_complex(arg_S1)
    # 介质2中剪切波角
    arg_S2 = (cS2 / cP1) * sin_P1
    theta_S2 = asin_complex(arg_S2)
    
    # 构建 4x4 系数矩阵 M（所有运算均为复数计算）
    M = np.array([
        [ np.sin(theta_P1)/(rho1*cP1),          np.cos(theta_S1)/(rho1*cS1),        -np.sin(theta_P2)/(rho2*cP2),           np.sin(theta_S2)/(rho2*cS2) ],
        [ np.cos(theta_P1)/(rho1*cP1),         -np.sin(theta_S1)/(rho1*cS1),         np.cos(theta_P2)/(rho2*cP2),           np.sin(theta_S2)/(rho2*cS2) ],
        [ -np.cos(2*theta_S1),                  np.sin(2*theta_S1),                  np.cos(2*theta_S2),                    np.sin(2*theta_S2) ],
        [ np.sin(2*theta_P1)/(cP1**2/cS1**2),   np.cos(2*theta_S1),                  np.sin(2*theta_P2)/(cP2**2/cS2**2),   -np.cos(2*theta_S2) ]
    ], dtype=np.complex128)
    
    # 构造右侧向量 b
    b = np.array([
         -np.sin(theta_P1)/(rho1*cP1),
          np.cos(theta_P1)/(rho1*cP1),
          np.cos(2*theta_S1),
          np.sin(2*theta_P1)/(cP1**2/cS1**2)
    ], dtype=np.complex128)
    
    # 求解线性方程组 M * [R_P, R_S, T_P, T_S]^T = b
    X = np.linalg.solve(M, b)

        # 定义各模式在各介质中的角阻抗（式 (3)）
    Z_P1 = (cP1 * rho1) / np.cos(theta_P1)
    Z_P2 = (cP2 * rho2) / np.cos(theta_P2)
    Z_S1 = (cS1 * rho1) / np.cos(theta_S1)
    Z_S2 = (cS2 * rho2) / np.cos(theta_S2)



    return X, theta_P2, theta_S1, theta_S2

# ---------------------
# 设置介质参数（文献中的 water – aluminum 参数）
rho1 = 1000                   # 水的密度 [kg/m^3]
cP1 = 1480                    # 水中长波速度 [m/s]
cS1 = 0.0013 + 0.0013j        # 模型中水的剪切波速度（采用复数，描述其强衰减）

rho2 = 2700                   # 铝的密度 [kg/m^3]
cP2 = 6420                    # 铝中长波速度 [m/s]
cS2 = 3040                    # 铝中剪切波速度 [m/s]

# 构建入射角数组（0到90度，转换为弧度）
angles_deg = np.linspace(0, 90, 181)    # 每0.5度一个点
angles_rad = np.deg2rad(angles_deg)

# 定义数组存放每个角度下的振幅系数
# 初始化数组保存振幅系数（复数）和能量（功率）系数
R_P_arr = np.zeros_like(angles_rad, dtype=np.complex128)
R_S_arr = np.zeros_like(angles_rad, dtype=np.complex128)
T_P_arr = np.zeros_like(angles_rad, dtype=np.complex128)
T_S_arr = np.zeros_like(angles_rad, dtype=np.complex128)

R_P_energy_arr = np.zeros_like(angles_rad, dtype=np.float64)
R_S_energy_arr = np.zeros_like(angles_rad, dtype=np.float64)
T_P_energy_arr = np.zeros_like(angles_rad, dtype=np.float64)
T_S_energy_arr = np.zeros_like(angles_rad, dtype=np.float64)


# 对各入射角循环计算振幅系数
for i, theta in enumerate(angles_rad):
    X, thetaP2, thetaS1, thetaS2 = compute_coeffs(theta, rho1, cP1, cS1, rho2, cP2, cS2)
    
    R_P, R_S, T_P, T_S = X[0], X[1], X[2], X[3]

    R_P_arr[i] = R_P
    R_S_arr[i] = R_S
    T_P_arr[i] = T_P
    T_S_arr[i] = T_S

    # 计算各模式对应的“角阻抗”，注意使用对应波的入射角
    # 介质1中长波阻抗
    Z_P1 = (cP1 * rho1) / np.cos(theta)
    # 介质2中长波阻抗
    Z_P2 = (cP2 * rho2) / np.cos(thetaP2)
    # 介质1中剪切波阻抗（液体中剪切波以复数形式描述）
    Z_S1 = (cS1 * rho1) / np.cos(thetaS1)
    # 介质2中剪切波阻抗
    Z_S2 = (cS2 * rho2) / np.cos(thetaS2)

    denom = np.real(1/np.conjugate(Z_P1))

        # 计算功率系数（能量系数），注意公式中定义的复共轭运算
    R_P_energy = (R_P * np.conjugate(R_P)).real
    R_S_energy = (R_S * np.conjugate(R_S)).real * (np.real(1/np.conjugate(Z_S1)) / denom)
    T_P_energy = (T_P * np.conjugate(T_P)).real * (np.real(1/np.conjugate(Z_P2)) / denom)
    T_S_energy = (T_S * np.conjugate(T_S)).real * (np.real(1/np.conjugate(Z_S2)) / denom)
    
    R_P_energy_arr[i] = R_P_energy
    R_S_energy_arr[i] = R_S_energy
    T_P_energy_arr[i] = T_P_energy
    T_S_energy_arr[i] = T_S_energy


plt.plot(angles_deg, R_P_energy_arr, label=r'$R_P^{(Pot)}$', linewidth=2)
plt.plot(angles_deg, R_S_energy_arr, label=r'$R_S^{(Pot)}$', linewidth=2)
plt.plot(angles_deg, T_P_energy_arr, label=r'$T_P^{(Pot)}$', linewidth=2)
plt.plot(angles_deg, T_S_energy_arr, label=r'$T_S^{(Pot)}$', linewidth=2)
plt.xlabel("incident angle (°)", fontsize=14)
plt.ylabel("intensity coefficient", fontsize=14)
plt.title("Water-Aluminum Interface", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
