from sympy import symbols, sympify
from pint import UnitRegistry
"""
Now Sympy will be used to handle the mathematical operations and Pint for handling the units. Our function 
y*x / (y+x) is first parsed by sympy and then the values x_val and y_val (which are pint quantities), are substituted 
into the equation manually using the Python function exec().
This will now yield the correct result with the correct unit.
Please keep in mind that exec should be used with caution, as it executes the code which can be harmful if the code is 
malicious. In above case, it's used safely as the formula it has to execute is defined by the user.
"""
ureg = UnitRegistry()
x, y = symbols('x y')

# Define the values with units
x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

# Pass the function as a string
function_string = 'y*x / (y+x)'

# Use sympify to convert the string into a sympy expression
f = sympify(function_string)

# Compute the result unit
unit_expr = str(f).replace('y', 'y_val').replace('x', 'x_val')
unit_result = eval(unit_expr)

print('Unit of result:', unit_result.units)