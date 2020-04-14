from .apihelpers import ApiHelpers
from .currency import Currency
from .security import Security

import datetime


class Transaction:  # Or trade?

    def __init__(self, date: datetime, security: Security, shares: int, transaction_fee, currency: Currency, long=True):
        self.date = date
        self.security = security
        self.shares = shares
        self.transaction_value = ApiHelpers.get_close_price(security.ticker, date) * shares
        self.transaction_cost = abs(self.transaction_value) * transaction_fee
        self.price = self.transaction_value + self.transaction_cost
        self.currency = currency
        self.long = long
