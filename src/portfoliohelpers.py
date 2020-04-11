from .portfolio import Portfolio
from .feecalculator import FeeFrequency
import datetime


class PortfolioHelpers:

    @staticmethod
    def collect_dividend(portfolio):
        # Go through all the securities and check if we got any dividend today.
        pass

    @staticmethod
    def update_splits(portfolio):
        # Go through all the securities and check if any splits occurred.
        pass

    @staticmethod
    def get_fee(portfolio: Portfolio, annual_fee: float, fee_frequency: FeeFrequency, date: datetime):
        if fee_frequency == FeeFrequency.weekly:
            fee = annual_fee / 52
        elif fee_frequency == FeeFrequency.monthly:
            fee = annual_fee / 12
        elif fee_frequency == FeeFrequency.yearly:
            fee = annual_fee

        return fee * portfolio.get_value(date)
