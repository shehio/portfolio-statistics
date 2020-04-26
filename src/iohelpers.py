from .portfolio import Portfolio
from .sector import Sector
from .security import Security

import csv
import datetime
import numpy as np


def compare_securities(security1: Security, security2: Security):
    return security1.ticker > security2.ticker


class IoHelpers:

    @staticmethod
    def write_holdings(account_name: str, portfolio: Portfolio, date: datetime):
        sorted_securities = np.sort(portfolio.securities)

        content = 'ticker,num.shares\n'
        for security in sorted_securities:
            content += f'{security.ticker},{security.shares}\n'
        content += f'{portfolio.cash.ticker},{portfolio.cash.shares}'

        text_file = open(f'./statements/H-{account_name}-{date}.csv', 'w')
        text_file.write(content)
        text_file.close()

    @staticmethod
    def write_account_summary(
            account_name, dates, deposits, withdrawals, dividends, fees,
            transactional_costs, values, income_returns, price_returns, total_returns):
        content = 'account.name,as.of.date,deposits,withdrawals,' \
              'dividends,fees,tc,value,income.return,price.return,total.return\n'

        for date, deposit, withdrawal, dividend, fee, transactional_cost,\
            value, income_return, price_return, total_return in zip(dates, deposits, withdrawals, dividends,
                                                                    fees, transactional_costs, values, income_returns,
                                                                    price_returns, total_returns):
            content += f'{account_name},{date},{deposit},{withdrawal},{dividend},' \
                   f'{fee},{transactional_cost},{value},{income_return},{price_return},{total_return}\n'

        text_file = open(f'./statements/A-{account_name}-{dates[len(dates) - 1]}.csv', 'w')
        text_file.write(content)
        text_file.close()
    
    @staticmethod
    def write_s_file(week_endings, weights_by_sector, returns_by_sector):
        content = 'week.ending, ICB.industry.num, ICB.industry.name, weight, "return'

    @staticmethod
    def get_sector_dict_from_russel_holdings():
        holdings = IoHelpers.read_csv('./../statements/H-R3000-2020-03-27.csv')
        next(holdings)  # throwing the fields away.
        holdings_dict = {}
        for holding in holdings:
            name = holding[3]
            sector_id = holding[19]
            sector_name = holding[20]
            holdings_dict[name] = Sector(sector_id, sector_name)

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
    def read_csv(file_name: str):  # This is not implemented properly.
        return csv.reader(open(file_name))
