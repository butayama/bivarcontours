from pint import UnitRegistry
from sympy import Float, Integer
from sympy.physics.units import meter, second, ampere, candela, kilogram, mole, kelvin, radian
UREG = UnitRegistry()
UnitQuantity = UREG.Quantity

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
    if str(pint_quantity.units) == 'dimensionless':
        return 1
    else:
        sympy_unit = unit_mapping_pint_sympy[pint_quantity.units]
    return sympy_unit


def create_sympy_quantity(magnitude, unit):
    return magnitude * unit


def sympy_to_pint_quantity(sympy_quantity):
    print(type(sympy_quantity))
    if isinstance(sympy_quantity, (int, float, Float, Integer)):  # handle primitive types
        return create_pint_quantity(sympy_quantity, 'dimensionless')

    value, sympy_unit = sympy_quantity.args

    # Check if sympy_unit is a string representation of a sympy physical unit
    sympy_units = [meter, second, ampere, candela, kilogram, mole, kelvin, radian]
    if str(sympy_unit) in map(str, sympy_units):
        sympy_unit = [unit for unit in sympy_units if str(unit) == str(sympy_unit)][0]

    # Attempt to get the pint unit
    try:
        pint_unit = sympy_to_pint_mapping[sympy_unit]
    except KeyError:
        raise KeyError(f"{sympy_unit} is not a key in the sympy_to_pint_mapping dictionary.")
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
