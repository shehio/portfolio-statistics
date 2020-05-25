from assignments.assignment_helpers import Helpers
from src.iohelpers import IoHelpers
from src.portfolio import Portfolio

# stock => book_to_price, IBES_2Yr_growth_rate, SPS_5Yr_growth_rate
stock_stats = IoHelpers.get_stock_stats_from_russel()

current_tickers = ["AAPL", "ALK", "AMZN", "ADBE", "GOOG", "CSCO", "CIT", "DAL", "EA", "GS",
                   "IBM", "LYFT", "EXPE", "MS", "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

current_date = Helpers.assignment7_end_date

_, _, _, portfolio, _, _, _, _ = Helpers.load_vars_from_pickle('./../pkls/a7.pkl')

portfolio_weights = portfolio.get_weights(current_date)
current_securities = portfolio_weights.keys()
total_book_to_price = 0
total_ibes_2_years = 0
total_sps_5_years = 0

for security in current_securities:
    print(f'{security.ticker}: {stock_stats[security.ticker]}')
    book_to_price, ibes_2_years, sps_5_years = stock_stats[security.ticker]
    weight = portfolio_weights[security]
    total_book_to_price += weight * book_to_price
    total_ibes_2_years += weight * ibes_2_years
    total_sps_5_years += weight * sps_5_years


print(f'Total Book To Price: {total_book_to_price}')
print(f'Total IBES Two-Year Growth-Rate: {total_ibes_2_years}')
print(f'Total SPS Five-Year Growth-Rate: {total_sps_5_years}')