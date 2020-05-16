import operator
from functools import reduce
import yfinance as yf
import datetime
import numpy as np


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def get_approximated_returns(prices_array: np.array):
    t_bills_ratio = (91 / 360)
    normalized_prices = prices_array / 100
    return 100 / 3 * (normalized_prices * t_bills_ratio) / (1 - (normalized_prices * t_bills_ratio))


# This could be more generic by passing in the symbol.
def get_t_bills_monthly_returns(
        _start_date: datetime.date,
        _end_date: datetime.date,
        get_returns_lambda=get_approximated_returns):
    prices = yf.download(
        '^IRX',
        start=_start_date,
        end=_end_date,
        progress=False)['Close']
    monthly_prices = prices.loc[prices.groupby(prices.index.to_period('M')).apply(lambda x: x.index.max())]
    monthly_prices_array = monthly_prices.to_numpy()

    return get_returns_lambda(monthly_prices_array)


if __name__ == '__main__':
    # Calculate the annualized geometric mean return for T-bills over the ten year period 2010–2019
    # and over the previous ten year period 2000–2009.
    # Observe the current level of T-bill returns compared with that of the last decade.
    # Our use of the approximation during this course, that cash returns are zero, appears to be reasonable.

    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2009, 12, 31)

    t_bills_returns = get_t_bills_monthly_returns(start_date, end_date)
    returns_count = t_bills_returns.shape[0]
    geometric_return = 100 * (np.float_power(
        prod(map(lambda _return: 1 + _return / 100.0, t_bills_returns)), 1.0 / returns_count) - 1)
    print(f'Geometric Mean Rate Of Return: {round(geometric_return, 2)}%')

    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2019, 12, 31)

    t_bills_returns = get_t_bills_monthly_returns(start_date, end_date)
    geometric_return = 100 * (np.float_power(
        prod(map(lambda _return: 1 + _return / 100.0, t_bills_returns)), 1.0 / returns_count) - 1)
    print(f'Geometric Mean Rate Of Return: {round(geometric_return, 2)}%')

