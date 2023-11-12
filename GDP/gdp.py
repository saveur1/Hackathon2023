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
  table1 = 'in billion Rwf'
  table1a= 'Shares at current prices'
  table2= "2017 prices in billion"
  table2a= "2017 prices previous year"
  table2b= "2017 prices percentage point"

  # Read the worksheet into a Pandas DataFrame
  df1 = pd.read_excel(excel_file, table1)
  df2 = pd.read_excel(excel_file, table1a)
  df3 = pd.read_excel(excel_file, table2)
  df4 = pd.read_excel(excel_file, table2a)
  df5 = pd.read_excel(excel_file, table2b)
  df2 = df2.apply(lambda x: x * 100)

  st.header("Macro-economic aggregates")
  table1,table1A=st.columns(2)
  table2,table2A,table2B=st.columns(3)
  with table1:
    st.subheader("Table 1")
    st.caption("Gross Domestic product by Kind of Activity at current prices ( in billion Rwf)")
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
  with table1A:
    st.subheader("Table 1A")
    st.caption("Gross Domestic product by Kind of Activity Shares at current prices ( percentages)")
    # Create a multiselect widget
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=2)

    # Filter the DataFrame based on the selected columns
    df2_filtered = df2[selected_columns2]
    # Convert the year column to a Pandas datetime object
    df2_filtered['YEAR'] = pd.to_datetime(df2['YEAR'])

    # Extract the date from the Pandas datetime object
    df2_filtered['YEAR'] = df2_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df2_filtered,use_container_width=True)
    
  with table2:
    st.subheader("Table 2")
    st.caption("Gross Domestic product by Kind of Activity at constant 2017 prices ( in billion Rwf)")
    # Create a multiselect widget
    selected_columns3 = st.multiselect('Filter: ',df3.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=3)

    # Filter the DataFrame based on the selected columns
    df3_filtered = df3[selected_columns3]
    # Convert the year column to a Pandas datetime object
    df3_filtered['YEAR'] = pd.to_datetime(df3['YEAR'])

    # Extract the date from the Pandas datetime object
    df3_filtered['YEAR'] = df3_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df3_filtered,use_container_width=True)
  with table2A:
    st.subheader("Table 2A")
    st.caption("Gross Domestic product by Kind of Activity Growth rates at constant 2017 prices ( percentage change from previous year)")
    # Create a multiselect widget
    selected_columns4 = st.multiselect('Filter: ',df4.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=4)

    # Filter the DataFrame based on the selected columns
    df4_filtered = df4[selected_columns4]
    # Convert the year column to a Pandas datetime object
    df4_filtered['YEAR'] = pd.to_datetime(df4['YEAR'])

    # Extract the date from the Pandas datetime object
    df4_filtered['YEAR'] = df4_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df4_filtered,use_container_width=True)
    
  with table2B:
    st.subheader("Table 2B")
    st.caption("Gross Domestic product by Kind of Activity Growth rates at constant 2017 prices ( Percentage points)")
    # Create a multiselect widget
    selected_columns5 = st.multiselect('Filter: ',df5.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=5)

    # Filter the DataFrame based on the selected columns
    df5_filtered = df5[selected_columns5]
    # Convert the year column to a Pandas datetime object
    df5_filtered['YEAR'] = pd.to_datetime(df5['YEAR'])

    # Extract the date from the Pandas datetime object
    df5_filtered['YEAR'] = df5_filtered['YEAR'].dt.date
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df5_filtered,use_container_width=True)
  with table3:
    st.subheader("Table 1A")
    st.caption("Gross Domestic product by Kind of Activity Shares at current prices ( percentages)")
    # Create a multiselect widget
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=6)

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