"""
In this code, X_qty and Y_qty are pint Quantity objects that hold the actual values along with their units.
I have replaced 'x' and 'y' in the function_string respectively with X_qty and Y_qty. Because we are now working with
pint quantities directly, pint will handle the unit computations for us.
And with this setup, NumPy’s broadcasting rules will let us calculate the result for all grid locations at once.
Keep in mind that eval is not safe to use in all cases, as it interprets a string as code. Ensure the string being
interpreted does not contain harmful commands.
Please adjust the range and number of x and y values according to your needs.
"""

import numpy as np
from pint import UnitRegistry

ureg = UnitRegistry()

# Define the range of x values and y values
x_values = np.linspace(1, 10, 10)
y_values = np.linspace(1, 15, 15)

# x and y axes values meshgrid
X, Y = np.meshgrid(x_values, y_values)

# Convert X, Y to pint Quantities
X_qty = X * ureg.meter
Y_qty = Y * ureg.meter

# Pass the function as a string
function_string = 'y*x*x / (y+x)'

# Replace y and x in function string with respective pint Quantities
function_string = function_string.replace('y', 'Y_qty').replace('x', 'X_qty')

# Calculate the result for each x, y pair
result_values = eval(function_string)

print(f'Units of result: {result_values.units}')