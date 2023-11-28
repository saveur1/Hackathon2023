import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.graph_objs as go
import plotly.express as px
import streamlit_option_menu as om
st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)


#Styles
with open("style.css") as t:
    st.markdown(f"<style>{ t.read() }</style>", unsafe_allow_html= True)


#                          GROSS DOMESTIC PRODUCT AT MACRO ECCONOMIC LEVEL
# -------------------------------------------------------------------------------------------------------------
#load excel file
df1=pd.read_excel('GDP.xlsx', sheet_name='macro_economic')
df1 = df1.rename(columns=lambda x: x.strip())

#Macro Economic Table
def MacroTable():
    with st.expander("Rwanda's GDP Macroeconomic Aggregates: A Historical Perspective from 1999 to 2022 Table"):
        showData = st.multiselect('Filter: ', df1.columns, default=[
                            "Years", "GDP at current prices", "GDP Growth rate at current prices", "Population Growth rate","Exchange Growth rate", "Implicit GDP deflator", "Implicit GDP deflator Growth rate", "GDP per head (in '000 Rwf)", "GDP per head (in current US dollars)"])
        st.dataframe(df1[showData],use_container_width=True)

def gdps_trends_chart():
    # Select the initial columns to be displayed
    initial_columns = ["GDP at current prices", "GDP at constant 2017 prices"]
    selected_columns= ['GDP at current prices','GDP at constant 2017 prices','Implicit GDP deflator', "GDP per head (in '000 Rwf)",'GDP per head (in current US dollars)','Gross Domestic Product at current prices']
    # Disable other columns except the initial columns
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns)
    fig = px.line(df1, x="Years", y=filtered_columns)
    fig.update_layout(title="Charting Rwanda's Economic Rise: A Line Graph Perspective on GDP from 1999 to 2022",yaxis_title="in billion Rwf",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

def gdp_growth_chart():
    # Select the initial columns to be displayed
    initial_columns = ['GDP Growth rate at current prices','GDP Growth rate at constant 2017 prices','Implicit GDP deflator Growth rate']
    selected_columns= ['GDP Growth rate at current prices','GDP Growth rate at constant 2017 prices','Implicit GDP deflator Growth rate']
    #st.text(df1.columns)
    # Disable other columns except the initial columns
    disabled_columns = list(set(df1.columns) - set(initial_columns))
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns)
    for column in filtered_columns:
         df1[column] *= 100
    df1[['Year', 'Month', 'Date']] = pd.to_datetime(df1['Years'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d').str.split('-').tolist()
    fig = px.line(df1, x=df1['Year'], y=filtered_columns)
    fig.update_layout(title="Charting Rwanda's Economic Rise: A Line Graph Perspective on GDP Growth in Percentage from 1999 to 2022",yaxis_title="Growth rate (Percentage)",yaxis=dict(title='Percentage Change', range=[-10,30]),xaxis=dict(
        rangeslider=dict(
            visible=True,
            range=[df1['Year'].min(), df1['Year'].max()]
        )
    ),legend=dict(yanchor="bottom", y=-0.5, xanchor="center", x=0.5),barmode="group")
    st.plotly_chart(fig, use_container_width=True)
#Calculate proportions of GDP contributed by various sectors.
def calculate_gdp_proportions():
    # Select the initial columns to be displayed
    initial_columns = ['Government','Private (includes changes in stock)']
    selected_columns= ['Government','Private (includes changes in stock)']
    #st.text(df1.columns)
    # Disable other columns except the initial columns
    disabled_columns = list(set(df1.columns) - set(initial_columns))
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns,key=np.random.randint(50,60))
    for column in filtered_columns:
         df1[column] *= 100
    fig = px.bar(df1, x="Years", y=filtered_columns)
    fig.update_layout(title="Total final consumption expenditure",yaxis_title="Percentage",yaxis=dict(title='Percentage Change', range=[0,100]),legend=dict(yanchor="bottom", y=-0.5, xanchor="center", x=0.5),barmode="group")
    st.plotly_chart(fig, use_container_width=True) 
      
#Analyze the relationship between gross capital formation and resource balance
def analyze_capital_formation_resource_balance():
    # Select the initial columns to be displayed
    initial_columns = ['Gross capital formation','Resource balance']
    selected_columns= ['Gross capital formation','Resource balance']
    #st.text(df1.columns)
    # Disable other columns except the initial columns
    disabled_columns = list(set(df1.columns) - set(initial_columns))
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns,key=np.random.randint(101, 111))
    for column in filtered_columns:
         df1[column] *= 100
    fig = px.bar(df1, x="Years", y=filtered_columns)
    fig.update_layout(title="gross capital formation and resource balance",yaxis_title="Percentage",yaxis=dict(title='Percentage Change', range=[-20,30]),legend=dict(yanchor="bottom", y=-0.5, xanchor="center", x=0.5),barmode="group")
    st.plotly_chart(fig, use_container_width=True)   
