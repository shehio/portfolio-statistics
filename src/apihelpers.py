import datetime
import pandas as pd
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
    def get_splits(ticker: str, date: datetime) -> float:
        security = yf.Ticker(ticker)
        return ApiHelpers.__extract_number_from_series(security.splits, date)

    @staticmethod
    def get_dividends(ticker: str, date: datetime) -> float:
        security = yf.Ticker(ticker)
        return ApiHelpers.__extract_number_from_series(security.dividends, date)

    @staticmethod
    def get_range_splits(ticker: str, start_date: datetime, end_date: datetime) -> float:
        security = yf.Ticker(ticker)
        return ApiHelpers.__extract_number_from_series_with_conditional_range(security.splits, start_date, end_date)

    @staticmethod
    def get_range_dividends(ticker: str, start_date: datetime, end_date: datetime) -> float:
        security = yf.Ticker(ticker)
        return ApiHelpers.__extract_number_from_series_with_conditional_range(security.dividends, start_date, end_date)

    @staticmethod
    def __get_price_common(ticker: str, date: datetime, field: str) -> float:
        return yf.download(ticker, start=date, period="1d", progress=False)[field][0]

    @staticmethod
    def __extract_number_from_series(series, date):
        data_frame = pd.DataFrame({'date': series.index, 'value': series.values})
        series_value = data_frame.loc[(data_frame['date'] == date.__str__())]['value']

        if series_value.size == 0:
            return 0
        return float(series_value)

    @staticmethod
    def __extract_number_from_series_with_conditional_range(series, start_date, end_date):
        data_frame = pd.DataFrame({'date': series.index, 'value': series.values})
        mask = (data_frame['date'] >= start_date.__str__()) & (data_frame['date'] <= end_date.__str__())
        data_frame = data_frame.loc[mask]['value']
        return float(sum(data_frame))