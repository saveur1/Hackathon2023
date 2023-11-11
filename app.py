import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.express as px
from streamlit_option_menu import option_menu
st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")

# Load the Excel workbook
excel_file = 'CPI.xlsx'
# ALL RWANDA
def all():
  # Select the worksheet you want to display
  sheet_name = 'rw'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.header("CONSUMER PRICE INDEX (All Rwanda)")
  st.subheader("Base: 2014; Reference: February 2014=100")
    
  # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"])

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
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"])

  fig = px.line(df, x='YEAR', y=selected_columns, title='Consumption by Year (Source: National Institute of Statistics of Rwanda)')
  
  st.plotly_chart(fig,use_container_width=True)
  
# ALL RWANDA
def Urban():
  # Select the worksheet you want to display
  sheet_name = 'urban1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.header("CONSUMER PRICE INDEX (All Urban)")
  st.subheader("Base: 2014; Reference: February 2014=100")
    
  # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"])

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
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"])

  fig = px.line(df, x='YEAR', y=selected_columns, title='Consumption by Year (Source: National Institute of Statistics of Rwanda)')
  
  st.plotly_chart(fig,use_container_width=True)

# ALL RWANDA
def Rural():
  # Select the worksheet you want to display
  sheet_name = 'rural1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.header("CONSUMER PRICE INDEX (All Rural)")
  st.subheader("Base: 2014; Reference: February 2014=100")
    
  # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"])

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
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"])

  fig = px.line(df, x='YEAR', y=selected_columns, title='Consumption by Year (Source: National Institute of Statistics of Rwanda)')
  
  st.plotly_chart(fig,use_container_width=True)
# ALL RWANDA

def Other_Indices():
  # Select the worksheet you want to display
  sheet_name = 'other_indices1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.header("CONSUMER PRICE INDEX (Other indices), Urban only")
  st.subheader("Base: 2014; Reference: February 2014=100")
    
  # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","Local Goods Index","Local Food and non-alcoholic beverages","Local Housing, water, electricity, gas and other fuels","Local Transport","Imported Goods Index","Imported Food and non-alcoholic beverages","Imported Furnishing, household equipment","Imported Transport","Fresh Products(1) index","Energy index","General Index excluding fresh Products and energy(2)"])

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
  selected_columns = st.multiselect('Filter: ',df.columns,default=["Local Goods Index","Imported Goods Index","Fresh Products(1) index","Energy index"])

  fig = px.line(df, x='YEAR', y=selected_columns, title='Consumption by Year (Source: National Institute of Statistics of Rwanda)')
  
  st.plotly_chart(fig,use_container_width=True)
# ALL RWANDA
def sideBar():
 # Create a sidebar
 sidebar = st.sidebar

 #  Add a header to the sidebar
 sidebar.header('Sidebar Header')

 # Add a text element to the sidebar
 sidebar.write('This is some text in the sidebar.')

 with st.sidebar:
    selected=option_menu(
        menu_title="CONSUMER PRICE INDEX",
        options=["Home","Urban","Rural","Other_Indices","All Rwanda"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    all()
 if selected=="Urban":
    #st.subheader(f"Page: {selected}")
    Urban()
 if selected=="Rural":
    #st.subheader(f"Page: {selected}")
    Rural()
 if selected=="Other_Indices":
    #st.subheader(f"Page: {selected}")
    Other_Indices()
 if selected=="All Rwanda":
    #st.subheader(f"Page: {selected}")
    all()


sideBar()
