from src.apihelpers import ApiHelpers
from src.currency import Currency
from src.iohelpers import IoHelpers
from src.portfolio import Portfolio
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory

from assignments.assignment_helpers import Helpers

import datetime
import numpy as np
import sympy

security_count = 20
maximum_security_weight = 0.2
maximum_cash_weight = 0.05
broker_transaction_cost = 0.001
fee_per_week = 0.01 * 0.01 * 2
annual_fee = 1.04 / 100
start_date = datetime.date(2020, 3, 27)
assignment1_end_date = datetime.date(2020, 4, 3)
assignment2_end_date = datetime.date(2020, 4, 9)
trade_date = datetime.date(2020, 4, 3)
weekly_fee_date = datetime.date(2020, 4, 3)
that_initial_balance = 1000 * 1000

current_tickers = ["AAPL", "ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT", "DAL", "EA", "GS",
                   "IBM", "LYFT", "EXPE", "MS", "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

weekly_fees = np.array([0])
dividends_collection = np.array([0])

# Q0
portfolio, week0_transaction_cost = Helpers.establish_equal_weight_portfolio(
    that_initial_balance,
    start_date,
    current_tickers,
    broker_transaction_cost)
Helpers.myprint([portfolio.__repr__()])

# Q1: Calculate the total value of the portfolio after the trades.
Helpers.myprint([f'The portfolios worth after making the initial transactions: {portfolio.get_value(start_date)}'])
IoHelpers.write_holdings('yassers', portfolio, start_date)

# Q2: Calculate the return of the transition period (prior to inception) based on the beginning value of $1 million.
portfolio_value_by_the_end_of_week_0 = portfolio.get_value(start_date)
first_income_return = 0
first_price_return = first_total_return = Helpers.get_price_return(
    value_before=that_initial_balance,
    value_after=portfolio_value_by_the_end_of_week_0)
Helpers.myprint([f'Total Return = Price Return = {first_total_return}, since dividends are all zero.'])

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
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
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
second_income_return = Helpers.get_div_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=new_portfolio.dividends)
second_price_return = Helpers.get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_1 - new_portfolio.dividends)
second_total_return = second_price_return + second_income_return
Helpers.myprint([f'Second Income Return = {second_income_return}',
         f'Second Price Return = {second_price_return}',
         f'Second Total Return = {second_total_return}'])

# ### Assignment 2:
#  Q1: Check your stocks for any splits or any dividends
# This implementation has bugs because splits and dividends should be checked simultaneously. Day by day.
dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio.reset_dividends()
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(new_portfolio, assignment1_end_date, assignment2_end_date)
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, assignment1_end_date, assignment2_end_date)

weekly_fee = PortfolioHelpers.get_fee(new_portfolio, annual_fee, FeeFrequency.weekly, assignment1_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
         f'The weekly fee on: {weekly_fee_date} is: {weekly_fee}, cash in portfolio afterwards: {new_portfolio.cash}'])

portfolio_value_by_the_end_of_week_2 = new_portfolio.get_value(assignment2_end_date)
third_income_return = Helpers.get_div_return(
    value_before=portfolio_value_by_the_end_of_week_1,
    value_after=new_portfolio.dividends)
third_price_return = Helpers.get_price_return(
    value_before=portfolio_value_by_the_end_of_week_1,
    value_after=portfolio_value_by_the_end_of_week_2 - new_portfolio.dividends)
third_total_return = third_price_return + third_income_return
Helpers.myprint([f'Third Income Return = {third_income_return}',
         f'Third Price Return = {third_price_return}',
         f'Third Total Return = {third_total_return}'])

dividends_collection = np.append(dividends_collection, new_portfolio.dividends)

# Q2:
# The returns calculated for the portfolio so far are net-of-fees returns. Calculate the following
# additional items, as of 10 April 2020:
# a. Calculate the linked net-of-fees return for the period from inception to 10 April 2020.
# Reminder: the inception of the portfolio measurement period is the market close on 27
# March 2020.
assignment2_portfolio_value = new_portfolio.get_value(assignment2_end_date)
net_of_fees_returns = Helpers.get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_2)
Helpers.myprint([f'Net of fees returns = {net_of_fees_returns}'])

