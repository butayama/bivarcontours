import ast

DIMENSIONS = {'x': 'm', 'y': 'm'}


def post_order(node):
    print(f"Visiting node: {node}")
    if isinstance(node, ast.Name):
        dim = DIMENSIONS.get(node.id, None)
        if dim is None:
            print(f"Error: Node {node.id} has no dimension in our DIMENSIONS.")
        return dim
    elif isinstance(node, ast.BinOp):
        print(f"Visiting BinOp node: {node}")
        left_dim = post_order(node.left)
        right_dim = post_order(node.right)
        if isinstance(node.op, ast.Mult):
            return left_dim + right_dim
        elif isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
            # ensuring dimensions match for addition and subtraction
            return left_dim if left_dim == right_dim else 'Error'
        elif isinstance(node.op, ast.Div):
            if left_dim == right_dim:
                return ''  # Division of similar units cancel each other out.
            elif left_dim.startswith(right_dim):
                r_dim = left_dim.replace(right_dim, '', 1)
                return r_dim
            else:
                print(f"Error: Node {node} division operation not handled.")
                return 'Error'
        else:
            print(f"Error: Node {node} operation type is not handled.")
            return 'Error'
    else:
        print(f"Skipping node type {type(node)} during post_order() traversal.")
    return ''


def main(formula):
    ast_tree = ast.parse(formula)
    # r_dim = post_order(ast_tree.body[0].value)
    r_dim = post_order(ast_tree.body[0])
    print(f"r_dim = {r_dim if r_dim else 'None'}")




if __name__ == '__main__':
    main("x  / (x - y)")