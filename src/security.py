class Security:

    def __init__(self, ticker, shares, market):
        self.ticker = ticker
        self.shares = shares
        self.market = market

    def __hash__(self):
        return hash((self.ticker, self.market))

    def __repr__(self):
        return f'{self.ticker}: {self.shares}'
