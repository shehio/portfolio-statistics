from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from assignments.assignment_helpers import Helpers

import numpy as np
import pickle

income_returns, price_returns, total_returns, new_portfolio, portfolio_values, transaction_costs,\
               weekly_fees, dividends_collection = Helpers.load_vars_from_pickle('a1.pkl')


# ### Assignment 2:
#  Q1: Check your stocks for any splits or any dividends
# This implementation has bugs because splits and dividends should be checked simultaneously. Day by day.
dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio.reset_dividends()
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(new_portfolio, Helpers.assignment1_end_date,
                                                            Helpers.assignment2_end_date)
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, Helpers.assignment1_end_date,
                                                          Helpers.assignment2_end_date)

weekly_fee = PortfolioHelpers.get_fee(new_portfolio, Helpers.annual_fee, FeeFrequency.weekly,
                                      Helpers.assignment1_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
                 f'The weekly fee on: {Helpers.weekly_fee_date} is: {weekly_fee}, cash in portfolio afterwards: {new_portfolio.cash}'])

portfolio_value_by_the_end_of_week_2 = new_portfolio.get_value(Helpers.assignment2_end_date)

portfolio_values = np.append(portfolio_values, portfolio_value_by_the_end_of_week_2)

third_income_return, third_price_return, third_total_return = Helpers.get_returns(
    new_portfolio,
    portfolio_values[1],
    Helpers.assignment2_end_date)

income_returns = np.append(income_returns, third_income_return)
price_returns = np.append(price_returns, third_price_return)
total_returns = np.append(total_returns, third_total_return)

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
assignment2_portfolio_value = new_portfolio.get_value(Helpers.assignment2_end_date)
net_of_fees_returns = Helpers.get_price_return(
    value_before=portfolio_values[0],
    value_after=portfolio_value_by_the_end_of_week_2)
Helpers.myprint([f'Net of fees returns = {net_of_fees_returns}'])

# b. Calculate an approximate gross-of-fees return from inception to this date. Describe any assumptions used.
assignment2_portfolio_value = new_portfolio.get_value(Helpers.assignment2_end_date)
gross_of_fees_returns = Helpers.get_price_return(
    value_before=portfolio_values[0],
    value_after=portfolio_value_by_the_end_of_week_2 + + sum(map(lambda fee: fee, weekly_fees)))
Helpers.myprint([f'Gross of fees returns = {gross_of_fees_returns}'])

# c. Assuming the portfolio is liquidated on 10 April 2020, calculate the post-tax post redemption
# return from inception to this date.Assume an income tax rate of 15% for both
# dividends and realized capital gains.
# Use this method: get_post_tax_liquidation_value.
assignment2_post_tax_portfolio_value = \
    PortfolioHelpers.get_post_tax_liquidation_value(
        current_value=portfolio_value_by_the_end_of_week_2,
        capital_gain=max(0, portfolio_value_by_the_end_of_week_2 - portfolio_values[0]),
        dividends=sum(map(lambda _dividend: _dividend, dividends_collection)),
        capital_gain_tax_rate=0.15,
        dividends_tax_rate=0.15)

Helpers.myprint([f'The pre-tax value of the portfolio: {assignment2_portfolio_value}',
                 f'The post-tax value of the portfolio: {assignment2_post_tax_portfolio_value}'])


# Saving data
output = open('a2.pkl', 'wb')

week2_transaction_cost = 0
transaction_costs = np.append(transaction_costs, week2_transaction_cost)

collection = np.array([income_returns, price_returns, total_returns, new_portfolio,
                       portfolio_values, transaction_costs, weekly_fees, dividends_collection])
Helpers.save_to_pickle(collection, 'a2.pkl')
