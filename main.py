import streamlit as st
import calculations
import pandas as pd


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





# Initialize session state
if 'salary_increases' not in st.session_state:
    st.session_state.salary_increases = []
if 'df' not in st.session_state:
    st.session_state.salary_increases_df = pd.DataFrame(columns=["salary", "start_year"])

# Temporary variables to hold input values before updating session state
temp_salary = st.number_input("New Salary", step=100, value=0)
temp_start_year = st.number_input("Starting in how many years?", min_value=0, value=0)

# Add a button to save the new increase only after inputs are filled
if st.button("Save Salary Increase"):
    # Append the new values to session state only after clicking "Save Salary Increase"
    st.session_state.salary_increases.append({"salary": temp_salary, "start_year": temp_start_year})

# Display input fields for each salary increase from session state
for index, increase in enumerate(st.session_state.salary_increases):
    salary = st.number_input(f"Salary Increase #{index + 1}:", value=increase["salary"], step=100, key=f"salary_{index}")
    start_year = st.number_input(f"Start Year for Increase #{index + 1}:", value=increase["start_year"], min_value=0, key=f"year_{index}")
    # Update session state with any modifications made to the inputs
    st.session_state.salary_increases[index] = {"salary": salary, "start_year": start_year}

# Add salary increases to the DataFrame
st.session_state.salary_increases_df = pd.DataFrame(st.session_state.salary_increases)

# Loop through the DataFrame and apply salary updates to pre_retirement_df
for _, increase in st.session_state.salary_increases_df.iterrows():
    salary = increase['salary']
    start_year = increase['start_year']
    start_month = (start_year * 12)+1
     
    calculations.set_salary(pre_retirement_df, salary, start_month)
    calculations.calc_salary_inflation(pre_retirement_df,salary_inflation,start_month+12)
    calculations.set_monthly_payment(pre_retirement_df)
    calculations.add_lump_sum(pre_retirement_df, balance, 1)
    calculations.calc_total_payment(pre_retirement_df)
    calculations.calc_fv_col(pre_retirement_df)
    fv_total = calculations.calc_fv_total(pre_retirement_df)



# Initialize session state
if 'future_value' not in st.session_state:
    st.session_state.future_value = fv_total
st.session_state.future_value = fv_total

st.write("### Future Value")
col1, col2 = st.columns(2)
with col1:
	st.metric(label="Unadjusted Value", value=f"${st.session_state.future_value:,.0f}", label_visibility="visible")

inflation_adjusted_fv = st.session_state.future_value / (1+inflation_rate/100)**years_to_retirement
with col2:
	st.metric(label="Inflation Adjusted Value", value=f"${inflation_adjusted_fv:,.0f}", label_visibility="visible")


st.write(pre_retirement_df)







# Display the updated DataFrame
st.write(st.session_state.salary_increases_df)


