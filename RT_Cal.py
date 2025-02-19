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
        sin_defraction_angle = self.material2.vp / self.material1.vp * math.sin(math.radians(angle_inc))
        return math.degrees(math.asin(sin_defraction_angle))
