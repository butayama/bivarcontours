"""
Please note, this is a simplistic handling which takes care of basic expressions without parentheses. Also, actual
checking of whether the dimensions can be added/subtracted (for example, meter and second can't be added/subtracted to
yield a meaningful physical quantity) is not covered in this code. Python doesn't understand physical dimensions,
that's why unit libraries like 'pint' exist.
This code only checks for text equality, i.e., it will consider 'meter' and 'm' to be different, although they are the
same unit. An actual unit library will have these edge cases covered in much more detail.
"""
def calculate_unit(formula, x_dim, y_dim):
    # Replace x and y in the formula with their dimensions
    formula = formula.replace("x", x_dim).replace("y", y_dim)

    # Split the formula by operation
    operations = set(["+", "-", "*", "/", "**"])
    operators = []
    operands = []
    current_operand = ""

    # Parse the formula
    for char in formula:
        if char in operations:
            operators.append(char)
            operands.append(current_operand.strip())
            current_operand = ""
        else:
            current_operand += char

    operands.append(current_operand.strip())  # Add the last operand

    # Calculate the resulting dimension
    for i, operator in enumerate(operators):
        if operator in ["+", "-"]:
            assert operands[i] == operands[i + 1], "Dimensions must be the same for addition/subtraction"
        elif operator == "*":
            operands[i + 1] = operands[i] + "*" + operands[i + 1]
        elif operator == "/":
            operands[i + 1] = operands[i] + "/" + operands[i + 1]
        elif operator == "**":
            assert operands[i + 1] == "", "Exponent must be dimensionless for power operation"
            operands[i + 1] = operands[i] + "^" + operands[i + 1]

    return operands[-1]


# Test the function
print(calculate_unit('y * y / (x + y)', 'm', 's'))