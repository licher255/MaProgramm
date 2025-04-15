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
    
    # 获取 P 波和 S 波的临界角（此处可用于其它判断，但下面主要依据 defraction_angle 返回的角度）
        critical_angle_p, critical_angle_s = self.calculate_critical_angles()
        rad_angle_inc = math.radians(angle_inc)
    # 入射介质的阻抗
        Z_inc = self.material1.density * self.material1.vp / math.cos(rad_angle_inc)

    # -------------------------------------------------------------------
    # 情况1：当入射角为 0，只存在纵波传输
        if angle_inc == 0:
            z1 = self.material1.density * self.material1.vp
            z2 = self.material2.density * self.material2.vp
        # P 波透射系数
            T_p = 2 * z2 / (z1 + z2)
        # 根据能量守恒，计算透射强度
            T_intensity_L = (z1 / z2) * T_p**2
            return T_intensity_L, 0
    # -------------------------------------------------------------------
    # 情况2：当 0 < angle_inc < θ_L 时，介质2中存在折射的纵波和横波
        elif angle_inc < critical_angle_p:
            trans_L_angle, trans_S_angle = self.calculate_defraction_angle(angle_inc)
            rad_angle_L = math.radians(trans_L_angle)
            rad_angle_S = math.radians(trans_S_angle)
            Z_L = self.material2.density * self.material2.vp / math.cos(rad_angle_L)
            Z_S = self.material2.density * self.material2.vs / math.cos(rad_angle_S)
            under_part = (Z_L * (math.cos(2 * rad_angle_S))**2 +
                            Z_S * (math.sin(2 * rad_angle_S))**2 + Z_inc)
            T_L = (self.material1.density / self.material2.density) * (2 * Z_L * math.cos(2 * rad_angle_S)) / under_part
            T_S = (self.material1.density / self.material2.density) * (-2 * Z_S * math.sin(2 * rad_angle_S)) / under_part
            T_intensity_L = (self.material2.density * math.tan(rad_angle_inc) /
                           (self.material1.density * math.tan(rad_angle_L))) * (T_L)**2
            T_intensity_S = (self.material2.density * math.tan(rad_angle_inc) /
                           (self.material1.density * math.tan(rad_angle_S))) * (T_S)**2
            return T_intensity_L, T_intensity_S
    #----------------------------------------------------------------------
    #  情况3： 当发生L wave全反射时：      
        elif angle_inc == critical_angle_p:
            T_intensity_L =0
            T_intensity_S =0
            return T_intensity_L, T_intensity_S
    # -------------------------------------------------------------------
    # 情况3：当 θ_L < angle_inc < θ_S 时，纵波转变为表面波（不传输），仅横波存在折射
        elif angle_inc < critical_angle_s:
        # 将纵波折射角视为 90°（表面波），直接置其传输系数为0
            trans_L_angle, trans_S_angle = self.calculate_defraction_angle(angle_inc)
            
            rad_angle_S = math.radians(trans_S_angle)

            Z_L = self.material2.density * self.material2.vp / math.sqrt(1-(self.material2.vp/self.material2.vp*math.sin(rad_angle_inc))**2)
            Z_S = self.material2.density * self.material2.vs / math.cos(rad_angle_S)
            Z_inc = self.material1.density * self.material1.vp /math.cos(rad_angle_inc)

            T_S = -(self.material1.density / self.material2.density)* (2 *Z_S * math.sin(2* rad_angle_S) /(Z_L*math.cos(2*rad_angle_S)**2 + Z_S*math.sin(2*rad_angle_S)**2 + Z_inc))
            
            T_intensity_S = (self.material2.density * math.tan(rad_angle_inc))/(self.material1.density* math.tan(rad_angle_S))* T_S**2

            #T_intensity_S = 1- self.calculate_R_I_coef(angle_inc)
            
            return 0, T_intensity_S

    # -------------------------------------------------------------------
    # 情况5：当入射角超过横波折射角或其他条件下，认为无透射能量
        else:
            return 0, 00
        

    def calculate_R_I_coef(self, angle_inc):
        rad_angle_inc = math.radians(angle_inc) 
        Teil1= math.sqrt(math.sin(rad_angle_inc)**2 - (self.material1.vp/ self.material2.vp)**2)
        Teil2 = self.material2.density / self.material1.density* math.cos(rad_angle_inc)
        R_P_L = -2 * math.atan(Teil1/Teil2)
        R_I_L = R_P_L**2

        return R_I_L


