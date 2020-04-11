from .currency import Currency


class Security:

    def __init__(self, ticker: str, shares: float, market: str, home_currency: Currency):
        self.ticker = ticker
        self.shares = shares
        self.market = market
        self.home_currency = home_currency

    def __hash__(self):
        return hash((self.ticker, self.market))

    def __repr__(self):
        return f'{self.ticker}: {self.shares}'
