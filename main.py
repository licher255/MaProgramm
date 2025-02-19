import json
from Material import Material
from RT_Cal import RT_Cal

def main():
    # Read the JSON file containing material properties
    with open('materials.json', 'r') as file:
        data = json.load(file)

    # Create a dictionary mapping material names (in lowercase) to their properties
    materials_data = {mat['name'].lower(): mat for mat in data['materials']}

    # Retrieve the properties for ice and steel
    ice_data = materials_data.get('plexiglass')
    steel_data = materials_data.get('steel')

    if not ice_data or not steel_data:
        print("Required materials (plexiglass and steel) not found in the JSON database.")
        return

    # Create Material instances for ice and steel
    ice = Material(ice_data['density'], ice_data['vp'], ice_data['vs'])
    steel = Material(steel_data['density'], steel_data['vp'], steel_data['vs'])

    # Create an RT_Cal instance using ice as the incident medium and steel as the transmission medium
    rt_calculator = RT_Cal(ice, steel)

    # Calculate and output vertical incidence coefficients
    reflt_coeff, trans_coeff = rt_calculator.calculate_vertical_coefficients()
    print("Vertical Incidence Coefficients:")
    print("Reflection Coefficient:{:.2f} ".format(reflt_coeff))
    print("Transmission Coefficient:{:.2f} ".format(trans_coeff))

    # Calculate and output the critical angles for P-wave and S-wave
    critical_angle_p, critical_angle_s = rt_calculator.calculate_critical_angles()
    print("\nCritical Angles:")
    if critical_angle_p is not None:
        print("P-wave Critical Angle(first critical angle): {:.2f} degrees".format(critical_angle_p))
    else:
        print("P-wave Critical Angle: Not defined")

    if critical_angle_s is not None:
        print("S-wave Critical Angle(second critical angle): {:.2f} degrees".format(critical_angle_s))
    else:
        print("S-wave Critical Angle: Not defined")
    #Calculate and output the defraction angle for P-wave, from plexiglass to steel
    angle_plexiglass = rt_calculator.calculate_defraction_angle(25)
    print("angle_Plexiglass_steel is {:.2f} degree".format(angle_plexiglass))


if __name__ == '__main__':
    main()
