import json
import numpy as np

from Material import Material
from RT_Cal import RT_Cal
from RT_Plot import RT_Plot

def main():

    with open('materials.json', 'r') as file:
        data = json.load(file)


    materials_data = {mat['name'].lower(): mat for mat in data['materials']}

    water_data = materials_data.get('water')
    ice_data = materials_data.get('ice')
    plexiglass_data = materials_data.get('plexiglass')
    aluminium_data = materials_data.get('aluminium')
    steel_data = materials_data.get('steel')
    epoxy_data = materials_data.get('epoxy')
    lead_data = materials_data.get('lead')
    zinc_data = materials_data.get('zinc')

    water = Material(water_data['name'],water_data['density'], water_data['vp'], water_data['vs'])
    ice = Material(ice_data['name'],ice_data['density'], ice_data['vp'], ice_data['vs'])
    plexiglass = Material(plexiglass_data['name'],plexiglass_data['density'], plexiglass_data['vp'], plexiglass_data['vs'])
    aluminium = Material(aluminium_data['name'],aluminium_data['density'], aluminium_data['vp'], aluminium_data['vs'])
    steel = Material(steel_data['name'],steel_data['density'], steel_data['vp'], steel_data['vs'])
    epoxy = Material(epoxy_data['name'],epoxy_data['density'], epoxy_data['vp'], epoxy_data['vs'])
    lead = Material(lead_data['name'],lead_data['density'], lead_data['vp'], lead_data['vs'])
    zinc = Material(zinc_data['name'],zinc_data['density'], zinc_data['vp'], zinc_data['vs'])

    rt_cal = RT_Cal(lead, aluminium)
    rt_plot = RT_Plot()
    rt_plot.plot_intensity(rt_cal, rt_cal.material1, rt_cal.material2)


if __name__ == '__main__':
    main()
 