def ValueAddedBy():
    data = pd.DataFrame({
        'Year': df1["Years"],
        'Agriculture': df1["Agriculture"],
        'Industry': df1["Industry"],
        'Services': df1["Services"],
        'Adjustments':df1["Adjustments"]
    })     
    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Agriculture']*100, name='Agriculture', marker=dict(color='blue'))
    trace2 = go.Bar(x=data['Year'], y=data['Industry']*100, name='Industry', marker=dict(color='orange'))
    trace3 = go.Bar(x=data['Year'], y=data['Services']*100, name='Services', marker=dict(color='green'))
    trace4 = go.Bar(x=data['Year'], y=data['Adjustments']*100, name='Adjustments', marker=dict(color='red'))

    # Create the layout for the chart
    layout = go.Layout(
        title='Value added by: Agriculture, Industry, Services, Adjustments',
        legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5),
        xaxis=dict(title='Year'),
        yaxis=dict(title='Percentage'),
        barmode='group'
    )
    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
    
#Analyze national income and expenditure in Rwanda, measured in Rwandan francs (Rwf billions)
def analyze_rwf_national_income_expenditure():
    data = pd.DataFrame({
        'Year': df1["Years"],
        'Gross Domestic Product at current prices': df1["Gross Domestic Product at current prices"],
        'Factor income from abroad, net': df1["Factor income from abroad, net"],
        'Gross National Income': df1["Gross National Income"],
        'Current transfers, net':df1["Current transfers, net"],
        'Gross National Disposible Income': df1["Gross National Disposible Income"],
        'Less Final consumption expenditure': df1["Less Final consumption expenditure"],
        'Gross National Saving':df1["Gross National Saving"],
        'Less Gross capital formation':df1["Less Gross capital formation"],
        'Net lending to the rest of the world':df1["Net lending to the rest of the world"]
    })     
    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Gross Domestic Product at current prices'], name='Gross Domestic Product at current prices', marker=dict(color='blue'))
    trace2 = go.Bar(x=data['Year'], y=data['Factor income from abroad, net'], name='Factor income from abroad, net', marker=dict(color='orange'))
    trace3 = go.Bar(x=data['Year'], y=data['Gross National Income'], name='Gross National Income', marker=dict(color='green'))
    trace4 = go.Bar(x=data['Year'], y=data['Current transfers, net'], name='Current transfers, net', marker=dict(color='red'))
    trace5 = go.Bar(x=data['Year'], y=data['Gross National Disposible Income'], name='Gross National Disposible Income', marker=dict(color='brown'))
    trace6 = go.Bar(x=data['Year'], y=data['Less Final consumption expenditure'], name='Less Final consumption expenditure', marker=dict(color='indigo'))
    trace7 = go.Bar(x=data['Year'], y=data['Gross National Saving'], name='Gross National Saving', marker=dict(color='tomato'))
    trace8 = go.Bar(x=data['Year'], y=data['Less Gross capital formation'], name='Less Gross capital formation', marker=dict(color='Pink'))
    trace9 = go.Bar(x=data['Year'], y=data['Net lending to the rest of the world'], name='Net lending to the rest of the world', marker=dict(color='gray'))

    # Create the layout for the chart
    layout = go.Layout(
        title='National income and expenditure',
        legend=dict(yanchor="bottom", y=-1.8, xanchor="center", x=0.5),
        xaxis=dict(title='Year'),
        yaxis=dict(title='Billion in RWF'),
        barmode='group',
        height=1000
    )
    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4,trace5, trace6, trace7, trace8, trace9], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
