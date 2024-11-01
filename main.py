import streamlit as st
import calculations


st.title("Pension Value Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
salary = col1.number_input("Salary", min_value=0, value=32000)
balance = col1.number_input("Starting Balance", min_value=0, value=10000)
growth_rate = col1.number_input("Annual Growth Rate (in %)", min_value=0.0, value=3.0)
contribution_rate = col2.number_input("Annual Salary Contribution (in %)", 
                                      min_value=0.0, value=8.0)
years_to_retirement = col2.number_input("Years to Retirement", min_value=1, value=40)
inflation_rate = col2.number_input("Inflation Rate (in %)", min_value=0.0, value=2.0)
salary_inflation = st.number_input("Salary Inflation Rate (in %)", min_value=0.0, value=2.0)



pre_retirement_df = calculations.create_table(years_to_retirement)
calculations.set_salary(pre_retirement_df, salary, 1)
calculations.set_growth_rate(pre_retirement_df,growth_rate,1)
calculations.set_contribution_rate(pre_retirement_df,contribution_rate,1)
calculations.calc_salary_inflation(pre_retirement_df,salary_inflation,13)
calculations.set_monthly_payment(pre_retirement_df)
calculations.add_lump_sum(pre_retirement_df, balance, 1)
calculations.calc_total_payment(pre_retirement_df)
calculations.calc_fv_col(pre_retirement_df)
fv_total = calculations.calc_fv_total(pre_retirement_df)



st.write("### Future Value")
col1, col2 = st.columns(2)
with col1:
	st.metric(label="Unadjusted Value", value=f"${fv_total:,.0f}", label_visibility="visible")

inflation_adjusted_fv = fv_total / (1+inflation_rate/100)**years_to_retirement
with col2:
	st.metric(label="Inflation Adjusted Value", value=f"${inflation_adjusted_fv:,.0f}", label_visibility="visible")


st.write(pre_retirement_df)