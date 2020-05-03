from src.iohelpers import IoHelpers
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency

from assignments.assignment_helpers import Helpers

import numpy as np

income_returns, price_returns, total_returns, new_portfolio, portfolio_values, transaction_costs, \
               weekly_fees, dividends_collection = Helpers.load_vars_from_pickle('a4.pkl')

new_portfolio.reset_dividends()

# 1. Holdings and account summary files
# For the week from 24 April to 01 May, check your portfolio for any splits and adjust holdings accordingly.
# Check for any dividends and add to the liquidity reserve accordingly. Calculate the management fee and
# deduct from the liquidity reserve. Trading is optional on 01 May. Use the writeHoldings function to write a
# holdings text file for 2020-05-01.
# Value the portfolio as of 01 May and calculate the portfolio income return, price return, and total rate of
# return for the period from 2020-04-24 to 2020-05-01. Use the writeAccountSummary function to write an
# account summary text file for the six periods through 2020-05-01. Submit the holdings and account
# summary.

print('Q1: Adjusting for dividends, splits, management fees, and Writing account summary ....')

# Get the fee before checking for splits and adding the dividend for this week.
weekly_fee = PortfolioHelpers.get_fee(
    new_portfolio,
    Helpers.annual_fee,
    FeeFrequency.weekly,
    Helpers.assignment4_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {round(portfolio_cash_before_fee, 2)}',
                 f'The weekly fee on: {Helpers.assignment4_end_date} is: {round(weekly_fee, 2)}, '
                 f'cash in portfolio afterwards: {round(new_portfolio.cash.shares, 2)}'])

new_portfolio = PortfolioHelpers.collect_dividends_if_any(
    new_portfolio,
    Helpers.assignment4_end_date,
    Helpers.assignment5_end_date)

dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(
    new_portfolio,
    Helpers.assignment4_end_date,
    Helpers.assignment5_end_date)

IoHelpers.write_holdings('yassers', new_portfolio, Helpers.assignment5_end_date)

portfolio_value_by_the_end_of_current_week = new_portfolio.get_value(Helpers.assignment5_end_date)
portfolio_values = np.append(portfolio_values, portfolio_value_by_the_end_of_current_week)

income_return, price_return, total_return = \
    Helpers.get_returns(new_portfolio, portfolio_values[len(portfolio_values) - 2], Helpers.assignment5_end_date)

income_returns = np.append(income_returns, income_return)
price_returns = np.append(price_returns, price_return)
total_returns = np.append(total_returns, total_return)

Helpers.myprint([f'Income Return =  {income_return}',
                 f'Price Return =   {price_return}',
                 f'Total Return =   {total_return}'])

# No trading.
transaction_costs = np.append(transaction_costs, 0)

IoHelpers.write_account_summary(
    account_name='yassers',
    dates=[Helpers.start_date,
           Helpers.assignment1_end_date,
           Helpers.assignment2_end_date,
           Helpers.assignment3_end_date,
           Helpers.assignment4_end_date,
           Helpers.assignment5_end_date],
    deposits=[Helpers.that_initial_balance, 0, 100_000, 0, 0, 0],
    withdrawals=[0, 0, 0, 0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=transaction_costs,
    values=portfolio_values,
    income_returns=income_returns,
    price_returns=price_returns,
    total_returns=total_returns)


collection = np.array([income_returns, price_returns, total_returns, new_portfolio,
                       portfolio_values, transaction_costs, weekly_fees, dividends_collection])
Helpers.save_to_pickle(collection, 'a5.pkl')
