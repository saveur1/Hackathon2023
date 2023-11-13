import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.graph_objs as go
import plotly.express as px
import streamlit_option_menu as om
st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")


# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


#                          GROSS DOMESTIC PRODUCT AT MACRO ECCONOMIC LEVEL
# -------------------------------------------------------------------------------------------------------------
#load excel file
df1=pd.read_excel('Tutorial Spread.xlsx', sheet_name='macro_economic')
df1 = df1.rename(columns=lambda x: x.strip())

#Macro Economic Table
def MacroTable():
    with st.expander("GDP Summary Table"):
        showData = st.multiselect('Filter: ', df1.columns, default=[
                            "Years", "GDP at current prices", "Growth rate-cp", "Growth rate", "Implicit GDP deflator", "Growth rate-d", "GDP per head (in '000 Rwf)", "GDP per head (in current US dollars)"])
        st.dataframe(df1[showData],use_container_width=True)

def gdps_trends_chart():
    selected_columns = st.multiselect("Filters:", df1.columns, default=[
            "GDP at current prices", "GDP at constant 2017 prices"])
    fig = px.line(df1, x="Years", y=selected_columns)

    st.plotly_chart(fig, use_container_width=True)

def donut_chart():
    # Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Sector': ['Agriculture', 'Industry', 'Services','Adjustments'],
        'Percentage': [
                        round(df1['Agriculture'][23]*100),
                        round(df1['Industry'][23]*100), 
                        round(df1['Services'][23]*100),
                        round(df1['Adjustments'][23]*100)
                       ]
    })

    # Create the trace for the chart
    trace = go.Pie(labels=data['Sector'], values=data['Percentage'], hole=0.5)

    # Create the layout for the chart
    layout = go.Layout(
        title='Percentage of GDP by Sector',
        annotations=[dict(text='Frw '+str(df1["GDP at current prices"][23])+' billion', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # Create the figure and plot it using Streamlit
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
 

def barchart_with_line():
    df2=pd.read_excel('Tutorial Spread.xlsx', sheet_name='Table2A')
    df2 = df2.rename(columns=lambda x: x.strip())

    # Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Year': df2["Activity description"][18:],
        'Agriculture': [x*100 for x in df2['AGRICULTURE, FORESTRY & FISHING'][18:]],
        'Industry': [x*100 for x in df2['INDUSTRY'][18:]],
        'Services': [x*100 for x in df2['SERVICES'][18:]],
        'GDP': [x*100 for x in df2['GROSS DOMESTIC PRODUCT (GDP)'][18:]],
    })

    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Agriculture'], name='Agriculture')
    trace2 = go.Bar(x=data['Year'], y=data['Industry'], name='Industry')
    trace3 = go.Bar(x=data['Year'], y=data['Services'], name='Services')
    trace4 = go.Scatter(x=data['Year'], y=data['GDP'], name='GDP')

    # Create the layout for the chart
    layout = go.Layout(
        title='Percentage Change in Agriculture, Industry, Services, and GDP',
        xaxis=dict(title='Years'),
        yaxis=dict(title='Percentage Change', range=[-7.5, 18]),
        barmode='group'
    )

    # Create the figure and plot it using Streamlit
    fig = go.Figure(data=[trace1, trace2, trace3,trace4], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def expanditure_on_gdp():
    df3=pd.read_excel('Tutorial Spread.xlsx', sheet_name='Table4A')
    df3 = df3.rename(columns=lambda x: x.strip())
   # Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Year': df3["Years"][8:],
        'Gross capital formation': df3["Gross capital formation"][8:],
        'Exports G&S': df3["Exports of goods & services"][8:],
        'Households': df3["Households and NGOs"][8:],
        'Government':df3["Government"][8:],
        'Imports G&S': df3["Imports of goods & services"][8:],
        'GDP': df3["Gross Domestic Product"][8:]
    })

    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Gross capital formation'], name='Gross capital formation', marker=dict(color='blue'))
    trace2 = go.Bar(x=data['Year'], y=data['Exports G&S'], name='Exports G&S', marker=dict(color='orange'))
    trace3 = go.Bar(x=data['Year'], y=data['Households'], name='Households', marker=dict(color='green'))
    trace4 = go.Bar(x=data['Year'], y=data['Government'], name='Government', marker=dict(color='red'))
    trace5 = go.Bar(x=data['Year'], y=data['Imports G&S'], name='Imports G&S', marker=dict(color='yellow'))
    trace6 = go.Scatter(x=data['Year'], y=data['GDP'], name='GDP', line=dict(color='black'))

    # Create the layout for the chart
    layout = go.Layout(
        title='Proportions of GDP and Percentage Change in GDP',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Billions of Francs', range=[-5000, 19000]),
        barmode='stack'
    )

    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def MacroEconomicHome():
    st.title(":house: Macro Economic Aggregate")
    st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

    MacroTable()
    
    # GDPs Trending Chart
    gdps_trends_chart()

    st.subheader(""" 
    Gross Domestic Product 2022
    """)

    col1,col2 = st.columns((2))
    with col1:
        donut_chart()
    with col2:
        barchart_with_line()

    st.subheader("Expenditure on GDP (Billion Frw)")
    expanditure_on_gdp()
#                                       CONSUMER PRICE INDEX
# -------------------------------------------------------------------------------------------------------------

# Load the Excel workbook
excel_file = 'CPI.xlsx'

# ALL RWANDA
def all():
   st.title("CONSUMER PRICE INDEX (All Rwanda)")
   st.subheader("Base: 2014; Reference: February 2014=100")
   st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
   # Select the worksheet you want to display
   sheet_name = 'rw'

   # Read the worksheet into a Pandas DataFrame
   df = pd.read_excel(excel_file, sheet_name)
      
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
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
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
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
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
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
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
   #side bar
   st.sidebar.image("logo/logo2.png")

   with st.sidebar:
      selected= om.option_menu(
         menu_title=None,
         options=["Home","Urban","Rural","Other_Indices","All Rwanda"],
         icons=["house","wallet-fill","view-stacked","three-dots","card-text"],
         menu_icon="cast",
         default_index = 0
      )
   if selected=="Home":
      MacroEconomicHome()
   if selected=="Urban":
      Urban()
   if selected=="Rural":
      Rural()
   if selected=="Other_Indices":
      Other_Indices()
   if selected=="All Rwanda":
      all()


sideBar()
