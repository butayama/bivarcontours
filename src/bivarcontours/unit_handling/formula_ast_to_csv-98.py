import ast
import csv

# Global variable for node count
node_counter = 0

def visit_node(node, tree_data, type_parent=''):
    global node_counter
    node_counter += 1
    node_id = node_counter

    # Collect type and attributes of current node
    tree_data.append({
        'id': node_id,
        'type': type(node).__name__,
        'parent': type_parent,
        **node.__dict__
    })

    # Iterate over children of current node
    for child_node in ast.iter_child_nodes(node):
        visit_node(child_node, tree_data, node_id)

    return tree_data


def post_order(formula):
    ast_tree = ast.parse(formula)
    tree_data = []
    visit_node(ast_tree, tree_data)
    return tree_data


def ast_data_table(tree_data):
    # write to csv
    with open('../../../csv/ast_data.csv', 'w', newline='') as csvfile:
        # get all unique keys
        fieldnames = set(k for d in tree_data for k in d.keys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in tree_data:
            writer.writerow(row)

if __name__ == '__main__':
    # the invocation of the function with formula
    tree_info = post_order("x * y / (x + y)")
    ast_data_table(tree_info)