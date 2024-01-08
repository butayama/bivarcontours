from pint import UnitRegistry
ureg = UnitRegistry()

def f(x, y):
    return x * y * y

x_val = 2 * ureg.meter
y_val = 3 * ureg.meter

result = f(x_val, y_val)

print(result)
print(result.units)