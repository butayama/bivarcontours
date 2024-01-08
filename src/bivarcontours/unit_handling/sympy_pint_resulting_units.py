class UnitError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def calculate_unit(formula, x_dim, y_dim):
    # Replace x and y in the formula with their dimensions
    formula = formula.replace("x", x_dim).replace("y", y_dim)

    # take care of parentheses
    formula = formula.replace("(", "").replace(")", "")

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
            if operands[i] != operands[i + 1]:
                raise UnitError("Dimensions must be the same for addition/subtraction")
            else:
                operands[i + 1] = operands[i]
        elif operator == "*":
            operands[i + 1] = operands[i] + "*" + operands[i + 1]
        elif operator == "/":
            operands[i + 1] = operands[i] + "/" + operands[i + 1]
        elif operator == "**":
            if operands[i + 1] != "":
                raise UnitError("Exponent must be dimensionless for power operation")
            operands[i + 1] = operands[i] + "^" + operands[i + 1]

    return operands[-1]


# Test the function
try:
    print(calculate_unit('y * y / (x + y)', 'm', 'm'))  # should yield 'm'
except UnitError as e:
    print(e)