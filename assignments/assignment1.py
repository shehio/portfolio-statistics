from src.currency import Currency
from src.iohelpers import IoHelpers
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from src.security import Security
from src.transaction import Transaction

from assignments.assignment_helpers import Helpers

import numpy as np

current_tickers = ["AAPL", "ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT", "DAL", "EA", "GS",
                   "IBM", "LYFT", "EXPE", "MS", "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

weekly_fees = np.array([0])
dividends_collection = np.array([0])

# Q0
portfolio, week0_transaction_cost = Helpers.establish_equal_weight_portfolio(
    Helpers.that_initial_balance,
    Helpers.start_date,
    current_tickers,
    Helpers.broker_transaction_cost)
Helpers.myprint([portfolio.__repr__()])

# Q1: Calculate the total value of the portfolio after the trades.
Helpers.myprint([f'The portfolios worth after making the initial transactions: {portfolio.get_value(Helpers.start_date)}'])
IoHelpers.write_holdings('yassers', portfolio, Helpers.start_date)

# Q2: Calculate the return of the transition period (prior to inception) based on the beginning value of $1 million.
portfolio_value_by_the_end_of_week_0 = portfolio.get_value(Helpers.start_date)
first_income_return, first_price_return, first_total_return = Helpers.get_returns(
    portfolio,
    Helpers.that_initial_balance,
    Helpers.start_date)
Helpers.myprint([f'Total Return = Price Return = {first_total_return}, since dividends are all zero.'])

# Q3: Check your stocks for any splits
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(portfolio, Helpers.start_date, Helpers.assignment1_end_date)

# # Q4: Check if your stocks distributed any dividends
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, Helpers.start_date, Helpers.assignment1_end_date)

# Q5: Calculate the management fee collected on April 3rd and deduct it from the liquidity reserve.
weekly_fee = PortfolioHelpers.get_fee(new_portfolio, Helpers.annual_fee, FeeFrequency.weekly, Helpers.start_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
                 f'The weekly fee on: {Helpers.weekly_fee_date} is: {weekly_fee}, cash in portfolio afterwards: {new_portfolio.cash}'])

# Q6: Make a trade.  # Eliminate the repeatability here.
week1_transaction_cost = 0
security = Security('AAPL', -1, 'NASDAQ', Currency.Dollars)
transaction = Transaction(Helpers.trade_date, security, -1, Helpers.broker_transaction_cost, Currency.Dollars)
week1_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

security = Security('ALK', 10, 'NASDAQ', Currency.Dollars)
transaction = Transaction(Helpers.trade_date, security, 10, Helpers.broker_transaction_cost, Currency.Dollars)
week1_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

IoHelpers.write_holdings('yassers', new_portfolio, Helpers.assignment1_end_date)
print(new_portfolio.__repr__())

# Q7:
portfolio_value_by_the_end_of_week_1 = new_portfolio.get_value(Helpers.assignment1_end_date)
second_income_return, second_price_return, second_total_return =\
    Helpers.get_returns(new_portfolio, portfolio_value_by_the_end_of_week_0, Helpers.assignment1_end_date)

Helpers.myprint([f'Second Income Return = {second_income_return}',
                 f'Second Price Return = {second_price_return}',
                 f'Second Total Return = {second_total_return}'])

portfolio_values = np.array([portfolio_value_by_the_end_of_week_0, portfolio_value_by_the_end_of_week_1])

income_returns = np.array([first_income_return, second_income_return])
price_returns = np.array([first_price_return, second_price_return])
total_returns = np.array([first_total_return, second_total_return])

transaction_costs = np.array([week0_transaction_cost, week1_transaction_cost])

# Saving data

collection = np.array([income_returns, price_returns, total_returns, new_portfolio,
                       portfolio_values, transaction_costs, weekly_fees, dividends_collection])
Helpers.save_to_pickle(collection, 'a1.pkl')