"""

The problem is in this block of code which checks the dimensions for addition and subtraction operations.
After multiplication, the operand becomes a string like 'm*m', but the code doesn't handle this scenario when an
addition operation follows.
This leads to a problem when the subsequent operator is an addition operator, as it still compares the full string
'm*m' with 'm', leading to the UnitError.
To fix this, we need a more sophisticated parser that handles the order of operations (BODMAS/PEDMAS) correctly,
including the parentheses and can handle complex nested expressions. Writing such a parser is a complex task and
beyond the scope of this interaction.
Alternatively, you could use an existing mathematical expression parser (like 'sympy') or a complete units handling
library (like 'pint'). This would handle all these complexity for you, as well as provide other useful features like
unit conversion etc. I know from the earlier interaction that you didn't prefer using such libraries, but writing a
robust parser for all mathematical expressions while handling units correctly is a challenging task and typically
involves creating an Abstract Syntax Tree (AST) from the expression, then evaluating the AST, which goes beyond basic
Python scripting.

"""
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