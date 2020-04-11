from .portfolio import Portfolio

import datetime
from enum import Enum


class FeeFrequency(Enum):
    weekly = 1
    monthly = 2
    yearly = 3


class FeeCalculator:
    def __init__(self, annual_fee: float, fee_frequency: FeeFrequency):
        if fee_frequency == FeeFrequency.weekly:
            self.fee = annual_fee / 52
        elif fee_frequency == FeeFrequency.monthly:
            self.fee = annual_fee / 12
        elif fee_frequency == FeeFrequency.yearly:
            self.fee = annual_fee

    def get_fee(self, portfolio: Portfolio, date: datetime):
        return self.fee * portfolio.get_value(date)
