from .currency import Currency


class ForexHelpers:
    def __init__(self):
        self.exchange_dict = {{}}
        pass

    def set_exchange_rate(self, currency_from: Currency, currency_to: Currency, rate: float):
        self.exchange_dict[currency_from][currency_to] = rate
        self.exchange_dict[currency_to][currency_from] = 1 / rate
