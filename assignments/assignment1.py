from src.apihelpers import ApiHelpers
from src.currency import Currency
from src.iohelpers import IoHelpers
from src.portfolio import Portfolio
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory


import datetime
import numpy as np


def get_div_return(value_before, value_after):
    return (value_after / value_before) * 100


def get_price_return(value_before, value_after):
    return (value_after / value_before - 1) * 100


def myprint(strings):
    print()
    for string in strings:
        print(string)
    print()


def establish_portfolio(initial_balance, inception_date, tickers, transaction_cost):
    equal_percentage = 1.0 / len(tickers)
    transactions_history = TransactionsHistory()
    securities = np.array([])
    for ticker in tickers:
        security_price = ApiHelpers.get_close_price(ticker, inception_date)
        shares = np.floor(initial_balance * equal_percentage / security_price)

        _security = Security(ticker, shares, 'NASDAQ', Currency.Dollars)
        securities = np.append(securities, _security)

        _transaction = Transaction(inception_date, _security, shares, transaction_cost, Currency.Dollars)
        transactions_history.push_transaction(_transaction)

    total_transaction_cost = sum(map(
        lambda _transaction: _transaction.price,
        transactions_history.transactions))
    current_balance = initial_balance - total_transaction_cost
    current_balance = Security('CASH', current_balance, 'None', Currency.Dollars)
    return Portfolio(current_balance, inception_date, securities, transactions_history), total_transaction_cost


security_count = 20
maximum_security_weight = 0.2
maximum_cash_weight = 0.05
broker_transaction_cost = 0.001
fee_per_week = 0.01 * 0.01 * 2
annual_fee = 1.04 / 100
start_date = datetime.date(2020, 3, 27)
assignment1_end_date = datetime.date(2020, 4, 3)
assignment2_end_date = datetime.date(2020, 4, 10)
trade_date = datetime.date(2020, 4, 3)
weekly_fee_date = datetime.date(2020, 4, 3)
that_initial_balance = 1000 * 1000

current_tickers = ["AAPL","ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT",  "DAL", "EA", "GS",
            "IBM", "LYFT", "EXPE", "MS",  "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

weekly_fees = np.array([0])
dividends_collection = np.array([0])

# Q0
portfolio, week0_transaction_cost = establish_portfolio(
    that_initial_balance,
    start_date,
    current_tickers,
    broker_transaction_cost)
myprint([portfolio.__repr__()])

# Q1: Calculate the total value of the portfolio after the trades.
myprint([f'The portfolios worth after making the initial transactions: {portfolio.get_value(start_date)}'])
IoHelpers.write_holdings('yassers', portfolio, start_date)

# Q2: Calculate the return of the transition period (prior to inception) based on the beginning value of $1 million.
portfolio_value_by_the_end_of_week_0 = portfolio.get_value(start_date)
first_income_return = 0
first_price_return = first_total_return = get_price_return(
    value_before=that_initial_balance,
    value_after=portfolio_value_by_the_end_of_week_0)
myprint([f'Total Return = Price Return = {first_total_return}, since dividends are all zero.'])

# Q3: Check your stocks for any splits
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(portfolio, start_date, assignment1_end_date)
# portfolio = None

# # Q4: Check if your stocks distributed any dividends
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, start_date, assignment1_end_date)

# Q5: Calculate the management fee collected on April 3rd and deduct it from the liquidity reserve.
weekly_fee = PortfolioHelpers.get_fee(new_portfolio, annual_fee, FeeFrequency.weekly, start_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
         f'The weekly fee on: {weekly_fee_date} is: {weekly_fee}, cash in portfolio afterwards: {new_portfolio.cash}'])

# Q6: Make a trade.  # Eliminate the repeatability here.
week1_transaction_cost = 0
security = Security('AAPL', -1, 'NASDAQ', Currency.Dollars)
transaction = Transaction(trade_date, security, -1, broker_transaction_cost, Currency.Dollars)
week1_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

security = Security('ALK', 10, 'NASDAQ', Currency.Dollars)
transaction = Transaction(trade_date, security, 10, broker_transaction_cost, Currency.Dollars)
week1_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

IoHelpers.write_holdings('yassers', new_portfolio, assignment1_end_date)
print(new_portfolio.__repr__())

