import operator

from src.inflationhelpers import InflationHelpers
from functools import reduce

import numpy as np


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def normalize_returns(nominal_returns, inflation_rate):
    return ((1 + nominal_returns) / (1 + inflation_rate)) - 1


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
cpi_values = np.array([210.036, 210.228, 215.949, 219.179, 225.672, 229.601, 233.049])
nominal_returns = np.array([-37.31, 28.34, 16.93, 1.03, 16.42, 33.55])

inflation_rates = np.array([])
for i in range(1, cpi_values.shape[0]):
    inflation_rates = np.append(inflation_rates, InflationHelpers.get_inflation(cpi_values[i - 1], cpi_values[i]))

print(inflation_rates)
# b. Calculate the real returns of the portfolio for years 2008 – 2013.
real_returns = np.array([])
for (nominal_return, inflation_rate) in zip(nominal_returns, inflation_rates):
    real_returns = np.append(real_returns, normalize_returns(nominal_return, inflation_rate))

print(real_returns)



# Q6:
# 6. Linking, averaging, and annualizing returns
# For the nominal portfolio returns in problem 5, calculate, over the full period:
# a. the cumulative return;
print(prod(map(lambda _real_return: _real_return, real_returns)))
cumulative_returns = np.float_power(
    prod(map(lambda _real_return: 1 + _real_return / 100.0, real_returns)),
    1.0 / real_returns.shape[0]) - 1

print(cumulative_returns)

# b. the arithmetic mean rate of return;
arithmetic_returns = sum(map(lambda _real_return: _real_return, real_returns)) / real_returns.shape[0]
print(arithmetic_returns)

# c. the geometric mean rate of return;
## Isn't that the same question as a?

# d. the geometric mean rate of return based on the approximation involving the arithmetic mean
# and the standard deviation.

s = np.std(list(map(lambda r: r / 100.0, real_returns)))
approximated_geometric_returns = arithmetic_returns - 1.0 / 2 * s * s

print(approximated_geometric_returns)
