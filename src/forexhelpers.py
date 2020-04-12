from .currency import Currency

import numpy as np


class ForexHelpers:
    def __init__(self):
        self.exchange_dict = {}
        pass

    def set_exchange_rate(self, currency_from: Currency, currency_to: Currency, rate: float):
        self.exchange_dict[currency_from] = {}
        self.exchange_dict[currency_from][currency_to] = rate

        self.exchange_dict[currency_to] = {}
        self.exchange_dict[currency_to][currency_from] = 1.0 / rate

    def get_exchange_rate(self, currency_from: Currency, currency_to: Currency):
        return self.exchange_dict[currency_from][currency_to]
