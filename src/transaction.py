class Transaction:  # Or trade?

    def __init__(self, stock, shares, price, currency, long=True):  # What about Bonds?
        self.stock = stock
        self.shares = shares
        self.price = price
        self.currency = currency
        self.long = long
