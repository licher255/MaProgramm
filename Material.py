class Material:
    """
    A class representing a material with density, P-wave velocity, and S-wave velocity.
    """

    def __init__(self, name, density, vp, vs):
        """
        Initialize the Material object.

        :param density: The density of the material (in kg/m^3).
        :param vp: The P-wave velocity (in m/s).
        :param vs: The S-wave velocity (in m/s).
        """
        self.name = name
        self.density = density
        self.vp = vp
        self.vs = vs
        if vs=="NA":
            self.vs= 0.0013+ 0.0013j

    def p_wave_impedance(self):
        """
        Calculate and return the P-wave impedance.

        P-wave impedance is defined as the product of density and P-wave velocity.

        :return: The P-wave impedance.
        """
        return self.density * self.vp

    def s_wave_impedance(self):
        """
        Calculate and return the S-wave impedance.

        S-wave impedance is defined as the product of density and S-wave velocity.

        :return: The S-wave impedance.
        """
        return self.density * self.vs
