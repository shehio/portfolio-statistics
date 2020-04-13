# 3. Income return, price return, and total return for a bond
# A Treasury bond with maturity date 15 May 2030 has a coupon rate of 6.250%. The coupon
# payments are semi-annual on 15 May and 15 November each year. The bond was recently
# quoted at the following clean prices per $100 of face value:
# 15 Feb 2020 150.08
# 15 Mar 2020 155.72

# Calculate, for the holding period from 15 Feb 2020 to 15 Mar 2020:
# a. the total rate of return;
total_return = ((155.72/150.08 - 1) + 0) * 100
# b. the price return;
price_return = (155.72/150.08 - 1) * 100
# c. the income return.
income_return = 0
print('Q3')
print(f'Income Return: {income_return}, Price Return: {price_return}, Total Return: {total_return}')
