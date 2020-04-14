from .apihelpers import ApiHelpers
from .security import Security

import datetime
import numpy as np


# Portfolio is immutable, you add your securities and that's that.
# If you want to add a new security, be it a stock, a bond, a foreign currency, an option, or a future, please
# refer to portfolio helpers.
class Portfolio:

    def __init__(
            self,
            cash: Security,
            inception_date: datetime,
            securities=np.array([]),
            transactions_history=None,
            constraints=None,
            dividends=0):
        self.cash = cash
        Portfolio.__validate_securities(securities)
        self.inception_date = inception_date
        self.securities = securities
        self.transactions_history = transactions_history
        self.constraints = constraints
        self.dividends = dividends

    def update_cash(self, cash):
        self.cash = cash

    def discount_fee(self, fee):
        updated_cash = self.cash.shares - fee
        self.cash.shares = updated_cash

    def get_value(self, date):
        return self.cash.shares + sum(map(
            lambda security: ApiHelpers.get_close_price(security.ticker, date) * security.shares, self.securities))

    def reset_dividends(self):
        self.dividends = 0

    def get_allocations(self):
        pass

    def contains(self, security):
        for _security in self.securities:
            if _security.ticker == security.ticker:
                return True
        return False

    def get_security(self, security):
        for _security in self.securities:
            if _security.ticker == security.ticker:
                return _security
        return None

    def get_pre_tax_liquidation_value(self, liquidation_date):
        return self.get_value(liquidation_date)

    def get_all_dividends(self, liquidation_date):
        current_dividends = sum(map(
            lambda security: ApiHelpers.get_range_dividends(security.ticker, self.inception_date, liquidation_date),
            self.securities))
        self.dividends += current_dividends
        self.cash.shares += current_dividends

    def write_holding(self, date):
        pass

    def __repr__(self):
        return f'{self.cash}, div: {self.dividends}, {self.securities}'

    @staticmethod
    def __validate_securities(securities):
        pass