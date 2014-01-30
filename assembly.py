#!/usr/bin/env python2

# Global Dictionaries
surf_dict = {}
cell_dict = {}
mat_dict = {}
univ_dict = {}
universe_id = 9

# Class Definitions
class Element(object):
    def __init__(self, name, xs, value):
        self.name = name
        self.xs = xs
        self.value = value

    def display(self):
        print '    Name: {0}'.format(self.name)
        print '    XS: {0}'.format(self.xs)
        print '    Value: {0}'.format(self.value)

class Nuclide(object):
    def __init__(self, name, xs, value):
        self.name = name
        self.xs = xs
        self.value = value

    def display(self):
        print '    Name: {0}'.format(self.name)
        print '    XS: {0}'.format(self.xs)
        print '    Value: {0}'.format(self.value)

class Sab(object):
    def __init__(self, name, xs):
        self.name = name
        self.xs = xs

    def display(self):
        print '    Name: {0}'.format(self.name)
        print '    XS: {0}'.format(self.xs)

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

    def display(self):
        print '\nMaterial ID: {0}'.format(self.id)
        print 'Elements:'
        for item in self.elements:
            item.display()
        print 'Nuclides:'
        for item in self.nuclides:
            item.display()
        print 'S(a,b):'
        self.sab.display()

class Surface(object):
    n_surfaces = 0
    def __init__(self, type, coeffs = "", comment=None):
        self.n_surfaces += 1
        self.id = self.n_surfaces
        self.type = type
        self.coeffs = coeffs
        self.comment = comment

    def display(self):
        print '\nSurface ID: {0}'.format(self.id)
        print 'TYPE: {0}'.format(self.type)
        print 'COEFFICIENTS: {0}'.format(self.coeffs)
        if comment != None:
            print 'COMMENT: {0}'.format(self.comment)

class Cell(object):
    n_cells = 0
    def __init__(self, surfaces, universe=None, fill=None, material=None, comment=None):
        self.n_cells += 1
        self.id = self.n_cells
        self.fill = fill
        self.material = material
        self.surfaces = surfaces
        self.comment = comment
        self.checked = False

        # universe options
        if universe == None:
            self.universe = 0
        elif univ_dict.has_key(universe):
            self.universe = univ_dict[universe]
        else:
            universe_id += 1
            univ_dict.update({universe:universe_id})
            self.universe = univ_dict[universe]

        # check cell setup
        self.checked = self.check_cell()
        if not self.checked:
            raise Exception('Cell needs fill or material!')

    def check_cell(self):
        if self.fill == None and self.material == None:
            return False
        if self.fill != None and self.material != None:
            return False
        return True

    def display(self):
        print '\nCell ID {0}'.format(self.id)
        if fill != None:
            print 'Fill: {0}'.format(self.fill)
        if material != None:
            print 'Material: {0}'.format(self.material)
        print 'Surfaces: {0}'.format(self.surfaces)
        if comment != None:
            print 'Comment: {0}'.format(self.comment)

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

    def display(self):
        '\nLattice ID: {0}'.format(self.id)
        'Type: {0}'.format(self.type)
        'Dimension: {0}'.format(self.dimension)
        'Lower Left: {0}'.format(self.lower_left)
        'Upper Right: {0}'.format(self.upper_right)
        'Universes: {0}'.format(self.universes)

# Global Routines
def add_surface(key, type, coeffs, comment=None):
     surf_dict.update({key:Surface(type, coeffs, comment)})

def add_cell(key, surfaces, universe=None, fill=None, material=None, comment=None):
    cell_dict.update({key:Cell(surfaces, universe, fill, material, comment)})
