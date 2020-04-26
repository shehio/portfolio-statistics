from src.iohelpers import IoHelpers

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


sectors_map = IoHelpers.get_sector_dict_from_russel_holdings()
holdings_files = [
    'H-yassers-2020-03-27.csv',
    'H-yassers-2020-04-03.csv',
    'H-yassers-2020-04-09.csv',
    'H-yassers-2020-04-17.csv']

for holdings_file in holdings_files:
    holdings = IoHelpers.get_securities_from_holdings_file(f'./../statements/{holdings_file}')
    print(get_sectors_from_holdings(holdings.keys(), sectors_map))



