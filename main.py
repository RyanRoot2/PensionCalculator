import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Pension Value Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
salary = col1.number_input("Salary", min_value=0, value=32000)
balance = col1.number_input("Starting Balance", min_value=0, value=10000)
rate = col1.number_input("Interest Rate (in %)", min_value=0.0, value=3.0)
contribution = col2.number_input("Total Contribution (in %)", min_value=0.0, value=8.0)
years = col2.number_input("Years to Retirement", min_value=1, value=40)

# Calculate the future value
pmt = salary*contribution/100/12
p = balance
n = 12
t = years
r = rate/100

growth = (1+(r/n))**(n*t)

future_value = p*growth + (pmt*(growth-1)/(r/n))

# Display the future value.

st.write("### Future Value")
col1, col2 = st.columns(2)
col1.metric(label="Monthly Contribution", value=f"${pmt:,.2f}")
col2.metric(label="Future Value", value=f"${future_value:,.2f}")