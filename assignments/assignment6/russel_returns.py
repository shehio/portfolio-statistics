from src.iohelpers import IoHelpers

import os

russel_returns = IoHelpers.read_russel_returns(os.path.realpath('./../statements/valueshist_US3000_all.csv'))
russel_returns = russel_returns[['Value_With_Dividends__USD_']]
index = russel_returns.index
russel_returns = russel_returns.loc[russel_returns.groupby(index.to_period('M')).apply(lambda x: x.index.max())]
print(russel_returns)
