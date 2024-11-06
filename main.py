import streamlit as st
import pandas as pd

import calculations
import input_form
import salary_increase



st.title("Pension Value Calculator")



# Call the form and get the input values
form_data = input_form.create_form()

# Initialise Salary Increase state
salary_increase.initialise_session_state()
salary_increase.display_salary_increases()
salary_increase.add_salary_increase()

# Initialise form, future value, and pre_retirement_df
input_form.init_session_state()


if st.session_state.form_data:
    # Perform calculations only if they haven’t been done yet
    st.session_state.pre_retirement_df = calculations.create_table(st.session_state.form_data['years_to_retirement'])
    
    # Perform calculations and set values in pre_retirement_df
    calculations.set_salary(st.session_state.pre_retirement_df, st.session_state.form_data['salary'], 1)
    calculations.set_growth_rate(st.session_state.pre_retirement_df, st.session_state.form_data['growth_rate'], 1)
    calculations.set_contribution_rate(st.session_state.pre_retirement_df, st.session_state.form_data['ee_contribution_rate'], 1)
    calculations.calc_salary_inflation(st.session_state.pre_retirement_df, st.session_state.form_data['salary_inflation'], 13)
    calculations.set_monthly_payment(st.session_state.pre_retirement_df)
    calculations.add_lump_sum(st.session_state.pre_retirement_df, st.session_state.form_data['balance'], 1)
    calculations.calc_total_payment(st.session_state.pre_retirement_df)
    calculations.calc_fv_col(st.session_state.pre_retirement_df)

    # Save future value total in session state
    st.session_state.fv_total = calculations.calc_fv_total(st.session_state.pre_retirement_df)

    # Display the future value and DataFrame
    fv_col, pv_col = st.columns(2)
    with fv_col:
        st.write(f"### Future Value: £{st.session_state.fv_total:,.0f}")
        
    with pv_col:
        fv = st.session_state.fv_total
        rate = st.session_state.form_data['inflation_rate']
        years = st.session_state.form_data['years_to_retirement']
        pv = calculations.calc_pv(fv, rate, years)
        st.write(f"### Inflation Adjusted: £{pv:,.0f}")


salary_increase.apply_salary_increase(st.session_state.pre_retirement_df)


if st.session_state.pre_retirement_df is not None:
    st.write(st.session_state.pre_retirement_df)
