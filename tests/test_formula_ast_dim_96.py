import pytest
import ast
from bivarcontours.unit_handling.formula_ast_dim_96 import post_order

pytestmark = pytest.mark.unit

DIMENSIONS = {'x': 'm', 'y': 'm'}


def test_post_order():
    formula1 = "x * y / (x + y)"
    ast_tree1 = ast.parse(formula1)
    r_dim1 = post_order(ast_tree1.body[0].value)
    assert r_dim1 == 'm'

    formula2 = "x  / (x - y)"
    ast_tree2 = ast.parse(formula2)
    r_dim2 = post_order(ast_tree2.body[0].value)
    assert r_dim2 == ''

    formula3 = "x - y"
    ast_tree3 = ast.parse(formula3)
    r_dim3 = post_order(ast_tree3.body[0].value)
    assert r_dim3 == 'm'

    formula4 = "x * y"
    ast_tree4 = ast.parse(formula4)
    r_dim4 = post_order(ast_tree4.body[0].value)
    assert r_dim4 == 'mm'


if __name__ == "__main__":
    pytest.main([__file__])