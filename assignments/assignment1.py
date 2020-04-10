from src.apihelpers import ApiHelpers
from src.transaction import Transaction
import datetime
import numpy as np


def establish_portfolio(initial_balance, tickers, transaction_cost, date):
    equal_percentage = 1.0 / len(tickers)
    share_counts = np.array([])
    current_balance = initial_balance

    for ticker in tickers:
        security_price = ApiHelpers.get_close_price(ticker, date)
        shares = np.floor(initial_balance * equal_percentage / security_price)
        share_counts = np.append(share_counts, shares)
        transaction = Transaction(ticker, shares)
        balance_spent = shares * security_price
        current_balance = current_balance - balance_spent - shares * transaction_cost

    return share_counts


security_count = 20
maximum_security_weight = 0.2
maximum_cash_weight = 0.05
transaction_cost = 0.001
fee_per_week = 0.01 * 0.01 * 2
start_date = datetime.date(2020, 3, 27)
end_date = datetime.date(2020, 4, 3)
trade_date = datetime.date(2020, 4, 3)
weekly_fee_date = datetime.date(2020, 4, 3)
initial_balance = 1000 * 1000

tickers = ["AAPL","ALK", "AMZN", "ADBE", "GOOGL", "CSCO", "CIT",  "DAL", "EA", "GS",
            "IBM", "LYFT", "EXPE", "MS",  "MSFT", "NKE", "T", "TWTR", "UBER", "VMW"]

print(establish_portfolio(initial_balance, tickers, transaction_cost, start_date))
