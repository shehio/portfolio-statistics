class Transaction:  # Or trade?

    def __init__(self, stock, shares, long=True):  # What about Bonds?
        self.stock = stock
        self.shares = shares
        self.long = long
