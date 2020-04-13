from src.currency import Currency
from src.forexhelpers import ForexHelpers

import numpy as np


def transform_values(values, forex_helpers, local_currency, foreign_currency):
    return np.array(list(map(
        lambda pair: pair[0] * pair[1].exchange_dict[local_currency][foreign_currency],
        zip(values, forex_helpers))))

# Q4)
# 4. Multi-currency portfolio return
# A U.S. dollar ($) based portfolio consists of assets denominated in dollars ($) and in euros (€) as
# follows:                       31 August           30 September
# U.S. equities                $38.1 million        $41.3 million
# Euro-zone equities           €31.3 million        €34.6 million
# Dollars per euro,               1.4380               1.3387
# spot exchange rate


forex_helpers_before = ForexHelpers()
forex_helpers_before.set_exchange_rate(Currency.Euros, Currency.Dollars, 1.4380)

forex_helpers_after = ForexHelpers()
forex_helpers_after.set_exchange_rate(Currency.Euros, Currency.Dollars, 1.3387)

us_equities = np.array([38.1, 41.3])
eu_equities = np.array([31.3, 34.6])


# For the portfolio for the month of September:
# a. calculate the rate of return in the base currency ($)
eu_equities_in_dollars = transform_values(
    eu_equities,
    [forex_helpers_before, forex_helpers_after],
    Currency.Euros,
    Currency.Dollars)
all_equities = eu_equities_in_dollars + us_equities
dates = np.array(['31 Aug', '30 Sep'])

print('Q4')
print('(a)')
print(f'Date            EU Equities in $')
for (date, equities) in zip(dates, eu_equities_in_dollars):
    print(f'{date}              {round(equities, 2)}')

print()
print(f'Date            Total Equities in $')
for (date, equities) in zip(dates, all_equities):
    print(f'{date}              {round(equities, 2)}')

print()
print(f'The return of equities in $: {100 * (all_equities[1] - all_equities[0]) / all_equities[0]}')
print()

# b. convert the return to a euro (€) based return
us_equities_in_euros = transform_values(
    us_equities,
    [forex_helpers_before,
     forex_helpers_after],
    Currency.Dollars,
    Currency.Euros)
all_equities = us_equities_in_euros + eu_equities

print('(b)')

print(f'Date            EU Equities in $')
for (date, equities) in zip(dates, us_equities_in_euros):
    print(f'{date}              {round(equities, 2)}')

print()
print(f'Date            Total Equities in $')
for (date, equities) in zip(dates, all_equities):
    print(f'{date}              {round(equities, 2)}')

print()
print(f'The return of equities in €: {100 * (all_equities[1] - all_equities[0]) / all_equities[0]}')
print()


