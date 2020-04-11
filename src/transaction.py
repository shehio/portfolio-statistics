from .apihelpers import ApiHelpers
from .currency import Currency
from .security import Security

import datetime


class Transaction:  # Or trade?

    def __init__(self, date: datetime, security: Security, shares: int, transaction_fee, currency: Currency, long=True):
        self.date = date
        self.security = security
        self.shares = shares
        self.price = ApiHelpers.get_close_price(security.ticker, date) * shares + abs(shares) * transaction_fee
        self.currency = currency
        self.long = long
