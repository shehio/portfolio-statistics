from src.iohelpers import IoHelpers
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency

from assignments.assignment_helpers import Helpers

import numpy as np

income_returns, price_returns, total_returns, new_portfolio, portfolio_values, transaction_costs, \
               weekly_fees, dividends_collection = Helpers.load_vars_from_pickle('a3.pkl')

new_portfolio.reset_dividends()

print('Q1: Adjusting for dividends, splits, management fees, and Writing account summary ....')
new_portfolio = PortfolioHelpers.collect_dividends_if_any(
    new_portfolio,
    Helpers.assignment3_end_date,
    Helpers.assignment4_end_date)

dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(
    new_portfolio,
    Helpers.assignment3_end_date,
    Helpers.assignment4_end_date)

IoHelpers.write_holdings('yassers', new_portfolio, Helpers.assignment4_end_date)

weekly_fee = PortfolioHelpers.get_fee(
    new_portfolio,
    Helpers.annual_fee,
    FeeFrequency.weekly,
    Helpers.assignment3_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
                 f'The weekly fee on: {Helpers.assignment3_end_date} is: {weekly_fee}, '
                 f'cash in portfolio afterwards: {new_portfolio.cash}'])

portfolio_value_by_the_end_of_week_4 = new_portfolio.get_value(Helpers.assignment4_end_date)
portfolio_values = np.append(portfolio_values, portfolio_value_by_the_end_of_week_4)

fifth_income_return, fifth_price_return, fifth_total_return = \
    Helpers.get_returns(new_portfolio, portfolio_values[3], Helpers.assignment4_end_date)

income_returns = np.append(income_returns, fifth_income_return)
price_returns = np.append(price_returns, fifth_price_return)
total_returns = np.append(total_returns, fifth_total_return)

transaction_costs = np.append(transaction_costs, 0)

IoHelpers.write_account_summary(
    account_name='yassers',
    dates=[Helpers.start_date,
           Helpers.assignment1_end_date,
           Helpers.assignment2_end_date,
           Helpers.assignment3_end_date,
           Helpers.assignment4_end_date],
    deposits=[Helpers.that_initial_balance, 0, 100_000, 0, 0],
    withdrawals=[0, 0, 0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=transaction_costs,
    values=portfolio_values,
    income_returns=income_returns,
    price_returns=price_returns,
    total_returns=total_returns)


collection = np.array([income_returns, price_returns, total_returns, new_portfolio,
                       portfolio_values, transaction_costs, weekly_fees, dividends_collection])
Helpers.save_to_pickle(collection, 'a4.pkl')
