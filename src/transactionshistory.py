import numpy as np


class TransactionsHistory:

    def __init__(self):
        self.transactions = np.array([])

    def push_transaction(self, transaction):
        self.transactions = np.append(self.transactions, transaction)
