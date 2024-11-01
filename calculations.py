import pandas as pd

def create_table(years_to_retirement):
    months_to_retirement = years_to_retirement*12
    columns = ['Salary','Contribution_Rate','Monthly_Payment','Annual_Interest_Rate',
               'Monthly_Interest_Rate','Number_of_Periods','Future_Value',
               'Lump_Sum','Total_Payment']
    df = pd.DataFrame(index=range(months_to_retirement),columns=columns)

    df['Number_of_Periods'] = range(months_to_retirement,0,-1)

    return df


def calc_total_payment(df):
    df['Lump_Sum'] = df['Lump_Sum'].fillna(0)
    df['Total_Payment'] = df['Monthly_Payment'] + df['Lump_Sum']


def add_lump_sum(df, lump_sum_amount, month):
    df.loc[month-1, 'Lump_Sum'] = lump_sum_amount


def set_salary(df, salary, start_month):
    df.loc[start_month-1:, 'Salary'] = salary


def set_contribution_rate(df, rate, start_month):
    df.loc[start_month-1:, 'Contribution_Rate'] = rate/100


def set_monthly_payment(df):
    df['Monthly_Payment'] = df['Salary'] * df['Contribution_Rate'] / 12


def set_growth_rate(df, annual_rate, start_month):
    df.loc[start_month-1:, 'Annual_Interest_Rate'] = annual_rate
    df.loc[start_month-1:, 'Monthly_Interest_Rate'] = annual_rate/12


def calc_salary_inflation(df, annual_rate, start_month):
    for month in range(start_month-1, len(df), 12):
        df.loc[month:, 'Salary'] *=  (1+annual_rate/100)
        df.loc[month:, 'Monthly_Payment'] = df.loc[month:, 'Salary']/12


def calc_fv_col(df):
    df['Future_Value'] = (df['Total_Payment'] * 
                              (1 + df['Monthly_Interest_Rate']/100)**df['Number_of_Periods']
    )


def calc_fv_total(df):
    fv_total = df['Future_Value'].sum()
    return fv_total