# b. Calculate an approximate gross-of-fees return from inception to this date. Describe any assumptions used.
assignment2_portfolio_value = new_portfolio.get_value(assignment2_end_date)
gross_of_fees_returns = Helpers.get_price_return(
    value_before=portfolio_value_by_the_end_of_week_0,
    value_after=portfolio_value_by_the_end_of_week_2 + + sum(map(lambda fee: fee, weekly_fees)))
Helpers.myprint([f'Gross of fees returns = {gross_of_fees_returns}'])

# c. Assuming the portfolio is liquidated on 10 April 2020, calculate the post-tax post redemption
# return from inception to this date.Assume an income tax rate of 15% for both
# dividends and realized capital gains.
# Use this method: get_post_tax_liquidation_value.
assignment2_post_tax_portfolio_value = \
    PortfolioHelpers.get_post_tax_liquidation_value(
        current_value=portfolio_value_by_the_end_of_week_2,
        capital_gain=max(0, portfolio_value_by_the_end_of_week_2 - portfolio_value_by_the_end_of_week_0),
        dividends=sum(map(lambda _dividend: _dividend, dividends_collection)),
        capital_gain_tax_rate=0.15,
        dividends_tax_rate=0.15)

Helpers.myprint([f'The pre-tax value of the portfolio: {assignment2_portfolio_value}',
         f'The post-tax value of the portfolio: {assignment2_post_tax_portfolio_value}'])

# Assignment 3:
new_portfolio.reset_dividends()
assignment3_end_date = datetime.date(2020, 4, 17)
assignment2_end_date = datetime.date(2020, 4, 9)  # Market was closed on Good Friday.
assignment3_trade_date = datetime.date(2020, 4, 17)
week3_cash_infusion = 100_000

# Question 1:
# Your client has deposited $100,000 to the account on 9 April 2020. Assume that the cash flow occurred at the close.
# Add the amount to the liquidity reserve on that date and adjust the total portfolio value accordingly.
# The portfolio weights will temporarily be out of compliance with the 5% limit on cash,
# but don’t be concerned about that for now.
# Use the writeHoldings function to write a revised holdings text file for 2014-04-09,
# with this deposit added to the liquidity reserve.
print('Q1: Writing the modified holdings for last week.')
new_portfolio.cash.shares += week3_cash_infusion
portfolio_value_by_the_end_of_week_2 = new_portfolio.get_value(assignment2_end_date)
IoHelpers.write_holdings('yassers', new_portfolio, assignment2_end_date)

# Question 2:
# For the week from 9 April to 17 April, check your portfolio for any splits and adjust holdings accordingly.
# Check for any dividends and add to the liquidity reserve accordingly.
# Calculate the management fee and deduct from the liquidity reserve.
# On 17 April, purchase (and/or optionally sell) shares at the closing prices on that date to
# bring the portfolio weights back to within the mandate guidelines.
# Use the writeHoldings function to write a holdings text file for 2020-04-17, after the transactions on that date.
# Please submit your holdings files for all four weeks.
print('Q2: Adjusting for dividends, splits, management fees, ....')
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, assignment2_end_date, assignment3_end_date)
dividends_collection = np.append(dividends_collection, new_portfolio.dividends)

new_portfolio = PortfolioHelpers.get_portfolio_after_splits(new_portfolio, assignment2_end_date, assignment3_end_date)

weekly_fee = PortfolioHelpers.get_fee(new_portfolio, annual_fee, FeeFrequency.weekly, assignment2_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
         f'The weekly fee on: {assignment2_end_date} is: {weekly_fee}, '
         f'cash in portfolio afterwards: {new_portfolio.cash}'])

week3_transaction_cost = 0
security = Security('AAPL', 170, 'NASDAQ', Currency.Dollars)
transaction = Transaction(assignment3_trade_date, security, 170, broker_transaction_cost, Currency.Dollars)
week3_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

security = Security('ALK', 1500, 'NASDAQ', Currency.Dollars)
transaction = Transaction(assignment3_trade_date, security, 1500, broker_transaction_cost, Currency.Dollars)
week3_transaction_cost += transaction.transaction_cost
new_portfolio = PortfolioHelpers.make_trade(new_portfolio, security, transaction)

