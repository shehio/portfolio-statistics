from assignments.assignment_helpers import Helpers
from src.iohelpers import IoHelpers

import numpy as np


def my_round(num):
    return round(num, 3)


# stock => book_to_price, IBES_2Yr_growth_rate, SPS_5Yr_growth_rate
stock_stats = IoHelpers.get_stock_stats_from_russel()

current_tickers = ["AAPL", "ALK", "AMZN", "ADBE", "GOOG", "CSCO", "CIT", "DAL", "EA", "GS",
                   "IBM", "LYFT", "EXPE", "MS", "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

current_date = Helpers.assignment7_end_date

income_returns, price_returns, total_returns, portfolio, _, _, _, _ = Helpers.load_vars_from_pickle('./../pkls/a7.pkl')

portfolio_weights = portfolio.get_weights(current_date)
current_securities = portfolio_weights.keys()
total_book_to_price = 0
total_ibes_2_years = 0
total_sps_5_years = 0

for security in current_securities:
    stats = stock_stats[security.ticker]
    print(f'{security.ticker},{my_round(stats[0])},{my_round(stats[1])},{my_round(stats[2])}')
    book_to_price, ibes_2_years, sps_5_years = stock_stats[security.ticker]
    weight = portfolio_weights[security]
    total_book_to_price += weight * book_to_price
    total_ibes_2_years += weight * ibes_2_years
    total_sps_5_years += weight * sps_5_years


print(f'Total Book To Price: {my_round(total_book_to_price)}')
print(f'Total IBES Two-Year Growth-Rate: {my_round(total_ibes_2_years)}')
print(f'Total SPS Five-Year Growth-Rate: {my_round(total_sps_5_years)}')

print()

# CSV -> Text -> Table In MS WORD
for income_return, price_return, total_return in zip(income_returns, price_returns, total_returns):
    print(f'{my_round(income_return)},{my_round(price_return)},{my_round(total_return)}')

portfolio_total_returns = np.array([total_returns[i] for i in range(1, len(total_returns))])
russel_total_returns = np.array([-2.49, 12.62, 3.02, -1.22, -0.016, 3.93, -2.33, 3.54])
russel_growth_returns = np.array([-2.02, 11.37, 5.33, -0.67, -0.09, 5.09, -0.92, 3.15])
russel_value_returns = np.array([-3.06, 14.18, 0.211, -1.923, 0.079, 2.45, -4.21, 4.086])

# Comparing to Growth Returns:
s1 = russel_growth_returns - russel_total_returns
a1 = portfolio_total_returns - russel_growth_returns
e1 = portfolio_total_returns - russel_total_returns

print(f'corr between s1 and a1: {my_round(np.corrcoef(s1, a1)[1][0])}')
print(f'corr between e1 and s1: {my_round(np.corrcoef(e1, s1)[1][0])}')

# Comparing to Value Returns:
s2 = russel_value_returns - russel_total_returns
a2 = portfolio_total_returns - russel_value_returns
e2 = portfolio_total_returns - russel_total_returns

print(f'corr between s2 and a2: {my_round(np.corrcoef(s2, a2)[1][0])}')
print(f'corr between e2 and s2: {my_round(np.corrcoef(e2, s2)[1][0])}')
