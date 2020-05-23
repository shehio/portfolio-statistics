import datetime
import numpy as np


def get_date(string_date: str) -> datetime.date:
    date_format = '%Y-%m-%d'
    return datetime.datetime.strptime(string_date, date_format)


if __name__ == '__main__':
    value_dict = {}
    date_strings = ['2020-03-27', '2020-04-03', '2020-04-09', '2020-04-17', '2020-04-24', '2020-05-01']
    # These are the numbers from the A-file at the end of 5/1.
    portfolio_values = [999001, 926389, 1180139 - 100000, 1200437, 1190158, 1186891]  # You should add the fees to these numbers.
    portfolio_beginning_values = [999001, 926389, 1180139, 1200437, 1190158, 1186891]

    for date_string, portfolio_value in zip(date_strings, portfolio_values):
        value_dict[get_date(date_string)] = portfolio_value

    # print(value_dict)

    iv0 = 100
    u1 = portfolio_values[0] / iv0

    ivt = iv0
    uts = []
    ivts = [ivt]

    beginning_value = portfolio_values[0]

    for i in range(0, len(portfolio_values) - 1):
        ut = portfolio_beginning_values[i] / ivts[i]
        uts.append(ut)
        ivt = portfolio_values[i + 1] / ut
        ivts.append(ivt)

print(f'Us: {np.round(uts, 0)}')
print(f'IV: {np.round(ivts, 2)}')
