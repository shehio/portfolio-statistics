from src.performance.assetattribution import AssetAttribution
from src.performance.portfolioattribution import PortfolioAttribution

from src.currency import Currency
from src.forexhelpers import ForexHelpers

import numpy as np
import sympy


def my_print(strings):
    print()
    for string in strings:
        print(string)
    print()


def my_round(number):
    return round(number, 4)


def Q1():
    portfolio_attribution = PortfolioAttribution(
        portfolio_weights=np.array([0.8, 0.2]),
        benchmark_weights=np.array([0.6, 0.4]),
        portfolio_returns=np.array([7.3, 6.6]),
        benchmark_returns=np.array([8.2, 4.5]))

    print(f'Allocations: {portfolio_attribution.get_allocations()}')
    print(f'Selections: {portfolio_attribution.get_selections()}')
    print(f'Interactions: {portfolio_attribution.get_interactions()}')
    print(f'Total: {portfolio_attribution.get_total_attribution()}')


def bond_return():
    # interest / percent / months * months from Feb * face value.
    interest_accrued_til_march = 1.5 / 100 / 12 * 1 * 1000
    interest_accrued_til_april = 1.5 / 100 / 12 * 2 * 1000
    price_in_march = 1071
    price_in_april = 1081
    income_return = (interest_accrued_til_april - interest_accrued_til_march) / price_in_march * 100
    price_return = (price_in_april / price_in_march - 1) * 100
    total_return = income_return + price_return

    # Calculate, for the holding period from 15 Feb 2020 to 15 Mar 2020:
    print('Q3')
    # a. the total rate of return;
    print('(a)')
    print(f'Total Return: {total_return}')

    # b. the price return;
    print('(b)')
    print(f'Price Return: {price_return}')

    # c. the income return.
    print('(c)')
    print(f'Income Return: {income_return}')


def Q7():
    time_wrighted_return = 112 / 100


def transform_values(values, forex_helpers, local_currency, foreign_currency):
    return np.array(list(map(
        lambda pair: pair[0] * pair[1].exchange_dict[local_currency][foreign_currency],
        zip(values, forex_helpers))))


def Q8():

    euros_forex_helpers_before = ForexHelpers()
    euros_forex_helpers_before.set_exchange_rate(Currency.Euros, Currency.Dollars, 1.4380)

    euros_forex_helpers_after = ForexHelpers()
    euros_forex_helpers_after.set_exchange_rate(Currency.Euros, Currency.Dollars, 1.3387)

    gbp_forex_helpers_before = ForexHelpers()
    gbp_forex_helpers_before.set_exchange_rate(Currency.GBP, Currency.Dollars, 1.6042)

    gbp_forex_helpers_after = ForexHelpers()
    gbp_forex_helpers_after.set_exchange_rate(Currency.GBP, Currency.Dollars, 1.5646)

    uk_equities = np.array([41.3, 38.1])
    eu_equities = np.array([34.6, 31.3])

    # For the portfolio for the month of September:
    # a. calculate the rate of return in the base currency ($)
    eu_equities_in_dollars = transform_values(
        eu_equities,
        [euros_forex_helpers_before, euros_forex_helpers_after],
        Currency.Euros,
        Currency.Dollars)

    gbp_equities_in_dollars = transform_values(
        uk_equities,
        [gbp_forex_helpers_before, gbp_forex_helpers_after],
        Currency.GBP,
        Currency.Dollars)

    print(eu_equities_in_dollars)
    print(gbp_equities_in_dollars)

    gbp_equities_in_euros = transform_values(
        eu_equities_in_dollars,
        [euros_forex_helpers_before, euros_forex_helpers_after],
        Currency.Dollars,
        Currency.Euros)

    all_assets_in_dollars = eu_equities + gbp_equities_in_euros
    print(all_assets_in_dollars)

    print(all_assets_in_dollars[1] / all_assets_in_dollars[0])


if __name__ == '__main__':
    bond_return()
    Q8()
    print(((1 + 0.3102) / (1 + 0.0229)) - 1)
    print((-8.20 / 100 + 18.71 / 100 + 10.37 / 100) / 3)
    print((1 - 8.20 / 100) * (1 + 18.71 / 100) * (1 + 10.37 / 100) - 1)

    r = sympy.symbols('r', real=True)
    equation = sympy.Eq(4106,  3249 * (1 + r) + 560 * (1 + r) ** (10 / 30))
    solved_r = sympy.solve(equation)
    print(f'All values from solve: {solved_r}')

    modified_dietz_return = (4106 - 3249 - 560) / (3249 + 560 * 10 / 30)
    print(f'All values from solve: {modified_dietz_return}')


    return_1 = 3220 / 3249
    return_2 = 4106 / (3220 + 560)
    print(return_1 * return_2)

    Q1()
