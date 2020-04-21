import operator

from src.inflationhelpers import InflationHelpers
from functools import reduce

import numpy as np


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def normalize_returns(_nominal_returns_percentage, _inflation_rate_percentage):
    return ((1 + _nominal_returns_percentage) / (1 + _inflation_rate_percentage)) - 1


# Q5
# A portfolio had returns for calendar years as shown:
# Year  Portfolio return       CPI value
# 2007                          210.036
# 2008      –37.31              210.228
# 2009      28.34               215.949
# 2010      16.93               219.179
# 2011      1.03                225.672
# 2012      16.42               229.601
# 2013      33.55               233.049

# a. Calculate the rates of inflation for years 2008 – 2013.
print('Q5')
years = np.array([2008, 2009, 2010, 2011, 2012, 2013])
cpi_values = np.array([210.036, 210.228, 215.949, 219.179, 225.672, 229.601, 233.049])
nominal_returns = np.array([-37.31, 28.34, 16.93, 1.03, 16.42, 33.55])

inflation_rates = np.array([])
for i in range(1, cpi_values.shape[0]):
    inflation_rates = np.append(inflation_rates, InflationHelpers.get_inflation(cpi_values[i - 1], cpi_values[i]))

print('(a)')
print(f'Year  Inflation Rate')
for (year, inflation_rate) in zip(years, inflation_rates):
    print(f'{year}      {round(inflation_rate, 2)}')

print()

# b. Calculate the real returns of the portfolio for years 2008 – 2013.
real_returns = np.array([])
for (nominal_return, inflation_rate) in zip(nominal_returns, inflation_rates):
    real_returns = np.append(real_returns, normalize_returns(nominal_return / 100, inflation_rate / 100))

print('(b)')
print(f'Nominal Returns     Real Returns')
for (nominal_return, real_return) in zip(nominal_returns, real_returns):
    print(f'    {nominal_return}            {round(real_return, 2)}')

# Q6:
# 6. Linking, averaging, and annualizing returns
# For the nominal portfolio returns in problem 5, calculate, over the full period:
# a. the cumulative return;
print('Q6')
print('(a)')
cumulative_return = prod(map(lambda _nominal_return: 1 + _nominal_return / 100.0, nominal_returns)) - 1
print(f'Cumulative Return: {cumulative_return}')

# b. the arithmetic mean rate of return;
arithmetic_return = sum(map(lambda _nominal_return: _nominal_return, nominal_returns)) / nominal_returns.shape[0]
print('(b)')
print(f'Arithmetic Mean Rate Of Return: {arithmetic_return}')

# c. the geometric mean rate of return;
print('(c)')
geometric_return = (np.float_power(
    prod(map(lambda _nominal_return: 1 + _nominal_return / 100.0, nominal_returns)),
    1.0 / nominal_returns.shape[0]) - 1) * 100
print(f'Geometric Mean Rate Of Return: {geometric_return}')

# d. the geometric mean rate of return based on the approximation involving the arithmetic mean
# and the standard deviation.
print('(d)')
s2 = 1 / (nominal_returns.shape[0] - 1) * sum(map(lambda r: (r / 100 - arithmetic_return / 100) ** 2, nominal_returns))
approximated_geometric_return = (arithmetic_return / 100 - (1.0 / 2) * s2) * 100
print(f'Approximated Geometric Mean Rate Of Return: {approximated_geometric_return}')
