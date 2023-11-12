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
  sheet_name = 'in billion Rwf'
  sheet_name2= 'Shares at current prices'

   # Read the worksheet into a Pandas DataFrame
  df1 = pd.read_excel(excel_file, sheet_name)
  df2 = pd.read_excel(excel_file, sheet_name2)
  df2 = df2.apply(lambda x: x * 100)

  st.header("Macro-economic aggregates")
  table1,table2=st.columns(2)
  with table1:
    # Create a multiselect widget
    selected_columns = st.multiselect('Filter: ',df1.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"])

    # Filter the DataFrame based on the selected columns
    df_filtered = df1[selected_columns]
    # Convert the year column to a Pandas datetime object
    df_filtered['YEAR'] = pd.to_datetime(df1['YEAR'])

    # Extract the date from the Pandas datetime object
    df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df_filtered,use_container_width=True)
  with table2:
    # Create a multiselect widget
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=2)

    # Filter the DataFrame based on the selected columns
    df2_filtered = df2[selected_columns]
    # Convert the year column to a Pandas datetime object
    df2_filtered['YEAR'] = pd.to_datetime(df2['YEAR'])

    # Extract the date from the Pandas datetime object
    df2_filtered['YEAR'] = df2_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df2_filtered,use_container_width=True)
  ## Graph
  st.subheader("Graph")
  column_names = df1.columns.tolist()
  column_names.remove('YEAR')

  left,right=st.columns(2)
   # Create a multiselect widget
  with left:
    selected_columns = st.multiselect('Filter: ',df1.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"])
    
    fig= px.line(df1, x='YEAR', y=selected_columns, title='Gross Domestic product by Kind of Activity at current prices ( in billion Rwf)')
    fig.update_layout(yaxis_title="Rwf in billion")
    left.plotly_chart(fig,use_container_width=True)
  with right:
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=1)
    fig2 = px.line(df2, x='YEAR', y=selected_columns2, title='Gross Domestic product by Kind of Activity Shares at current prices ( percentages)')
    fig2.update_layout(yaxis_title="Percentage")
    right.plotly_chart(fig2,use_container_width=True)
all()