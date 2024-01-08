import pytest
from sympy import simplify, sympify
from bivarcontours.unit_handling.formula_ast_dim import post_order

DIMENSIONS = {'x': 'm', 'y': 's'}
FORMULAS = ["x + y", "x - y", "x * y", "x / y", "x**2", "(x + y) / y", "(x + y) + y"]

@pytest.mark.parametrize("formula, expected", [
    ("x + y", 'Dimension Mismatch'),
    ("x - y", 'Dimension Mismatch'),
    ("x * y", 'm*s'),
    ("x / y", 'm/s'),
    ("x**2", 'Unhandled Operator'),
    ("(x + y) / y", 'Dimension Mismatch'),
    ("(x + y) + y", 'Dimension Mismatch'),
    ])
def test_post_order(formula, expected):
    r_dim = post_order(formula)
    assert r_dim == expected, f"For formula: {formula}, expected: {expected}, but got: {r_dim}"

def test_simplify_equivalent_formulas():
    for formula in FORMULAS:
        r_dim1 = post_order(formula)
        r_dim2 = post_order(str(simplify(sympify(formula))))
        assert r_dim1 == r_dim2, f"{formula} != {str(simplify(sympify(formula)))} but they should be equivalent"

if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])