print(new_portfolio)
assert new_portfolio.cash.shares / new_portfolio.get_value(assignment3_end_date) < 0.05

IoHelpers.write_holdings('yassers', new_portfolio, assignment3_end_date)

# Question 3
# Value the portfolio as of 17 April and calculate the portfolio income return, price return, and total
# rate of return for the week ending 2020-04-17. Use the writeAccountSummary function to write an
# account summary text file for the four end-of-week dates through 2020-04-17.
print('Q3: Writing account summary.')
portfolio_value_by_the_end_of_week_3 = new_portfolio.get_value(assignment3_end_date)
fourth_income_return = Helpers.get_div_return(
    value_before=portfolio_value_by_the_end_of_week_2,
    value_after=new_portfolio.dividends)
fourth_price_return = Helpers.get_price_return(
    value_before=portfolio_value_by_the_end_of_week_2,
    value_after=portfolio_value_by_the_end_of_week_3 - new_portfolio.dividends)
fourth_total_return = fourth_income_return + fourth_price_return

IoHelpers.write_account_summary(
    account_name='yassers',
    dates=[start_date, assignment1_end_date, assignment2_end_date, assignment3_end_date],
    deposits=[that_initial_balance, 0, 100_000, 0],
    withdrawals=[0, 0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=[week0_transaction_cost, week1_transaction_cost, 0, week3_transaction_cost],
    values=[
        portfolio_value_by_the_end_of_week_0,
        portfolio_value_by_the_end_of_week_1,
        portfolio_value_by_the_end_of_week_2,
        portfolio_value_by_the_end_of_week_3],
    income_returns=[first_income_return, second_income_return, third_income_return, fourth_income_return],
    price_returns=[first_price_return, second_price_return, third_price_return, fourth_price_return],
    total_returns=[first_total_return, second_total_return, third_total_return, fourth_total_return])

# Question 4
# Assume that the initial cash flow of $1 million entered the portfolio at the end of the day on 23 March 2020.
# For the full period from 23 March 2020 to 17 April 2020, Calculate:
# a. The time-weighted rate of return
# b.The money-weighted rate of return. With your solution, show the equation that the rate must satisfy.
print('Q4: Time-Weighted Returns vs Money-Weighted Returns.')
week1_return = portfolio_value_by_the_end_of_week_1 / portfolio_value_by_the_end_of_week_0
week2_return = portfolio_value_by_the_end_of_week_2 / portfolio_value_by_the_end_of_week_1
week3_return = (portfolio_value_by_the_end_of_week_3 - week3_cash_infusion) / portfolio_value_by_the_end_of_week_2
time_weighted_rate_of_return = week3_return * week2_return * week1_return - 1

r = sympy.symbols('r', real=True)
equation = sympy.Eq(
    portfolio_value_by_the_end_of_week_3,
    portfolio_value_by_the_end_of_week_0 * (1 + r) + week3_cash_infusion * ((1 + r) ** (7 / 21)))
internal_rate_of_return = money_weighted_rate_of_return = sympy.solve(equation)
print(f'All values from solve: {internal_rate_of_return}')
Helpers.myprint([f'Time-Weighted rate of return = {time_weighted_rate_of_return}',
         f'Money-Weighted rate of return = {internal_rate_of_return[0]}'])

# Question 5
# Suppose that the portfolio valuation on 9 April is not available. For the period from 2020-04-03 to 2020-04-17:
# a. Calculate a return using the mid-point Dietz formula.
simple_dietz_return = \
    (portfolio_value_by_the_end_of_week_3 - portfolio_value_by_the_end_of_week_1 - week3_cash_infusion) / \
    (portfolio_value_by_the_end_of_week_1 + week3_cash_infusion / 2)

# b. Calculate a return using the modified (day-weighted) Dietz formula.
modified_dietz_return = \
    (portfolio_value_by_the_end_of_week_3 - portfolio_value_by_the_end_of_week_1 - week3_cash_infusion) / \
    (portfolio_value_by_the_end_of_week_1 + week3_cash_infusion * 8 / 14)

# c. Calculate the internal rate of return.
equation = sympy.Eq(
    portfolio_value_by_the_end_of_week_3,
    portfolio_value_by_the_end_of_week_1 * (1 + r) + week3_cash_infusion * (1 + r) ** (8 / 14))
money_weighted_rate_of_return_for_weeks_1_3 = sympy.solve(equation)
print(f'All values from solve: {money_weighted_rate_of_return_for_weeks_1_3}')

# d. For comparison, also calculate the true time-weighted return, using the 9 April valuation.
week2_return = (portfolio_value_by_the_end_of_week_2 - week3_cash_infusion) / portfolio_value_by_the_end_of_week_1
week3_return = portfolio_value_by_the_end_of_week_3 / portfolio_value_by_the_end_of_week_2
true_time_weighted_rate_of_return = week3_return * week2_return * week1_return - 1

Helpers.myprint(['Q5',
         f'Simple Dietz return = {simple_dietz_return}',
         f'Modified Dietz rate of return = {modified_dietz_return}',
         f'Money-Weighted rate of return = {money_weighted_rate_of_return_for_weeks_1_3[0]}',
         f'True Time-Weighted rate of return = {true_time_weighted_rate_of_return}'])

# Question 6
# For this question, we are interested in the time-weighted return from 2020-03-27 to 2020-04-17.
# As in question 5, suppose that the portfolio valuation on 9 April is not available.

# a. Calculate a return using the linked mid-point Dietz method.
week_3_1_simple_dietz_return = \
    (portfolio_value_by_the_end_of_week_3 - portfolio_value_by_the_end_of_week_1 - week3_cash_infusion) / \
    (portfolio_value_by_the_end_of_week_1 + week3_cash_infusion / 2)
week1_simple_dietz_return = (portfolio_value_by_the_end_of_week_1 - portfolio_value_by_the_end_of_week_0) / \
                            portfolio_value_by_the_end_of_week_0
linked_simple_dietz_return = (1 + week1_simple_dietz_return) * (1 + week_3_1_simple_dietz_return) - 1

# b. Calculate a return using the linked modified Dietz method.
week_3_1_modified_dietz_return = \
    (portfolio_value_by_the_end_of_week_3 - portfolio_value_by_the_end_of_week_1 - week3_cash_infusion) / \
    (portfolio_value_by_the_end_of_week_1 + week3_cash_infusion * 8 / 14)

linked_modified_dietz_return = (1 + week1_simple_dietz_return) * (1 + week_3_1_modified_dietz_return) - 1

# c. Calculate a return using the linked IRR method.
equation = sympy.Eq(
    portfolio_value_by_the_end_of_week_1,
    portfolio_value_by_the_end_of_week_0 * (1 + r))  # Should this be initial balance?
irr_1 = sympy.solve(equation)
print(f'All values from solve: {irr_1}')

equation = sympy.Eq(
    portfolio_value_by_the_end_of_week_3,
    portfolio_value_by_the_end_of_week_1 * (1 + r) + week3_cash_infusion * ((1 + r) ** 8 / 14))
irr_3 = sympy.solve(equation)
print(f'All values from solve: {irr_3}')

linked_money_weighted_rate_of_return = (1 + irr_1[0]) * (1 + irr_3[1]) - 1

# d. For comparison, also calculate the true time-weighted return, using the 9 April valuation.
# Calculated already from Question 5.
week1_return = portfolio_value_by_the_end_of_week_1 / portfolio_value_by_the_end_of_week_0
week2_return = portfolio_value_by_the_end_of_week_2 / portfolio_value_by_the_end_of_week_1
week3_return = (portfolio_value_by_the_end_of_week_3 - week3_cash_infusion) / portfolio_value_by_the_end_of_week_2
true_time_weighted_rate_of_return = week3_return * week2_return * week1_return - 1

Helpers.myprint(['Q6',
         f'Linked simple_dietz_return = {linked_simple_dietz_return}',
         f'Linked modified Dietz rate of return = {linked_modified_dietz_return}',
         f'Linked money-Weighted rate of return = {linked_money_weighted_rate_of_return}',
         f'True Time-Weighted rate of return = {true_time_weighted_rate_of_return}'])
