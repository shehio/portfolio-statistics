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


if __name__ == "__main__":
    portfolio_returns = [0.0242, 0.0551, 0.0115, 0.0189, -0.0278, 0.0061]
    benchmark_returns = [0.0212, 0.0611, 0.0106, 0.0398, -0.0241, 0.0061]
    print(link_arithmetic_excess_returns(portfolio_returns, benchmark_returns))
    print(link_geometric_excess_returns(portfolio_returns, benchmark_returns))
    # portfolio_returns = [50, 50]
    # benchmark_returns = [0, 0]
    # allocations = [50, 0]
    # selection = [0, 50]
