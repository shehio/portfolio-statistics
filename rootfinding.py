import sympy


r = sympy.symbols('r', real=True, positive=True)
equation = sympy.Eq(
    120.2075,
    100 * (1 + r) + 100 * ((1 + r) ** 8/21))
output_r = sympy.solve(equation)
print(f'r = {output_r}')

equation = sympy.Eq(
    926388.5303777423,
    1000_1000 * (1 - r))  # Should this be initial balance?
print(sympy.solve(equation))
