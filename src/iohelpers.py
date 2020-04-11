from .portfolio import Portfolio

import numpy as np

class IoHelpers:

    @staticmethod
    def write_holdings(portfolio: Portfolio):
        csv = ''
        for security in portfolio.securities:
            csv += f'{security.ticker},{security.shares}\n'
        csv += f'{portfolio.cash.ticker}, {portfolio.cash.shares}'

    @staticmethod
    def write_account_summary(account_name, dates, portfolios: np.array()):
        csv = 'account.name,as.of.date,deposits,withdrawals,dividends,fees,tc,value,income.return,price.return,total.return'

        for portfolio, withdrawal, dividends, fees, tc, value, income_return, price_return, total_return in zip(dates, portfolios, withdrawals, dividends, fees, tc, value, income_returns, price_returns, total_returns):
            for security in portfolio.securities:
                csv += f'{security.ticker},{security.shares}'
            csv += f'{portfolio.cash.ticker}, {portfolio.cash.shares}'


