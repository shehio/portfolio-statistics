from src.apihelpers import ApiHelpers
from src.currency import Currency
from src.iohelpers import IoHelpers
from src.portfolio import Portfolio
from src.portfoliohelpers import PortfolioHelpers
from src.portfoliohelpers import FeeFrequency
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory


import datetime
import numpy as np
import sympy

class Helpers:

    @staticmethod
    def get_div_return(value_before, value_after):
        return (value_after / value_before) * 100

    @staticmethod
    def get_price_return(value_before, value_after):
        return (value_after / value_before - 1) * 100

    @staticmethod
    def myprint(strings):
        print()
        for string in strings:
            print(string)
        print()

    @staticmethod
    def establish_equal_weight_portfolio(initial_balance, inception_date, tickers, broker_transaction_cost):
        equal_percentage = 1.0 / len(tickers)
        transactions_history = TransactionsHistory()
        securities = np.array([], dtype=Security)
        for ticker in tickers:
            security_price = ApiHelpers.get_close_price(ticker, inception_date)
            shares = np.floor(initial_balance * equal_percentage / security_price)

            _security = Security(ticker, shares, 'NASDAQ', Currency.Dollars)
            securities = np.append(securities, _security)

            _transaction = Transaction(inception_date, _security, shares, broker_transaction_cost, Currency.Dollars)

        total_transaction_cost = sum(map(
            lambda _transaction: _transaction.price,
            transactions_history.transactions))
        current_balance = initial_balance - total_transaction_cost
        current_balance = Security('CASHX', current_balance, 'None', Currency.Dollars)
        return Portfolio(current_balance, inception_date, securities, transactions_history), total_transaction_cost

    @staticmethod
    def make_assignment1_trade(_portfolio: Portfolio, _trade_date, _broker_transaction_cost):
        # Eliminate the repeatability here.
        _transaction_cost = 0
        _security = Security('AAPL', -1, 'NASDAQ', Currency.Dollars)
        _transaction = Transaction(_trade_date, _security, -1, _broker_transaction_cost, Currency.Dollars)
        _transaction_cost += _transaction.transaction_cost
        _new_portfolio = PortfolioHelpers.make_trade(_portfolio, _security, _transaction)

        _security = Security('ALK', 10, 'NASDAQ', Currency.Dollars)
        _transaction = Transaction(_trade_date, _security, 10, _broker_transaction_cost, Currency.Dollars)
        _transaction_cost += _transaction.transaction_cost
        return PortfolioHelpers.make_trade(_new_portfolio, _security, _transaction), _transaction_cost
