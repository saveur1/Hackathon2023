import streamlit as st
import numpy as np
import pandas as pd
import time
st.selectbox('Select your favorite fruit:', [('apple', 'Apple'), ('banana', 'Banana'), ('orange', 'Orange')], key='fruit')

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(1)
    st.success("Done!")
    
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)

st.header("Test two")
sheet="rural1"
# Load the Excel file containing CPI data
data = pd.read_excel('CPI.xlsx',sheet)
# Create a selectbox to choose the base year
data[['Year', 'Month', 'Date']] = pd.to_datetime(data['YEAR'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d').str.split('-').tolist()

sorted_year=sorted(data['Year'].unique(), reverse=True)
sorted_month=sorted(data['Month'].unique(), reverse=True)
# Create a selectbox to choose the current year/month
current_year = st.selectbox('Select Current Year', sorted_year)
current_month = st.selectbox('Select Current Month', sorted_month)

# Create a slider with the label "Select years" and a range of years from 1980 to 2023
selected_years = st.slider("Select years",2009,2022, (2017,2022))

# Display the selected years
st.write(selected_years[1])