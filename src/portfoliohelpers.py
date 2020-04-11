from .currency import Currency
from .feecalculator import FeeFrequency
from .portfolio import Portfolio
from .security import Security
from .transaction import Transaction

import datetime
import numpy as np


class PortfolioHelpers:

    @staticmethod
    def collect_dividend(portfolio):
        # Go through all the securities and check if we got any dividend today.
        pass

    @staticmethod
    def update_splits(portfolio):
        # Go through all the securities and check if any splits occurred.
        pass

    @staticmethod  # Assume all cash is of the same currency for now. Also, assume all trades are long for now.
    def make_trade(portfolio, security, transaction: Transaction):
        if portfolio.contains(security):
            old_security = portfolio.get_security(security)
            security.shares += old_security.shares
            new_securities = portfolio.securities
            index = np.where(new_securities == old_security)
            np.delete(new_securities, index, None)
            np.append(new_securities, security)
        else:
            new_securities = portfolio.securities
            np.append(new_securities, security)

        cash = Security('CASH', portfolio.cash.shares - transaction.price, 'None', Currency.Dollars)
        return Portfolio(cash, transaction.date, new_securities)

    @staticmethod
    def get_fee(portfolio: Portfolio, annual_fee: float, fee_frequency: FeeFrequency, date: datetime):
        if fee_frequency == FeeFrequency.weekly:
            fee = annual_fee / 52
        elif fee_frequency == FeeFrequency.monthly:
            fee = annual_fee / 12
        elif fee_frequency == FeeFrequency.yearly:
            fee = annual_fee

        return fee * portfolio.get_value(date)