def MemorandumItems():
  def population():
      st.info("Rwanda Population Growth rate")
      populationInMillion,populationGrowthRate=st.columns(2)
      with populationInMillion:
        fig = px.area(df1, x="Years", y="Total population (millions)")
        fig.update_layout(title="Total population (millions)",yaxis_title="Population in Million",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
      with populationGrowthRate:
        selectedColumn=df1["Population Growth rate"]*100
        fig = px.area(df1, x="Years", y=selectedColumn)
        fig.update_layout(title="population Growth Rate",yaxis_title="Growth Rate",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)  
  def ExchangeRate():
      st.info("Exchange rate: Rwf per US dollar")
      ExchangeRwfUSD,ExchangeGrowthRate=st.columns(2)
      with ExchangeRwfUSD:
        fig = px.area(df1, x="Years", y="Exchange rate: Rwf per US dollar")
        fig.update_layout(title="Exchange rate: Rwf per US dollar",yaxis_title="Rwf per US dollar",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
      with ExchangeGrowthRate:
        selectedColumn=df1["Exchange Growth rate"]*100
        fig = px.area(df1, x="Years", y=selectedColumn)
        fig.update_layout(title="Exchange growth rate: Rwf per US dollar",yaxis_title="Exchange Growth Rate (Percentage)",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
  population()  
  ExchangeRate()  

def barchart_with_line():
    df2=pd.read_excel('GDP.xlsx', sheet_name='Table2A')
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
        legend=dict(yanchor="bottom", y=-0.8, xanchor="center", x=0.5),
        xaxis=dict(title='Years'),
        yaxis=dict(title='Percentage Change', range=[-7.5, 18]),
        barmode='group'
    )

    # Create the figure and plot it using Streamlit
    fig = go.Figure(data=[trace1, trace2, trace3,trace4], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def MacroEconomicHome():
    st.subheader(":house: Rwanda's GDP Macroeconomic Aggregates")

    MacroTable()
    
    # GDPs Trending Chart
    st.subheader(""" 
    Gross Domestic Product (Rwf billions)
    """)
    gdps_trends_charts,gdp_growth_charts=st.columns(2)
    with gdps_trends_charts:
        gdps_trends_chart()
    with gdp_growth_charts:
        gdp_growth_chart()
        
    st.subheader(""" 
    Proportions of GDP
    """)
    Calculate_gdp_proportions,Analyze_capital_formation_resource_balance=st.columns(2)
    with Calculate_gdp_proportions:
      calculate_gdp_proportions()
    with Analyze_capital_formation_resource_balance:
      analyze_capital_formation_resource_balance()
    ValueAddedBy()    
    st.subheader("""National income and expenditure (Rwf billions)""")
    analyze_rwf_national_income_expenditure()
    st.subheader(""" Memorandum items""")
    MemorandumItems()
    
    
    st.subheader("""
    Rwanda's GDP Highlights in 2022: A Visual Representation
    """)

    col1,col2 = st.columns((2))
    with col1:
        donut_chart()
    with col2:
        barchart_with_line()
    
def kindOfActivity():
  excel_file = 'GDP.xlsx'
  # Select the worksheet you want to display
  table1 = 'TABLE1'
  table1a= 'TABLE1A'
  table2= "TABLE2"
  table2a= "TABLE2AA"
  table2b= "TABLE2B"
  table3 = "TABLE3"

  # Read the worksheet into a Pandas DataFrame
  df1 = pd.read_excel(excel_file, table1)
  df2 = pd.read_excel(excel_file, table1a)
  df3 = pd.read_excel(excel_file, table2)
  df4 = pd.read_excel(excel_file, table2a)
  df5 = pd.read_excel(excel_file, table2b)
  df6 = pd.read_excel(excel_file, table3)
  #df2 = df2.apply(lambda x: x * 100)
  #df4 = df4.apply(lambda x: x * 100)
  df2 = df2.apply(lambda x: x * 100 if x.name != 'YEAR' else x)
  df4 = df4.apply(lambda x: x * 100 if x.name != 'YEAR' else x)
  

  st.subheader("Gross Domestic product by Kind of Activity")
  section1,section2=st.columns(2)
  section3,section4=st.columns(2)

  with section1:
      graph1,table1= st.tabs(["📈 Chart", "🗃 Data"])
      graph1A,table1A= st.tabs(["📈 Chart", "🗃 Data"])
  with section2:
      graph2,table2= st.tabs(["📈 Chart", "🗃 Data"])
      graph2A,table2A= st.tabs(["📈 Chart", "🗃 Data"])
  with section3:
      graph2B,table2B= st.tabs(["📈 Chart", "🗃 Data"])
  with section4:
      graph3,table3= st.tabs(["📈 Chart", "🗃 Data"])  

  with table1:
    st.subheader("Table 1")
    st.caption("Gross Domestic product by Kind of Activity at current prices ( in billion Rwf)")

    # Create a multiselect widget
    selected_columns = st.multiselect('Filter: ',df1.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"])
    # Convert the Year column to datetime format
    df1["YEAR"] = pd.to_datetime(df1["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df1["YEAR"] = df1["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df1,use_container_width=True)
  with table1A:
    st.subheader("Table 1A")
    st.caption("Gross Domestic product by Kind of Activity Shares at current prices ( percentages)")
    
    # Create a multiselect widget
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=2)

    # Convert the Year column to datetime format
    df2["YEAR"] = pd.to_datetime(df2["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df2["YEAR"] = df2["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df2,use_container_width=True)
    
  with table2:
    st.subheader("Table 2")
    st.caption("Gross Domestic product by Kind of Activity at constant 2017 prices ( in billion Rwf)")

    # Create a multiselect widget
    selected_columns3 = st.multiselect('Filter: ',df3.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=3)

    # Convert the Year column to datetime format
    df3["YEAR"] = pd.to_datetime(df3["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df3["YEAR"] = df3["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df3,use_container_width=True)
    
  with table2A:
    st.subheader("Table 2A")
    st.caption("Gross Domestic product by Kind of Activity Growth rates at constant 2017 prices ( percentage change from previous year)")
    # Create a multiselect widget
    selected_columns4 = st.multiselect('Filter: ',df4.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"], key=4)

    # Convert the Year column to datetime format
    df4["YEAR"] = pd.to_datetime(df4["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df4["YEAR"] = df4["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df4,use_container_width=True)
    
  with table2B:
    st.subheader("Table 2B")
    st.caption("Gross Domestic product by Kind of Activity Growth rates at constant 2017 prices ( Percentage points)")

    # Create a multiselect widget
    selected_columns5 = st.multiselect('Filter: ',df5.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=5)

    # Convert the Year column to datetime format
    df5["YEAR"] = pd.to_datetime(df5["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df5["YEAR"] = df5["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df5,use_container_width=True)
      
  with table3:
    st.subheader("Table 3")
    st.caption("Gross Domestic product by Kind of Activity Deflators (2017=100)")

    # Create a multiselect widget
    selected_columns6 = st.multiselect('Filter: ',df6.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=6)

    # Convert the Year column to datetime format
    df6["YEAR"] = pd.to_datetime(df6["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df6["YEAR"] = df6["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df6,use_container_width=True)
    
  
  ## Graph Functions
 
  column_names = df1.columns.tolist()
  column_names.remove('YEAR')

  # Create a multiselect widget
  with graph1:
    selected_columns1 = st.multiselect('Filter: ',df1.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=0)
    
    fig= px.line(df1, x='YEAR', y=selected_columns1, title='GDP by Kind of Activity at current prices ( in billion Rwf)')
    fig.update_layout(yaxis_title="Rwf in billion",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph1.plotly_chart(fig,use_container_width=True)
  
  with graph1A:
    selected_columns2 = st.multiselect('Filter: ',df2.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=11)
    
    fig= px.line(df2, x='YEAR', y=selected_columns2, title='GDP by Kind of Activity Shares at current prices ( percentages)')
    fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph1A.plotly_chart(fig,use_container_width=True)
    
  with graph2:
    selected_columns3 = st.multiselect('Filter: ',df3.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=12)
    fig2 = px.line(df3, x='YEAR', y=selected_columns3, title='GDP by Kind of Activity at constant 2017 prices(in billion Rwf) ')
    fig2.update_layout(yaxis_title="in billion Rwf",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph2.plotly_chart(fig2,use_container_width=True)
    
  with graph2A:
    selected_columns4 = st.multiselect('Filter: ',df4.columns,default=["GROSS DOMESTIC PRODUCT (GDP)"],key=13)
    fig2 = px.bar(df4, x='YEAR', y=selected_columns4, title='GDP by Kind of Activity Growth rates at constant 2017 prices ( percentage change from previous year)')
    fig2.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph2A.plotly_chart(fig2,use_container_width=True)
    
  with graph2B:
    selected_columns5 = st.multiselect('Filter: ',df5.columns,default=["GROSS DOMESTIC PRODUCT (GDP)"],key=14)
    fig2 = px.bar(df5, x='YEAR', y=selected_columns5, title='GDP by Kind of Activity Growth rates at constant 2017 prices ( Percentage points)')
    fig2.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph2B.plotly_chart(fig2,use_container_width=True)
    
  with graph3:
    selected_columns6 = st.multiselect('Filter: ',df6.columns,default=["GROSS DOMESTIC PRODUCT (GDP)"],key=15)
    fig2 = px.bar(df6, x='YEAR', y=selected_columns6, title='GDP by Kind of Activity Deflators (2017=100)')
    fig2.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
    graph3.plotly_chart(fig2,use_container_width=True)

#                                       CONSUMER PRICE INDEX
# -------------------------------------------------------------------------------------------------------------

# Load the Excel workbook
excel_file = 'CPI.xlsx'
allRwanda_Weights= 'allRwanda_Weights'
urban_Weights= 'urban_Weights'
rural_Weights= 'rural_Weights'
otherIndices_Weights= 'otherIndices_Weights'
weight1 = pd.read_excel(excel_file, allRwanda_Weights)
weight2 = pd.read_excel(excel_file, urban_Weights)
weight3 = pd.read_excel(excel_file, rural_Weights)
weight4 = pd.read_excel(excel_file, otherIndices_Weights)
# ALL RWANDA
def all():
   st.subheader("Rwanda's CPI from 2009 to 2022")
   st.info("Base: 2014; Reference: February 2014=100")
   # Select the worksheet you want to display
   sheet_name = 'rw'
   
   # Read the worksheet into a Pandas DataFrame
   df = pd.read_excel(excel_file, sheet_name)
   with st.expander("""Rwanda's CPI from 2009 to 2022 TABLE"""):  
      # Create a multiselect widget
      selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"])

      # Filter the DataFrame based on the selected columns
      df_filtered = df[selected_columns]
      # Convert the year column to a Pandas datetime object
      df_filtered['YEAR'] = pd.to_datetime(df['YEAR'])

      # Extract the date from the Pandas datetime object
      df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
      # Display the filtered DataFrame in 
      st.dataframe(df_filtered)
   
   column_names = df.columns.tolist()
   column_names.remove('YEAR')


   # Create a multiselect widget
   selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"])

   fig = px.line(df, x='YEAR', y=selected_columns, title='Tracking Rwandas Inflationary Landscape: CPI Analysis from 2009 to 2022')
   fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
   st.plotly_chart(fig,use_container_width=True)


# URBAN SECTOR
def Urban():
  # Select the worksheet you want to display
  sheet_name = 'urban1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.subheader("Urban CPI in Rwanda: 2009 to 2022")
  st.info("Base: 2014; Reference: February 2014=100")
    
  with st.expander("""Urban CPI in Rwanda: 2009 to 2022 TABLE"""):  
      # Create a multiselect widget
      selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"],key=22)

      # Filter the DataFrame based on the selected columns
      df_filtered = df[selected_columns]
      # Convert the year column to a Pandas datetime object
      df_filtered['YEAR'] = pd.to_datetime(df['YEAR'])

      # Extract the date from the Pandas datetime object
      df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
      # Display the filtered DataFrame in 
      st.dataframe(df_filtered)
  
  column_names = df.columns.tolist()
  column_names.remove('YEAR')


   # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"],key=23)

  fig = px.line(df, x='YEAR', y=selected_columns, title='Deciphering Urban Consumption Dynamics in Rwanda: A Focus on CPI Trends from 2009 to 2022')
  fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig,use_container_width=True)

# ALL RWANDA
def Rural():
  # Select the worksheet you want to display
  sheet_name = 'rural1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.subheader("Rural CPI in Rwanda: 2009 to 2022)")
  st.info("Base: 2014; Reference: February 2014=100")
    
  with st.expander("""Rural CPI in Rwanda: 2009 to 2022 TABLE"""):  
      # Create a multiselect widget
      selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","   Bread and cereals","Meat","Milk, cheese and eggs","Vegetables","Non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"],key=24)

      # Filter the DataFrame based on the selected columns
      df_filtered = df[selected_columns]
      # Convert the year column to a Pandas datetime object
      df_filtered['YEAR'] = pd.to_datetime(df['YEAR'])

      # Extract the date from the Pandas datetime object
      df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
      # Display the filtered DataFrame in 
      st.dataframe(df_filtered)
  
  column_names = df.columns.tolist()
  column_names.remove('YEAR')

   # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["GENERAL INDEX (CPI)"],key=25)

  fig = px.line(df, x='YEAR', y=selected_columns, title='Unveiling Rural Consumption Dynamics in Rwanda: A Focus on CPI Trends from 2009 to 2022')
  fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig,use_container_width=True)
  
  
# Other indices function
def Other_Indices():
  # Select the worksheet you want to display
  sheet_name = 'other_indices1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.subheader("Other indices CPI in Rwanda: 2009 to 2022, Urban only")
  st.info("Base: 2014; Reference: February 2014=100")
    
  

  with st.expander("""Other indices CPI in Rwanda: 2009 to 2022 TABLE"""):  
     # Create a multiselect widget
      selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","Local Goods Index","Local Food and non-alcoholic beverages","Local Housing, water, electricity, gas and other fuels","Local Transport","Imported Goods Index","Imported Food and non-alcoholic beverages","Imported Furnishing, household equipment","Imported Transport","Fresh Products(1) index","Energy index","General Index excluding fresh Products and energy(2)"])
      # Filter the DataFrame based on the selected columns
      df_filtered = df[selected_columns]
      # Convert the year column to a Pandas datetime object
      df_filtered['YEAR'] = pd.to_datetime(df['YEAR'])

      # Extract the date from the Pandas datetime object
      df_filtered['YEAR'] = df_filtered['YEAR'].dt.date
      # Display the filtered DataFrame in 
      st.dataframe(df_filtered)
  column_names = df.columns.tolist()
  column_names.remove('YEAR')


   # Create a multiselect widget
  selected_columns = st.multiselect('Filter: ',df.columns,default=["Local Goods Index","Imported Goods Index","Fresh Products(1) index","Energy index"])

  fig = px.bar(df, x='YEAR', y=selected_columns, title='Complementing CPI Analysis with Additional Indices: A Comprehensive Look at Rwandas Consumption Trends')
  fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig,use_container_width=True)

def CPI_general():
  # Select the worksheet you want to display
  sheet_name2 = 'General indices'
   # Read the worksheet into a Pandas DataFrame
  dfa = pd.read_excel(excel_file, sheet_name2)
  # Select the initial columns to be displayed
  selected_columns=dfa.columns
  fig = px.line(dfa, x="YEAR", y=selected_columns)
  fig.update_layout(title="Charting Rwanda's Economic Rise: A Line Graph Perspective on GDP from 1999 to 2022",yaxis_title="in billion Rwf",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig, use_container_width=True)
 

#GDP 
def ExpenditureOnGDP():
    st.subheader("Expenditure on GDP (Billion Frw)")
    df3=pd.read_excel('GDP.xlsx', sheet_name='Table4A')
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
        legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5),
        xaxis=dict(title='Year'),
        yaxis=dict(title='in billion Rwf', range=[-5000, 20000]),
        barmode='stack'
    )

    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
     
def weights():
      tablew1,tablew2=st.columns(2)
      tablew3,tablew4=st.columns(2)
      with tablew1:
            st.subheader("Overall Consumption in Rwanda Table")
            st.caption("Overall Consumption in Rwanda")
            with st.expander("""Expand"""): 
                  st.dataframe(weight1)
                  
      with tablew2:
            st.subheader("Consumption Trends in Urban Rwanda Table")
            st.caption("Consumption Trends in Urban Rwanda")
            with st.expander("""Expand"""): 
                  st.dataframe(weight2)
                  
      with tablew3:
            st.subheader("Consumption Pattern in Rural Rwanda Table")
            st.caption("Consumption Pattern in Rural Rwanda")
            with st.expander("""Expand"""): 
                  st.dataframe(weight3)
                  
      with tablew4:
            st.subheader("Consumption Analysis Based on Other Indices Table")
            st.caption("Consumption Analysis Based on Other Indices")
            with st.expander("""Expand"""): 
                  st.dataframe(weight4)
      allw,urbanw=st.columns(2)
      rularw,otherw=st.columns(2)
      with allw:
            fig11 = px.bar(weight1, 
                            x='Categories', 
                            y='Weights',
                            orientation="v", 
                            title='Overall Consumption in Rwanda'
                            )
            fig11.update_layout(yaxis_title="Weights",legend=dict(yanchor="bottom", y=1, xanchor="right", x=0.5))
            st.plotly_chart(fig11,use_container_width=True)
      with urbanw:
            fig11 = px.bar(weight2, 
                            x='Categories', 
                            y='Weights',
                            orientation="v", 
                            title='Consumption Trends in Urban Rwanda'
                            )
            fig11.update_layout(yaxis_title="Weights",legend=dict(yanchor="bottom", y=1, xanchor="right", x=0.5))
            st.plotly_chart(fig11,use_container_width=True)
            
      with rularw:
            fig11 = px.bar(weight3, 
                            x='Categories', 
                            y='Weights',
                            orientation="v", 
                            title='Consumption Pattern in Rural Rwanda'
                            )
            fig11.update_layout(yaxis_title="Weights",legend=dict(yanchor="bottom", y=1, xanchor="right", x=0.5))
            st.plotly_chart(fig11,use_container_width=True)
      with otherw:
            fig11 = px.bar(weight4, 
                            x='Categories', 
                            y='Weights',
                            orientation="v", 
                            title='Consumption Analysis Based on Other Indices'
                            )
            fig11.update_layout(yaxis_title="Weights",legend=dict(yanchor="bottom", y=1, xanchor="right", x=0.5))
            st.plotly_chart(fig11,use_container_width=True)
     
#SIDEBAR
def cpi_dashboard():
    st.title("CPI Dashboard")
    # Create the navigation bar
    tab1, tab2,tab3, tab4 = st.tabs(["Weights", "All Rwanda","Urban", "Rural"])

    # Style
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    # Display CPI dashboard attributes
    with tab1:
       weights()
    with tab2:
      all()
    with tab3:
       Urban()
    with tab4:
       Rural()

    CPI_general()  

def gdp_dashboard():
    st.title("GDP Dashboard")
    # Display GDP dashboard option
        # Create the navigation bar
    tab1, tab2,tab3, = st.tabs(["Macro economic aggregates", "GDP BY Kind of activity","Expenditure on GDP"])
    # Display GDP dashboard attributes
    with tab1:
       MacroEconomicHome()
    with tab2:
      kindOfActivity()
    with tab3:
       ExpenditureOnGDP()

def home_dashboard():
    
    st.title("GDP and CPI Dashboard")
    df_selection=df1
    df_selection = df_selection.rename(columns=lambda x: x.strip())
    df_selection[['Year', 'Month', 'Date']] = pd.to_datetime(df_selection['Years'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d').str.split('-').tolist()
    # Solting Year
    sorted_year=sorted(df_selection['Year'].unique(), reverse=True)
    # Configurable Year
    year  = st.selectbox(label="GDP and CPI Summary",options=sorted_year)
    
    # GDP and CPI summary
    total1,total2,total3,total4,total5=st.columns(5,gap='small')
    with total1:
        st.metric(label=f"GDP per Capita in {year}",value=f"{145.8995:,.0f}",delta="1.2 °F")

    with total2:
        st.metric(label=f"GNP in {year}",value=f"{12.555:,.0f}", delta="-8%")

    with total3:
        st.metric(label=f"Nominal GDP in {year}",value=f"{1345.0033:,.0f}",delta="10%")

    with total4:
        st.metric(label=f"Real GDP in {year}",value=f"{7451.3344:,.0f}",delta="84 Billions")

    with total5:
        st.metric(label=f"Total Population as in {year}",value=5,delta="100%")
    
    # GDP Charts
    def threeD_barchart():
      years = [2000, 2001, 2002, 2003,
          2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]

      fig = go.Figure()
      fig.add_trace(go.Bar(x=years,
                      y=[180, 236, 207, 236, 263,
                        350, 430, 474, 526, 488, 537, 500, 439],
                      name='GDP at Current Price',
                      marker_color='rgb(55, 83, 109)'
                      ))
      fig.add_trace(go.Bar(x=years,
                      y=[37, 43, 55, 56, 88, 105, 156, 270,
                        299, 340, 403, 549, 499],
                      name='GDP at Constant 2017',
                      marker_color='rgb(26, 118, 255)'
                      ))

      fig.update_layout(
          title='GDP at current price and GDP at constant 2017',
          xaxis_tickfont_size=14,
          yaxis=dict(
              title='Rwf (Billions)',
              titlefont_size=20,
              tickfont_size=14,
          ),
          legend=dict(
              xanchor="left",
              yanchor="bottom",
              x=0,
              y=-0.4,
              bgcolor='rgba(255, 255, 255, 0)',
              bordercolor='rgba(255, 255, 255, 0)'
          ),
          barmode='group',
          bargap=0.3, # gap between bars of adjacent location coordinates.
          bargroupgap=0.1 # gap between bars of the same location coordinate.
      )
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
        trace = go.Pie(labels=data['Sector'], values=data['Percentage'], hole=0.5,)

        # Create the layout for the chart
        layout = go.Layout(
            title=f'Percentage of GDP by Sector in {year}',
            legend=dict(yanchor="bottom", y=-0.8, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, b=0, t=40),
            annotations=[dict(text=f'Frw<br />{ "{:,}".format(df1["GDP at current prices"][23]) }<br />billion', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )

        # Create the figure and plot it using Streamlit
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        threeD_barchart()
    with col2:
        donut_chart()

    #CPI Charts
    CPI_general()
    # Divider
    st.markdown("""---""")



#  SIDE BAR CONFIGURATIONS
st.sidebar.image("logo/logo2.png")

st.sidebar.markdown("# Welcome Back! ~ <span style='color:rgb(40,79,141)'>Admin</span>", unsafe_allow_html=True)
with st.sidebar:
  selected = om.option_menu(
    menu_title="",
    options=["Home","GDP","CPI","Welcome to the Future"],
    icons=["house","wallet-fill","view-stacked"],
    default_index=0
  )

if selected == "Home":
  home_dashboard()
elif selected == "GDP":
  gdp_dashboard()
elif selected == "CPI":
  cpi_dashboard()
# Copyright notice
st.markdown("<div style='font-style:italic;text-align:center'>Copyright (c) 2023 Methode & Saveur</div>",unsafe_allow_html=True)