from src.apihelpers import ApiHelpers
from src.iohelpers import IoHelpers

import datetime
import numpy as np


def get_sectors_from_holdings(_holdings, _sectors_map):
    aggregate_map = {}
    for key in _holdings:
        if key == 'CASHX':
            continue

        sector = _sectors_map[key][1]

        if sector in aggregate_map.keys():
            array = aggregate_map[sector]
            array = np.append(array, key)
        else:
            array = np.array([key])

        aggregate_map[sector] = array

    return aggregate_map


def get_money_in_sector(tickers: dict, _holdings_map: dict, _date: datetime):
    _sum = 0
    for ticker in tickers:
        _sum += ApiHelpers.get_close_price(ticker, _date) * _holdings_map[ticker]

    return _sum


def get_money_in_all_sectors(_holdings_by_sectors, _holdings_map: dict, _date: datetime):
    money_in_sectors = {}
    for _sector in _holdings_by_sectors.keys():
        money_in_sectors[_sector] = get_money_in_sector(_holdings_by_sectors[_sector], _holdings_map, _date)

    return money_in_sectors


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

for holdings_file, date in zip(holdings_files, dates):
    holdings = IoHelpers.get_securities_from_holdings_file(f'./../statements/{holdings_file}')
    print(get_sectors_from_holdings(holdings.keys(), sectors_map))
    sectors_from_holdings = get_sectors_from_holdings(holdings, sectors_map)
    money_in_all_sectors = get_money_in_all_sectors(sectors_from_holdings, holdings, date)
    portfolio_value = sum(money_in_all_sectors.values())
    print(dict(map(lambda entry: (entry[0], entry[1] / portfolio_value), money_in_all_sectors.items())))



