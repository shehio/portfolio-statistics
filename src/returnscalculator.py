from .portfolio import Portfolio

import datetime


class ReturnsCalculator:

    @staticmethod
    def calculate_nominal_returns(
            portfolio1: Portfolio,
            date1: datetime,
            portfolio2: Portfolio,
            date2: datetime):
        portfolio2_value = portfolio2.get_value(date2)
        portfolio1_value = portfolio1.get_value(date1)

        return portfolio2_value / portfolio1_value - 1

    @staticmethod
    def calculate_real_returns(
            portfolio1: Portfolio,
            cpi_index1: float,
            date1: datetime,
            portfolio2: Portfolio,
            cpi_index2: float,
            date2: datetime):
        portfolio2_value = portfolio2.get_value(date2)
        portfolio1_value = portfolio1.get_value(date1)

        return ((portfolio2_value / portfolio1_value) / (cpi_index2 / cpi_index1)) - 1
