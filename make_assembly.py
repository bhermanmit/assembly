#!/usr/bin/env python2

from assembly import *
import numpy as np
from collections import OrderedDict

# Input Data
settings = {
'batches' : 500,
'inactive' : 100,
'particles' : 1000,
'run_cmfd' : 'true'
}
n_densities = 1 # number of unique densities from hzp to 0.66
n_temps = 1  # number of unique fuel temperature linear from 600 to 1200
n_water = 25 # number of water materials, cmfd regions
cmfd = {
'power' : 17.674e6,
'flowrate' : 88.5145,
'inlet_enthalpy' : 1301740.,
'n_assemblies': 1,
'boron' : 975,
'thinner' : 1,
'thouter' : 1,
'interval' : 1000,
'begin':500,
'active_flush':70,
'feedback':'false'
}

# Global data
hzp_density = 0.73986            # Highest density
low_density = 0.66               # Lowest density
pin_pitch = 1.25984              # Pin pitch
assy_pitch = 21.50364            # Assembly pitch
active_core_height = 365.76      # Active core height
axial_surfaces = { 
'lowest_extent':0.0,             # Lowest plane of model
'lower_plenum':20.0,             # Top of lower plenum/Bottom Support Plate
'support_plate':35.16,           # Top of Support plate/Bottom of Fuel Rod
'baf':36.007,                    # Bottom of Active Fuel
'grid1bot':37.8790,              # Grid 1 Bottom
'bpbot':41.0870,                 # Bottom of Burnable Absorbers
'grid1top':42.0700,              # Grid 1 Top
'dptop':45.0790,                 # Dashpot Top
'grid2bot':99.1640,              # Grid 2 Bottom
'grid2top':104.879,              # Grid 2 Top
'grid3bot':151.361,              # Grid 3 Bottom
'grid3top':157.076,              # Grid 3 Top
'grid4bot':203.558,              # Grid 4 Bottom
'grid4top':209.273,              # Grid 4 Top
'grid5bot':255.755,              # Grid 5 Bottom
'grid5top':261.470,              # Grid 5 Top
'grid6bot':307.952,              # Grid 6 Bottom
'grid6top':313.667,              # Grid 6 Top
'grid7bot':360.149,              # Grid 7 Bottom
'grid7top':365.864,              # Grid 7 Top
'taf':401.767,                   # Top of Active Fuel
'grid8bot':412.529,              # Grid 8 Bottom
'grid8top':416.720,              # Grid 8 Top
'topplugbot':421.223,            # Bottom of Top End Plug
'rodtop':423.272,                # Top of fuel rod
'nozzlebot':426.617,             # Bottom of Nozzle
'nozzletop':435.444,             # Top of Nozzle
'highest_extent':455.444         # Highest plane of problem 
}

axial_labels = [
'Lowest plane of model',
'Top of lower plenum/Bottom Support Plate',
'Top of Support plate/Bottom of Fuel Rod',
'Bottom of Active Fuel',
'Grid 1 Bottom',
'Bottom of Burnable Absorbers',
'Grid 1 Top',
'Dashpot Top',
'Grid 2 Bottom',
'Grid 2 Top',
'Grid 3 Bottom',
'Grid 3 Top',
'Grid 4 Bottom',
'Grid 4 Top',
'Grid 5 Bottom',
'Grid 5 Top',
'Grid 6 Bottom',
'Grid 6 Top',
'Grid 7 Bottom',
'Grid 7 Top',
'Top of Active Fuel',
'Grid 8 Bottom',
'Grid 8 Top',
'Bottom of Top End Plug',
'Top of fuel rod',
'Bottom of Nozzle',
'Top of Nozzle',
'Highest plane of problem']

def main():

    # Create all static materials
    create_static_materials()

    # Create surfaces
    create_surfaces()

    # Create grid info
    create_gridstrap()

    # Create static pins
    create_fuelpin()
    create_bppin()
    create_bppinDP()
    create_gtpin()
    create_gtpinDP()
    create_fuelplenumpin()
    create_bpplenumpin()

    # Create axial regions
    create_axial_regions()

    # Make assembly
    create_assembly()

    # Create core
    create_core()

    # Create cmfd
    create_cmfd()

    # Write OpenMC files
    write_openmc_input()

def create_static_materials():

    # HZP Water Material
    mat_hzph2o = Material('h2o_hzp', 'HZP Water @ 0.73986 g/cc')
    mat_hzph2o.add_nuclide('B-10', '71c', '8.0042e-06')
    mat_hzph2o.add_nuclide('B-11', '71c', '3.2218e-05')
    mat_hzph2o.add_nuclide('H-1', '71c', '4.9457e-02')
    mat_hzph2o.add_nuclide('H-2', '71c', '7.4196e-06')
    mat_hzph2o.add_nuclide('O-16', '71c', '2.4672e-02')
    mat_hzph2o.add_nuclide('O-17', '71c', '6.0099e-05')
    mat_hzph2o.add_sab('lwtr', '15t')
    mat_hzph2o.add_color('0 0 255')
    mat_hzph2o.finalize()

    # Helium Material
    mat_hel = Material('he', 'Helium for Gap')
    mat_hel.add_nuclide('He-4', '71c', '2.4044e-04')
    mat_hel.add_color('255 218 185')
    mat_hel.finalize()

    # Air Material
    mat_air = Material('air', 'Air for Instrumentation Tubes')
    mat_air.add_nuclide('C-Nat', '71c', '6.8296e-09')
    mat_air.add_nuclide('O-16', '71c', '5.2864e-06')
    mat_air.add_nuclide('O-17', '71c', '1.2877e-08')
    mat_air.add_nuclide('N-14', '71c', '1.9681e-05')
    mat_air.add_nuclide('N-15', '71c', '7.1900e-08')
    mat_air.add_nuclide('Ar-36', '71c', '7.9414e-10')
    mat_air.add_nuclide('Ar-38', '71c', '1.4915e-10')
    mat_air.add_nuclide('Ar-40', '71c', '2.3506e-07')
    mat_air.add_color('255 255 255')
    mat_air.finalize()

    # Inconel Material
    mat_in = Material('in', 'Inconel 718 for Grids')
    mat_in.add_nuclide('Si-28', '71c', '5.6753e-04')
    mat_in.add_nuclide('Si-29', '71c', '2.8831e-05')
    mat_in.add_nuclide('Si-30', '71c', '1.9028e-05')
    mat_in.add_nuclide('Cr-50', '71c', '7.8239e-04')
    mat_in.add_nuclide('Cr-52', '71c', '1.5088e-02')
    mat_in.add_nuclide('Cr-53', '71c', '1.7108e-03')
    mat_in.add_nuclide('Cr-54', '71c', '4.2586e-04')
    mat_in.add_nuclide('Mn-55', '71c', '7.8201e-04')
    mat_in.add_nuclide('Fe-54', '71c', '1.4797e-03')
    mat_in.add_nuclide('Fe-56', '71c', '2.3229e-02')
    mat_in.add_nuclide('Fe-57', '71c', '5.3645e-04')
    mat_in.add_nuclide('Fe-58', '71c', '7.1392e-05')
    mat_in.add_nuclide('Ni-58', '71c', '2.9320e-02')
    mat_in.add_nuclide('Ni-60', '71c', '1.1294e-02')
    mat_in.add_nuclide('Ni-61', '71c', '4.9094e-04')
    mat_in.add_nuclide('Ni-62', '71c', '1.5653e-03')
    mat_in.add_nuclide('Ni-64', '71c', '3.9864e-04')
    mat_in.add_color('101 101 101')
    mat_in.finalize()

    # Stainless Steel Material
    mat_ss = Material('ss', 'Stainless Steel 304')
    mat_ss.add_nuclide('Si-28', '71c', '9.5274e-04')
    mat_ss.add_nuclide('Si-29', '71c', '4.8400e-05')
    mat_ss.add_nuclide('Si-30', '71c', '3.1943e-05')
    mat_ss.add_nuclide('Cr-50', '71c', '7.6778e-04')
    mat_ss.add_nuclide('Cr-52', '71c', '1.4806e-02')
    mat_ss.add_nuclide('Cr-53', '71c', '1.6789e-03')
    mat_ss.add_nuclide('Cr-54', '71c', '4.1791e-04')
    mat_ss.add_nuclide('Mn-55', '71c', '1.7604e-03')
    mat_ss.add_nuclide('Fe-54', '71c', '3.4620e-03')
    mat_ss.add_nuclide('Fe-56', '71c', '5.4345e-02')
    mat_ss.add_nuclide('Fe-57', '71c', '1.2551e-03')
    mat_ss.add_nuclide('Fe-58', '71c', '1.6703e-04')
    mat_ss.add_nuclide('Ni-58', '71c', '5.6089e-03')
    mat_ss.add_nuclide('Ni-60', '71c', '2.1605e-03')
    mat_ss.add_nuclide('Ni-61', '71c', '9.3917e-05')
    mat_ss.add_nuclide('Ni-62', '71c', '2.9945e-04')
    mat_ss.add_nuclide('Ni-64', '71c', '7.6261e-05')
    mat_ss.add_color('0 0 0')
    mat_ss.finalize()

    # Zircaloy Material
    mat_zr = Material('zr', 'Zircaloy-4')
    mat_zr.add_nuclide('O-16', '71c', '3.0743e-04')
    mat_zr.add_nuclide('O-17', '71c', '7.4887e-07')
    mat_zr.add_nuclide('Cr-50', '71c', '3.2962e-06')
    mat_zr.add_nuclide('Cr-52', '71c', '6.3564e-05')
    mat_zr.add_nuclide('Cr-53', '71c', '7.2076e-06')
    mat_zr.add_nuclide('Cr-54', '71c', '1.7941e-06')
    mat_zr.add_nuclide('Fe-54', '71c', '8.6699e-06')
    mat_zr.add_nuclide('Fe-56', '71c', '1.3610e-04')
    mat_zr.add_nuclide('Fe-57', '71c', '3.1431e-06')
    mat_zr.add_nuclide('Fe-58', '71c', '4.1829e-07')
    mat_zr.add_nuclide('Zr-90', '71c', '2.1827e-02')
    mat_zr.add_nuclide('Zr-91', '71c', '4.7600e-03')
    mat_zr.add_nuclide('Zr-92', '71c', '7.2758e-03')
    mat_zr.add_nuclide('Zr-94', '71c', '7.3734e-03')
    mat_zr.add_nuclide('Zr-96', '71c', '1.1879e-03')
    mat_zr.add_nuclide('Sn-112', '71c', '4.6735e-06')
    mat_zr.add_nuclide('Sn-114', '71c', '3.1799e-06')
    mat_zr.add_nuclide('Sn-115', '71c', '1.6381e-06')
    mat_zr.add_nuclide('Sn-116', '71c', '7.0055e-05')
    mat_zr.add_nuclide('Sn-117', '71c', '3.7003e-05')
    mat_zr.add_nuclide('Sn-118', '71c', '1.1669e-04')
    mat_zr.add_nuclide('Sn-119', '71c', '4.1387e-05')
    mat_zr.add_nuclide('Sn-120', '71c', '1.5697e-04')
    mat_zr.add_nuclide('Sn-122', '71c', '2.2308e-05')
    mat_zr.add_nuclide('Sn-124', '71c', '2.7897e-05')
    mat_zr.add_color('201 201 201')
    mat_zr.finalize()

    # UO2 at 2.4% enrichment Material
    mat_fuel24 = Material('fuel24', 'UO2 Fuel 2.4 w/o')
    mat_fuel24.add_nuclide('U-234', '71c', '4.4843e-06')
    mat_fuel24.add_nuclide('U-235', '71c', '5.5815e-04')
    mat_fuel24.add_nuclide('U-238', '71c', '2.2408e-02')
    mat_fuel24.add_nuclide('O-16', '71c', '4.5829e-02')
    mat_fuel24.add_nuclide('O-17', '71c', '1.1164e-04')
    mat_fuel24.add_color('255 215 0')
    mat_fuel24.finalize()

    # Borosilicate Glass Material
    mat_bsg = Material('bsg', 'Borosilicate Glass in BP Rod')
    mat_bsg.add_nuclide('B-10', '71c', '9.6506e-04')
    mat_bsg.add_nuclide('B-11', '71c', '3.9189e-03')
    mat_bsg.add_nuclide('O-16', '71c', '4.6511e-02')
    mat_bsg.add_nuclide('O-17', '71c', '1.1330e-04')
    mat_bsg.add_nuclide('Al-27', '71c', '1.7352e-03')
    mat_bsg.add_nuclide('Si-28', '71c', '1.6924e-02')
    mat_bsg.add_nuclide('Si-29', '71c', '8.5977e-04')
    mat_bsg.add_nuclide('Si-30', '71c', '5.6743e-04')
    mat_bsg.add_color('0 255 0')
    mat_bsg.finalize()

