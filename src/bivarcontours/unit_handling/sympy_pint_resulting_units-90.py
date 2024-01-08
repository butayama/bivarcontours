"""
Here, in the expression, the y and x have same units (meters). Hence operation between them like 'y+x' would not
change the unit (still remains meter).
So, the final unit would be meter * meter * meter / meter = meter ** 2.
This approach assumes that the operations in the formula are commensurate with good metrology practice
and the step of division with ureg.meter, is done considering that the sum operation in the denominator does not
change the original unit (i.e., meter). I hope above code helps to resolve your query. Please modify this example
to fit your exact calculations and units.
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
X, Y = np.meshgrid(x_values.magnitude, y_values.magnitude)

# Evaluation of the function
result_expr = "Y*X / (Y+X)"
result = ne.evaluate(result_expr)

# Compute the expected unit as per the dimensions of variables in the expression
unit = y_values.units * x_values.units * x_values.units / ureg.meter

print("Numerical result: ", result)
print("Units of result: ", unit)