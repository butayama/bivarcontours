from sympy import symbols, sympify
from pint import UnitRegistry

ureg = UnitRegistry()
x, y = symbols('x y')

x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

# Pass the function as a string
function_string = 'y*x / (y+x)'

# Use sympify to convert the string into a sympy expression
f = sympify(function_string)

# Substitute symbols with pint quantities
f_pint_variable = f.subs({x:x_val, y:y_val})

# Symbolic calculation
unit_result = f_pint_variable

print(f'Unit of result: {unit_result}')