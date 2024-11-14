import streamlit as st
import pandas as pd

import calculations
import input_form
import salary_increase
import retirement_form
import retirement_calcs



st.title("Pension Value Calculator")
st.warning(
    "This tool provides illustrative calculations only and should not be considered financial advice. "
    "For personalized financial guidance, please consult with a licensed financial advisor. "
    "The information presented is not regulated and should not be relied upon for making investment or retirement decisions."
)




# Call the form and get the input values
form_data = input_form.create_form()

# Initialise Salary Increase state
salary_increase.initialise_session_state()
salary_increase.display_salary_increases()
salary_increase.add_salary_increase()

# Initialise form, future value, and pre_retirement_df
input_form.init_session_state()


if st.session_state.form_data:
    # Perform calculations if the form is submitted
    st.session_state.pre_retirement_df = calculations.create_table(st.session_state.form_data['years_to_retirement'])
    
    # Perform calculations and set values in pre_retirement_df
    df = st.session_state.pre_retirement_df
    salary = st.session_state.form_data['salary']
    start_month = 1
    salary_inflation = st.session_state.form_data['salary_inflation']

    calculations.set_growth_rate(st.session_state.pre_retirement_df, st.session_state.form_data['growth_rate'], 1)
    calculations.set_contribution_rate(st.session_state.pre_retirement_df, st.session_state.form_data['ee_contribution_rate'], 1)
    calculations.add_lump_sum(st.session_state.pre_retirement_df, st.session_state.form_data['balance'], 1)
    calculations.salary_df_functions(df, salary, start_month, salary_inflation)

salary_increase.apply_salary_increase(st.session_state.pre_retirement_df)



if st.session_state.fv_total is not None:
    # Display the future value and inflation adjusted value
    fv_col, pv_col = st.columns(2)
    with fv_col:
        st.write(f"### Future Value: £{st.session_state.fv_total:,.0f}")
        
    with pv_col:
        fv = st.session_state.fv_total
        rate = st.session_state.form_data['inflation_rate']
        years = st.session_state.form_data['years_to_retirement']
        pv = calculations.calc_pv(fv, rate, years)
        st.write(f"### Real Value: £{pv:,.0f}")


if st.session_state.fv_total is not None:
    st.write("### Retirement Data")
    retirement_form_data = retirement_form.create_form()
    retirement_form.init_session_state()

    if st.session_state.ret_form_data is not None:

        years_of_retirement = st.session_state.ret_form_data["years_of_retirement"]
        lump_sum = st.session_state.ret_form_data["lump_sum"]
        annual_growth = st.session_state.ret_form_data["ret_growth_rate"]
        inflation = st.session_state.ret_form_data["ret_inflation"]
        balance = pv

        monthly_payment = retirement_calcs.calculate_retirement_income(years_of_retirement, lump_sum, annual_growth, inflation, balance)
        
        monthly_col, annual_col = st.columns(2)

        with monthly_col:
            st.write(f"### Real Monthly Payment: £{monthly_payment:,.0f}")
        with annual_col:
            st.write(f"### Real Annual Income: £{monthly_payment*12:,.0f}")


if st.session_state.pre_retirement_df is not None:
    st.write("### Detailed growth table")
    st.write(st.session_state.pre_retirement_df)
