from src.apihelpers import ApiHelpers
from src.portfolio import Portfolio
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory


import datetime
import numpy as np


def establish_portfolio(initial_balance, tickers, transaction_cost, date):
    equal_percentage = 1.0 / len(tickers)
    current_balance = initial_balance
    transactions_history = TransactionsHistory()
    securities = np.array([])

    for ticker in tickers:
        security_price = ApiHelpers.get_close_price(ticker, date)
        shares = np.floor(initial_balance * equal_percentage / security_price)

        security = Security(ticker, shares, 'NASDAQ')
        securities = np.append(securities, security)

        transaction = Transaction(ticker, shares, security_price)
        transactions_history.push_transaction(transaction)

        balance_spent = shares * security_price
        current_balance = current_balance - balance_spent - shares * transaction_cost

    current_balance = Security('CASH', current_balance, 'None')
    return Portfolio(current_balance, securities, transactions_history)


security_count = 20
maximum_security_weight = 0.2
maximum_cash_weight = 0.05
broker_transaction_cost = 0.001
fee_per_week = 0.01 * 0.01 * 2
start_date = datetime.date(2020, 3, 27)
end_date = datetime.date(2020, 4, 3)
trade_date = datetime.date(2020, 4, 3)
weekly_fee_date = datetime.date(2020, 4, 3)
that_initial_balance = 1000 * 1000

current_tickers = ["AAPL","ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT",  "DAL", "EA", "GS",
            "IBM", "LYFT", "EXPE", "MS",  "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

# Q0
portfolio = establish_portfolio(that_initial_balance, current_tickers, broker_transaction_cost, start_date)
# print(portfolio.__repr__())

# Q1: Calculate the total value of the portfolio after the trades.
print(f'The total worth of the portfolio after making the initial transactions: {portfolio.get_value(end_date)}')

# Q2: Calculate the return of the transition period (prior to inception) based on the beginning value of $1 million.
initial_portfolio_value = portfolio.get_value(end_date)
first_price_return = (initial_portfolio_value - that_initial_balance) / initial_portfolio_value * 100
first_total_return = first_price_return

print(f'Total Return = Price Return = {first_total_return}, since dividends are all zero.')

# Q3: Check your stocks for any splits
for stock in portfolio.securities:
    print(f'split for ticker: {stock.ticker} on {start_date} is: {ApiHelpers.get_splits(stock.ticker, start_date)}')

# Q4: Check if your stocks distributed any dividends
for stock in portfolio.securities:
    print(f'split for ticker: {stock.ticker} on {start_date} is: {ApiHelpers.get_splits(stock.ticker, start_date)}')
