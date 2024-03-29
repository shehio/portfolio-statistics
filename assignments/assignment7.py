from src.iohelpers import IoHelpers
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency

from assignments.assignment_helpers import Helpers

import numpy as np

income_returns, price_returns, total_returns, new_portfolio, portfolio_values, transaction_costs, \
               weekly_fees, dividends_collection = Helpers.load_vars_from_pickle('pkls/a62.pkl')

new_portfolio.reset_dividends()

# 1.	For the weeks from 15 May to 22 May,
# a.	Check your portfolio for any splits and adjust holdings accordingly.
# b.	Check for any dividends and add to the liquidity reserve accordingly.
# c.	Calculate the management fee and deduct from the liquidity reserve.
# d.	Trading is optional.
# e.	Use the writeHoldings function to write holdings text files for 2020-05-22.
# f.	Value the portfolio as of 22 May and calculate the portfolio income return,
#       price return, and total rate of return for the period from 2020-05-15 to 2020-05-22.
# g.	Use the writeAccountSummary function to write an account summary text file for the nine periods through 2020-05-22.

print('Q1: Adjusting for dividends, splits, management fees, and Writing account summary ....')

# Get the fee before checking for splits and adding the dividend for this week.
weekly_fee = PortfolioHelpers.get_fee(
    new_portfolio,
    Helpers.annual_fee,
    FeeFrequency.weekly,
    Helpers.assignment6_2_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {round(portfolio_cash_before_fee, 2)}',
                 f'The weekly fee on: {Helpers.assignment6_2_end_date} is: {round(weekly_fee, 2)}, '
                 f'cash in portfolio afterwards: {round(new_portfolio.cash.shares, 2)}'])

new_portfolio = PortfolioHelpers.collect_dividends_if_any(
    new_portfolio,
    Helpers.assignment6_2_end_date,
    Helpers.assignment7_end_date)

dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(
    new_portfolio,
    Helpers.assignment6_2_end_date,
    Helpers.assignment7_end_date)

IoHelpers.write_holdings('yassers', new_portfolio, Helpers.assignment7_end_date)

portfolio_value_by_the_end_of_current_week = new_portfolio.get_value(Helpers.assignment7_end_date)
portfolio_values = np.append(portfolio_values, portfolio_value_by_the_end_of_current_week)

income_return, price_return, total_return = \
    Helpers.get_returns(new_portfolio, portfolio_values[len(portfolio_values) - 2], Helpers.assignment7_end_date)

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
           Helpers.assignment5_end_date,
           Helpers.assignment6_1_end_date,
           Helpers.assignment6_2_end_date,
           Helpers.assignment7_end_date],
    deposits=[Helpers.that_initial_balance, 0, 100_000, 0, 0, 0, 0, 0, 0],
    withdrawals=[0, 0, 0, 0, 0, 0, 0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=transaction_costs,
    values=portfolio_values,
    income_returns=income_returns,
    price_returns=price_returns,
    total_returns=total_returns)


collection = np.array([income_returns, price_returns, total_returns, new_portfolio,
                       portfolio_values, transaction_costs, weekly_fees, dividends_collection])
Helpers.save_to_pickle(collection, 'pkls/a7.pkl')
