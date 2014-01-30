#!/usr/bin/env python2

# Packages
from collections import OrderedDict

# Global Dictionaries
surf_dict = OrderedDict() 
cell_dict = OrderedDict() 
mat_dict = OrderedDict()
univ_dict = OrderedDict()
lat_dict = OrderedDict()

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
        Material.n_materials += 1
        self.id = Material.n_materials
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
        Surface.n_surfaces += 1
        self.id = Surface.n_surfaces
        self.type = type
        self.coeffs = coeffs
        self.comment = comment

    def display(self):
        print '\nSurface ID: {0}'.format(self.id)
        print 'TYPE: {0}'.format(self.type)
        print 'COEFFICIENTS: {0}'.format(self.coeffs)
        if self.comment != None:
            print 'COMMENT: {0}'.format(self.comment)

    def write_xml(self):
        xml_str = ""
        xml_str += """  <surface id="{id:>6}" type="{type:<17}" coeffs="{coeffs:>25}"/>""".format(id = self.id, type = self.type, coeffs = self.coeffs)
        if self.comment != None:
            xml_str += """  <!--{0:^40}-->""".format(self.comment)
        xml_str += "\n"
        return xml_str

class Universe(object):
    n_universes = 0
    def __init__(self, value=None):
        if value != None:
            self.id = value 
        else:
            Universe.n_universes += 1
            self.id = 9 + Universe.n_universes
        self.cells = []

    def add_cell(self, key):
        self.cells.append(key)

    def display(self):
        print '\nUniverse ID: {0}'.format(self.id)
        print 'Cells: {0}'.format(self.cells)

class Cell(object):
    n_cells = 0
    def __init__(self, surfaces, universe=None, fill=None, material=None, comment=None):
        Cell.n_cells += 1
        self.id = Cell.n_cells
        self.fill = fill
        self.material = material
        self.surfaces = surfaces
        self.universe = universe
        self.comment = comment
        self.checked = False

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
        if self.fill != None:
            print 'Fill: {0}'.format(self.fill)
        if self.material != None:
            print 'Material: {0}'.format(self.material)
        print 'Surfaces: {0}'.format(self.surfaces)
        print 'Universe: {0}'.format(self.universe)
        if self.comment != None:
            print 'Comment: {0}'.format(self.comment)

    def write_xml(self):
        xml_str = ""
        if self.fill == None:
          xml_str += """  <cell id="{id:>6}" universe="{univ:<6}" material="{mat:>6}" surfaces="{surfs:>12}"/>""".format(id = self.id, univ = self.universe, mat = self.material, surfs = self.surfaces)
        else:
          xml_str += """  <cell id="{id:>6}" universe="{univ:<6}" fill="{fill:>10}" surfaces="{surfs:>12}"/>""".format(id = self.id, univ = self.universe, fill = self.fill, surfs = self.surfaces)
        if self.comment != None:
            xml_str += """  <!--{0:^40}-->""".format(self.comment)
        xml_str += "\n"
        return xml_str
        

class Lattice(object):
    n_lattices = 0
    def __init__(self, dimension, lower_left, width, universes, comment=None):
        Lattice.n_lattices += 1
        self.id = Lattice.n_lattices
        self.type = "rectangular"
        self.dimension = dimension
        self.lower_left = lower_left
        self.width = width
        self.universes = universes
        self.comment = comment

        # Get lattice dimension
        self.nx = dimension.split()[0]
        self.ny = dimension.split()[1]

    def display(self):
        print '\nLattice ID: {0}'.format(self.id)
        print 'Type: {0}'.format(self.type)
        print 'Dimension: {0}'.format(self.dimension)
        print 'Lower Left: {0}'.format(self.lower_left)
        print 'Width: {0}'.format(self.width)
        print 'Universes: {0}'.format(self.universes)
        if self.comment != None:
          print 'Comment: {0}'.format(self.comment)

    def write_xml(self):
        xml_str = "\n"
        if self.comment != None:
            xml_str += """  <!--{0:^40}-->\n""".format(self.comment)
        xml_str += """  <lattice id="{id:>6}" type="{type}", dimension={dim}>\n""".format(id = self.id, type = self.type, dim = self.dimension)
        xml_str += """    <lower_left>{lleft}</lower_left>\n""".format(lleft = self.lower_left)
        xml_str += """    <width>{width}</width>\n""".format(width = self.width)
        xml_str += """    <universes>{univs}    </universes>\n""".format(univs = self.universes)
        xml_str += """  </lattice>\n"""
        return xml_str

# Global Routines
def add_surface(key, type, coeffs, comment=None):
     surf_dict.update({key:Surface(type, coeffs, comment)})

def add_cell(key, surfaces, universe=None, fill=None, material=None, comment=None):

    # Get universe ID
    if universe == None:
        if not univ_dict.has_key('global'):
            univ_dict.update({'global':Universe(0)})
        univ_dict['global'].add_cell(key)
        universe = univ_dict['global'].id
    elif univ_dict.has_key(universe):
        univ_dict[universe].add_cell(key)
        universe = univ_dict[universe].id
    else:
        univ_dict.update({universe:Universe()})
        univ_dict[universe].add_cell(key)
        universe = univ_dict[universe].id

    # Add the cell
    cell_dict.update({key:Cell(surfaces, universe, fill, material, comment)})

def add_lattice(key, dimension, lower_left, width, universes, comment=None):
    lat_dict.update({key:Lattice(dimension, lower_left, width, universes, comment)})
