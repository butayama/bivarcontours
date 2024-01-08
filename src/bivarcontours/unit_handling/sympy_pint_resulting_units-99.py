from sympy import symbols
from sympy import Function
from pint import UnitRegistry

ureg = UnitRegistry()
x, y = symbols('x y')

class f(Function):
    @classmethod
    def eval(cls, x, y):
        return x * y * y

x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

# Symbolic calculation
symbolic_result = f(x, y).subs({x: 2, y: 3})

# Unit calculation
unit_result = (x_val.units * y_val.units * y_val.units)

print(f'Symbolic result: {symbolic_result}')
print(f'Unit of result: {unit_result}')