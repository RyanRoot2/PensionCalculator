import streamlit as st
import pandas as pd

# Initialize session state variables
def initialise_session_state():
    if "salary_increases" not in st.session_state:
        st.session_state.salary_increases = []
    if "salary_increases_df" not in st.session_state:
        st.session_state.salary_increases_df = pd.DataFrame(columns=["salary", "start_year"])
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "temp_salary" not in st.session_state:
        st.session_state.temp_salary = 0
    if "temp_start_year" not in st.session_state:
        st.session_state.temp_start_year = 0

# Callback function to add salary increase to session state
def add_to_salary_increases():
    st.session_state.salary_increases.append({
        "salary": st.session_state.temp_salary,
        "start_year": st.session_state.temp_start_year
    })
    # Update the DataFrame with the latest list of increases
    st.session_state.salary_increases_df = pd.DataFrame(st.session_state.salary_increases)
    # Hide the form after submission
    st.session_state.show_form = False

# Function to display the salary increase form
def add_salary_increase():
    if st.button("Add Salary Increase"):
        st.session_state.show_form = True

    # Show form if "Add Salary Increase" has been clicked
    if st.session_state.show_form:
        with st.form(key="salary_increase_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("New Salary", value=st.session_state.temp_salary, key="temp_salary")
            with col2:
                st.number_input("Starting in how many years?", min_value=0, value=st.session_state.temp_start_year, key="temp_start_year")
            # Use form_submit_button with a callback
            st.form_submit_button("Save Salary Increase", on_click=add_to_salary_increases)

# Function to display saved salary increases
def display_salary_increases():
    st.write("### Saved Salary Increases")
    st.write(st.session_state.salary_increases_df)

# Main code
initialise_session_state()
display_salary_increases()
add_salary_increase()
