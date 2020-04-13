from .portfolio import Portfolio


class IoHelpers:

    @staticmethod
    def write_holdings(account_name, portfolio: Portfolio):
        csv = 'ticker,num.shares'
        for security in portfolio.securities:
            csv += f'{security.ticker},{security.shares}\n'
        csv += f'{portfolio.cash.ticker},{portfolio.cash.shares}'

        text_file = open(f'H-{account_name}-{portfolio.inception_date}', 'w')
        text_file.write(csv)
        text_file.close()

    @staticmethod
    def write_account_summary(
            account_name, dates, deposits, withdrawals, dividends, fees,
            transactional_costs, values, income_returns, price_returns, total_returns):
        csv = 'account.name,as.of.date,deposits,withdrawals,' \
              'dividends,fees,tc,value,income.return,price.return,total.return'

        for date, deposit, withdrawal, dividend, fee, transactional_cost,\
            value, income_return, price_return, total_return in zip(dates, deposits, withdrawals, dividends,
                                                                    fees, transactional_costs, values, income_returns,
                                                                    price_returns, total_returns):
            csv += f'{account_name},{date},{deposit},{withdrawal},{dividend},' \
                   f'{fee},{transactional_cost},{value},{income_return},{price_return},{total_return}'

        text_file = open(f'A-{account_name-dates[dates.length - 1]}', 'w')
        text_file.write(csv)
        text_file.close()