def create_surfaces():

    # Create fuel pin surfaces
    add_surface('fuelOR', 'z-cylinder', '0.0 0.0 0.392180', comment = 'Fuel Outer Radius')
    add_surface('cladIR', 'z-cylinder', '0.0 0.0 0.400050', comment = 'Clad Inner Radius')
    add_surface('cladOR', 'z-cylinder', '0.0 0.0 0.457200', comment = 'Clad Outer Radius')
    add_surface('springOR', 'z-cylinder', '0.0 0.0 0.06459', comment = 'Spring radius')

    # Create Guide Tube surfaces
    add_surface('gtIR', 'z-cylinder', '0.0 0.0 0.561340', comment = 'Guide Tube Inner Radius above Dashpot')
    add_surface('gtOR', 'z-cylinder', '0.0 0.0 0.601980', comment = 'Guide Tube Outer Radius above Dashpot')
    add_surface('gtIRdp', 'z-cylinder', '0.0 0.0 0.504190', comment = 'Guide Tube Inner Radius at Dashpot')
    add_surface('gtORdp', 'z-cylinder', '0.0 0.0 0.546100', comment = 'Guide Tube Outer Radius at Dashpot')

    # Burnable Poison surfaces
    add_surface('bpIR1', 'z-cylinder', '0.0 0.0 0.214000', comment = 'Burnable Absorber Rod Inner Radius 1')
    add_surface('bpIR2', 'z-cylinder', '0.0 0.0 0.230510', comment = 'Burnable Absorber Rod Inner Radius 2')
    add_surface('bpIR3', 'z-cylinder', '0.0 0.0 0.241300', comment = 'Burnable Absorber Rod Inner Radius 3')
    add_surface('bpIR4', 'z-cylinder', '0.0 0.0 0.426720', comment = 'Burnable Absorber Rod Inner Radius 4')
    add_surface('bpIR5', 'z-cylinder', '0.0 0.0 0.436880', comment = 'Burnable Absorber Rod Inner Radius 5')
    add_surface('bpIR6', 'z-cylinder', '0.0 0.0 0.483870', comment = 'Burnable Absorber Rod Inner Radius 6')

    # Top/Bottom Grid Spacer Surfaces
    add_surface('gridTBleft', 'x-plane', '-0.62208', comment = 'Top/Bottom Left Grid Spacer')
    add_surface('gridTBright', 'x-plane', '0.62208', comment = 'Top/Bottom Right Grid Spacer')
    add_surface('gridTBback', 'y-plane', '-0.62208', comment = 'Top/Bottom Back Grid Spacer')
    add_surface('gridTBfront', 'y-plane', '0.62208', comment = 'Top/Bottom Front Grid Spacer')

    # Intermediate Grid Spacer Surfaces
    add_surface('gridIleft', 'x-plane', '-0.60978', comment = 'Intermediate Left Grid Spacer')
    add_surface('gridIright', 'x-plane', '0.60978', comment = 'Intermediate Right Grid Spacer')
    add_surface('gridIback', 'y-plane', '-0.60978', comment = 'Intermediate Back Grid Spacer')
    add_surface('gridIfront', 'y-plane', '0.60978', comment = 'Intermediate Front Grid Spacer')

    # Grid Strap surfaces (need to convert to a pin cell universe coordinate system)
    strap_offset = assy_pitch/2.0 - 10.73635
    strap_left = pin_pitch/2.0 - strap_offset
    strap_right = -pin_pitch/2.0 + strap_offset
    strap_back = pin_pitch/2.0 - strap_offset 
    strap_front = -pin_pitch/2.0 + strap_offset
    add_surface('strapleft', 'x-plane', '{0}'.format(strap_left), comment = 'Grid Strap Left')
    add_surface('strapright', 'x-plane', '{0}'.format(strap_right), comment = 'Grid Strap Right')
    add_surface('strapback', 'y-plane', '{0}'.format(strap_back), comment = 'Grid Strap Back')
    add_surface('strapfront', 'y-plane', '{0}'.format(strap_front), comment = 'Grid Strap Front')

    # Core surfaces
    box = assy_pitch/2.0
    add_surface('core_left', 'x-plane', '{0}'.format(-box), 'reflective', 'Core left surface')
    add_surface('core_right', 'x-plane', '{0}'.format(box), 'reflective', 'Core right surface')
    add_surface('core_back', 'y-plane', '{0}'.format(-box), 'reflective', 'Core back surface')
    add_surface('core_front', 'y-plane', '{0}'.format(box), 'reflective', 'Core front surface')
    add_surface('core_bottom', 'z-plane', '{0}'.format(axial_surfaces['lowest_extent']), 'vacuum', 'Core bottom surface')
    add_surface('core_top', 'z-plane', '{0}'.format(axial_surfaces['highest_extent']), 'vacuum', 'Core top surface')

