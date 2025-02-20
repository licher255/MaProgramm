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

class RT_Cal:
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
        Transmission coefficient (T) = 2 * Z1 / (Z2 + Z1)

        :return: A tuple (reflection_coefficient, transmission_coefficient).
        """
        # Calculate P-wave impedances for both materials
        Z1 = self.material1.density * self.material1.vp
        Z2 = self.material2.density * self.material2.vp

        reflection_coefficient = (Z2 - Z1) / (Z2 + Z1)
        transmission_coefficient = 2 * Z1 / (Z2 + Z1)
        return reflection_coefficient, transmission_coefficient

    def calculate_critical_angles(self):
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
        # Calculate critical angle for P-wave: sin(theta) = vp1/vp2
        ratio_p = self.material1.vp / self.material2.vp
        if ratio_p <= 1:
            critical_angle_p = math.degrees(math.asin(ratio_p))
        else:
            critical_angle_p = None

        # Calculate critical angle for S-wave: sin(theta) = vp1/vs2
        ratio_s = self.material1.vp / self.material2.vs
        if ratio_s <= 1:
            critical_angle_s = math.degrees(math.asin(ratio_s))
        else:
            critical_angle_s = None

        return critical_angle_p, critical_angle_s
    
    def calculate_defraction_angle(self, angle_inc):
        # from m1 incidence to m2 with angle_inc(deg)
        sin_trans_L_angle = self.material2.vp / self.material1.vp * math.sin(math.radians(angle_inc))
        trans_L_angle = math.degrees(math.asin(sin_trans_L_angle))
        sin_trans_S_angle = self.material2.vs / self.material1.vp * math.sin(math.radians(angle_inc))
        trans_S_angle = math.degrees(math.asin(sin_trans_S_angle))
        return trans_L_angle, trans_S_angle
    

    def calculate_intensity_coef(self,angle_inc):
        """
        calculate the fluid-solid interface.
        """
        trans_L_angle, trans_S_angle = self.calculate_defraction_angle(angle_inc)

        Z_inc = self.material1.density * self.material1.vp /angle_inc
        Z_L   = self.material2.density * self.material2.vp /trans_L_angle
        Z_S   = self.material2.density * self.material2.vs /trans_S_angle

        # transmission coefficient:

        under_part = Z_L* (math.cos(2* trans_S_angle)^2) + Z_S* (math.sin(2* trans_S_angle)^2) + Z_inc 

        T_L = (self.material1.density/ self.material2. density) * (2* Z_L* math.cos(2* trans_S_angle))/ under_part
        T_S = (self.material1.density/ self.material2. density) * (-2* Z_S* math.sin(2* trans_S_angle))/ under_part

        # the acoustic intensity reflection and transmission coefficients:
        # transalte from degree to radians
        rad_angle_inc = math.radians(angle_inc)
        rad_angle_L   = math.radians(trans_L_angle)
        rad_angle_S   = math.radians(trans_S_angle)

        T_intensity_L = (self.material2.density* math.tan(rad_angle_inc)/ self.material1.density/ math.tan(rad_angle_L)) * (T_L)^2
        T_intensity_S = (self.material2.density* math.tan(rad_angle_inc)/ self.material1.density/ math.tan(rad_angle_S)) * (T_S)^2

        return T_intensity_L, T_intensity_S