import ast

formula = "x * y / (x + y)"

# Parse the formula to an AST
tree = ast.parse(formula)

# Print the tree
print(ast.dump(tree))


def to_puml(node, indent=''):
    node_name = node.id if isinstance(node, ast.Name) else type(node).__name__
    result = indent + '* ' + node_name + '\n'
    for child in ast.iter_child_nodes(node):
        result += to_puml(child, indent + '*')
    return result


def tree_to_puml(tree):
    return '@startmindmap\n' + to_puml(tree) + '@endmindmap'


ast_tree = ast.parse(formula)
print(tree_to_puml(ast_tree))
