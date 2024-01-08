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
            r_dim = left_dim + right_dim
        elif isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
            # ensuring dimensions match for addition and subtraction
            r_dim = left_dim if left_dim == right_dim else 'Error'
        elif isinstance(node.op, ast.Div):
            # bringing dimensions back to normal after division
            r_dim = left_dim.replace(right_dim, '') if left_dim == right_dim + right_dim else 'Error'
        else:
            print(f"Error: Node {node} operation type is not handled.")
        return r_dim
    else:
        print(f"Skipping node type {type(node)} during post_order() traversal.")
    return ''


formula = "x * y / (x + y)"
ast_tree = ast.parse(formula)
r_dim = post_order(ast_tree.body[0].value)
print(f"r_dim = {r_dim if r_dim else 'None'}")