from .portfolio import Portfolio
from .sector import Sector

import csv
import datetime
import numpy as np
import pandas


class IoHelpers:

    @staticmethod
    def write_holdings(account_name: str, portfolio: Portfolio, date: datetime):
        sorted_securities = np.sort(portfolio.securities)

        content = 'ticker,num.shares\n'
        for security in sorted_securities:
            content += f'{security.ticker},{security.shares}\n'
        content += f'{portfolio.cash.ticker},{portfolio.cash.shares}'

        csv_file = open(f'./statements/holdings/H-{account_name}-{date}.csv', 'w')
        csv_file.write(content)
        csv_file.close()

    @staticmethod
    def write_account_summary(
            account_name, dates, deposits, withdrawals, dividends, fees,
            transactional_costs, values, income_returns, price_returns, total_returns):
        content = 'account.name,as.of.date,deposits,withdrawals,' \
                  'dividends,fees,tc,value,income.return,price.return,total.return\n'

        for date, deposit, withdrawal, dividend, fee, transactional_cost, \
            value, income_return, price_return, total_return in zip(dates, deposits, withdrawals, dividends,
                                                                    fees, transactional_costs, values, income_returns,
                                                                    price_returns, total_returns):
            content += f'{account_name},{date},{deposit},{withdrawal},{dividend},' \
                       f'{fee},{transactional_cost},{value},{income_return},{price_return},{total_return}\n'

        csv_file = open(f'./statements/accountsummeries/A-{account_name}-{dates[len(dates) - 1]}.csv', 'w')
        csv_file.write(content)
        csv_file.close()

    @staticmethod  # The keys of both dicts inside both list have to be identical.
    def write_s_file(week_endings, weights_by_sector_list, returns_by_sector_list):
        content = 'week.ending, ICB.industry.num, ICB.industry.name, weight, return\n'
        for (date, weights_dict, returns_dict) in zip(week_endings, weights_by_sector_list, returns_by_sector_list):
            for sector in weights_dict.keys():
                content += f'{date},{sector.id},{sector.name},' \
                           f'{weights_dict[sector] * 100},{returns_dict[sector] * 100}\n'

        csv_file = open(f'./../statements/S-yassers-{week_endings[len(week_endings) - 1]}.csv', 'w')
        csv_file.write(content)
        csv_file.close()

    @staticmethod
    def get_sector_dict_from_russel_holdings():
        holdings = IoHelpers.read_csv('./../statements/H-R3000-2020-03-27.csv')
        next(holdings)  # throwing the fields away.
        holdings_dict = {}
        sectors = {}
        for holding in holdings:
            name = holding[3]
            sector_id = holding[19]
            sector_name = holding[20]

            if sector_id in sectors.keys():
                holdings_dict[name] = sectors[sector_id]
            else:
                sector = Sector(sector_id, sector_name)
                sectors[sector_id] = sector
                holdings_dict[name] = sector

        return holdings_dict

    @staticmethod  # No fractional stocks allowed.
    def get_securities_from_holdings_file(file_name: str):
        holdings = IoHelpers.read_csv(file_name)
        next(holdings)  # throwing the fields away.
        holdings_dict = {}
        for holding in holdings:
            holdings_dict[holding[0]] = int(float(holding[1]))

        return holdings_dict

    @staticmethod
    def get_stock_stats_from_russel():
        csv = IoHelpers.read_csv('./../statements/H-R1000-chars-2019-05-31.csv')
        next(csv)  # throwing the fields away.
        stats = {}
        for csv_line in csv:
            ticker = csv_line[1]
            book_to_price = 0 if csv_line[-4] == 'NA' else float(csv_line[-4])
            IBES_2Yr_growth_rate = 0 if csv_line[-3] == 'NA' else float(csv_line[-3])
            SPS_5Yr_growth_rate = 0 if csv_line[-1] == 'NA' else float(csv_line[-1])
            stats[ticker] = (book_to_price, IBES_2Yr_growth_rate, SPS_5Yr_growth_rate)

        return stats

    @staticmethod
    def read_csv(file_name: str):  # This is not implemented properly.
        return csv.reader(open(file_name))

    @staticmethod
    def read_russel_returns(file_name: str):
        return pandas.read_csv(
            file_name,
            index_col='Date',
            parse_dates=['Date'],
            date_parser=lambda date: datetime.datetime.strptime(date, "%m/%d/%Y"))
