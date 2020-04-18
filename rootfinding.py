import sympy


r = sympy.symbols('r', real=True, positive=True)
equation = sympy.Eq(
    120.2075,
    100 * (1 + r) + 100 * ((1 + r) ** 8/21))
output_r = sympy.solve(equation)
print(f'r = {output_r}')

