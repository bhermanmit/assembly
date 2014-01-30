#!/usr/bin/env python2

from assembly import *
import numpy as np

def main():

    # Create all static materials
    create_static_materials()

    # Create all surfaces
    create_surfaces()

    # Create water materials 
    create_water_material('h2o1', 0.73986)
    create_water_material('h2o2', 0.66)

    # Create fuel pins
    create_fuelpin('pin1', 'h2o1')
    create_fuelpin('pin2', 'h2o2')
    cell_dict['water_pin1'].display()
    cell_dict['water_pin2'].display()
    univ_dict['pin1'].display()

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
    mat_hzph2o.finalize()

    # Helium Material
    mat_hel = Material('he', 'Helium for Gap')
    mat_hel.add_nuclide('He-4', '71c', '2.4044e-04')
    mat_hel.finalize()

    # Air Material
    mat_air = Material('air', 'Air for Instrumentation Tubes')
    mat_air.add_element('C', '71c', '6.8296e-09')
    mat_air.add_nuclide('O-16', '71c', '5.2864e-06')
    mat_air.add_nuclide('O-17', '71c', '1.2877e-08')
    mat_air.add_nuclide('N-14', '71c', '1.9681e-05')
    mat_air.add_nuclide('N-15', '71c', '7.1900e-08')
    mat_air.add_nuclide('Ar-36', '71c', '7.9414e-10')
    mat_air.add_nuclide('Ar-38', '71c', '1.4915e-10')
    mat_air.add_nuclide('Ar-40', '71c', '2.3506e-07')
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
    mat_zr.finalize()

    # UO2 at 2.4% enrichment Material
    mat_fuel24 = Material('fuel24', 'UO2 Fuel 2.4 w/o')
    mat_fuel24.add_nuclide('U-234', '71c', '4.4843e-06')
    mat_fuel24.add_nuclide('U-235', '71c', '5.5815e-04')
    mat_fuel24.add_nuclide('U-238', '71c', '2.2408e-02')
    mat_fuel24.add_nuclide('O-16', '71c', '4.5829e-02')
    mat_fuel24.add_nuclide('O-17', '71c', '1.1164e-04')
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
    mat_bsg.finalize()

def create_surfaces():

    # Create fuel pin surfaces
    add_surface('fuelOR', 'z-cylinder', '0.0 0.0 0.392180', 'Fuel Outer Radius')
    add_surface('cladIR', 'z-cylinder', '0.0 0.0 0.400050', 'Clad Inner Radius')
    add_surface('cladOR', 'z-cylinder', '0.0 0.0 0.457200', 'Clad Outer Radius')

    # Create Guide Tube surfaces
    add_surface('gtIRad', 'z-cylinder', '0.0 0.0 0.561340', 'Guide Tube Inner Radius above Dashpot')
    add_surface('gtORad', 'z-cylinder', '0.0 0.0 0.601980', 'Guide Tube Outer Radius above Dashpot')
    add_surface('gtIRbd', 'z-cylinder', '0.0 0.0 0.504190', 'Guide Tube Inner Radius at Dashpot')
    add_surface('gtORbd', 'z-cylinder', '0.0 0.0 0.546100', 'Guide Tube Outer Radius at Dashpot')

    # Burnable Poison surfaces
    add_surface('bpIR1', 'z-cylinder', '0.0 0.0 0.214000', 'Burnable Absorber Rod Inner Radius 1')
    add_surface('bpIR2', 'z-cylinder', '0.0 0.0 0.230510', 'Burnable Absorber Rod Inner Radius 2')
    add_surface('bpIR3', 'z-cylinder', '0.0 0.0 0.241300', 'Burnable Absorber Rod Inner Radius 3')
    add_surface('bpIR4', 'z-cylinder', '0.0 0.0 0.426720', 'Burnable Absorber Rod Inner Radius 4')
    add_surface('bpIR5', 'z-cylinder', '0.0 0.0 0.436880', 'Burnable Absorber Rod Inner Radius 5')
    add_surface('bpIR6', 'z-cylinder', '0.0 0.0 0.483870', 'Burnable Absorber Rod Inner Radius 6')
    add_surface('bpIR7', 'z-cylinder', '0.0 0.0 0.561340', 'Burnable Absorber Rod Inner Radius 7')
    add_surface('bpIR8', 'z-cylinder', '0.0 0.0 0.601980', 'Burnable Absorber Rod Inner Radius 8')

def create_fuelpin(pin_key, water_key):

    # Fuel Pellet
    add_cell('fuel_'+pin_key, 
        surfaces = '-{0}'.format(surf_dict['fuelOR'].id), 
        universe = pin_key,
        material = mat_dict['fuel24'].id)

    # Gas Gap
    add_cell('gap_'+pin_key,
        surfaces = '{0} -{1}'.format(surf_dict['fuelOR'].id, surf_dict['cladIR'].id),
        universe = pin_key,
        material = mat_dict['he'].id)

    # Clad
    add_cell('clad_'+pin_key,
        surfaces = '{0} -{1}'.format(surf_dict['cladIR'].id, surf_dict['cladOR'].id),
        universe = pin_key,
        material = mat_dict['zr'].id)

    # Surrounding Water
    add_cell('water_'+pin_key,
        surfaces = '{0}'.format(surf_dict['cladOR'].id),
        universe = pin_key,
        material = mat_dict[water_key].id)

def create_water_material(key, water_density):

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
    mat_h2o.finalize()

if __name__ == '__main__':
    main()