def create_fuelpin():

    # Fuel Pellet
    add_cell('fuel', 
        surfaces = '-{0}'.format(surf_dict['fuelOR'].id), 
        universe = 'fuel',
        material = mat_dict['fuel24'].id,
        comment = 'Fuel pellet')

    # Gas Gap
    add_cell('gap',
        surfaces = '{0} -{1}'.format(surf_dict['fuelOR'].id, surf_dict['cladIR'].id),
        universe = 'fuel',
        material = mat_dict['he'].id,
        comment = 'Fuel pin gas gap')

    # Clad
    add_cell('clad',
        surfaces = '{0}'.format(surf_dict['cladIR'].id),
        universe = 'fuel',
        material = mat_dict['zr'].id,
        comment = 'Fuel pin clad')

def create_bppin():

    # Inner Air Region
    add_cell('air1BP',
        surfaces = '-{0}'.format(surf_dict['bpIR1'].id),
        universe = 'bp',
        material = mat_dict['air'].id,
        comment = 'BP inner air')

    # Inner Stainless Steel Region
    add_cell('ss1BP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR1'].id, surf_dict['bpIR2'].id),
        universe = 'bp',
        material = mat_dict['ss'].id,
        comment = 'BP inner stainless')

    # Middle Air Region
    add_cell('air2BP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR2'].id, surf_dict['bpIR3'].id),
        universe = 'bp',
        material = mat_dict['air'].id,
        comment = 'BP middle air')

    # Borosilicate Glass Region
    add_cell('bsgBP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR3'].id, surf_dict['bpIR4'].id),
        universe = 'bp',
        material = mat_dict['bsg'].id,
        comment = 'BP borosilicate')

    # Outer Air Region
    add_cell('air3BP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR4'].id, surf_dict['bpIR5'].id),
        universe = 'bp',
        material = mat_dict['air'].id,
        comment = 'BP outer air')

    # Outer Stainless Steel Region
    add_cell('ss2BP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR5'].id, surf_dict['bpIR6'].id),
        universe = 'bp',
        material = mat_dict['ss'].id,
        comment = 'BP outer stainless')

    # Moderator Region
    add_cell('modBP',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR6'].id, surf_dict['gtIR'].id),
        universe = 'bp',
        material = mat_dict['h2o_hzp'].id,
        comment = 'BP moderator')

    # Tube Clad
    add_cell('cladBP',
        surfaces = '{0}'.format(surf_dict['gtIR'].id),
        universe = 'bp',
        material = mat_dict['zr'].id,
        comment = 'BP clad')

def create_bppinDP():

    # Inner Air Region
    add_cell('air1BPdp',
        surfaces = '-{0}'.format(surf_dict['bpIR1'].id),
        universe = 'bpDP',
        material = mat_dict['air'].id,
        comment = 'BP inner air at DP')

    # Inner Stainless Steel Region
    add_cell('ss1BPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR1'].id, surf_dict['bpIR2'].id),
        universe = 'bpDP',
        material = mat_dict['ss'].id,
        comment = 'BP inner stainless at DP')

    # Middle Air Region
    add_cell('air2BPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR2'].id, surf_dict['bpIR3'].id),
        universe = 'bpDP',
        material = mat_dict['air'].id,
        comment = 'BP middle air at DP')

    # Borosilicate Glass Region
    add_cell('bsgBPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR3'].id, surf_dict['bpIR4'].id),
        universe = 'bpDP',
        material = mat_dict['bsg'].id,
        comment = 'BP borosilicate at DP')

    # Outer Air Region
    add_cell('air3BPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR4'].id, surf_dict['bpIR5'].id),
        universe = 'bpDP',
		material = mat_dict['air'].id,
		comment = 'BP outer air at DP')

    # Outer Stainless Steel Region
    add_cell('ss2BPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR5'].id, surf_dict['bpIR6'].id),
        universe = 'bpDP',
        material = mat_dict['ss'].id,
        comment = 'BP outer stainless at DP')

    # Moderator Region
    add_cell('modBPdp',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR6'].id, surf_dict['gtIRdp'].id),
        universe = 'bpDP',
        material = mat_dict['h2o_hzp'].id,
        comment = 'BP moderator at DP')

    # Tube Clad
    add_cell('cladBPdp',
        surfaces = '{0}'.format(surf_dict['gtIRdp'].id),
        universe = 'bpDP',
        material = mat_dict['zr'].id,
        comment = 'BP clad at DP')

def create_gtpin():

    # Moderator Region
    add_cell('modGT',
        surfaces = '-{0}'.format(surf_dict['gtIR'].id),
        universe = 'gt',
        material = mat_dict['h2o_hzp'].id,
        comment = 'GT moderator')

    # Tube Clad
    add_cell('cladGT',
        surfaces = '{0}'.format(surf_dict['gtIR'].id),
        universe = 'gt',
        material = mat_dict['zr'].id,
        comment = 'GT clad')

def create_gtpinDP():

    # Moderator Region
    add_cell('modGTdp',
        surfaces = '-{0}'.format(surf_dict['gtIRdp'].id),
        universe = 'gtDP',
        material = mat_dict['h2o_hzp'].id,
        comment = 'GT moderator at DP')

    # Tube Clad
    add_cell('cladGTdp',
        surfaces = '{0}'.format(surf_dict['gtIRdp'].id),
        universe = 'gtDP',
        material = mat_dict['zr'].id,
        comment = 'GT clad at DP')

def create_fuelplenumpin():

    # Fuel Pin
    add_cell('rodplenumspring',
        surfaces = '-{0}'.format(surf_dict['springOR'].id),
        universe = 'fuelplenum',
        material = mat_dict['in'].id,
        comment = 'Inconel Spring in Fuel Pin')
    add_cell('rodplenumgap',
        surfaces = '{0} -{1}'.format(surf_dict['springOR'].id, surf_dict['cladIR'].id),
        universe = 'fuelplenum',
        material = mat_dict['he'].id,
        comment = 'Helium Outside Spring in Fuel Pin')
    add_cell('rodplenumclad',
        surfaces = '{0}'.format(surf_dict['cladIR'].id),
        universe = 'fuelplenum',
        material = mat_dict['zr'].id,
        comment = 'Clad Outside Spring in Fuel Pin')

def create_bpplenumpin():

    # BP pin
    add_cell('bpplenumss',
        surfaces = '-{0}'.format(surf_dict['bpIR6'].id),
        universe = 'bpplenum',
        material = mat_dict['ss'].id,
        comment = 'Stainless Steel BP pin in GT')
    add_cell('bpplenummod',
        surfaces = '{0} -{1}'.format(surf_dict['bpIR6'].id, surf_dict['gtIR'].id),
        universe = 'bpplenum',
        material = mat_dict['h2o_hzp'].id,
        comment = 'Moderator between SS BP pin and GT')
    add_cell('bpplenumclad',
        surfaces = '{0}'.format(surf_dict['gtIR'].id),
        universe = 'bpplenum',
        material = mat_dict['zr'].id,
        comment = 'Clad of GT surrounding SS BP pin')

