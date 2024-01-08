from sympy import symbols, sympify
from pint import UnitRegistry
import re

ureg = UnitRegistry()
x, y = symbols('x y')

# Pass the function as a string
function_string = 'y*x / (y+x)'

# Use sympify to convert the string into a sympy expression
f = sympify(function_string)

x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

# Symbolic calculation
symbolic_result = f.subs({x:2, y:3})

# Split the function string into variables and operators
elements = re.split(r'(\W+)', function_string)

# Initial unit result is 1
unit_result = 1 * ureg.dimensionless

# Iterate over elements in the function string
for element in elements:
    if element == 'x':
        unit_result *= x_val.units
    elif element == 'y':
        unit_result *= y_val.units
    elif element == '/':
        unit_result /= ureg.dimensionless

print(f'Symbolic result: {symbolic_result}')
print(f'Unit of result: {unit_result}')