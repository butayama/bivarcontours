"""Tests for bivarcontours.py.
Run all tests with:
(bivarcontours-py3.12) uwe@hpi5-p8:~/PycharmProjects/bivarcontourss$ python -m pytest -v
Python files in bivarcontours/tests/
are found without needing to attempt relative import.
"""
import pytest
from bivarcontours.bivarcontours import (cplot, calculate_z, calculate_formula_dimension, unit_validation, Contour,
                                         _is_valid_filename, _sanitize_filename)
from click.testing import CliRunner
from pint import DimensionalityError
from sympy import symbols, sympify
import sympy.physics.units as sympy_units
from result_unit.result_unit import formula_result_unit, UnitError
from result_unit.map_base_units import UnitQuantity, UREG, sympy_to_pint_quantity
SIBASE = sympy_units.UnitSystem.get_unit_system("SI")._base_units
from unittest.mock import MagicMock, patch


@pytest.mark.parametrize("filename,expected",
    [
        ("validfilename.png", True),
        ("invalid/filename.png", False),
        ("valid_filename.png", True),
        ("/invalid_filename.png", False),
        ("file/name.png", False),
        ("file@name.png", False),
        ("file name.png", False),
        ("/invalid/name/", False),
        ("^validfil?e'name.png", False),
        ("invalid/filename.png", False),
        ("/invalid[x]filename<y>.png", False),
        ("filename_with_special_chars@.png", False),
        ("filename_with_special_chars*.png", False),
    ]
)
def test_is_valid_filename(filename, expected):
    assert _is_valid_filename(filename) == expected


@pytest.mark.parametrize("filename,expected_output",
    [
        ("file/name.png", "file_name.png"),
        ("file@name.png", "file_name.png"),
        ("file name.png", "file_name.png"),
        ("/invalid/name/", "_invalid_name_"),
        ("^validfil?e'name.png", "_validfil_e_name.png"),
        ("invalid/filename.png", "invalid_filename.png"),
        ("/invalid[x]filename<y>.png", "_invalid_x_filename_y_.png"),
        ("filename_with_special_chars@.png", "filename_with_special_chars_.png"),
        ("filename_with_special_chars*.png", "filename_with_special_chars_.png"),
    ]
)
def test_sanitize_filename(filename,expected_output):
        assert _sanitize_filename(filename) == expected_output


def test_bivarcontours():
    runner = CliRunner()
    result = runner.invoke(cplot, ["Test_Rechteck_Flaeche", "a", "b", "x * y", "m**2", "0.1", "2",
                                   "0.2", "m", "0.2", "3", "0.3", "m", "false", "-v", "true"])
    assert result.exit_code == 0


@pytest.mark.parametrize('x_quant, y_quant, formula, expected_dim', [
    (3 * UREG.meter, 4 * UREG.meter, 'x + y', UREG.meter),  # unit of addition result is meter
    (3 * UREG.meter, 2 * UREG.second, 'x * y', UREG.meter * UREG.second),
    # unit of multiplication result is meter*second
    (10 * UREG.second, 2 * UREG.second, 'x / y', UREG.dimensionless),  # unit of division result is dimensionless
    (5 * UREG.meter, 2 * UREG.meter, 'x * y', UREG.meter ** 2),  # unit of multiplication result is meter**2
])
def test_calculate_formula_dimension(formula, x_quant, y_quant, expected_dim):
    result_dim = calculate_formula_dimension(formula, x_quant, y_quant, expected_dim)
    assert result_dim == expected_dim


def test_calculate_z():
    assert calculate_z('x + y', 5, 7, '') == 12
    with raises(ZeroDivisionError):
        calculate_z('x / y', 5, 0, '')


def test_unit_validation():
    unit_validation(['pound', 'inch'])
    with raises(UnitError):
        unit_validation(['bogus1', 'bogus2'])


def test_contour_init():
    # Test valid instance
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')
    assert isinstance(contour, Contour)

    # Test invalid dimensions
    with raises(UnitError):
        contour = Contour('title', 'label_1', 'label_2', 'x + y', 'bogus_dim',
                          1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')


def test_contour_formula_dimensionality_dim_1_dim_2():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')
    with raises(DimensionalityError):
        contour.initialize_values()


def test_contour_formula_dimensionality_dim_res():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'day',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'm', 'false')
    with raises(DimensionalityError):
        contour.initialize_values()


def test_contour_initialize_values():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'm', 3, 4, 0.2, 'mile', 'false')
    contour.initialize_values()
    assert contour.start_1 is not None
    assert contour.start_2 is not None


def test_contour_initialize_dimension_one_values():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'cm', 3, 4, 0.2, 'mile', 'false')
    contour.initialize_dimension_one_values()
    assert contour.start_1 is not None


def test_contour_initialize_dimension_two_values():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'hour',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'minutes', 'false')
    contour.initialize_dimension_two_values()
    assert contour.start_2 is not None


def test_contour_methods_swap_axes_false():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'mm', 3, 4, 0.2, 'mile', 'false')

    contour.initialize_values()
    assert contour.start_1 is not None
    assert contour.start_2 is not None

    contour.initialize_dimension_one_values()
    assert contour.start_1 is not None

    contour.initialize_dimension_two_values()
    assert contour.start_2 is not None

    contour.initialize_diagram_labels()
    assert contour.label_x is not None
    assert contour.label_y is not None

    contour.set_values_for_contour_calc_with_scalars_scaled_to_base_units()
    assert contour.x_values is not None
    assert contour.y_values is not None

    contour.filename_for_saved_contour_figure()
    assert contour.filename is not None

    contour.x_values = [1, 2, 3]
    contour.y_values = [1, 2, 3]
    contour.compute_values()
    assert contour.vals is not None
    assert contour.hl is not None

# def test_contour_methods_swap_axes_true():
#     contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
#                       1, 2, 0.1, 'mm', 3, 4, 0.2, 'mile', 'true')
