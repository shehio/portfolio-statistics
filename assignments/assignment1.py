from src.apihelpers import ApiHelpers
from src.currency import Currency
from src.portfolio import Portfolio
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory


import datetime
import numpy as np


def establish_portfolio(initial_balance, inception_date, tickers, transaction_cost, date):
    equal_percentage = 1.0 / len(tickers)
    transactions_history = TransactionsHistory()
    securities = np.array([])

    for ticker in tickers:
        security_price = ApiHelpers.get_close_price(ticker, date)
        shares = np.floor(initial_balance * equal_percentage / security_price)

        security = Security(ticker, shares, 'NASDAQ', Currency.Dollars)
        securities = np.append(securities, security)

        transaction = Transaction(inception_date, security, shares, security_price, Currency.Dollars)
        transactions_history.push_transaction(transaction)

    current_balance = sum(map(lambda _transaction: transaction.price, transactions_history.transactions))
    current_balance = Security('CASH', current_balance, 'None', Currency.Dollars)
    return Portfolio(current_balance, inception_date, securities, transactions_history)


security_count = 20
maximum_security_weight = 0.2
maximum_cash_weight = 0.05
broker_transaction_cost = 0.001
fee_per_week = 0.01 * 0.01 * 2
annual_fee = 1.04 / 100
start_date = datetime.date(2020, 3, 27)
end_date = datetime.date(2020, 4, 3)
trade_date = datetime.date(2020, 4, 3)
weekly_fee_date = datetime.date(2020, 4, 3)
that_initial_balance = 1000 * 1000

current_tickers = ["AAPL","ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT",  "DAL", "EA", "GS",
            "IBM", "LYFT", "EXPE", "MS",  "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

# Q0
portfolio = establish_portfolio(that_initial_balance, start_date, current_tickers, broker_transaction_cost, start_date)
# print(portfolio.__repr__())

# Q1: Calculate the total value of the portfolio after the trades.
print(f'The total worth of the portfolio after making the initial transactions: {portfolio.get_value(end_date)}')

# Q2: Calculate the return of the transition period (prior to inception) based on the beginning value of $1 million.
initial_portfolio_value = portfolio.get_value(start_date)
first_price_return = (initial_portfolio_value - that_initial_balance) / initial_portfolio_value * 100
first_total_return = first_price_return

print(f'Total Return = Price Return = {first_total_return}, since dividends are all zero.')

# # Q3: Check your stocks for any splits
# for stock in portfolio.securities:
#     print(f'split for ticker: {stock.ticker} from {start_date} to {end_date} is: '
#           f'{ApiHelpers.get_range_splits(stock.ticker, start_date, end_date)}')

# # Q4: Check if your stocks distributed any dividends
# for stock in portfolio.securities:
#     print(f'split for ticker: {stock.ticker} on {start_date} to {end_date} is: '
#           f'{ApiHelpers.get_range_dividends(stock.ticker, start_date, end_date)}')

# Q5: Calculate the management fee collected on April 3rd and deduct it from the liquidity reserve.
weekly_fee = PortfolioHelpers.get_fee(portfolio,  annual_fee, FeeFrequency.weekly, weekly_fee_date)
portfolio.discount_fee(weekly_fee)
print(f'The weekly fee on date: {weekly_fee_date} is: {weekly_fee}, the cash value afterwards: {portfolio.cash}')

# Q6: Make a trade.
security = Security('AAPL', -1, 'NASDAQ', Currency.Dollars)
transaction = Transaction(trade_date, security, -1, broker_transaction_cost, Currency.Dollars)
new_portfolio = PortfolioHelpers.make_trade(portfolio, security, transaction)

security = Security('ALK', 10, 'NASDAQ', Currency.Dollars)
transaction = Transaction(trade_date, security, 10, broker_transaction_cost, Currency.Dollars)
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

# Q7:
current_portfolio_value = new_portfolio.get_value(end_date)
second_price_return = (current_portfolio_value - initial_portfolio_value) / current_portfolio_value * 100
second_total_return = second_price_return
print(f'Total Return = Price Return = {second_total_return}, since dividends are all zero.')
