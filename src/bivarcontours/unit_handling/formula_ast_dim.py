"""
formula_ast_dim.py
Abstract Syntax Tree code with stack based post order traversal method.
Rules to be followed:
    formula1 = "x + y"  # unit: m + m = m
        formula1.1 = "x + y"  # unit: m + s = ERROR
    formula2 = "x - y"  # unit: m - m = m
        formula1.1 = "x - y"  # unit: m + s = ERROR
    formula3 = "x * y"  # unit: m * s = ms
    formula4 = "x / y"  # unit: m / s = m/s
    formula5 = "x**2"   # unit: m^2
    formula6 = "(x + y) / y"  # unit: (m + s) / s = dimensionless
These rules must be interpreted along with the correct mathematical order of operations (BIDMAS/BODMAS/PEDMAS).
"""

import ast

DIMENSIONS = {'x': 'm', 'y': 's'}

def post_order(formula):
    print(f"Post order traversing starts here")
    ast_tree = ast.parse(formula)
    stack = [(False, ast_tree.body[0].value)]
    out = []

    while stack:
        visit, node = stack.pop()
        if isinstance(node, ast.Name):
            dim = DIMENSIONS.get(node.id, None)
            out.append(dim)
        elif isinstance(node, ast.BinOp):
            if visit:
                right_dim = out.pop()
                left_dim = out.pop()
                if isinstance(node.op, ast.Mult):
                    result_dim = left_dim + '*' + right_dim
                elif isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
                    result_dim = left_dim if left_dim == right_dim else 'Dimension Mismatch'
                elif isinstance(node.op, ast.Div):
                    result_dim = left_dim + '/' + right_dim if left_dim != right_dim else ''
                else:
                    result_dim = 'Unhandled Operator'
                out.append(result_dim)
            else:
                stack.extend([(True, node), (False, node.right), (False, node.left)])
        else:
            print(f"Skipping node type {type(node)} during post_order() traversal.")

    return out[0]


def main(formula):
    r_dim = post_order(formula)
    print(f"r_dim = {r_dim if r_dim else 'None'}")

if __name__ == '__main__':
    main("x / (x - y)")