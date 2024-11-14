import streamlit as st

# Create a state for the form
def init_session_state():
    # Initialize form data and future value in session state
    if 'ret_form_data' not in st.session_state:
        st.session_state.ret_form_data = None
    if 'ret_salary' not in st.session_state:
        st.session_state.ret_salary = None
    if 'retirement_df' not in st.session_state:
        st.session_state.retirement_df = None



# Create the form
def create_form():
        
    with st.form(key="retirement_form"):
        # Create two columns for input fields
        col1, col2 = st.columns(2)

        # Column 1 inputs
        with col1:
            years_of_retirement = st.number_input("Years of Retirement", min_value=0, value=34)
            ret_growth_rate = st.number_input("Annual Growth Rate (in %)", min_value=0.0, value=2.5)


        # Column 2 inputs
        with col2:
            lump_sum = st.number_input(f"Lump Sum % of Real Value", min_value=0.0, value=0.0)
            ret_inflation = st.number_input("Inflation Rate (in %)", min_value=0.0, value=2.0)

        # Submit button
        submitted = st.form_submit_button("Submit")

    # Return all input values if the form is submitted
        if submitted:
            st.session_state.ret_form_data = {
                "years_of_retirement": years_of_retirement,
                "ret_growth_rate": ret_growth_rate,
                "lump_sum": lump_sum,
                "ret_inflation": ret_inflation
            }
        else:
            return None  # Return None if the form hasn't been submitted