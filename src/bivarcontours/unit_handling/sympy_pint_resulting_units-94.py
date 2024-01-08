import numpy as np
from pint import UnitRegistry
from sympy import symbols, lambdify, sympify

ureg = UnitRegistry()

# Pass the function as a string
function_string = 'y*x / (y+x)'

# Use sympify to convert the string into a sympy expression
f_sympy = sympify(function_string)

# Create lambda function for vectorized operations
f = lambdify((symbols('y'), symbols('x')), f_sympy, 'numpy')

# Define the range of x and y values
x_values = np.linspace(1, 10, 10) * ureg.meter
y_values = np.linspace(1, 15, 15) * ureg.meter

# x and y axes values meshgrid
X, Y = np.meshgrid(x_values.m, y_values.m)

# Calculate the result for each x, y pair
result_values = f(Y, X) * ureg.meter

print(f'Units of result: {result_values.units}')