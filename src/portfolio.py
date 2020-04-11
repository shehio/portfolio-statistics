from .apihelpers import ApiHelpers

import numpy as np


class Portfolio:

    def __init__(self, cash, securities=np.array([]), transactions_history=None, constraints=None):
        self.cash = cash
        Portfolio.__validate_securities(securities)
        self.securities = securities
        self.transactions_history = transactions_history
        self.constraints = constraints

    def add_security(self, security):
        if np.isin(security, self.securities):
            self.securities.insert(self.securities.get(security) + security.shares)  # Correct this.
        else:
            np.append(self.securities, security)

    def update_cash(self, cash):
        self.cash = cash

    def get_value(self, date):
        return self.cash.shares + sum(map(
            lambda security: ApiHelpers.get_close_price(security.ticker, date) * security.shares, self.securities))

    def weekly_fee(self, fee_percentage):
        pass

    def get_allocations(self):
        pass

    def get_pre_tax_liquidation(self, date):
        pass

    def get_post_tax_liquidation(self, date, capital_gain_tax_rate):
        pass

    def write_holding(self):
        pass

    @staticmethod
    def __validate_securities(securities):
        pass

    def __repr__(self):
        return f'{self.cash}, {self.securities}'
