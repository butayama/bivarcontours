"""Tests for bivarcontours.py.
Run all tests with:
(bivarcontours-py3.12) uwe@hpi5-p8:~/PycharmProjects/bivarcontourss$ python -m pytest -v
Python files in bivarcontours/tests/
are found without needing to attempt relative import.
"""

from bivarcontours.bivarcontours import cplot, calculate_z, unit_validation, Contour, UnitError
from click.testing import CliRunner
import pytest
from pint import UndefinedUnitError, DimensionalityError


def test_bivarcontours():
    runner = CliRunner()
    result = runner.invoke(cplot, ["Test_Rechteck_Flaeche", "a", "b", "x * y", "m**2", "0.1", "2",
                                   "0.2", "m", "0.2", "3", "0.3", "m", "false", "-v", "true"])
    assert result.exit_code == 0


def test_calculate_z():
    assert calculate_z('x + y', 5, 7, '') == 12
    with pytest.raises(ZeroDivisionError):
        calculate_z('x / y', 5, 0, '')


def test_unit_validation():
    unit_validation(['pound', 'inch'])
    with pytest.raises(UnitError):
        unit_validation(['bogus1', 'bogus2'])


def test_contour_init():
    # Test valid instance
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')
    assert isinstance(contour, Contour)

    # Test invalid dimensions
    with pytest.raises(UnitError):
        contour = Contour('title', 'label_1', 'label_2', 'x + y', 'bogus_dim',
                          1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')


def test_contour_formula_dimensionality_dim_1_dim_2():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'inch',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'mile', 'false')
    with pytest.raises(DimensionalityError):
        contour.initialize_values()


def test_contour_formula_dimensionality_dim_res():
    contour = Contour('title', 'label_1', 'label_2', 'x + y', 'day',
                      1, 2, 0.1, 'week', 3, 4, 0.2, 'm', 'false')
    with pytest.raises(DimensionalityError):
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