def create_fuelpin_cell(cell_key, pin_key, water_key, grid = None):

    # Fill static fuel pin
    add_cell('fuelpin_'+cell_key,
        surfaces = '-{0}'.format(surf_dict['cladOR'].id),
        universe = cell_key,
        fill = univ_dict[pin_key].id,
        comment = 'Fuel pin fill for coolant')

    if grid != None:

        # Allow this to work with TB and I grids
        gridleft = 'grid'+grid+'left'
        gridright = 'grid'+grid+'right'
        gridback = 'grid'+grid+'back'
        gridfront = 'grid'+grid+'front'

        # Determine grid spacer material
        if grid == 'TB':
            gridmat = 'in'
        elif grid == 'I':
            gridmat = 'zr'
        else:
            raise Exception('Grid type not recognized - ' + grid)

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0} {1} -{2} {3} -{4}'.format(surf_dict['cladOR'].id, surf_dict[gridleft].id, surf_dict[gridright].id,
                                                      surf_dict[gridback].id, surf_dict[gridfront].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around fuel pin before grid ' + grid)

        # Fill in grid (requires 4 cells because OpenMC doesn't have union operator)
        add_cell('gridtbn_'+cell_key,
            surfaces = '{0} {1} -{2}'.format(surf_dict[gridfront].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer N')
        add_cell('gridtbs_'+cell_key,
            surfaces = '-{0} {1} -{2}'.format(surf_dict[gridback].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer S')
        add_cell('gridtbe_'+cell_key,
            surfaces = '{0}'.format(surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer NE/E/SE')
        add_cell('gridtbw_'+cell_key,
            surfaces = '-{0}'.format(surf_dict[gridleft].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer SW/W/NW')

    else:

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0}'.format(surf_dict['cladOR'].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around fuel pin')

def create_bppin_cell(cell_key, pin_key, water_key, grid = None):

    # Fill static bp pin
    add_cell('bppin_'+cell_key,
        surfaces = '-{0}'.format(surf_dict['gtOR'].id),
        universe = cell_key,
        fill = univ_dict[pin_key].id,
        comment = 'BP pin fill for coolant')

    if grid != None:

        # Allow this to work with TB and I grids
        gridleft = 'grid'+grid+'left'
        gridright = 'grid'+grid+'right'
        gridback = 'grid'+grid+'back'
        gridfront = 'grid'+grid+'front'

        # Determine grid spacer material
        if grid == 'TB':
            gridmat = 'in'
        elif grid == 'I':
            gridmat = 'zr'
        else:
            raise Exception('Grid type not recognized - ' + grid)

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0} {1} -{2} {3} -{4}'.format(surf_dict['gtOR'].id, surf_dict[gridleft].id, surf_dict[gridright].id,
                                                      surf_dict[gridback].id, surf_dict[gridfront].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around BP pin before grid ' + grid)

        # Fill in grid (requires 4 cells because OpenMC doesn't have union operator)
        add_cell('gridtbn_'+cell_key,
            surfaces = '{0} {1} -{2}'.format(surf_dict[gridfront].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer N')
        add_cell('gridtbs_'+cell_key,
            surfaces = '-{0} {1} -{2}'.format(surf_dict[gridback].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer S')
        add_cell('gridtbe_'+cell_key,
            surfaces = '{0}'.format(surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer NE/E/SE')
        add_cell('gridtbw_'+cell_key,
            surfaces = '-{0}'.format(surf_dict[gridleft].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer SW/W/NW')

    else:

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0}'.format(surf_dict['gtOR'].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around BP pin')

def create_bppinDP_cell(cell_key, pin_key, water_key, grid = None):

    # Fill static bp pin at DP
    add_cell('bppinDP_'+cell_key,
        surfaces = '-{0}'.format(surf_dict['gtORdp'].id),
        universe = cell_key,
        fill = univ_dict[pin_key].id,
        comment = 'BP pin fill for coolant at DP')

    if grid != None:

        # Allow this to work with TB and I grids
        gridleft = 'grid'+grid+'left'
        gridright = 'grid'+grid+'right'
        gridback = 'grid'+grid+'back'
        gridfront = 'grid'+grid+'front'

        # Determine grid spacer material
        if grid == 'TB':
            gridmat = 'in'
        elif grid == 'I':
            gridmat = 'zr'
        else:
            raise Exception('Grid type not recognized - ' + grid)

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0} {1} -{2} {3} -{4}'.format(surf_dict['gtORdp'].id, surf_dict[gridleft].id, surf_dict[gridright].id,
                                                      surf_dict[gridback].id, surf_dict[gridfront].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around BP pin at DP before grid ' + grid)

        # Fill in grid (requires 4 cells because OpenMC doesn't have union operator)
        add_cell('gridtbn_'+cell_key,
            surfaces = '{0} {1} -{2}'.format(surf_dict[gridfront].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer N')
        add_cell('gridtbs_'+cell_key,
            surfaces = '-{0} {1} -{2}'.format(surf_dict[gridback].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer S')
        add_cell('gridtbe_'+cell_key,
            surfaces = '{0}'.format(surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer NE/E/SE')
        add_cell('gridtbw_'+cell_key,
            surfaces = '-{0}'.format(surf_dict[gridleft].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer SW/W/NW')

    else:

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0}'.format(surf_dict['gtORdp'].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around BP pin at DP')

def create_gtpin_cell(cell_key, pin_key, water_key, grid = None):

    # Fill static gt pin
    add_cell('gtpin_'+cell_key,
        surfaces = '-{0}'.format(surf_dict['gtOR'].id),
        universe = cell_key,
        fill = univ_dict[pin_key].id, 
        comment = 'GT pin fill for coolant')

    if grid != None:

        # Allow this to work with TB and I grids
        gridleft = 'grid'+grid+'left'
        gridright = 'grid'+grid+'right'
        gridback = 'grid'+grid+'back'
        gridfront = 'grid'+grid+'front'

        # Determine grid spacer material
        if grid == 'TB':
            gridmat = 'in'
        elif grid == 'I':
            gridmat = 'zr'
        else:
            raise Exception('Grid type not recognized - ' + grid)

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0} {1} -{2} {3} -{4}'.format(surf_dict['gtOR'].id, surf_dict[gridleft].id, surf_dict[gridright].id,
                                                      surf_dict[gridback].id, surf_dict[gridfront].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around GT pin before grid ' + grid)

        # Fill in grid (requires 4 cells because OpenMC doesn't have union operator)
        add_cell('gridtbn_'+cell_key,
            surfaces = '{0} {1} -{2}'.format(surf_dict[gridfront].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer N')
        add_cell('gridtbs_'+cell_key,
            surfaces = '-{0} {1} -{2}'.format(surf_dict[gridback].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer S')
        add_cell('gridtbe_'+cell_key,
            surfaces = '{0}'.format(surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer NE/E/SE')
        add_cell('gridtbw_'+cell_key,
            surfaces = '-{0}'.format(surf_dict[gridleft].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer SW/W/NW')

    else:

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0}'.format(surf_dict['gtOR'].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around GT pin')

def create_gtpinDP_cell(cell_key, pin_key, water_key, grid = None):

    # Fill static bp pin at DP
    add_cell('gtpinDP_'+cell_key,
        surfaces = '-{0}'.format(surf_dict['gtORdp'].id),
        universe = cell_key,
        fill = univ_dict[pin_key].id,
        comment = 'GT pin fill for coolant at DP')

    if grid != None:

        # Allow this to work with TB and I grids
        gridleft = 'grid'+grid+'left'
        gridright = 'grid'+grid+'right'
        gridback = 'grid'+grid+'back'
        gridfront = 'grid'+grid+'front'

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0} {1} -{2} {3} -{4}'.format(surf_dict['gtORdp'].id, surf_dict[gridleft].id, surf_dict[gridright].id,
                                                      surf_dict[gridback].id, surf_dict[gridfront].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around GT pin at DP before grid ' + grid)

        # Determine grid spacer material
        if grid == 'TB':
            gridmat = 'in'
        elif grid == 'I':
            gridmat = 'zr'
        else:
            raise Exception('Grid type not recognized - ' + grid)

        # Fill in grid (requires 4 cells because OpenMC doesn't have union operator)
        add_cell('gridtbn_'+cell_key,
            surfaces = '{0} {1} -{2}'.format(surf_dict[gridfront].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer N')
        add_cell('gridtbs_'+cell_key,
            surfaces = '-{0} {1} -{2}'.format(surf_dict[gridback].id, surf_dict[gridleft].id, surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer S')
        add_cell('gridtbe_'+cell_key,
            surfaces = '{0}'.format(surf_dict[gridright].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer NE/E/SE')
        add_cell('gridtbw_'+cell_key,
            surfaces = '-{0}'.format(surf_dict[gridleft].id),
            universe = cell_key,
            material = mat_dict[gridmat].id,
            comment = grid + ' Grid Spacer SW/W/NW')

    else:

        # Fill in water coolant
        add_cell('cool_'+cell_key,
            surfaces = '{0}'.format(surf_dict['gtORdp'].id),
            universe = cell_key,
            material = mat_dict[water_key].id,
            comment = 'Coolant around GT pin at DP')

def create_gridstrap():

    # Moderator universe
    add_cell('water_mod',
        surfaces = '',
        universe = 'mod',
        material =  mat_dict['h2o_hzp'].id,
        comment = 'Moderator universe')

    # North grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_N_'+gridmat,
            surfaces = '-{0}'.format(surf_dict['strapfront'].id),
            universe = 'strap_N_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'North {0} grid strap'.format(gridmat))
        add_cell('strap_N_mod_'+gridmat,
            surfaces = '{0}'.format(surf_dict['strapfront'].id),
            universe = 'strap_N_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod north of {0} north grid strap'.format(gridmat))

    # Northeast grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_NE_'+gridmat,
            surfaces = '-{0} -{1}'.format(surf_dict['strapright'].id, surf_dict['strapfront'].id),
            universe = 'strap_NE_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'Northeast {0} grid strap'.format(gridmat))
        add_cell('strap_NE_mod_n_'+gridmat,
            surfaces = '-{0} {1}'.format(surf_dict['strapright'].id, surf_dict['strapfront'].id),
            universe = 'strap_NE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod north of {0} northeast grid strap'.format(gridmat))
        add_cell('strap_NE_mod_e_'+gridmat,
            surfaces = '{0} -{1}'.format(surf_dict['strapright'].id, surf_dict['strapfront'].id),
            universe = 'strap_NE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod east of {0} northeast grid strap'.format(gridmat))
        add_cell('strap_NE_mod_ne_'+gridmat,
            surfaces = '{0} {1}'.format(surf_dict['strapright'].id, surf_dict['strapfront'].id),
            universe = 'strap_NE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod northeast of {0} northeast grid strap'.format(gridmat))

    # East grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_E_'+gridmat,
            surfaces = '-{0}'.format(surf_dict['strapright'].id),
            universe = 'strap_E_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'East {0} grid strap'.format(gridmat))
        add_cell('strap_E_mod_'+gridmat,
            surfaces = '{0}'.format(surf_dict['strapright'].id),
            universe = 'strap_E_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod east of {0} east grid strap'.format(gridmat))

    # Southeast grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_SE_'+gridmat,
            surfaces = '-{0} {1}'.format(surf_dict['strapright'].id, surf_dict['strapback'].id),
            universe = 'strap_SE_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'Southeast {0} grid strap'.format(gridmat))
        add_cell('strap_SE_mod_s_'+gridmat,
            surfaces = '-{0} -{1}'.format(surf_dict['strapright'].id, surf_dict['strapback'].id),
            universe = 'strap_SE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod south of {0} southeast grid strap'.format(gridmat))
        add_cell('strap_SE_mod_e_'+gridmat,
            surfaces = '{0} {1}'.format(surf_dict['strapright'].id, surf_dict['strapback'].id),
            universe = 'strap_SE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod east of {0} southeast grid strap'.format(gridmat))
        add_cell('strap_SE_mod_se_'+gridmat,
            surfaces = '{0} -{1}'.format(surf_dict['strapright'].id, surf_dict['strapback'].id),
            universe = 'strap_SE_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod southeast of {0} southeast grid strap'.format(gridmat))

    # South grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_S_'+gridmat,
            surfaces = '{0}'.format(surf_dict['strapback'].id),
            universe = 'strap_S_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'South {0} grid strap'.format(gridmat))
        add_cell('strap_S_mod_'+gridmat,
            surfaces = '-{0}'.format(surf_dict['strapback'].id),
            universe = 'strap_S_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod south of {0} south grid strap'.format(gridmat))

    # Southwest grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_SW_'+gridmat,
            surfaces = '{0} {1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_SW_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'Southwest {0} grid strap'.format(gridmat))
        add_cell('strap_SW_mod_s_'+gridmat,
            surfaces = '{0} -{1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_SW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod south of {0} southwest grid strap'.format(gridmat))
        add_cell('strap_SW_mod_w_'+gridmat,
            surfaces = '-{0} {1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_SW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod west of {0} southwest grid strap'.format(gridmat))
        add_cell('strap_SW_mod_sw_'+gridmat,
            surfaces = '-{0} -{1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_SW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod southwest of {0} southwest grid strap'.format(gridmat))

    # West grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_W_'+gridmat,
            surfaces = '{0}'.format(surf_dict['strapleft'].id),
            universe = 'strap_W_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'West {0} grid strap'.format(gridmat))
        add_cell('strap_W_mod_'+gridmat,
            surfaces = '-{0}'.format(surf_dict['strapleft'].id),
            universe = 'strap_W_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod west of {0} west grid strap'.format(gridmat))

    # Northwest grid strap
    for gridmat in ['ss', 'zr']:
        add_cell('strap_NW_'+gridmat,
            surfaces = '{0} -{1}'.format(surf_dict['strapleft'].id, surf_dict['strapfront'].id),
            universe = 'strap_NW_'+gridmat,
            material = mat_dict[gridmat].id,
            comment = 'Northwest {0} grid strap'.format(gridmat))
        add_cell('strap_NW_mod_s_'+gridmat,
            surfaces = '{0} {1}'.format(surf_dict['strapleft'].id, surf_dict['strapfront'].id),
            universe = 'strap_NW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod north of {0} northwest grid strap'.format(gridmat))
        add_cell('strap_NW_mod_w_'+gridmat,
            surfaces = '-{0} -{1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_NW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod west of {0} northwest grid strap'.format(gridmat))
        add_cell('strap_NW_mod_sw_'+gridmat,
            surfaces = '-{0} {1}'.format(surf_dict['strapleft'].id, surf_dict['strapback'].id),
            universe = 'strap_NW_'+gridmat,
            material = mat_dict['h2o_hzp'].id,
            comment = 'Mod northwest of {0} northest grid strap'.format(gridmat))

def create_lattice(lat_key, fuel_key, bp_key, gt_key, it_key, grid=False, comment = None):

    # Get ids
    fuel_id = univ_dict[fuel_key].id
    bp_id = univ_dict[bp_key].id
    gt_id = univ_dict[gt_key].id
    it_id = univ_dict[it_key].id

    # Check for grid
    if grid == 'TB':
        no_id = univ_dict['strap_N_ss'].id
        ne_id = univ_dict['strap_NE_ss'].id
        ea_id = univ_dict['strap_E_ss'].id
        se_id = univ_dict['strap_SE_ss'].id
        so_id = univ_dict['strap_S_ss'].id
        sw_id = univ_dict['strap_SW_ss'].id
        we_id = univ_dict['strap_W_ss'].id
        nw_id = univ_dict['strap_NW_ss'].id
    elif grid == 'I':
        no_id = univ_dict['strap_N_zr'].id
        ne_id = univ_dict['strap_NE_zr'].id
        ea_id = univ_dict['strap_E_zr'].id
        se_id = univ_dict['strap_SE_zr'].id
        so_id = univ_dict['strap_S_zr'].id
        sw_id = univ_dict['strap_SW_zr'].id
        we_id = univ_dict['strap_W_zr'].id
        nw_id = univ_dict['strap_NW_zr'].id
    else:
        no_id = univ_dict['mod'].id
        ne_id = univ_dict['mod'].id
        ea_id = univ_dict['mod'].id
        se_id = univ_dict['mod'].id
        so_id = univ_dict['mod'].id
        sw_id = univ_dict['mod'].id
        we_id = univ_dict['mod'].id
        nw_id = univ_dict['mod'].id


    # Calculate coordinates
    lleft = -19.0*pin_pitch / 2.0

    # Make lattice
    add_lattice(lat_key,
        dimension = '19 19',
        lower_left = '{0} {0}'.format(lleft),
        width = '{0} {0}'.format(pin_pitch),
        universes = { 'fp': fuel_id,
                      'pa': bp_id,
                      'pb': gt_id,
                      'pc': bp_id,
                      'pd': bp_id,
                      'pe': bp_id,
                      'pf': bp_id,
                      'pg': gt_id,
                      'ph': gt_id,
                      'pi': gt_id,
                      'pj': bp_id,
                      'pk': gt_id,
                      'pl': gt_id,
                      'pm': it_id,
                      'pn': gt_id,
                      'po': gt_id,
                      'pp': bp_id,
                      'pq': gt_id,
                      'pr': gt_id,
                      'ps': gt_id,
                      'pt': bp_id,
                      'pu': bp_id,
                      'pv': bp_id,
                      'pw': bp_id,
                      'px': gt_id,
                      'py': bp_id,
                      'no': no_id,
                      'ne': ne_id,
                      'ea': ea_id,
                      'se': se_id,
                      'so': so_id,
                      'sw': sw_id,
                      'we': we_id,
                      'nw': nw_id},
        comment = comment)

def create_axial_regions():

    # Support Plate
    add_cell('suppin', 
        surfaces = '-{0}'.format(surf_dict['cladOR'].id), 
        universe = 'supplate',
        material = mat_dict['ss'].id,
        comment = 'Support plate pin')
    add_cell('supmod',
        surfaces = '{0}'.format(surf_dict['cladOR'].id),
        universe = 'supplate',
        material = mat_dict['h2o_hzp'].id,
        comment = 'Moderator around support plate')
    create_gtpin_cell('gt_hzp', 'gt', 'h2o_hzp')

    # Make lattice for support plate
    create_lattice('support_plate', 'supplate', 'mod', 'mod', 'gt_hzp', comment = 'Support Plate')

    # Bottom of Fuel Rod lattice
    add_cell('rodpin', 
        surfaces = '-{0}'.format(surf_dict['cladOR'].id), 
        universe = 'botfpin',
        material = mat_dict['zr'].id,
        comment = 'Bottom Fuel Rod pin')
    add_cell('rodmod',
        surfaces = '{0}'.format(surf_dict['cladOR'].id),
        universe = 'botfpin',
        material = mat_dict['h2o_hzp'].id,
        comment = 'Moderator around Bottom Fuel Rod')
    create_gtpinDP_cell('gtDP_hzp', 'gtDP', 'h2o_hzp')
    create_lattice('bottom_fuel', 'botfpin', 'gtDP_hzp', 'gtDP_hzp', 'gt_hzp', comment = 'Bottom of Fuel Rod')

    # Compute water region thickness
    water_size = active_core_height/float(n_water)

    # Determine where water planes are
    more = True
    water_planes = []
    current_plane = axial_surfaces['baf']
    while(more):
        current_plane += water_size
        water_planes.append(current_plane)
        if current_plane + water_size > axial_surfaces['taf']:
            more = False
    water_planes.append(axial_surfaces['taf'])

    # Set up function for water density calculation
    try:
        d_rho = (hzp_density - low_density) / float(n_densities - 1)
    except ZeroDivisionError:
        d_rho = 0.0
    def coolant_density(idx): return hzp_density - d_rho*float(idx + 1)

    # Add lower core surfaces
    add_surface('lower_plenum', 'z-plane', '{0}'.format(axial_surfaces['lower_plenum']), comment = 'Bottom Support Plate')
    add_surface('support_plate', 'z-plane', '{0}'.format(axial_surfaces['support_plate']), comment = 'Top Support Plate')

    # Begin loop from BAF to TAF
    add_surface('baf', 'z-plane', '{0}'.format(axial_surfaces['baf']), comment = 'Bottom of Active Fuel')
    bottom_surface = ['baf']
    top_surface = []
    grids = []
    label_idx = 0
    water_idx = 0
    grid = False
    grid_id = 0
    for plane in OrderedDict(sorted(axial_surfaces.items(), key=lambda t: t[1])):

        # start above baf
        if axial_surfaces[plane] <= axial_surfaces['baf']:
            continue

        # stop after taf
        if axial_surfaces[plane] > axial_surfaces['taf']:
            break

        # check for grid
        if grid:
            grids.append(grid_id)
        else:
            grids.append(0)
        if 'grid' in plane and 'bot' in plane:
            grid = True
            grid_id += 1
        elif 'grid' in plane and 'top' in plane:
            grid = False

        # check if we hit a water plane first
        label = axial_labels[label_idx]
        subplane = 1
        while water_planes[water_idx] < axial_surfaces[plane]:
            axial_labels.insert(label_idx,label + ' Water Region {0}'.format(subplane))
            add_surface(plane+'_water {0}'.format(subplane), 'z-plane', '{0}'.format(water_planes[water_idx]), comment = axial_labels[label_idx])
            bottom_surface.append(plane+'_water {0}'.format(subplane))
            top_surface.append(plane+'_water {0}'.format(subplane))
            axial_surfaces.update({plane+'_water {0}'.format(subplane):water_planes[water_idx]})
            label_idx += 1
            water_idx += 1
            subplane += 1
            grids.append(grid)
            if water_idx >= len(water_planes):
                break

        # add surface
        add_surface(plane, 'z-plane', '{0}'.format(axial_surfaces[plane]), comment = axial_labels[label_idx])
        bottom_surface.append(plane)
        top_surface.append(plane)
        label_idx += 1
    del bottom_surface[len(bottom_surface)-1] # delete the last entry

    # Loop around axial regions
    water_idx = 0
    for i in range(len(bottom_surface)):
        bottom = bottom_surface[i]
        top = top_surface[i]
        if axial_surfaces[top] <= axial_surfaces['dptop']:
            dp = True
        else:
            dp = False
        grid = grids[i]
        add_axial('{0}_{1}'.format(axial_labels[i+3], axial_labels[i+4]),
            bottom = bottom,
            top = top,
            dp = dp,
            grid = grid,
            water_idx = water_idx,
            cool_rho = coolant_density(water_idx))
        if water_planes[water_idx] == axial_surfaces[top]:
            water_idx += 1

def create_assembly():

    # Add lower plenum region 
    add_cell('lower_plenum',
        surfaces = '-{0}'.format(surf_dict['lower_plenum'].id),
        universe = 'assembly',
        material = mat_dict['h2o_hzp'].id,
        comment = 'Lower Plenum')
    add_plot('plot_lower_plenum',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['lowest_extent'] + axial_surfaces['lower_plenum'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'lower_plenum')

    # Add support plate 
    add_cell('support_plate',
        surfaces = '{0} -{1}'.format(surf_dict['lower_plenum'].id, surf_dict['support_plate'].id),
        universe = 'assembly',
        fill = lat_dict['support_plate'].id,
        comment = 'Support Plate')
    add_plot('plot_support_plate',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['lower_plenum'] + axial_surfaces['support_plate'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'support_plate')

    # Add bottom of fuel pin 
    add_cell('bottom_fuel',
        surfaces = '{0} -{1}'.format(surf_dict['support_plate'].id, surf_dict['baf'].id),
        universe = 'assembly',
        fill = lat_dict['bottom_fuel'].id,
        comment = 'Bottom of fuel rods')
    add_plot('plot_bottom_fuel',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['support_plate'] + axial_surfaces['baf'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'bottom_fuel')

    # Build active core
    i = 0
    current_water = -1
    for item in axial_dict.keys():

        # Get the current axial region
        axial = axial_dict[item]

        # Create water material for this axial region
        #     if not yet created
        grid_counter = 0
        if current_water != axial.water_idx:

            # Color for plots
            color = -156.0/(hzp_density - low_density) * \
                    (axial.cool_rho - hzp_density)

            # Water material
            create_water_material('water_{0}'.format(axial.water_idx),
                                  axial.cool_rho, color)

            # Make this the current water index
            current_water = axial.water_idx

        # Check for grid
        if axial.grid > 0:
            if axial.grid == 1 or axial.grid == 8:
                grid = 'TB'
            else:
                grid = 'I'
        else:
            grid = None

        # Create fuel pin and guide tube for this water region
        create_fuelpin_cell('fpw_{0}'.format(i), 'fuel', 'water_{0}'.format(current_water), grid=grid)
        if axial.dp:
            create_gtpinDP_cell('gtw_{0}'.format(i), 'gtDP', 'water_{0}'.format(current_water), grid=grid)
        else:
            create_gtpin_cell('gtw_{0}'.format(i), 'gt', 'water_{0}'.format(current_water), grid=grid)

        # Check to create bp pin
        if axial_surfaces[axial.bottom] >= axial_surfaces['bpbot']:
            if axial.dp:
                create_bppinDP_cell('bpw_{0}'.format(i), 'bpDP', 'water_{0}'.format(current_water), grid=grid)
            else:
                create_bppin_cell('bpw_{0}'.format(i), 'bp', 'water_{0}'.format(current_water), grid=grid)
            bp_key = 'bpw_{0}'.format(i)
        else:
            bp_key = 'gtw_{0}'.format(i)

        # Create a lattice
        create_lattice('lat_{0}'.format(i), 
            fuel_key = 'fpw_{0}'.format(i),
            bp_key = bp_key,
            gt_key = 'gtw_{0}'.format(i),
            it_key = 'gtw_{0}'.format(i),
            grid = grid,
            comment = 'Lattice active region {0}'.format(i))
 
        # Fill lattice into axial cell
        add_cell(item,
            surfaces = '{0} -{1}'.format(surf_dict[axial.bottom].id, surf_dict[axial.top].id),
            universe = 'assembly',
            fill = lat_dict['lat_{0}'.format(i)].id, 
            comment = 'Cell fill lattice active region {0}'.format(i))

        # Add a plot
        add_plot('plot_active_region_{0}'.format(i),
            origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces[axial.bottom] + axial_surfaces[axial.top])),
            width = '{0} {0}'.format(assy_pitch+5),
            basis = 'xy',
            filename = 'active_region_{0}'.format(i))

        i += 1 # next axial region
    i -= 1
    # Add pin plenum region before grid 8
    create_fuelpin_cell('fuelpinplenum', 'fuelplenum', 'water_{0}'.format(current_water))
    create_bppin_cell('bppinplenum', 'bpplenum', 'water_{0}'.format(current_water))
    create_lattice('pinplenum', 'fuelpinplenum', 'bppinplenum', 'gtw_{0}'.format(i), 'gtw_{0}'.format(i), comment = 'Pin Plenum before Grid 8')
    add_surface('grid8bot', 'z-plane', '{0}'.format(axial_surfaces['grid8bot']), comment = 'Grid 8 Bottom')
    add_cell('pinplenum',
        surfaces = '{0} -{1}'.format(surf_dict['taf'].id, surf_dict['grid8bot'].id),
        universe = 'assembly',
        fill = lat_dict['pinplenum'].id,
        comment = 'Cell fill Lattice Pin Plenum before Grid 8')
    add_plot('plot_pin_plenum',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['taf'] + axial_surfaces['grid8bot'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'pin_plenum')

    # Add Grid 8 region
    create_fuelpin_cell('fuelpinplenumgrid8', 'fuelplenum', 'water_{0}'.format(current_water), grid = 'TB')
    create_bppin_cell('bppinplenumgrid8', 'bpplenum', 'water_{0}'.format(current_water), grid = 'TB')
    create_gtpin_cell('gtpinplenumgrid8', 'gt', 'water_{0}'.format(current_water), grid = 'TB')
    create_lattice('pinplenumgrid8', 'fuelpinplenumgrid8', 'bppinplenumgrid8', 'gtpinplenumgrid8', 'gtpinplenumgrid8', grid = 'TB', comment = 'Pin Plenum at Grid 8')
    add_surface('grid8top', 'z-plane', '{0}'.format(axial_surfaces['grid8top']), comment = 'Grid 8 Top')
    add_cell('pinplenumgrid8',
        surfaces = '{0} -{1}'.format(surf_dict['grid8bot'].id, surf_dict['grid8top'].id),
        universe = 'assembly',
        fill = lat_dict['pinplenumgrid8'].id,
        comment = 'Cell fill Lattice Pin Plenum at Grid 8')
    add_plot('plot_pin_plenumgrid',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['grid8bot'] + axial_surfaces['grid8top'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'pin_plenum_grid8')

    # Add pin plenum region above grid 8
    add_surface('topplugbot', 'z-plane', '{0}'.format(axial_surfaces['topplugbot']), comment = 'Bottom of Top End Plug')
    add_cell('pinplenum2', 
        surfaces = '{0} -{1}'.format(surf_dict['grid8top'].id, surf_dict['topplugbot'].id),
        universe = 'assembly',
        fill = lat_dict['pinplenum'].id,
        comment = 'Cell fill Lattice Pin Plenum after Grid 8')
    add_plot('plot_pin_plenum2',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['grid8top'] + axial_surfaces['topplugbot'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'pin_plenum2')

    # Make zircaloy fuel pin for top plug
    add_cell('fueltopplugzr',
        surfaces = '-{0}'.format(surf_dict['cladOR'].id),
        universe = 'topplug',
        material = mat_dict['zr'].id,
        comment = 'Zircaloy Fuel Top Plug')
    add_cell('fueltopplugcool',
        surfaces = '{0}'.format(surf_dict['cladOR'].id),
        universe = 'topplug',
        material = mat_dict['water_{0}'.format(current_water)].id,
        comment = 'Coolant around Fuel Top Plug')
    create_lattice('topplug', 'topplug', 'bppinplenum', 'gtw_{0}'.format(i), 'gtw_{0}'.format(i), comment = 'Fuel Top Plug')
    add_surface('rodtop', 'z-plane', '{0}'.format(axial_surfaces['rodtop']), comment = 'Top of Fuel Rod')
    add_cell('rodtopplug', 
        surfaces = '{0} -{1}'.format(surf_dict['topplugbot'].id, surf_dict['rodtop'].id),
        universe = 'assembly',
        fill = lat_dict['topplug'].id,
        comment = 'Cell fill Lattice Top End Plug')
    add_plot('plot_topplug',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['topplugbot'] + axial_surfaces['rodtop'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'top_plug')

    # Water region before nozzle 
    add_cell('upperwater',
        surfaces = '',
        universe = 'upperwater',
        material = mat_dict['water_{0}'.format(current_water)].id,
        comment = 'Coolant in before nozzle')
    create_lattice('beforenozzle', 'upperwater', 'bppinplenum', 'gtw_{0}'.format(i), 'gtw_{0}'.format(i), comment = 'Before Nozzle')
    add_surface('nozzlebot', 'z-plane', '{0}'.format(axial_surfaces['nozzlebot']), comment = 'Bottom of Nozzle')
    add_cell('beforenozzle', 
        surfaces = '{0} -{1}'.format(surf_dict['rodtop'].id, surf_dict['nozzlebot'].id),
        universe = 'assembly',
        fill = lat_dict['beforenozzle'].id,
        comment = 'Before nozzle')
    add_plot('plot_beforenozzle',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['rodtop'] + axial_surfaces['nozzlebot'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'before_nozzle')

    # Nozzle Region
    # Fuel Pin
    add_cell('fuel_nozzle_ss',
        surfaces = '-{0}'.format(surf_dict['cladOR'].id),
        universe = 'fuel_nozzle',
        material = mat_dict['ss'].id,
        comment = 'SS Fuel Pin to approximate Nozzle')
    add_cell('fuel_nozzle_cool',
        surfaces = '{0}'.format(surf_dict['cladOR'].id),
        universe = 'fuel_nozzle',
        material = mat_dict['water_{0}'.format(current_water)].id,
        comment = 'Coolant around fuel pin in nozzle')

    # BP Pin
    add_cell('bp_nozzle_ss',
        surfaces = '-{0}'.format(surf_dict['bpIR6'].id),
        universe = 'bp_nozzle',
        material = mat_dict['ss'].id,
        comment = 'SS BP Pin to approximate Nozzle')
    add_cell('bp_nozzle_cool',
        surfaces = '{0}'.format(surf_dict['bpIR6'].id),
        universe = 'bp_nozzle',
        material = mat_dict['water_{0}'.format(current_water)].id,
        comment = 'Coolant around bp pin in nozzle')

    create_lattice('nozzle', 'fuel_nozzle', 'bp_nozzle', 'upperwater', 'upperwater', comment = 'Nozzle')
    add_surface('nozzletop', 'z-plane', '{0}'.format(axial_surfaces['nozzletop']), comment = 'Top of Nozzle')
    add_cell('nozzle', 
        surfaces = '{0} -{1}'.format(surf_dict['nozzlebot'].id, surf_dict['nozzletop'].id),
        universe = 'assembly',
        fill = lat_dict['nozzle'].id,
        comment = 'Nozzle')
    add_plot('plot_nozzle',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['nozzlebot'] + axial_surfaces['nozzletop'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'nozzle')

    # Add upper plenum region 
    add_cell('upper_plenum',
        surfaces = '{0}'.format(surf_dict['nozzletop'].id),
        universe = 'assembly',
        material = mat_dict['water_{0}'.format(current_water)].id,
        comment = 'Upper Plenum')
    add_plot('plot_upper_plenum',
        origin = '0.0 0.0 {0}'.format(0.5*(axial_surfaces['nozzletop'] + axial_surfaces['highest_extent'])),
        width = '{0} {0}'.format(assy_pitch+5),
        basis = 'xy',
        filename = 'upper_plenum')

def create_core():
    add_cell('core',
        surfaces = '{0} -{1} {2} -{3} {4} -{5}'.format(surf_dict['core_left'].id, surf_dict['core_right'].id,
                                                       surf_dict['core_back'].id, surf_dict['core_front'].id,
                                                       surf_dict['core_bottom'].id, surf_dict['core_top'].id),
        fill = univ_dict['assembly'].id,
        comment = 'Core fill')

    add_plot('plot_axial',
        origin = '0.0 {0} {1}'.format(6*pin_pitch,0.5*(axial_surfaces['highest_extent'] + axial_surfaces['lowest_extent'])),
        width = '{0} {1}'.format(assy_pitch+5, axial_surfaces['highest_extent'] - axial_surfaces['lowest_extent'] + 5),
        basis = 'xz',
        filename = 'axial')

def create_water_material(key, water_density, color=None):

    # Avagadros Number
    NA = 0.60221415

    # Molar masses of nuclides
    MH1 = 1.0078250
    MH2 = 2.0141018
    MB10 = 10.0129370
    MB11 = 11.0093054
    MO16 = 15.9949146196
    MO17 = 16.9991317
    MO18 = 17.999161

    # Molar masses of natural elements
    MH = 1.00794
    MB = 10.811
    MO = 15.9994

    # Natrual abundances
    aH1 = 0.99985
    aH2 = 0.00015
    aB10 = 0.199
    aB11 = 0.801
    aO16 = 0.99757
    aO17 = 0.00038
    aO18 = 0.00205

    # Boron info
    ppm = 975
    wBph2o = ppm * 10**-6

    # Molecular mass of pure water
    Mh2o = 2*MH + MO

    # Compute number density of pure water
    Nh2o = water_density * NA / Mh2o

    # Compute mass density of borated water
    rhoh2oB = water_density / (1.0 - wBph2o)

    # Compute number densities of elements
    NB = wBph2o * rhoh2oB * NA / MB
    NH = 2.0 * Nh2o
    NO = Nh2o

    # Compute isotopic number densities
    NB10 = aB10 * NB
    NB11 = aB11 * NB
    NH1 = aH1 * NH
    NH2 = aH2 * NH
    NO16 = aO16 * NO
    NO17 = aO17 * NO
    NO18 = aO18 * NO

    mat_h2o = Material(key, 'HZP Water @ {0} g/cc'.format(water_density))
    mat_h2o.add_nuclide('B-10', '71c', str(NB10))
    mat_h2o.add_nuclide('B-11', '71c', str(NB11))
    mat_h2o.add_nuclide('H-1', '71c', str(NH1))
    mat_h2o.add_nuclide('H-2', '71c', str(NH2))
    mat_h2o.add_nuclide('O-16', '71c', str(NO16))
    mat_h2o.add_nuclide('O-17', '71c', str(NO17 + NO18))
    mat_h2o.add_sab('lwtr', '15t')
    if color != None:
        mat_h2o.add_color('{0} {0} 255'.format(int(color)))
    mat_h2o.finalize()

def create_cmfd():

    # Put mesh info in
    dz = (axial_surfaces['taf'] - axial_surfaces['baf'])/float(n_water)
    mx = -assy_pitch/2.0
    my = -assy_pitch/2.0
    mz = axial_surfaces['baf'] - dz
    px = assy_pitch/2.0
    py = assy_pitch/2.0
    pz = axial_surfaces['taf'] + dz
    cmfd.update({'lower_left': '{0} {1} {2}'.format(mx, my, mz)})
    cmfd.update({'upper_right':'{0} {1} {2}'.format(px, py, pz)})
    cmfd.update({'dimension':'1 1 {0}'.format(n_water + 2)})
    map_str = "1\n"
    for i in range(n_water):
        map_str += "2\n"
    map_str += "1\n"
    cmfd.update({'map':map_str})

    # Put water id map in
    water_str = "0\n"
    current_id = -1 
    for key in axial_dict.keys():
        axial = axial_dict[key]
        if axial.water_idx != current_id:
            current_id = axial.water_idx
            water_str += "{0}\n".format(mat_dict['water_{0}'.format(current_id)].id)
    water_str += "0"
    cmfd.update({'water_map':water_str})

    # Put enrichment and bp map together
    enr_str = "0.0\n"
    bp_str = "0\n"
    for i in range(n_water):
        enr_str += "2.4\n"
        bp_str += "12\n"
    enr_str += "0.0"
    bp_str += "0"
    cmfd.update({'enr_map':enr_str})
    cmfd.update({'bp_map':bp_str})

    # Fuel temperature
    temp_low = 600.0
    temp_high = 1200.0
    try:
        temp_slope = (temp_high - temp_low)/float(n_temps - 1)
    except ZeroDivisionError:
        temp_slope = 0.0
    temp_str = "{0}\n".format(temp_low)
    for i in range(n_water):
        temp = temp_slope*i + temp_low
        temp_str += "{0}\n".format(temp)
    temp_str += "{0}".format(temp_low)
    cmfd.update({'fuel_temp':temp_str})

    # Density
    density_str = "0.0\n"
    current_id = -1 
    for key in axial_dict.keys():
        axial = axial_dict[key]
        if axial.water_idx != current_id:
            current_id = axial.water_idx
            density_str += "{0}\n".format(axial.cool_rho)
    density_str += "0.0"
    cmfd.update({'density':density_str})

    # Normalization
    cmfd.update({'norm':n_water})

def write_openmc_input():

############ Geometry File ##############

    # Heading info
    geo_str = ""
    geo_str += \
"""<?xml version="1.0" encoding="UTF-8"?>\n<geometry>\n\n"""

    # Write out surfaces
    for item in surf_dict.keys():
        geo_str += surf_dict[item].write_xml()

    # Write out cells
    geo_str += "\n"
    for item in cell_dict.keys():
        geo_str += cell_dict[item].write_xml()

    # Write out lattices
    geo_str += "\n"
    for item in lat_dict.keys():
        geo_str += lat_dict[item].write_xml()

    # Write out footer info
    geo_str += \
"""\n</geometry>"""
    with open('geometry.xml','w') as fh:
        fh.write(geo_str)

############ Materials File ##############

    # Heading info
    mat_str = ""
    mat_str += \
"""<?xml version="1.0" encoding="UTF-8"?>\n<materials>\n\n"""

    # Write out materials
    for item in mat_dict.keys():
        mat_str += mat_dict[item].write_xml()
        mat_str += "\n"

    # Write out footer info
    mat_str += \
"""</materials>"""
    with open('materials.xml','w') as fh:
        fh.write(mat_str)

############ Settings File ##############

    settings.update({
'xbot' : -assy_pitch/2.0,
'ybot' : -assy_pitch/2.0,
'zbot' : axial_surfaces['baf'],
'xtop' : assy_pitch/2.0,
'ytop' : assy_pitch/2.0,
'ztop' : axial_surfaces['taf'],
'entrX' : 1,
'entrY' : 1,
'entrZ' : n_water
    })

    set_str = """<?xml version="1.0" encoding="UTF-8"?>
<settings>

  <!-- Parameters for criticality calculation -->
  <eigenvalue batches="{batches}" inactive="{inactive}" particles="{particles}" />

  <!-- Starting source -->
  <source>
    <space type="box">
      <parameters>{xbot} {ybot} {zbot} {xtop} {ytop} {ztop}</parameters>
    </space>
  </source>
  
  <!-- Shannon Entropy -->
  <entropy>
    <dimension> {entrX} {entrY} {entrZ} </dimension>
    <lower_left> {xbot} {ybot} {zbot} </lower_left>
    <upper_right> {xtop} {ytop} {ztop} </upper_right>
  </entropy>

  <!-- Run CMFD -->
  <run_cmfd> {run_cmfd} </run_cmfd>

</settings>""".format(**settings)
    with open('settings.xml','w') as fh:
        fh.write(set_str)

############ Plots File ##############

    plot_str = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    plot_str += """<plots>\n"""
    for item in plot_dict.keys():
        plot_str += plot_dict[item].write_xml()
        plot_str += "\n"
    plot_str += """</plots>""".format(x = assy_pitch+5, y = assy_pitch+5)
    with open('plots.xml','w') as fh:
        fh.write(plot_str)

############ CMFD File ###############

    cmfd_str = """<?xml version="1.0" encoding="UTF-8"?>
<cmfd>

  <!-- This file auto-generated by beavrs.py  -->
  <mesh>
    <lower_left>{lower_left}</lower_left>
    <upper_right>{upper_right}</upper_right>
    <dimension>{dimension}</dimension>
    <albedo>1.0 1.0 1.0 1.0 0.0 0.0</albedo>
    <map>
{map}
    </map>
    <energy>0.0 0.625e-6 20.0</energy>
  </mesh>
  
  <thermal>
    <water_map>
{water_map} 
    </water_map>

    <enr_map>
{enr_map}
    </enr_map>

    <bp_map>
{bp_map}
    </bp_map>

    <fuel_temp>
{fuel_temp}
    </fuel_temp>

    <density>
{density}
    </density>

    <core_power> {power} </core_power>
    <core_flowrate> {flowrate} </core_flowrate>
    <inlet_enthalpy> {inlet_enthalpy} </inlet_enthalpy>
    <n_assemblies> {n_assemblies} </n_assemblies>
    <boron> {boron} </boron>
    <maxthinner> {thinner} </maxthinner>
    <maxthouter> {thouter} </maxthouter>
    <interval> {interval} </interval>
  </thermal>

  <begin> {begin} </begin>
  <active_flush> {active_flush} </active_flush>
  <feedback> {feedback} </feedback>
  <norm> {norm} </norm>
  <downscatter> true </downscatter>
  <power_monitor> true </power_monitor>
</cmfd>
""".format(**cmfd)
    with open('cmfd.xml','w') as fh:
        fh.write(cmfd_str)

if __name__ == '__main__':
    main()