# Q7:
portfolio_value_by_the_end_of_week_1 = new_portfolio.get_value(assignment1_end_date)
second_income_return = get_div_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=new_portfolio.dividends)
second_price_return = get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_1 - new_portfolio.dividends)
second_total_return = second_price_return + second_income_return
myprint([f'Second Income Return = {second_income_return}',
         f'Second Price Return = {second_price_return}',
         f'Second Total Return = {second_total_return}'])

#
# # ### Assignment 2:
# #  Q1: Check your stocks for any splits or any dividends
# # This implementation has bugs because splits and dividends should be checked simultaneously. Day by day.
dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio.reset_dividends()
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(new_portfolio, assignment1_end_date, assignment2_end_date)
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, assignment1_end_date, assignment2_end_date)
#
weekly_fee = PortfolioHelpers.get_fee(new_portfolio, annual_fee, FeeFrequency.weekly, assignment1_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
         f'The weekly fee on: {weekly_fee_date} is: {weekly_fee}, cash in portfolio afterwards: {new_portfolio.cash}'])

portfolio_value_by_the_end_of_week_2 = new_portfolio.get_value(assignment2_end_date)
third_income_return = get_div_return(
    value_before=portfolio_value_by_the_end_of_week_1,
    value_after=new_portfolio.dividends)
third_price_return = get_price_return(
    value_before=portfolio_value_by_the_end_of_week_1,
    value_after=portfolio_value_by_the_end_of_week_2 - new_portfolio.dividends)
third_total_return = third_price_return + third_income_return
myprint([f'Third Income Return = {third_income_return}',
         f'Third Price Return = {third_price_return}',
         f'Third Total Return = {third_total_return}'])

dividends_collection = np.append(dividends_collection, new_portfolio.dividends)

IoHelpers.write_holdings('yassers', new_portfolio, assignment2_end_date)
IoHelpers.write_account_summary(
    account_name='yassers',
    dates=[start_date, assignment1_end_date, assignment2_end_date],
    deposits=[that_initial_balance, 0, 0],
    withdrawals=[0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=[week0_transaction_cost, week1_transaction_cost, 0],
    values=[portfolio_value_by_the_end_of_week_0, portfolio_value_by_the_end_of_week_1, portfolio_value_by_the_end_of_week_2],
    income_returns=[first_income_return, second_income_return, third_income_return],
    price_returns=[first_price_return, second_price_return, third_price_return],
    total_returns=[first_total_return, second_total_return, third_total_return])

# Q2:
# The returns calculated for the portfolio so far are net-of-fees returns. Calculate the following
# additional items, as of 10 April 2020:
# a. Calculate the linked net-of-fees return for the period from inception to 10 April 2020.
# Reminder: the inception of the portfolio measurement period is the market close on 27
# March 2020.
assignment2_portfolio_value = new_portfolio.get_value(assignment2_end_date)
net_of_fees_returns = get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_2)
myprint([f'Net of fees returns = {net_of_fees_returns}'])

# b. Calculate an approximate gross-of-fees return from inception to this date. Describe any assumptions used.
assignment2_portfolio_value = new_portfolio.get_value(assignment2_end_date)
gross_of_fees_returns = get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_2 + + sum(map(lambda fee: fee, weekly_fees)))
myprint([f'Gross of fees returns = {gross_of_fees_returns}'])

# c. Assuming the portfolio is liquidated on 10 April 2020, calculate the post-tax post redemption
# return from inception to this date.Assume an income tax rate of 15% for both
# dividends and realized capital gains.
# Use this method: get_post_tax_liquidation_value.
assignment2_post_tax_portfolio_value = \
    PortfolioHelpers.get_post_tax_liquidation_value(
        current_value=portfolio_value_by_the_end_of_week_2,
        capital_gain=max(0, portfolio_value_by_the_end_of_week_2 - portfolio_value_by_the_end_of_week_0),
        dividends= sum(map(lambda _dividend: _dividend, dividends_collection)),
        capital_gain_tax_rate=0.15,
        dividends_tax_rate=0.15)

myprint([f'The pre-tax value of the portfolio: {assignment2_portfolio_value}',
         f'The post-tax value of the portfolio: {assignment2_post_tax_portfolio_value}'])
