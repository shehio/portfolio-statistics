from src.iohelpers import IoHelpers
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency

from assignments.assignment_helpers import Helpers

import datetime
import numpy as np
import pickle

pkl_file = open('a1.pkl', 'rb')

portfolio_value_by_the_end_of_week_0 = pickle.load(pkl_file)
portfolio_value_by_the_end_of_week_1 = pickle.load(pkl_file)

income_returns = pickle.load(pkl_file)
price_returns = pickle.load(pkl_file)
total_returns = pickle.load(pkl_file)

week0_transaction_cost = pickle.load(pkl_file)
week1_transaction_cost = pickle.load(pkl_file)

pkl_file.close()

pkl_file = open('a2.pkl', 'rb')

week2_transaction_cost = pickle.load(pkl_file)
portfolio_value_by_the_end_of_week_2 = pickle.load(pkl_file)

income_returns = pickle.load(pkl_file)
price_returns = pickle.load(pkl_file)
total_returns = pickle.load(pkl_file)

new_portfolio = pickle.load(pkl_file)

weekly_fees = pickle.load(pkl_file)
dividends_collection = pickle.load(pkl_file)

pkl_file.close()

pkl_file = open('a3.pkl', 'rb')

income_returns = pickle.load(pkl_file)
price_returns = pickle.load(pkl_file)
total_returns = pickle.load(pkl_file)

weekly_fees = pickle.load(pkl_file)
dividends_collection = pickle.load(pkl_file)

new_portfolio = pickle.load(pkl_file)

week3_transaction_cost = pickle.load(pkl_file)

pkl_file.close()

new_portfolio.reset_dividends()
assignment3_end_date = datetime.date(2020, 4, 17)
assignment4_end_date = datetime.date(2020, 4, 24)

print('Q2: Adjusting for dividends, splits, management fees, ....')
new_portfolio = PortfolioHelpers.collect_dividends_if_any(new_portfolio, assignment3_end_date, assignment4_end_date)
dividends_collection = np.append(dividends_collection, new_portfolio.dividends)
new_portfolio = PortfolioHelpers.get_portfolio_after_splits(new_portfolio, assignment3_end_date, assignment4_end_date)

weekly_fee = PortfolioHelpers.get_fee(new_portfolio, Helpers.annual_fee, FeeFrequency.weekly, assignment3_end_date)
weekly_fees = np.append(weekly_fees, weekly_fee)

portfolio_cash_before_fee = new_portfolio.cash.shares
new_portfolio.discount_fee(weekly_fee)
Helpers.myprint([f'The cash before discounting the fee is: {portfolio_cash_before_fee}',
                 f'The weekly fee on: {assignment3_end_date} is: {weekly_fee}, '
                 f'cash in portfolio afterwards: {new_portfolio.cash}'])

print('Q3: Writing account summary.')
portfolio_value_by_the_end_of_week_3 = new_portfolio.get_value(assignment3_end_date)

fifth_income_return, fifth_price_return, fifth_total_return = Helpers.get_returns(new_portfolio,
                                                                                     portfolio_value_by_the_end_of_week_3,
                                                                                     assignment4_end_date)

IoHelpers.write_account_summary(
    account_name='yassers',
    dates=[Helpers.start_date, Helpers.assignment1_end_date, Helpers.assignment2_end_date, assignment3_end_date],
    deposits=[Helpers.that_initial_balance, 0, 100_000, 0],
    withdrawals=[0, 0, 0, 0],
    dividends=dividends_collection,
    fees=weekly_fees,
    transactional_costs=[week0_transaction_cost, week1_transaction_cost, 0, week3_transaction_cost, week4_transaction_cost],
    values=[
        portfolio_value_by_the_end_of_week_0,
        portfolio_value_by_the_end_of_week_1,
        portfolio_value_by_the_end_of_week_2,
        portfolio_value_by_the_end_of_week_3],
    income_returns=[first_income_return, second_income_return, third_income_return, fourth_income_return],
    price_returns=[first_price_return, second_price_return, third_price_return, fourth_price_return],
    total_returns=[first_total_return, second_total_return, third_total_return, fourth_total_return])
