# 3. Income return, price return, and total return for a bond
# A Treasury bond with maturity date 15 May 2030 has a coupon rate of 6.250%. The coupon
# payments are semi-annual on 15 May and 15 November each year. The bond was recently
# quoted at the following clean prices per $100 of face value:
# 15 Feb 2020 150.08
# 15 Mar 2020 155.72

# interest / percent / months * months from Nov * face value.
interest_accrued_til_feb = 6.25 / 100 / 12 * 3 * 100
interest_accrued_til_march = 6.25 / 100 / 12 * 4 * 100
price_in_feb = 150.08
price_in_march = 155.72
income_return = (interest_accrued_til_march - interest_accrued_til_feb) / price_in_feb * 100
price_return = (price_in_march/price_in_feb - 1) * 100
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
