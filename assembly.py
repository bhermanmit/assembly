#!/usr/bin/env python2

# Global Dictionaries
surf_dict = {}
cell_dict = {}
mat_dict = {}

# Class Definitions
class Element(object):
    def __init__(self, name, xs, value):
        self.name = name
        self.xs = xs
        self.value = value

class Nuclide(object):
    def __init__(self, name, xs, value):
        self.name = name
        self.xs = xs
        self.value = value

class Sab(object):
    def __init__(self, name, xs):
        self.name = name
        self.xs = xs

class Material(object):
    n_materials = 0
    def __init__(self, key, comment = None):
        self.n_materials += 1
        self.id = self.n_materials
        self.elements = []
        self.nuclides = []
        self.sab = None
        self.key = key
        self.comment = comment

    def add_element(self, name, xs, value):
        self.elements.append(Element(name, xs, value))

    def add_nuclide(self, name, xs, value):
        self.nuclides.append(Nuclide(name, xs, value))

    def add_sab(self, name, xs):
        self.sab = Sab(name, xs)

    def finalize(self):
        mat_dict.update({self.key:self})

class Surface(object):
    n_surfaces = 0
    def __init__(self, type, coeffs = "", comment=None):
        self.n_surfaces += 1
        self.id = self.n_surfaces
        self.type = type
        self.coeffs = coeffs
        self.comment = comment

class Cell(object):
    n_cells = 0
    def __init__(self, surfaces, universe=None, fill=None, material=None, comment=None):
        self.n_cells += 1
        self.id = self.n_cells
        self.universe = universe
        self.fill = fill
        self.material = material
        self.surfaces = surfaces
        self.comment = comment
        self.checked = False

        # check cell setup
        self.checked = self.check_cell()
        if not self.checked:
            raise Exception('Cell needs a universe and fill or material!')

    def check_cell(self):
        if self.universe == None:
            return False
        if self.fill == None and self.material == None:
            return False
        return True

class Lattice(object):
    n_lattices = 0
    def __init__(self, dimension, lower_left, upper_right, universes):
        self.n_lattices += 1
        self.id = self.n_lattices
        self.type = "rectangular"
        self.dimension = dimension
        self.lower_left = lower_left
        self.upper_right = upper_right
        self.universes = universes

        # Get lattice dimension
        self.nx = dimension.split()[0]
        self.ny = dimension.split()[1]

# Global Routines
def add_surface(key, type, coeffs, comment=None):
     surf_dict.update({key:Surface(type, coeffs, comment)})

def add_cell(key, surfaces, universe=None, fill=None, material=None, comment=None):
    cell_dict.update({key:Cell(surfaces, universe, fill, material, comment)})
