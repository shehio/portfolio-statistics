import numpy as np


def link_arithmetic_excess_returns(_portfolio_returns, _benchmark_returns):
    arithmetic_excess_returns = 0
    total_portfolio_return = 1
    total_benchmark_return = 1
    for portfolio_return, benchmark_return in zip(_portfolio_returns, _benchmark_returns):
        excess = portfolio_return * 100 - benchmark_return * 100
        kt = __calculate_kt(portfolio_return, benchmark_return)
        arithmetic_excess_returns += kt * excess

        total_portfolio_return *= (1 + portfolio_return)
        total_benchmark_return *= (1 + benchmark_return)

    num = np.log(total_portfolio_return) - np.log(total_benchmark_return)
    denum = (total_portfolio_return - 1) - (total_benchmark_return - 1)
    ck = num / denum

    arithmetic_excess_returns /= ck

    return arithmetic_excess_returns


def link_geometric_excess_returns(_portfolio_returns, _benchmark_returns):
    geometric_excess_returns = 1
    for portfolio_return, benchmark_return in zip(_portfolio_returns, _benchmark_returns):
        excess = portfolio_return * 100 - benchmark_return * 100
        kt = __calculate_kt(portfolio_return, benchmark_return)
        geometric_excess_returns *= np.exp(kt * excess)

    return geometric_excess_returns - 1


def __calculate_kt(portfolio_return, benchmark_return):
    num = np.log(1 + portfolio_return) - np.log(1 + benchmark_return)
    denum = portfolio_return - benchmark_return

    if denum == 0:
        kt = 1 / (1 + portfolio_return)
    else:
        kt = num / denum

    return kt


# Example from the slides in lecture 5.
def example_from_lecture():
    _portfolio_returns = [0.0242, 0.0551, 0.0115, 0.0189, -0.0278, 0.0061]
    _benchmark_returns = [0.0212, 0.0611, 0.0106, 0.0398, -0.0241, 0.0061]
    print(f'Linked Arithmetic Excess Returns {link_arithmetic_excess_returns(_portfolio_returns, _benchmark_returns)}')
    print(f'Linked Geometric Excess Returns {link_geometric_excess_returns(_portfolio_returns, _benchmark_returns)}')


# 2.	The benchmark for your portfolio is the Russell 1000 total return index.
# A stock market index value can be regarded as the value of a portfolio holding the constituent stocks in weights
# defined by the index. The Russell 1000 index is an index of large capitalization U.S. common stocks.
# Historical values of the Russell 1000 index are available at:
# https://www.ftserussell.com/products/russell-index-values.
# The year-to-date Russell 1000 index values file valuesytd_US1000.csv is posted with the assignment.
# The column named “Value_With_Dividends__USD_” holds the total return index values,
# while the column named “Value_Without_Dividends__USD_” holds the price return index values.
#
# For the period from 2020-03-27 to 2020-04-24, calculate:
# a.	The Russell 1000 total return.
#
# b.	The arithmetic excess return of your portfolio over the benchmark.
#
# c.	The geometric excess return of your portfolio over the benchmark.
def Q2():
    _portfolio_returns = [-0.072686, 0.16596, 0.01719, -0.008562]  # discarded: -0.0999,
    _benchmark_returns = [7932 / 8135 - 1, 8933 / 7932 - 1, 9203 / 8933 - 1, 9090 / 9203 - 1]
    print(f'Russel 1000 Total Return from 3/27 to 4/24: {(9090 / 8134 - 1) * 100}%')
    print(f'Linked Arithmetic Excess Returns {link_arithmetic_excess_returns(_portfolio_returns, _benchmark_returns)}')
    print(f'Linked Geometric Excess Returns {link_geometric_excess_returns(_portfolio_returns, _benchmark_returns)}')


if __name__ == "__main__":
    Q2()
