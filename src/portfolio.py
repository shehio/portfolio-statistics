import numpy as np


class Portfolio:

    def __init__(self, securities, cash, constraints):
        self.__validate__securities(securities)
        self.securities = securities
        self.cash = cash

    def get_value(self):
        pass

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
