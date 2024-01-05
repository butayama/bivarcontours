from pint import UnitRegistry
from sympy.physics.units import (ampere, candela, kelvin, kilogram, meter, mole, radian, second)

UREG = UnitRegistry()
unit_mapping_pint_sympy = {
    UREG.meter: meter,  # length
    UREG.second: second,  # time
    UREG.ampere: ampere,  # current
    UREG.candela: candela,  # luminosity
    UREG.gram: kilogram / 1000,  # mass
    UREG.mole: mole,  # substance
    UREG.kelvin: kelvin,  # temperature
    UREG.radian: radian,  # angle
}

sympy_to_pint_mapping = {
    meter: UREG.meter,  # length
    second: UREG.second,  # time
    ampere: UREG.ampere,  # current
    candela: UREG.candela,  # luminosity
    kilogram: UREG.gram * 1000,  # mass
    mole: UREG.mole,  # substance
    kelvin: UREG.kelvin,  # temperature
    radian: UREG.radian  # angle
}


def create_pint_quantity(value, unit):
    return UREG.Quantity(f'{value} {unit}')


def pint_to_sympy_unit(value, pint_unit):
    pint_quantity = create_pint_quantity(value, pint_unit)

    # Ensure you're getting the pint units (not value)
    return unit_mapping_pint_sympy[pint_quantity.units]


def create_sympy_quantity(value, sympy_unit):
    return value * sympy_unit


def sympy_to_pint_quantity(sympy_quantity):
    value, sympy_unit = sympy_quantity.args
    pint_unit = sympy_to_pint_mapping[sympy_unit]
    return create_pint_quantity(value, pint_unit)


if __name__ == '__main__':
    print("Convert Pint to Sympy Quantity")
    value = 5  # example value
    unit = 'meter'  # example unit
    pint_quantity = create_pint_quantity(value, unit)
    pint_unit = pint_quantity.units
    sympy_unit = pint_to_sympy_unit(value, pint_unit)
    sympy_quantity = create_sympy_quantity(pint_quantity.magnitude, sympy_unit)
    print(f"pint_quantity = {pint_quantity}, pint_unit = {pint_unit}, sympy_unit = {sympy_unit}, "
          f" sympy_quantity = {sympy_quantity}")

    print("Convert Sympy to Pint Quantity")
    sympy_quantity = create_sympy_quantity(value, sympy_unit)
    pint_quantity = sympy_to_pint_quantity(sympy_quantity)
    print(f"sympy_quantity = {sympy_quantity}, pint_unit = {pint_unit}, pint_quantity = {pint_quantity}")
