"""
The numexpr library makes it possible to perform faster numerical computations, but it doesn't natively support units.
Anyway, we could first evaluate the function symbolically with the units, and then pass the resulting unit as a string
to numexpr for numerical evaluation.
"""
import numpy as np
from pint import UnitRegistry
from numexpr import evaluate
from sympy import symbols, lambdify, sympify

# Create the unit registry (used to add units to your array data)
ureg = UnitRegistry()

# Define the range of x values and y values
x_values = np.linspace(1, 10, 10) * ureg.meter
y_values = np.linspace(1, 15, 15) * ureg.meter

# Create x and y symbols
x, y = symbols('x y')

# Define the function as a symbolic expression
expr = sympify("y*x*x / (y+x)")

# Replace symbols with actual physical quantities
simplified_expr = expr.subs({x: x_values.units, y: y_values.units})

# Convert sympy expression to string
equation = str(simplified_expr)

# Create a dictionary with actual numerical values for x and y
local_dict = {"x" : x_values.magnitude, "y" : y_values.magnitude}

# Evaluate the expression using numexpr library with defined dictionary for x and y values
result_values = evaluate(equation, local_dict=local_dict)

# Print the unit of result
print(f'Units of result: {simplified_expr.units}')