import datetime
from functools import reduce
import operator
import numpy as np

from assignments.assignment6.tbills import get_t_bills_monthly_returns
from assignments.assignment6.russelreturns import get_russel_monthly_returns


def prod(iterable):
    return reduce(operator.mul, iterable, 1)

# The decade of the 2000s has been called the “lost decade” for the U.S. economy (Neil Irwin, “Aughts
# were a lost decade for U.S. economy, workers,” The Washington Post, 2 January 2010). We will take a
# look at the returns from investments in stocks and cash over this decade. You may use either R or a
# spreadsheet to do the following analysis.
#
# For the period from 2000-12-31 to 2010-12-31, form 11 portfolios of the two assets, R3000 and cash
# (proxied by T-bills), using constant weights, ranging from 100% cash/0% equities, to 0% cash/100%
# equities, in ten percent increments in weight. Assume the portfolios are rebalanced monthly to the fixed
# weights (ignore transaction costs). Calculate the monthly returns of the 11 portfolios.
#
# For each of the 11 portfolios, calculate the standard deviation of the returns, the arithmetic mean return,
# the geometric mean return, and the approximate geometric mean return using the equation given in
# Lecture 3.
#
# Plot the results on a graph (or on three graphs, if you wish), with the mean returns – arithmetic
# and geometric – on the vertical axis, and the standard deviation of returns on the horizontal axis.
#
# Comment on the accuracy of the approximate geometric mean return. Would an investment in any of the
# fixed mix strategies have resulted in greater ending wealth than an investment in cash or stocks alone
# over the decade? Write up your analysis in a document and submit.


def get_arithmetic_return(portfolio_returns):
    periods = portfolio_returns.shape[0]
    return sum(map(lambda _return: _return, portfolio_returns)) / periods


def get_geometric_return(portfolio_returns):
    returns_count = len(portfolio_returns)
    returns_product = prod(map(lambda _return: 1 + _return / 100.0, portfolio_returns))
    return 100 * (np.float_power(returns_product, 1.0 / returns_count) - 1)


def get_approximated_geometric_return(portfolio_returns):
    returns_count = len(portfolio_returns)
    arithmetic_return = get_arithmetic_return(portfolio_returns)
    s2 = 1 / (returns_count - 1) * sum(map(lambda r: (r / 100 - arithmetic_return / 100) ** 2, portfolio_returns))
    return 100 * (arithmetic_return / 100 - s2 / 2)


if __name__ == '__main__':
    ratios = np.array([i * 0.1 for i in range(11)])

    t_bills_start_date = datetime.date(2001, 1, 1)
    russel_start_date = datetime.date(2000, 12, 1)
    end_date = datetime.date(2010, 12, 31)

    t_bills_returns = get_t_bills_monthly_returns(t_bills_start_date, end_date)
    russel_monthly_returns = get_russel_monthly_returns(russel_start_date, end_date)

    # print(len(t_bills_returns))
    # print(len(russel_monthly_returns))

    portfolios_returns = list(map(lambda ratio: t_bills_returns * ratio + russel_monthly_returns * (1 - ratio), ratios))

    print(f'Portfolio Returns: {portfolios_returns}')

    arithmetic_returns = \
        list(map(lambda portfolio_returns: get_arithmetic_return(portfolio_returns), portfolios_returns))
    print(f'Arithmetic Returns: {np.round(arithmetic_returns, 2)}')

    geometric_returns = \
        list(map(lambda portfolio_returns: get_geometric_return(portfolio_returns), portfolios_returns))
    print(f'Geometric Returns: {np.round(geometric_returns, 2)}')

    portfolios_returns_real = list(map(lambda portfolio_returns: portfolio_returns / 100, portfolios_returns))
    standard_deviations = \
        list(map(lambda portfolio_returns: np.std(portfolio_returns), portfolios_returns_real))
    print(f'Standard Deviations: {np.round(standard_deviations, 2)}')

    approximated_geometric_returns = \
        list(map(lambda portfolio_returns: get_approximated_geometric_return(portfolio_returns), portfolios_returns))
    print(f'Approximated Geometric Returns: {np.round(approximated_geometric_returns, 2)}')

    import matplotlib.pyplot as plt

    plt.axis([0, 0.05, -0.1, 0.3])
    plt.plot(standard_deviations, arithmetic_returns, label='Arithmetic Returns')
    plt.plot(standard_deviations, geometric_returns, label='Geometric Returns')
    plt.plot(standard_deviations, approximated_geometric_returns, label='Approximated Geometric Returns')
    plt.legend()
    plt.xlabel('Standard Deviations')
    plt.show()
