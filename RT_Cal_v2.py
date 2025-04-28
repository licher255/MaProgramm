"""
Literature : Fundamentals of Ultrasonic Nondestructive Evaluation, Lester W.Schmerr Jr.

This is a program which calculates the reflection and transmission coefficients.
considering the situation of Cyro-UT, there are only 2 interfaces:
1. a fluid-solid interface (Oblique incidence)
2. a solid-solid Interface

density : $rho$
wave speed : $c$

incident wave:
reflected wave:
transmitted wave:

transmission coefficient:
reflection coefficient:

transmission coefficient of Ligitudinal wave
transmission coefficient of transversal wave

reflection coefficient of Ligitudinal wave
reflection coefficient of transversal wave

"""

import math
import numpy as np

class RT_Cal_v2:
    """
    A class for calculating reflection and transmission coefficients,
    and critical angles for oblique incidence between two materials.
    """

    def __init__(self, material1, material2):
        """
        Initialize the RT_Cal object with two Material instances.

        :param material1: The first material (incident medium).
        :param material2: The second material (transmission medium).
        """
        self.material1 = material1
        self.material2 = material2

    def calculate_vertical_coefficients(self):
        """
        Calculate reflection and transmission coefficients for vertical incidence.

        The P-wave impedance is used for these calculations.
        Reflection coefficient (R) = (Z2 - Z1) / (Z2 + Z1)
        Transmission coefficient (T) = 2 * Z2 / (Z2 + Z1)

        :return: A tuple (reflection_coefficient, transmission_coefficient).
        """
        # Calculate P-wave impedances for both materials
        Z1 = self.material1.density * self.material1.vp
        Z2 = self.material2.density * self.material2.vp

        reflection_coefficient = (Z2 - Z1) / (Z2 + Z1)
        transmission_coefficient = 2 * Z2 / (Z2 + Z1)
        return reflection_coefficient, transmission_coefficient


        """
        Calculate the critical angles for P-wave and S-wave during oblique incidence.

        For vertical incidence from material1 to material2:
          - P-wave critical angle is defined by: sin(θ_c_p) = vp1 / vp2
          - S-wave critical angle is defined by: sin(θ_c_s) = vp1/ vs2
        If the ratio is greater than 1, the critical angle is not defined (None).

        The angles are returned in degrees.

        :return: A tuple (critical_angle_p, critical_angle_s) where:
                 critical_angle_p: Critical angle for P-wave transmission.
                 critical_angle_s: Critical angle for S-wave transmission.
        """
    def calculate_critical_angles(self):
        # Calculate critical angle for P-wave: sin(theta) = vp1/vp2
        ratio_p = self.material1.vp / self.material2.vp
        if ratio_p <= 1:
            critical_angle_p = math.degrees(math.asin(ratio_p))
        else:
            critical_angle_p = 90

        # Calculate critical angle for S-wave: sin(theta) = vp1/vs2
        ratio_s = self.material1.vp / self.material2.vs
        if ratio_s <= 1:
            critical_angle_s = math.degrees(math.asin(ratio_s))
        else:
            critical_angle_s = 90

        return critical_angle_p, critical_angle_s
    
    def calculate_defraction_angle(self, angle_inc):
    # 根据入射角（单位：度）计算介质2中折射的纵波和横波角度
        sin_trans_L_angle = self.material2.vp / self.material1.vp * math.sin(math.radians(angle_inc))
        sin_trans_S_angle = self.material2.vs / self.material1.vp * math.sin(math.radians(angle_inc))
    
        if abs(sin_trans_L_angle) > 1:
            trans_L_angle = None  
        else:
            trans_L_angle = math.degrees(math.asin(sin_trans_L_angle))
    
        if abs(sin_trans_S_angle) > 1:
            trans_S_angle = None
        else:
            trans_S_angle = math.degrees(math.asin(sin_trans_S_angle))
    
        return trans_L_angle, trans_S_angle


    def calculate_intensity_coef(self, angle_inc):
        """
        用矩阵方法计算给定入射角（度）下的振幅系数和能量（强度）系数：
        返回一个字典，包含 R_P, R_S, T_P, T_S 的强度系数。
        """
        # 1. 参数提取
        asin_complex = np.lib.scimath.arcsin
        
        rho1, cP1, cS1 = (self.material1.density,
                          self.material1.vp,
                          self.material1.vs if np.iscomplexobj(self.material1.vs) 
                            else self.material1.vs + 0j)
        rho2, cP2, cS2 = (self.material2.density,
                          self.material2.vp,
                          self.material2.vs)

        # 2. 角度转换
        theta_P1 = np.deg2rad(angle_inc)
        sin_P1 = np.sin(theta_P1)

        # 3. 通过 Snell 计算复数折射角
        theta_P2 = asin_complex((cP2 / cP1) * sin_P1)
        theta_S1 = asin_complex((cS1 / cP1) * sin_P1)
        theta_S2 = asin_complex((cS2 / cP1) * sin_P1)

        # 4. 构建线性方程 M X = b
        M = np.array([
            [ np.sin(theta_P1)/(rho1*cP1),  np.cos(theta_S1)/(rho1*cS1),
             -np.sin(theta_P2)/(rho2*cP2),  np.sin(theta_S2)/(rho2*cS2) ],
            [ np.cos(theta_P1)/(rho1*cP1), -np.sin(theta_S1)/(rho1*cS1),
              np.cos(theta_P2)/(rho2*cP2),  np.sin(theta_S2)/(rho2*cS2) ],
            [ -np.cos(2*theta_S1),           np.sin(2*theta_S1),
              np.cos(2*theta_S2),           np.sin(2*theta_S2) ],
            [  np.sin(2*theta_P1)/(cP1**2/cS1**2),  np.cos(2*theta_S1),
               np.sin(2*theta_P2)/(cP2**2/cS2**2), -np.cos(2*theta_S2) ]
        ], dtype=np.complex128)

        b = np.array([
            -np.sin(theta_P1)/(rho1*cP1),
             np.cos(theta_P1)/(rho1*cP1),
             np.cos(2*theta_S1),
             np.sin(2*theta_P1)/(cP1**2/cS1**2)
        ], dtype=np.complex128)

        R_P, R_S, T_P, T_S = np.linalg.solve(M, b)

        # 5. 计算角阻抗并归一化因子
        Z_P1 = (cP1 * rho1) / np.cos(theta_P1)
        Z_P2 = (cP2 * rho2) / np.cos(theta_P2)
        Z_S1 = (cS1 * rho1) / np.cos(theta_S1)
        Z_S2 = (cS2 * rho2) / np.cos(theta_S2)
        norm = np.real(1/np.conjugate(Z_P1))

        # 6. 计算能量（强度）系数
        R_P_energy = (R_P * np.conjugate(R_P)).real
        R_S_energy = (R_S * np.conjugate(R_S)).real * (np.real(1/np.conjugate(Z_S1)) / norm)
        T_P_energy = (T_P * np.conjugate(T_P)).real * (np.real(1/np.conjugate(Z_P2)) / norm)
        T_S_energy = (T_S * np.conjugate(T_S)).real * (np.real(1/np.conjugate(Z_S2)) / norm)

        return {
            'R_P': R_P_energy,
            'R_S': R_S_energy,
            'T_P': T_P_energy,
            'T_S': T_S_energy
        }

