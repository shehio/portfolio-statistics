import datetime
import yfinance as yf


class ApiHelpers:

    @staticmethod
    def get_close_price(ticker: str, date: datetime) -> float:
        return ApiHelpers.__get_price_common(ticker, date, 'Close')

    @staticmethod
    def get_open_price(ticker: str, date: datetime) -> float:
        return ApiHelpers.__get_price_common(ticker, date, 'Open')

    @staticmethod
    def get_high_price(ticker: str, date: datetime) -> float:
        return ApiHelpers.__get_price_common(ticker, date, 'High')

    @staticmethod
    def get_low_price(ticker: str, date: datetime) -> float:
        return ApiHelpers.__get_price_common(ticker, date, 'Low')

    @staticmethod
    def __get_price_common(ticker: str, date: datetime, field: str) -> float:
        return yf.download(ticker, start=date, period="1d", progress=False)[field][0]
