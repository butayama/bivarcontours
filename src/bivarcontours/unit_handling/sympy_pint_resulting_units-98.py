from sympy import symbols, sympify
from pint import UnitRegistry

ureg = UnitRegistry()
x, y = symbols('x y')

# Pass the function as a string
function_string = 'x*y*y'

# Use sympify to convert the string into a sympy expression
f = sympify(function_string)

x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

# Symbolic calculation
symbolic_result = f.subs({x:2, y:3})

# Unit calculation
unit_result = x_val.units * y_val.units * y_val.units

print(f'Symbolic result: {symbolic_result}')
print(f'Unit of result: {unit_result}')