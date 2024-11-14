import pandas as pd

def create_table(starting_balance, target_salary, years_of_retirement, lump_sum, growth_rate, inflation):
    # Need to update this if I want to use it for a new methodology
    
    # Calculate the number of months in retirement
    months_of_retirement = years_of_retirement * 12
    monthly_withdrawal = target_salary / 12

    # Define the columns
    columns = ['Balance', 'Period', 'Withdrawal', 'Growth Rate', 'Inflation', 'Remaining Balance']

    # Create the DataFrame
    df = pd.DataFrame(index=range(months_of_retirement), columns=columns)

    # Fill in the initial balance and period
    df['Balance'] = starting_balance
    df['Period'] = range(months_of_retirement, 0, 1)
    df['Withdrawal'] = monthly_withdrawal

    return df


def calculate_retirement_income(years_of_retirement, lump_sum, annual_growth, inflation, balance):

    # Convert annual growth and inflation rates to monthly rates
    monthly_growth_rate = (1 + annual_growth/100) ** (1 / 12)
    monthly_inflation_rate = (1 + inflation/100) ** (1 / 12)

    r = (monthly_growth_rate / monthly_inflation_rate)-1

    # Total number of months in retirement
    months_of_retirement = years_of_retirement * 12
    n = months_of_retirement

    initial_balance = balance * (1 - lump_sum/100)

    # Using the amortization formula to calculate the fixed monthly withdrawal
    # Formula: PMT = P * [ r(1 + r)^n / (1+r)^n -1 ]
    # where:
    # PMT = fixed monthly payment
    # P = initial balance
    # r = effective monthly growth rate
    # n = number of periods (months)

    pmt =  initial_balance * (r*(1+r)**n)/(((1+r)**n)-1)

    return pmt