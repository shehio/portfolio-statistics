from src.apihelpers import ApiHelpers
from src.sector import Sector
from src.iohelpers import IoHelpers

import datetime
import numpy as np

CASHX_INDUSTRY_ID = 0
CASHX_INDUSTRY_NAME = 'Liquidity Reserve'
CASH_SECTOR = Sector(CASHX_INDUSTRY_ID, CASHX_INDUSTRY_NAME)


# One common classification scheme for equity securities is the Industry Classification Benchmark (ICB)
# scheme, described at https://www.ftserussell.com/data/industry-classification-benchmark-icb and in the
# documents posted in the course readings. Also posted is a file, H-R3000-2020-03-27.csv, that contains
# the holdings and ICB classifications of the constituents of the Russell 3000 as of 2020-03-27. This data
# was supplied courtesy of FTSE Russell. You are welcome to browse the contents of this file, which
# includes many items that are typically provided daily by an index vendor to its clients.
# Posted with the assignment is the file getICBIndustries.R. Included in the script is the function
# getSectors() that gets the sector numbers and sector names for a vector of tickers. The usage example in
# the file does the following:
# • Reads the R3000 holdings file,
# • Reads your holdings file,
# • Downloads prices and calculates the market values of the holdings,
# • Extracts the sectors for your tickers,
# • Aggregates the market values by sector,
# • Adds rows for sectors with zero holdings,
# • Calculates weights by sector,
# • Adds a date column.
# The example code does all of the above in a loop through the weekly holdings dates and concatenates
# the sector weights into a single table.
# Read and modify the example code to run on your holdings files. Understanding the example will be
# useful for the next step.

# The file S-R1000-2020-04-17.csv contains a weekly history of sector weights and returns for the Russell
# 1000 Index. This data was supplied courtesy of FTSE Russell. The goal of this assignment is to build a
# similar history table from your weekly portfolio holdings.
# Posted with the assignment is the file calcWeightsAndReturns.R. The function in this file calculates
# weights and returns of assets over a single week, given the holdings at the beginning of the week, and
# cash flow information from the Account Summary. The asset returns are calculated assuming all
# transactions and cash flows occur at the end of the week. Holdings are adjusted for splits and asset
# returns include dividends. The function returns the holdings table augmented with columns including ABV,
# weight, AEV, and return.
# The example code calls the function in a loop over the weekly dates.
# You are to modify the code in the loop to complete the calculation of sector weights and returns for your
# portfolio holdings:
# • Get the sector information for your assets and merge with the holdings table,
# • Aggregate the ABV and AEV by sector,
# • Calculate weights and returns by sector,
# • Add rows to the table for sectors that have zero weight,
# • Add a date column to the table,
# • Concatenate the sector weights and returns into a single table.
# Write the final history table to a file named like S-<uwid>-<yyyy-mm-dd>.csv and submit.
# We will use the sector weights and returns files to calculate sector-based performance attribution in next
# week’s assignment. If you wish, you may go ahead and calculate attribution from your sector weights and
# returns and the R1000 sector weights and returns.

def get_sectors_from_holdings(_holdings: dict, _sectors_map: dict):

    portfolio_sectors = {}
    for key in _holdings:
        if key == 'CASHX':
            portfolio_sectors[CASH_SECTOR] = np.array([key])
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
        if _sector.id == CASHX_INDUSTRY_ID:
            money_in_sectors[_sector] = _holdings_map[_holdings_by_sectors[_sector][0]]
        else:
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
    'H-yassers-2020-04-17.csv',
    'H-yassers-2020-04-24.csv']

dates = [
    datetime.date(2020, 3, 27),
    datetime.date(2020, 4, 3),
    datetime.date(2020, 4, 9),
    datetime.date(2020, 4, 17),
    datetime.date(2020, 4, 24)
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
