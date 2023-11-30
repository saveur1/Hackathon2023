import pandas as pd
import streamlit as st

# Load the Excel file
excel_file_path = 'CPI.xlsx'
sheet_name = 'urban1'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Rename the 'YEAR' column to 'year'
df = df.rename(columns={'YEAR': 'year'})

# Calculate monthly and annual inflation rates
df['year'] = pd.to_datetime(df['year'])
df.set_index('year', inplace=True)

# Calculate monthly inflation rate
df_monthly_inflation = df.pct_change()*100

# Calculate annual inflation rate using the provided formula
base_year = df.index.min().year
df_annual_inflation = ((df.resample('Y').ffill() - df.resample('Y').ffill().shift(1)) / df.resample('Y').ffill().shift(1)) * 100

# Streamlit app
st.title('Inflation Rate Calculator')

# Display the original data
st.subheader('Original Data')
st.dataframe(df)

# Display the monthly inflation rates
st.subheader('Monthly Inflation Rates')
st.dataframe(df_monthly_inflation)

# Display the annual inflation rates
st.subheader('Annual Inflation Rates')
st.dataframe(df_annual_inflation)

# Save the calculated data to a new Excel file if needed
df_monthly_inflation.to_excel('~/monthly_inflation.xlsx')
df_annual_inflation.to_excel('~/annual_inflation.xlsx')