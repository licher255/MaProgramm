import json
import numpy as np

from Material import Material
from RT_Cal import RT_Cal
from RT_Plot import RT_Plot
from RT_Cal_v2 import RT_Cal_v2

def main():

    with open('materials.json', 'r') as file:
        data = json.load(file)


    materials_data = {mat['name'].lower(): mat for mat in data['materials']}

    alIce_data = materials_data.get('al ice composite')
    BiSn_data =materials_data.get('bi sn')
    gallium_data = materials_data.get('gallium')
    ice_data = materials_data.get('ice')
    lead_data = materials_data.get('lead')
    water_data = materials_data.get('water')
    wax_data = materials_data.get('wax')
    rexolite_data= materials_data.get ('rexolite')
    zinc_data = materials_data.get('zinc')

    aluminium_data = materials_data.get('aluminium')
    stainlessSteel347 = materials_data.get('stainless steel347')
    hastelloyX =materials_data.get('hastelloy x')


    alIce = Material(alIce_data['name'], alIce_data['density'], alIce_data['vp'], alIce_data['vs'])
    BiSn = Material(BiSn_data['name'], BiSn_data['density'], BiSn_data['vp'], BiSn_data['vs'])
    gallium = Material(gallium_data['name'], gallium_data['density'], gallium_data['vp'], gallium_data['vs'])
    lead = Material(lead_data['name'], lead_data['density'], lead_data['vp'], lead_data['vs'])
    wax = Material(wax_data['name'], wax_data['density'], wax_data['vp'], wax_data['vs'])
    water = Material(water_data['name'], water_data['density'], water_data['vp'],water_data['vs'])
    ice = Material(ice_data['name'], ice_data['density'], ice_data['vp'], ice_data['vs'])
    rexolite = Material(rexolite_data['name'], rexolite_data['density'], rexolite_data['vp'], rexolite_data['vs'])
    zinc = Material(zinc_data['name'], zinc_data['density'], zinc_data['vp'], zinc_data['vs'])
    aluminium = Material(aluminium_data['name'], aluminium_data['density'], aluminium_data['vp'], aluminium_data['vs'])
    stainless_steel_347 = Material(stainlessSteel347['name'], stainlessSteel347['density'], stainlessSteel347['vp'], stainlessSteel347['vs'])
    hastelloy_x = Material(hastelloyX['name'], hastelloyX['density'], hastelloyX['vp'], hastelloyX['vs'])

    #rt_cal = RT_Cal(water, aluminium)
    rt_cal =RT_Cal_v2(water, aluminium)
    rt_plot = RT_Plot()
    rt_plot.plot_intensity(rt_cal, rt_cal.material1, rt_cal.material2)


if __name__ == '__main__':
    main()
 