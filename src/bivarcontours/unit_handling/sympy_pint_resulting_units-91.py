"""
In the above code, numexpr.evaluate operation is performed elementwise (like numpy does) on the entire arrays.
It offers faster array operation computation by making better use of memory caches and the CPU's instruction pipeline.
The resulting unit is calculated based on the fact that the unit of the final result for the function y*x*x / (y+x)
would be meter * meter * meter / (meter + meter) -> meter^2.
Please modify this example to fit your exact calculations and units.
"""
import numpy as np
import numexpr as ne
from pint import UnitRegistry

# Create the unit registry
ureg = UnitRegistry()

# Define the range of x values and y values
x_values = np.array([2] * 5) * ureg.meter
y_values = np.array([3] * 5) * ureg.meter

# x and y axes values meshgrid
X, Y = np.meshgrid(x_values, y_values)
x = X.magnitude
y = Y.magnitude

function_string = 'y*x*x / (y+x)'

# Evaluate the function using numexpr
result = ne.evaluate(function_string)

# Compute the resulting unit
unit = x_values.units * x_values.units * y_values.units / (y_values.units + x_values.units)

print("Numerical result: ", result)
print("Units of result: ", unit)