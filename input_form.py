import streamlit as st

# Create a state for the form
def init_session_state():
    # Initialize form data and future value in session state
    if 'form_data' not in st.session_state:
        st.session_state.form_data = None
    if 'fv_total' not in st.session_state:
        st.session_state.fv_total = None
    if 'pre_retirement_df' not in st.session_state:
        st.session_state.pre_retirement_df = None


# Create the form
def create_form():
        
    with st.form(key="input_form"):
        # Create two columns for input fields
        col1, col2 = st.columns(2)

        # Column 1 inputs
        with col1:
            age = st.number_input("Age", min_value=0, value=30)
            balance = st.number_input("Starting Balance", min_value=0.0, value=10000.0)
            sal_sac = st.toggle("Is your pension Salary Sacrifice?",["Yes","No"])

            if not sal_sac:
                st.warning("Relief at source calculations are not implemented yet, sorry!")


        # Column 2 inputs
        with col2:
            retirement_age = st.number_input("Retirement Age", min_value=0, value=66)
            salary = st.number_input("Annual Salary", min_value=0.0, value=32000.0)

        #Because the rows aren't aligned...

        col1, col2 = st.columns(2)
        with col1:
            ee_contribution_rate = st.number_input("Your Contribution Rate (in %)", min_value=0.0, value=4.0)
            growth_rate = st.number_input("Annual Growth Rate (in %)", min_value=0.0, value=4.0)
            salary_inflation = st.number_input("Salary Inflation Rate (in %)", min_value=0.0, value=2.0)

        with col2:
            er_contribution_rate = st.number_input("Employer Contribution Rate (in %)", min_value=0.0, value=4.0)
            inflation_rate = st.number_input("Inflation Rate (in %)", min_value=0.0, value=2.0)
        

        # Calculate years to retirement
        years_to_retirement = retirement_age - age

        # Submit button
        submitted = st.form_submit_button("Submit")

    # Return all input values if the form is submitted
        if submitted:
            st.session_state.form_data = {
                "years_to_retirement": years_to_retirement,
                "balance": balance,
                "sal_sac": sal_sac,
                "salary": salary,
                "ee_contribution_rate": ee_contribution_rate,
                "er_contribution_rate": er_contribution_rate,
                "growth_rate": growth_rate,
                "salary_inflation": salary_inflation,
                "inflation_rate": inflation_rate
            }
        else:
            return None  # Return None if the form hasn't been submitted