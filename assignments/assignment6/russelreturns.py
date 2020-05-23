import datetime
import os
import numpy as np
import pandas as pd

from src.iohelpers import IoHelpers

column_of_interest = 'Value_With_Dividends__USD_'
russel_file = './../statements/valueshist_US3000_all.csv'

# 4. The Russell 3000 index represents approximately 98% of the market capitalization of U.S. common stocks.
# Historical values of the Russell 3000 index are available at:
# https://www.ftserussell.com/products/russell-index-values.
# A file valueshist_US3000_all.csv of daily values of the Russell 3000 index is posted with the assignment.
# In the file readIndexHistory.R file is a function, readIndexHistory(histfile), that reads a Russell index history file
# and returns an xts object with month-end index values. Run this script and its support functions following the example
# in the file. Calculate monthly total returns for the Russell 3000 index. Use these returns for problem 4.


def get_last_month_data_from_russel(filename: str) -> pd.DataFrame:
    _russel_values = IoHelpers.read_russel_returns(filename)
    _russel_values = _russel_values[[column_of_interest]]
    index = _russel_values.index
    return _russel_values.loc[_russel_values.groupby(index.to_period('M')).apply(lambda x: x.index.max())]


def get_returns_between_dates(values: pd.DataFrame, _start_date: np.datetime64, _end_date: np.datetime64) -> np.array:
    values = values.loc[(values.index > _start_date) & (values.index <= _end_date)]
    column = values[[column_of_interest]]
    returns = (column / column.shift() - 1) * 100
    returns = returns.to_numpy()
    returns = returns[~ np.isnan(returns)]
    return returns


def get_russel_monthly_returns(
        _start_date: datetime.date,
        _end_date: datetime.date,
        _russel_values_file=os.path.realpath(russel_file)):
    _russel_values = get_last_month_data_from_russel(os.path.realpath(russel_file))
    return get_returns_between_dates(_russel_values, np.datetime64(_start_date), np.datetime64(_end_date))


if __name__ == '__main__':
    start_date = datetime.date(1999, 12, 31)
    end_date = datetime.date(2009, 12, 31)
    print(np.round(get_russel_monthly_returns(start_date, end_date), 2))

    start_date = datetime.date(2009, 12, 31)
    end_date = datetime.date(2019, 12, 31)
    print(np.round(get_russel_monthly_returns(start_date, end_date), 2))
