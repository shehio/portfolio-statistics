from src.apihelpers import ApiHelpers

import yfinance as yf
import datetime
import numpy as np


def get_approximated_returns(prices_array: np.array):
    t_bills_ratio = (91 / 360)
    normalized_prices = prices_array / 100
    return 100 / 3 * (normalized_prices * t_bills_ratio) / (1 - (normalized_prices * t_bills_ratio))


def get_t_bills_monthly_returns(start_date: datetime.date, end_date: datetime.date, get_returns_lambda):
    prices_dataframe = yf.download(
        '^IRX',
        start=start_date,
        end=end_date,
        progress=False)['Close']
    monthly_prices = prices_dataframe.loc[
        prices_dataframe.groupby(prices_dataframe.index.to_period('M')).apply(lambda x: x.index.max())]
    monthly_prices_array = monthly_prices.to_numpy()

    return get_returns_lambda(monthly_prices_array)


if __name__ == '__main__':
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2010, 1, 1)

    print(get_t_bills_monthly_returns(start_date, end_date, get_approximated_returns))
