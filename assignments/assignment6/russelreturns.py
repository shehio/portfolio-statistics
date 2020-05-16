import datetime
import os
import numpy as np
import pandas as pd

from src.iohelpers import IoHelpers

column_of_interest = 'Value_With_Dividends__USD_'


def get_last_moth_data_from_russel(filename: str) -> pd.DataFrame:
    _russel_values = IoHelpers.read_russel_returns(filename)
    _russel_values = _russel_values[[column_of_interest]]
    index = _russel_values.index
    return _russel_values.loc[_russel_values.groupby(index.to_period('M')).apply(lambda x: x.index.max())]


def get_returns_between_dates(values: pd.DataFrame, _start_date: datetime, _end_date: datetime) -> np.array:
    _start_date = np.datetime64(_start_date)
    _end_date = np.datetime64(_end_date)
    values = values.loc[(values.index > _start_date) & (values.index <= _end_date)]
    column = values[[column_of_interest]]
    returns = (column / column.shift() - 1) * 100
    returns = returns.to_numpy()
    returns = returns[~ np.isnan(returns)]
    return returns


if __name__ == '__main__':
    russel_values = get_last_moth_data_from_russel(os.path.realpath('./../statements/valueshist_US3000_all.csv'))

    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2009, 12, 31)
    print(np.round(get_returns_between_dates(russel_values, start_date, end_date), 2))

    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2019, 12, 31)
    print(np.round(get_returns_between_dates(russel_values, start_date, end_date), 2))
