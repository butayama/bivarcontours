import pytest
from bivarcontours.unit_handling.map_base_units import (pint_to_sympy_unit, sympy_to_pint_quantity,
                                                        unit_mapping_pint_sympy, create_sympy_quantity)

pytestmark = pytest.mark.unit


def test_map_units():
    for pint_unit, sympy_unit in unit_mapping_pint_sympy.items():
        # Create some random non-zero values for testing
        value = 5

        pint_quantity = pint_unit * value
        sympy_result_unit = pint_to_sympy_unit(value, pint_unit)
        assert sympy_result_unit == sympy_unit

        sympy_quantity_expected = value * sympy_unit
        sympy_quantity_1 = create_sympy_quantity(value, sympy_result_unit)
        assert sympy_quantity_1 == sympy_quantity_expected, (f"Expected {sympy_quantity_expected} "
                                                             f"but got {sympy_quantity_1}")

        sympy_quantity_2 = value * sympy_unit
        pint_quantity_1 = sympy_to_pint_quantity(sympy_quantity_2)
        assert pint_quantity_1 == pint_quantity

    print("All unit conversions are working correctly.")
