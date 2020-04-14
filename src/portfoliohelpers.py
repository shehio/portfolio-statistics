from .apihelpers import ApiHelpers
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
            new_securities = np.delete(new_securities, index, None)
            new_securities = np.append(new_securities, security)
        else:
            new_securities = portfolio.securities
            np.append(new_securities, security)

        cash = Security('CASH', portfolio.cash.shares - transaction.price, 'None', Currency.Dollars)
        return Portfolio(cash, transaction.date, new_securities, dividends=portfolio.dividends)

    @staticmethod
    def get_portfolio_after_splits(portfolio: Portfolio, start_date: datetime, end_date: datetime):
        new_securities = portfolio.securities
        create_new_portfolio = False
        for stock in portfolio.securities:
            # print(stock.ticker)
            aggregate_splits = ApiHelpers.get_range_splits(stock.ticker, start_date, end_date)
            if aggregate_splits != 0:
                print(f'split for ticker: {stock.ticker} from {start_date} to {end_date} is: {aggregate_splits}')
                new_securities = PortfolioHelpers.__add_split_stock(new_securities, stock, aggregate_splits)
        if create_new_portfolio:
            return Portfolio(portfolio.cash, end_date, new_securities)
        else:
            return portfolio

    @staticmethod  # Requires major refactoring
    def collect_dividends_if_any(portfolio: Portfolio, start_date: datetime, end_date: datetime):
        new_cash = 0
        for stock in portfolio.securities:
            aggregate_dividends = ApiHelpers.get_range_dividends(stock.ticker, start_date, end_date)
            if aggregate_dividends != 0:
                print(f'dividends for ticker: {stock.ticker} from {start_date} to {end_date} is: {aggregate_dividends}')
                new_cash += aggregate_dividends * stock.shares
        if new_cash > 0:
            old_cash = portfolio.cash
            aggregate_cash = old_cash.shares + new_cash
            aggregate_cash = Security(old_cash.ticker, aggregate_cash, 'None', Currency.Dollars)
            return Portfolio(aggregate_cash, end_date, portfolio.securities, dividends=new_cash)
        else:
            return portfolio

    @staticmethod
    def get_fee(portfolio: Portfolio, annual_fee: float, fee_frequency: FeeFrequency, date: datetime):
        if fee_frequency == FeeFrequency.weekly:
            fee = annual_fee / 52
        elif fee_frequency == FeeFrequency.monthly:
            fee = annual_fee / 12
        elif fee_frequency == FeeFrequency.yearly:
            fee = annual_fee

        return fee * portfolio.get_value(date)

    @staticmethod
    def __add_split_stock(new_securities, stock, aggregate_splits):
        split_stock = stock
        split_stock.shares = split_stock.shares * aggregate_splits
        index = np.where(new_securities == stock)
        np.delete(new_securities, index, None)
        np.append(new_securities, split_stock)
        return new_securities
