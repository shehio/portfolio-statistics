from src.apihelpers import ApiHelpers

from datetime import date


def test_get_close_price():
    assert 36.560001373291016 == ApiHelpers.get_close_price('DOW', date(2020, 4, 10))

