import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.express as px
from streamlit_option_menu import option_menu
st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")

# Load the Excel workbook
excel_file = 'GDP.xlsx'
# ALL RWANDA
def all():
  # Select the worksheet you want to display
  sheet_name = 'Macro-economic aggregates'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.header("Macro-economic aggregates")

  # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GDP at current prices","GDP at constant 2017 prices","Implicit GDP deflator","GDP per head (in '000 Rwf)","GDP per head (in current US dollars)","Gross Domestic Product at current prices","Factor income from abroad, net","Gross National Disposible Income","Less Final consumption expenditure","Gross National Saving"])

  # Filter the DataFrame based on the selected columns
  df_filtered = df[selected_columns]
  # Convert the year column to a Pandas datetime object
  df_filtered['YEAR'] = pd.to_datetime(df['YEAR'])

  # Extract the date from the Pandas datetime object
  df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
  # Display the filtered DataFrame in Streamlit

  st.dataframe(df_filtered)
  
  st.subheader("Graph")
  column_names = df.columns.tolist()
  column_names.remove('YEAR')


   # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GDP at current prices"])

  fig = px.line(df, x='YEAR', y=selected_columns, title='Consumption by Year (Source: National Institute of Statistics of Rwanda)')
  
  st.plotly_chart(fig,use_container_width=True)
all()