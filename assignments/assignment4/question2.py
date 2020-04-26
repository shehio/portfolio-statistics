from src.apihelpers import ApiHelpers
from src.iohelpers import IoHelpers

import datetime
import numpy as np


def get_sectors_from_holdings(_holdings: dict, _sectors_map: dict):
    portfolio_sectors = {}
    for key in _holdings:
        if key == 'CASHX':
            continue

        sector = _sectors_map[key]

        if sector in portfolio_sectors.keys():
            array = np.append(portfolio_sectors[sector], key)
        else:
            array = np.array([key])

        portfolio_sectors[sector] = array

    return portfolio_sectors


def get_money_in_sector(tickers: dict, _holdings_map: dict, _date: datetime):
    _sum = 0
    for ticker in tickers:
        _sum += ApiHelpers.get_close_price(ticker, _date) * _holdings_map[ticker]

    return _sum


def get_money_by_sector(_holdings_by_sectors, _holdings_map: dict, _date: datetime):
    money_in_sectors = {}
    for _sector in _holdings_by_sectors.keys():
        money_in_sectors[_sector] = get_money_in_sector(_holdings_by_sectors[_sector], _holdings_map, _date)

    return money_in_sectors


def read_holdings(file_name):
    return IoHelpers.get_securities_from_holdings_file(f'./../statements/{file_name}')


# For now, assume that the keys for both dictionaries are identical.
def get_returns_per_sector(_money_by_sector1: dict, _money_by_sector2: dict):
    return dict(map(
        lambda sector: (sector, _money_by_sector2[sector] / _money_by_sector1[sector] - 1),
        _money_by_sector2.keys()))


def get_weight_by_sector(_money_by_sector: dict):
    portfolio_value = sum(_money_by_sector.values())
    return dict(map(lambda entry: (entry[0], entry[1] / portfolio_value), _money_by_sector.items()))


def iteration_setup(iteration_number):
    _date1 = dates[iteration_number]
    _date2 = dates[iteration_number + 1]
    _holdings1 = read_holdings(holdings_files[iteration_number])
    _holdings2 = read_holdings(holdings_files[iteration_number + 1])
    return _date1, _date2, _holdings1, _holdings2


sectors_map = IoHelpers.get_sector_dict_from_russel_holdings()
holdings_files = [
    'H-yassers-2020-03-27.csv',
    'H-yassers-2020-04-03.csv',
    'H-yassers-2020-04-09.csv',
    'H-yassers-2020-04-17.csv']

dates = [
    datetime.date(2020, 3, 27),
    datetime.date(2020, 4, 3),
    datetime.date(2020, 4, 9),
    datetime.date(2020, 4, 17)
]

returns_per_sectors_list = np.array([], dtype=dict)
weights_per_sectors_list = np.array([], dtype=dict)

for i in range(0, len(dates) - 1):
    date1, date2, holdings1, holdings2 = iteration_setup(i)
    sectors1 = get_sectors_from_holdings(holdings1, sectors_map)
    sectors2 = get_sectors_from_holdings(holdings2, sectors_map)
    money_by_sector1 = get_money_by_sector(sectors1, holdings1, date1)
    money_by_sector2 = get_money_by_sector(sectors2, holdings2, date2)

    returns_per_sectors_list = np.append(
        returns_per_sectors_list,
        get_returns_per_sector(money_by_sector1, money_by_sector2))

    weights_per_sectors_list = np.append(
        weights_per_sectors_list,
        get_weight_by_sector(money_by_sector2))

dates.pop(0)
IoHelpers.write_s_file(dates, weights_per_sectors_list, returns_per_sectors_list)
