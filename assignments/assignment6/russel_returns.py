import datetime
import os
import numpy as np
import pandas as pd

from src.iohelpers import IoHelpers


def get_returns_between_dates(values: pd.DataFrame, start_date: np.datetime64, end_date: np.datetime64) -> np.array:
    values = values.loc[(values.index > start_date) & (values.index <= end_date)]

    returns = (values.Value_With_Dividends__USD_ / values.Value_With_Dividends__USD_.shift() - 1) * 100
    returns = returns.to_numpy()
    returns = returns[~ np.isnan(returns)]
    return returns


if __name__ == '__main__':
    russel_values = IoHelpers.read_russel_returns(os.path.realpath('./../statements/valueshist_US3000_all.csv'))
    russel_values = russel_values[['Value_With_Dividends__USD_']]
    index = russel_values.index
    russel_values = russel_values.loc[russel_values.groupby(index.to_period('M')).apply(lambda x: x.index.max())]

    start_date = np.datetime64(datetime.date(2000, 1, 1))
    end_date = np.datetime64(datetime.date(2009, 12, 31))
    print(np.round(get_returns_between_dates(russel_values, start_date, end_date), 2))

    start_date = np.datetime64(datetime.date(2010, 1, 1))
    end_date = np.datetime64(datetime.date(2019, 12, 31))
    print(np.round(get_returns_between_dates(russel_values, start_date, end_date), 2))
