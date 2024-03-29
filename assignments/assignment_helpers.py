from src.apihelpers import ApiHelpers
from src.currency import Currency
from src.portfolio import Portfolio
from src.portfoliohelpers import PortfolioHelpers
from src.security import Security
from src.transaction import Transaction
from src.transactionshistory import TransactionsHistory

import datetime
import numpy as np
import pickle


class Helpers:
    security_count = 20
    maximum_security_weight = 0.2
    maximum_cash_weight = 0.05
    broker_transaction_cost = 0.001
    fee_per_week = 0.01 * 0.01 * 2
    annual_fee = 1.04 / 100

    start_date = datetime.date(2020, 3, 27)
    weekly_fee_date = datetime.date(2020, 4, 3)

    that_initial_balance = 1000 * 1000
    week3_cash_infusion = 100_000

    assignment1_end_date = datetime.date(2020, 4, 3)
    assignment2_end_date = datetime.date(2020, 4, 9)  # Market was closed on Good Friday.
    assignment3_end_date = datetime.date(2020, 4, 17)
    assignment4_end_date = datetime.date(2020, 4, 24)
    assignment5_end_date = datetime.date(2020, 5, 1)
    assignment6_1_end_date = datetime.date(2020, 5, 8)
    assignment6_2_end_date = datetime.date(2020, 5, 15)
    assignment7_end_date = datetime.date(2020, 5, 22)

    trade_date = datetime.date(2020, 4, 3)
    assignment3_trade_date = datetime.date(2020, 4, 17)

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
            transactions_history.push_transaction(_transaction)

        total_transaction_value = sum(map(
            lambda _transaction: _transaction.price,
            transactions_history.transactions))

        total_transaction_cost = sum(map(
            lambda _transaction: _transaction.transaction_cost,
            transactions_history.transactions))

        current_balance = initial_balance - total_transaction_value
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

    @staticmethod
    def get_returns(portfolio, total_value_last_week, calculation_date):
        portfolio_value_this_week = portfolio.get_value(calculation_date)
        income_return = Helpers.get_div_return(
            value_before=total_value_last_week,
            value_after=portfolio.dividends)
        price_return = Helpers.get_price_return(
            value_before=total_value_last_week,
            value_after=portfolio_value_this_week - portfolio.dividends)
        total_return = income_return + price_return

        return income_return, price_return, total_return

    @staticmethod
    def load_vars_from_pickle(file):
        pkl_file = open(file, 'rb')

        income_returns = pickle.load(pkl_file)
        price_returns = pickle.load(pkl_file)
        total_returns = pickle.load(pkl_file)

        new_portfolio = pickle.load(pkl_file)

        portfolio_values = pickle.load(pkl_file)
        transaction_costs = pickle.load(pkl_file)

        weekly_fees = pickle.load(pkl_file)
        dividends_collection = pickle.load(pkl_file)

        pkl_file.close()

        return income_returns, price_returns, total_returns, new_portfolio, portfolio_values, transaction_costs, \
               weekly_fees, dividends_collection

    @staticmethod
    def save_to_pickle(collection, file):

        output = open(file, 'wb')

        for var in collection:
            pickle.dump(var, output)

        output.close()
