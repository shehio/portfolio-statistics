import numpy as np


class TransactionsHistory:

    def __init__(self):
        self.transactions = np.Array()

    def push_transaction(self, transaction):  # What about Bonds?
        self.transactions.push(transaction)
