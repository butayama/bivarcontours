from pint import UnitRegistry
from sympy.physics.units import (ampere, candela, kelvin, kilogram, meter, mole, radian, second)
from sympy.physics.units import Quantity
from sympy import sympify

# Define the pint unit registry
ureg = UnitRegistry()
Q_ = ureg.Quantity

# Define a dictionary mapping pint units to sympy units
unit_mapping_pint_sympy = {
    ureg.meter: meter,  # length
    ureg.second: second,  # time
    ureg.ampere: ampere,  # current
    ureg.candela: candela,  # luminosity
    ureg.gram: kilogram / 1000,  # mass
    ureg.mole: mole,  # substance
    ureg.kelvin: kelvin,  # temperature
    ureg.radian: radian,  # angle
    # add any additional units as needed
}

# Define a dictionary mapping sympy units to pint units
sympy_to_pint_mapping = {
    meter: ureg.meter,  # length
    second: ureg.second,  # time
    ampere: ureg.ampere,  # current
    candela: ureg.candela,  # luminosity
    kilogram: ureg.gram * 1000,  # mass
    mole: ureg.mole,  # substance
    kelvin: ureg.kelvin,  # temperature
    radian: ureg.radian  # angle
    # add additional units as required
}


def pint_to_sympy_quantity(value, unit):
    # Convert the pint quantity to a sympy quantity
    pint_quantity = Q_(f'{value} {unit}')
    sympy_unit = unit_mapping_pint_sympy[pint_quantity.units]
    sympy_quantity = pint_quantity.magnitude * sympy_unit
    return sympy_quantity


def sympy_to_pint_quantity(sympy_quantity):
    # use .args to extract the value and units in sympy
    # assuming the format is in the form of (value, unit)
    value, sympy_unit = sympy_quantity.args

    # Map the sympy unit with pint unit
    pint_unit = sympy_to_pint_mapping[sympy_unit]

    # Return pint quantity
    pint_quantity = Q_(f'{value} {pint_unit}')
    return pint_quantity


if __name__ == '__main__':
    value = 5  # example value
    unit = 'meter'  # example unit

    print("Convert Pint to Sympy Quantity")
    # With a pint quantity
    pint_quantity = Q_(f'{value} {unit}')

    # Get the unit from pint_quantity
    pint_unit = pint_quantity.units

    # Map the pint unit to the sympy unit
    sympy_unit = pint_to_sympy_quantity(value, pint_unit)

    # Create a sympy quantity
    sympy_quantity = pint_quantity.magnitude

    print(f"pint_quantity = {pint_quantity}, pint_unit = {pint_unit}, sympy_unit = {sympy_unit}, "
          f" sympy_quantity = {sympy_quantity}")

    print("Convert Sympy to Pint Quantity")

    # Create a SymPy quantity
    sympy_quantity = sympy_unit

    # Convert to Pint Quantity
    pint_quantity = sympy_to_pint_quantity(sympy_quantity)

    print(f"sympy_quantity = {sympy_quantity}, pint_unit = {pint_unit}, pint_quantity = {pint_quantity}")
