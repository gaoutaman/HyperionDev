"""Investment and Bond calculators"""

import math

# Print menu
print("--------------------------------------------------------------------")
print("Choose either 'investment' or 'bond' from the menu below to proceed:")
print("--------------------------------------------------------------------")
print("1. Investment - to calculate the amount of interest you'll earn on your investment")
print("2. Bond       - to calculate the amount you'll have to pay on a home loan")

# Choose calculator
setting = input().lower()

# Investment calculator
if setting == "investment":

    # get info
    print("Investment selected")
    deposit = float(input("How much money are you depositing? "))
    rate = float(
        input("Enter the interest rate. (Leave out '%' sign) "))
    years = float(input("How many years do you want to invest for? "))
    interest = input("Simple or Compound interest? ").lower()

    if interest == "simple":  # calculate simple interest
        amount = deposit * (1 + (rate/100) * years)
    elif interest == "compound":  # calculate compound interest
        amount = deposit * math.pow((1+(rate/100)), years)
    print(f"Total amount: {round(amount,2)}")

# Bond calculator
elif setting == "bond":

    # get info
    print("Bond selected")
    house = float(input("How much is the house worth? "))
    rate = float(input("Enter the interest rate. (Leave out '%' sign) "))
    months = float(
        input("How many months are you planning to take to repay the bond? "))
    i = rate/1200  # monthly interest rate
    # calculate repayment
    repayment = (i*house)/(1-math.pow(1+i, -months))
    print(f"Monthly repayment is {round(repayment,2)}")

# Error
else:
    print("Please select either 'investment' or 'bond' from the menu")
