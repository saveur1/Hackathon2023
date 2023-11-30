import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.graph_objs as go
import plotly.express as px
import streamlit_option_menu as om
from bisect import bisect_left

st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)


#Styles
with open("style.css") as t:
    st.markdown(f"<style>{ t.read() }</style>", unsafe_allow_html= True)


#                          GROSS DOMESTIC PRODUCT AT MACRO ECCONOMIC LEVEL
# -------------------------------------------------------------------------------------------------------------
#load excel files
df_macro=pd.read_excel('GDP.xlsx', sheet_name='macro_economic')
df_macro = df_macro.rename(columns=lambda x: x.strip())

expenditure_cp = pd.read_excel('GDP.xlsx', sheet_name='expenditure_cp')
expenditure_cp = expenditure_cp.rename(columns=lambda x: x.strip())

current_bf = pd.read_excel('GDP.xlsx', sheet_name='current_bf')
current_bf = current_bf.rename(columns=lambda x: x.strip())

current_perc = pd.read_excel('GDP.xlsx', sheet_name='current_perc')
current_perc = current_perc.rename(columns=lambda x: x.strip())

constant_2017 = pd.read_excel('GDP.xlsx', sheet_name='constant_2017')
constant_2017 = constant_2017.rename(columns=lambda x: x.strip())

constant_2017_perc = pd.read_excel('GDP.xlsx', sheet_name='constant_2017_perc')
constant_2017_perc = constant_2017_perc.rename(columns=lambda x: x.strip())

constant_2017_perc = pd.read_excel('GDP.xlsx', sheet_name='constant_2017_perc')
constant_2017_perc = constant_2017_perc.rename(columns=lambda x: x.strip())
#Macro Economic Table
def MacroTable():
    with st.expander("Rwanda's GDP Macroeconomic Aggregates: A Historical Perspective from 1999 to 2022 Table"):
        showData = st.multiselect('Filter: ', df_macro.columns, default=[
                            "Years", "GDP at current prices", "GDP Growth rate at current prices", "Population Growth rate","Exchange Growth rate", "Implicit GDP deflator", "Implicit GDP deflator Growth rate", "GDP per head (in '000 Rwf)", "GDP per head (in current US dollars)"])
        st.dataframe(df_macro[showData],use_container_width=True)
#Calculate proportions of GDP contributed by various sectors.
def calculate_gdp_proportions():
    # Select the initial columns to be displayed
    initial_columns = ['Government','Private (includes changes in stock)']
    selected_columns= ['Government','Private (includes changes in stock)']
    #st.text(df_macro.columns)
    # Disable other columns except the initial columns
    disabled_columns = list(set(df_macro.columns) - set(initial_columns))
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns,key=np.random.randint(50,60))
    for column in filtered_columns:
         df_macro[column] *= 100
    fig = px.bar(df_macro, x="Years", y=filtered_columns)
    fig.update_layout(title="Total final consumption expenditure",yaxis_title="Percentage",yaxis=dict(title='Percentage Change', range=[0,100]),legend=dict(yanchor="bottom", y=-0.5, xanchor="center", x=0.5),barmode="group")
    st.plotly_chart(fig, use_container_width=True) 
      
#Analyze the relationship between gross capital formation and resource balance
def analyze_capital_formation_resource_balance():
    # Select the initial columns to be displayed
    initial_columns = ['Gross capital formation','Resource balance']
    selected_columns= ['Gross capital formation','Resource balance']
    #st.text(df_macro.columns)
    # Disable other columns except the initial columns
    disabled_columns = list(set(df_macro.columns) - set(initial_columns))
    filtered_columns = st.multiselect("Filters:",selected_columns , default=initial_columns,key=np.random.randint(101, 111))
    for column in filtered_columns:
         df_macro[column] *= 100
    fig = px.bar(df_macro, x="Years", y=filtered_columns)
    fig.update_layout(title="gross capital formation and resource balance",yaxis_title="Percentage",yaxis=dict(title='Percentage Change', range=[-20,30]),legend=dict(yanchor="bottom", y=-0.5, xanchor="center", x=0.5),barmode="group")
    st.plotly_chart(fig, use_container_width=True)   
def ValueAddedBy():
    data = pd.DataFrame({
        'Year': df_macro["Years"],
        'Agriculture': df_macro["Agriculture"],
        'Industry': df_macro["Industry"],
        'Services': df_macro["Services"],
        'Adjustments':df_macro["Adjustments"]
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
        'Year': df_macro["Years"],
        'Gross Domestic Product at current prices': df_macro["Gross Domestic Product at current prices"],
        'Factor income from abroad, net': df_macro["Factor income from abroad, net"],
        'Gross National Income': df_macro["Gross National Income"],
        'Current transfers, net':df_macro["Current transfers, net"],
        'Gross National Disposible Income': df_macro["Gross National Disposible Income"],
        'Less Final consumption expenditure': df_macro["Less Final consumption expenditure"],
        'Gross National Saving':df_macro["Gross National Saving"],
        'Less Gross capital formation':df_macro["Less Gross capital formation"],
        'Net lending to the rest of the world':df_macro["Net lending to the rest of the world"]
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
  df_macro = pd.read_excel(excel_file, table1)
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
    selected_columns = st.multiselect('Filter: ',df_macro.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"])
    # Convert the Year column to datetime format
    df_macro["YEAR"] = pd.to_datetime(df_macro["YEAR"], format="%Y")

    # Format the Year column as YYYY
    df_macro["YEAR"] = df_macro["YEAR"].dt.strftime("%Y")
    # Display the filtered DataFrame in Streamlit
    st.dataframe(df_macro,use_container_width=True)
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
 
  column_names = df_macro.columns.tolist()
  column_names.remove('YEAR')

  # Create a multiselect widget
  with graph1:
    selected_columns1 = st.multiselect('Filter: ',df_macro.columns,default=["GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=0)
    
    fig= px.line(df_macro, x='YEAR', y=selected_columns1, title='GDP by Kind of Activity at current prices ( in billion Rwf)')
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
  fig.update_layout(yaxis_title="Index",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
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
  fig.update_layout(yaxis_title="Index",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
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
  fig.update_layout(yaxis_title="Index",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig,use_container_width=True)

def CPI_general():
  # Select the worksheet you want to display
  sheet_name2 = 'General indices'
   # Read the worksheet into a Pandas DataFrame
  dfa = pd.read_excel(excel_file, sheet_name2)
  # Select the initial columns to be displayed
  selected_columns=dfa.columns
  
  fig = px.line(dfa[8:], x="YEAR", y=selected_columns)
  fig.update_layout(title="Rwanda's inflation year on year",yaxis_title="Index",legend=dict(yanchor="bottom", y=-0.7, xanchor="center", x=0.5),
                        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=2, label='2Y', step='year',),
                dict(count=4, label='4Y', step='year'),
                dict(count=7, label='7Y', step='year'),
                dict(step='all')
            ]))
        
                  ),
                         height=1000 
  )
  # Set the y-axis range
             
  fig.layout.paper_bgcolor = '#F0F0F0'  # Light gray                     )
  st.plotly_chart(fig, use_container_width=True)
      

#SIDEBAR
def cpi_dashboard():
    st.title("CPI Dashboard")
    # Create the navigation bar
    tab2,tab3, tab4 = st.tabs(["All Rwanda","Urban", "Rural"])

    # Style
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    # Display CPI dashboard attributes

    with tab2:
      all()
    with tab3:
       Urban()
    with tab4:
       Rural()

    CPI_general()  

def gdp_dashboard():
    def economic_activities():
        st.markdown(""" 
        #### <div style="margin-top:20px">GDP at Current Price from 2007 to 2022</div>
        """,unsafe_allow_html=True)

        def agriculture_chart():
            x = current_bf["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Export crops"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Export crops',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=current_bf["Food crops"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Food crops',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Livestock & livestock products"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Livestock & livestock products',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Fishing"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Fishing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Forestry"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Forestry',
            ))

            fig.update_layout(
                title='AGRICULTURE, FORESTRY & FISHING from 2007 to 2022',
                yaxis=dict(
                    title="Agriculture Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)
        def current_price_gdp():
            y_cp = current_bf["GROSS DOMESTIC PRODUCT (GDP)"][8:]

            x = current_bf["Years"][8:]


            # Creating Figure Handle
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, 
                y=y_cp,
                mode='lines+markers',
                line_color='rgb(40,79,141)',
                name='GDP at Current Price',
            ))

            fig.update_layout(
                title='GDP at Current Price from 2007 to 2022',
                yaxis=dict(
                    title="GDP in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                height = 450
            )

            annotations = []

            y_tp = np.round(y_cp, decimals=2)

            # Adding labels
            for yd, xd in zip( y_tp, x ):
                # labeling the Bar Population (Millions)
                annotations.append(dict(xref='x1', 
                                        yref='y1',
                                        y=yd + 500, 
                                        x=xd,
                                        text="{:,}".format(yd) + 'B',
                                        font=dict(family='Arial', size=12,
                                                  color='rgb(50, 171, 96)'),
                                        showarrow=False))

            fig.update_layout(annotations=annotations)

            st.plotly_chart(fig, use_container_width=True)
        def industry_chart():
            x = current_bf["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Mining & quarrying"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Mining & quarrying',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=current_bf["TOTAL MANUFACTURING"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Total Manufacturing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Electricity"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Electricity',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Water & waste management"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Water & waste management',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["Construction"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Construction',
            ))

            fig.update_layout(
                title='INDUSTRY from 2007 to 2022',
                yaxis=dict(
                    title="Industry Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)      
        def services_chart():
            x = current_bf["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=current_bf["TRADE &TRANSPORT"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 0,1.0)',
                          width=2),
                  ),
                  name='Trade and Transport',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=current_bf["OTHER SERVICES"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Other Services',
            ))

            fig.update_layout(
                title='SERVICES from 2007 to 2022',
                yaxis=dict(
                    title="Services Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)       
        def taxes_chart():
            x = current_bf["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=current_bf["TAXES LESS SUBSIDIES ON PRODUCTS"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        def percent_eco_change_chart():
            x = current_perc["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in current_perc["AGRICULTURE, FORESTRY & FISHING"][8:]],
                marker=dict(
                    color='rgba(50, 171, 96, 0.6)',
                    line=dict(
                        color='rgba(50, 171, 96, 1.0)',
                        width=2),
                ),
                name='Agriculture, Forestry and Fishing',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in current_perc["INDUSTRY"][8:]],
                marker=dict(
                    color='rgba(255, 77, 77,0.6)',
                    line=dict(
                        color='rgba(255, 77, 77,1.0)',
                        width=2),
                ),
                name='Industry',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in current_perc["SERVICES"][8:]],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Services',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in current_perc["TAXES LESS SUBSIDIES ON PRODUCTS"][8:]],
                marker=dict(
                    color='rgba(255, 166, 0,0.6)',
                    line=dict(
                        color='rgba(255, 166, 0,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[0,100],
                    domain=[0, 0.8],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        
        # GDP Aggregate
        current_price_gdp()
        
        # Industry and Agriculture
        agriculture, industry=st.columns(2)
        with agriculture:
            agriculture_chart()
        with industry:
            industry_chart()

        # Services and Taxes
        services, taxes=st.columns(2)
        with services:
            services_chart()
        with taxes:
            taxes_chart()
            
        st.markdown(""" 
        ###### Percentage Contribution of Sectors to GDP
        """,unsafe_allow_html=True)
        percent_eco_change_chart()



        st.markdown(""" 
        #### <div style="margin-top:20px">GDP at constant 2017 prices from 2007 to 2022</div>
        """,unsafe_allow_html=True)
                
        def agriculture_constant_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Export crops"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Export crops',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["Food crops"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Food crops',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Livestock & livestock products"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Livestock & livestock products',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Fishing"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Fishing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Forestry"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Forestry',
            ))

            fig.update_layout(
                title='AGRICULTURE, FORESTRY & FISHING from 2007 to 2022',
                yaxis=dict(
                    title="Agriculture Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)
        def constant_price_2017_gdp():
            y_cp = constant_2017["GROSS DOMESTIC PRODUCT (GDP)"][8:]

            x = constant_2017["Years"][8:]


            # Creating Figure Handle
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, 
                y=y_cp,
                mode='lines+markers',
                line_color='rgb(40,79,141)',
                name='GDP at Constant 2017 Prices',
            ))

            fig.update_layout(
                title='GDP at Constant 2017 Prices from 2007 to 2022',
                yaxis=dict(
                    title="GDP in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                height = 450
            )

            annotations = []

            y_tp = np.round(y_cp, decimals=2)

            # Adding labels
            for yd, xd in zip( y_tp, x ):
                # labeling the Bar Population (Millions)
                annotations.append(dict(xref='x1', 
                                        yref='y1',
                                        y=yd + 500, 
                                        x=xd,
                                        text="{:,}".format(yd) + 'B',
                                        font=dict(family='Arial', size=12,
                                                  color='rgb(50, 171, 96)'),
                                        showarrow=False))

            fig.update_layout(annotations=annotations)

            st.plotly_chart(fig, use_container_width=True)
        def industry_constant_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Mining & quarrying"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Mining & quarrying',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["TOTAL MANUFACTURING"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Total Manufacturing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Electricity"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Electricity',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Water & waste management"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Water & waste management',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Construction"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Construction',
            ))

            fig.update_layout(
                title='INDUSTRY from 2007 to 2022',
                yaxis=dict(
                    title="Industry Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)      
        def services_constant_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["TRADE &TRANSPORT"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 0,1.0)',
                          width=2),
                  ),
                  name='Trade and Transport',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["OTHER SERVICES"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Other Services',
            ))

            fig.update_layout(
                title='SERVICES from 2007 to 2022',
                yaxis=dict(
                    title="Services Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)       
        def taxes_constant_chart():
            x = constant_2017["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["TAXES LESS SUBSIDIES ON PRODUCTS"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        def percent_eco_change_constant_chart():
            x = constant_2017_perc["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["AGRICULTURE, FORESTRY & FISHING"][8:]],
                marker=dict(
                    color='rgba(50, 171, 96, 0.6)',
                    line=dict(
                        color='rgba(50, 171, 96, 1.0)',
                        width=2),
                ),
                name='Agriculture, Forestry and Fishing',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["INDUSTRY"][8:]],
                marker=dict(
                    color='rgba(255, 77, 77,0.6)',
                    line=dict(
                        color='rgba(255, 77, 77,1.0)',
                        width=2),
                ),
                name='Industry',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["SERVICES"][8:]],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Services',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["TAXES LESS SUBSIDIES ON PRODUCTS"][8:]],
                marker=dict(
                    color='rgba(255, 166, 0,0.6)',
                    line=dict(
                        color='rgba(255, 166, 0,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))
            fig.add_trace(go.Line(
                x=x,
                y=[x*100 for x in constant_2017_perc["GROSS DOMESTIC PRODUCT (GDP)"][8:]],
                marker=dict(
                    color='rgb(5, 1, 21)',
                    line=dict(
                        color='rgb(5, 1, 21)',
                        width=2),
                ),
                name='Gross Domestic Product',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[-5,30],
                    domain=[0, 0.8],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        
        # GDP Aggregate
        constant_price_2017_gdp()
        
        # Industry and Agriculture
        agriculture, industry=st.columns(2)
        with agriculture:
            agriculture_constant_chart()
        with industry:
            industry_constant_chart()

        # Services and Taxes
        services, taxes=st.columns(2)
        with services:
            services_constant_chart()
        with taxes:
            taxes_constant_chart()
            
        st.markdown(""" 
        ###### GDP Growth rates at constant 2017 prices
        """,unsafe_allow_html=True)
        percent_eco_change_constant_chart()



        st.markdown(""" 
        #### <div style="margin-top:20px">GDP Deflators [2017=100] prices from 2007 to 2022</div>
        """,unsafe_allow_html=True)
                
        def agriculture_deflators_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Export crops"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Export crops',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["Food crops"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Food crops',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Livestock & livestock products"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Livestock & livestock products',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Fishing"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Fishing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Forestry"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Forestry',
            ))

            fig.update_layout(
                title='AGRICULTURE, FORESTRY & FISHING from 2007 to 2022',
                yaxis=dict(
                    title="Agriculture Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)
        def deflators_price_2017_gdp():
            y_cp = constant_2017["GROSS DOMESTIC PRODUCT (GDP)"][8:]

            x = constant_2017["Years"][8:]


            # Creating Figure Handle
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, 
                y=y_cp,
                mode='lines+markers',
                line_color='rgb(40,79,141)',
                name='GDP at Constant 2017 Prices',
            ))

            fig.update_layout(
                title='GDP at Constant 2017 Prices from 2007 to 2022',
                yaxis=dict(
                    title="GDP in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                height = 450
            )

            annotations = []

            y_tp = np.round(y_cp, decimals=2)

            # Adding labels
            for yd, xd in zip( y_tp, x ):
                # labeling the Bar Population (Millions)
                annotations.append(dict(xref='x1', 
                                        yref='y1',
                                        y=yd + 500, 
                                        x=xd,
                                        text="{:,}".format(yd) + 'B',
                                        font=dict(family='Arial', size=12,
                                                  color='rgb(50, 171, 96)'),
                                        showarrow=False))

            fig.update_layout(annotations=annotations)

            st.plotly_chart(fig, use_container_width=True)
        def industry_deflators_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Mining & quarrying"][8:],
                  marker=dict(
                      color='rgba(255, 255, 0,0.6)',
                      line=dict(
                          color='rgba(255, 255, 0,1.0)',
                          width=2),
                  ),
                  name='Mining & quarrying',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["TOTAL MANUFACTURING"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Total Manufacturing',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Electricity"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 1.0)',
                          width=2),
                  ),
                  name='Electricity',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Water & waste management"][8:],
                  marker=dict(
                      color='rgba(255, 77, 77,0.6)',
                      line=dict(
                          color='rgba(255, 77, 77,1.0)',
                          width=2),
                  ),
                  name='Water & waste management',
            ))
            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["Construction"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Construction',
            ))

            fig.update_layout(
                title='INDUSTRY from 2007 to 2022',
                yaxis=dict(
                    title="Industry Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)      
        def services_deflators_chart():
            x = constant_2017["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=constant_2017["TRADE &TRANSPORT"][8:],
                  marker=dict(
                      color='rgba(255, 166, 0,0.6)',
                      line=dict(
                          color='rgba(255, 166, 0,1.0)',
                          width=2),
                  ),
                  name='Trade and Transport',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["OTHER SERVICES"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Other Services',
            ))

            fig.update_layout(
                title='SERVICES from 2007 to 2022',
                yaxis=dict(
                    title="Services Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                barmode = "stack"
              )

            st.plotly_chart(fig, use_container_width=True)       
        def taxes_deflators_chart():
            x = constant_2017["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=constant_2017["TAXES LESS SUBSIDIES ON PRODUCTS"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        def percent_eco_change_deflators_chart():
            x = constant_2017_perc["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["AGRICULTURE, FORESTRY & FISHING"][8:]],
                marker=dict(
                    color='rgba(50, 171, 96, 0.6)',
                    line=dict(
                        color='rgba(50, 171, 96, 1.0)',
                        width=2),
                ),
                name='Agriculture, Forestry and Fishing',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["INDUSTRY"][8:]],
                marker=dict(
                    color='rgba(255, 77, 77,0.6)',
                    line=dict(
                        color='rgba(255, 77, 77,1.0)',
                        width=2),
                ),
                name='Industry',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["SERVICES"][8:]],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Services',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in constant_2017_perc["TAXES LESS SUBSIDIES ON PRODUCTS"][8:]],
                marker=dict(
                    color='rgba(255, 166, 0,0.6)',
                    line=dict(
                        color='rgba(255, 166, 0,1.0)',
                        width=2),
                ),
                name='Taxes',
            ))
            fig.add_trace(go.Line(
                x=x,
                y=[x*100 for x in constant_2017_perc["GROSS DOMESTIC PRODUCT (GDP)"][8:]],
                marker=dict(
                    color='rgb(5, 1, 21)',
                    line=dict(
                        color='rgb(5, 1, 21)',
                        width=2),
                ),
                name='Gross Domestic Product',
            ))

            fig.update_layout(
                title='TAXES LESS SUBSIDIES ON PRODUCTS from 2007 to 2022',
                yaxis=dict(
                    title="Taxes Value in Billions",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[-5,30],
                    domain=[0, 0.8],
                ),
                xaxis=dict(
                    title="Years",
                    showline=False,
                    showticklabels=True,
                    showgrid=True,
                ),
                legend=dict(x=0.029, y=1.038, font_size=10),
                margin=dict(l=100, r=20, t=70, b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
              )

            st.plotly_chart(fig, use_container_width=True)
        
        # GDP Aggregate
        deflators_price_2017_gdp()
        
        # Industry and Agriculture
        agriculture, industry=st.columns(2)
        with agriculture:
            agriculture_deflators_chart()
        with industry:
            industry_deflators_chart()

        # Services and Taxes
        services, taxes=st.columns(2)
        with services:
            services_deflators_chart()
        with taxes:
            taxes_deflators_chart()
            
        st.markdown(""" 
        ###### GDP Growth rates at constant 2017 prices
        """,unsafe_allow_html=True)
        percent_eco_change_deflators_chart()
    
    st.title("GDP Dashboard")
    # Display GDP dashboard option
    tab1, tab2 = st.tabs(["Economic Activities","Expenditure on GDP"])
    # Display GDP dashboard attributes
    with tab1:
       economic_activities()
    with tab2:
      kindOfActivity()

def home_dashboard():
    
  st.title("GDP and CPI Dashboard")
  tab1,tab2=st.tabs(["GDP","CPI"])
  # GDP SUMMARY BASED ON YEAR
  def gdp_home():
    df_selection=df_macro
    df_selection = df_selection.rename(columns=lambda x: x.strip())
    year = st.selectbox("End Year", options=df_selection["Years"].iloc[::-1])
    
    # Gdp Summary Function
    def gdp_summary_cards():
        exp_years = [int(x) for x in df_macro["Years"]]
        
        def get_index(item, arr):
           return bisect_left(arr, item)
        
        def get_value(table_column):
           return df_macro[table_column][get_index(year, exp_years)]
        
        print(df_macro["GDP per head (in '000 Rwf)"][get_index(year, exp_years)])
        # GDP and CPI summary
        total1,total2,total3,total4,total5=st.columns(5,gap='small')
        with total1:
            st.metric(label=f"GDP per Capita in { year }",value=f"""{ get_value("GDP per head (in '000 Rwf)") }""", delta=f"12%")

        with total2:
            st.metric(label=f"Gross National Income in { year }",value=f"{ get_value('Gross National Income') }", delta=f"12%")

        with total3:
            st.metric(label=f"GDP at current price in { year }",value=f"{ get_value('GDP at current prices') }",delta=f"{ get_value('GDP Growth rate at current prices')*100 }%")

        with total4:
            st.metric(label=f"GDP at constantant 2017 in { year }",value=f"{ get_value('GDP at constant 2017 prices')}",delta=f"{get_value('GDP Growth rate at constant 2017 prices')*100 }%")

        with total5:
            st.metric(label=f"Total Population as in { year }",value=get_value("Total population (millions)"),delta=f"{get_value('Population Growth rate')*100 }%")
    
    # GDP Charts function
    def threeD_barchart():
      years = df_macro["Years"][8:]
      fig = go.Figure()
      fig.add_trace(go.Bar(
                      x=years,
                      y=df_macro["GDP at current prices"][8:],
                      name='GDP at Current Price',
                      marker_color='rgb(40,79,141)',
                      ))
      fig.add_trace(go.Scatter(
                      x=years,
                      y= ["{:.1f}%".format(x * 100) for x in df_macro["GDP Growth rate at current prices"][8:]],
                      name='Growth Rate',
                      marker_color='rgb(255, 77, 77)',
                      mode="lines",
                      yaxis="y2"
                      ))

      fig.update_layout(
          title='GDP at current price from 2007 to 2022',
          xaxis_tickfont_size=14,
          xaxis=dict(title="Years"),
          yaxis=dict(
              title='Rwf (Billions)',
              titlefont_size=20,
              tickfont_size=14,
          ),
          yaxis2=dict(
              title="Percentages(%)",
              overlaying="y",
              side="right"
              ),
          legend=dict(
              xanchor="left",
              yanchor="bottom",
              x=0,
              y=-0.4,
              bgcolor='rgba(255, 255, 255, 0)',
              bordercolor='rgba(255, 255, 255, 0)'
          ),
          template="gridon",
          bargap=0.3, # gap between bars of adjacent location coordinates.
          bargroupgap=0.1 # gap between bars of the same location coordinate.
      )
      st.plotly_chart(fig, use_container_width=True)
         
    # Single Year GDP by sector function
    def donut_chart():
      # Create a dataframe with the data from the image
        data = pd.DataFrame({
            'Sector': ['Agriculture', 'Industry', 'Services','Adjustments'],
            'Percentage': [
                            round(df_macro['Agriculture'][23]*100),
                            round(df_macro['Industry'][23]*100), 
                            round(df_macro['Services'][23]*100),
                            round(df_macro['Adjustments'][23]*100)
                          ]
        })

        # Create the trace for the chart
        trace = go.Pie(labels=data['Sector'], values=data['Percentage'], hole=0.5,)

        # Create the layout for the chart
        layout = go.Layout(
            title=f'Percentage of GDP by Sector in',
            legend=dict(yanchor="bottom", y=-0.8, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, b=0, t=40),
            annotations=[dict(text=f'Frw<br />{ "{:,}".format(df_macro["GDP at current prices"][23]) }<br />billion', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )

        # Create the figure and plot it using Streamlit
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig, use_container_width=True)
    
    #GDP Inflation function
    def nominal_and_real_gdp():
        years = df_macro["Years"][8:]
        fig = go.Figure()
        fig.add_trace(go.Bar(
                        x=years,
                        y=df_macro["GDP at current prices"][8:],
                        name='GDP at Current Prices',
                        marker_color='rgb(40,79,141)'
                        ))
        fig.add_trace(go.Bar(
                        x=years,
                        y=df_macro["GDP at constant 2017 prices"][8:],
                        name='GDP at constant 2017 prices',
                        marker_color='rgb(82,169,226)'
                        ))
        fig.add_trace(go.Scatter(
                        x=years,
                        y= ["{:.1f}%".format(x * 100) for x in df_macro["Implicit GDP deflator Growth rate"][8:]],
                        name='Implicit GDP deflator Growth rate',
                        marker_color='rgb(26, 118, 255)',
                        mode="lines",
                        yaxis="y2"
                        ))

        fig.update_layout(
            title='GDP at current price from 2007 to 2022',
            xaxis_tickfont_size=14,
            xaxis=dict(title="Years"),
            yaxis=dict(
                title='Rwf (Billions)',
                titlefont_size=20,
                tickfont_size=14,
            ),
            yaxis2=dict(
                title="Percentages(%)",
                overlaying="y",
                side="right"
                ),
            legend=dict(
                xanchor="left",
                yanchor="bottom",
                x=0,
                y=-0.4,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            template="gridon",
            bargap=0.3, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        st.plotly_chart(fig, use_container_width=True)

    def MemorandumItems():
        def population_growth_illustration():
              y_population = df_macro["Total population (millions)"][8:]
                  
              y_pop_rate = [x * 100 for x in df_macro["Population Growth rate"][8:]]

              x = df_macro["Years"][8:]


              # Creating two subplots
              fig = go.Figure()

              fig.add_trace(go.Bar(
                  x=x,
                  y=y_population,
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=1),
                  ),
                  name='Populations in Millions',
              ))

              fig.add_trace(go.Scatter(
                  x=x, 
                  y=y_pop_rate,
                  mode='lines+markers',
                  line_color='rgb(128, 0, 128)',
                  name='Population Growth Rate',
                  yaxis="y2"
              ))

              fig.update_layout(
                  title='Population and Growth rate',
                  yaxis=dict(
                      title="Population in Millions",
                      showgrid=False,
                      showline=False,
                      showticklabels=True,
                      domain=[0, 0.85],
                  ),
                  yaxis2=dict(
                      title=" Population Growth Rate (%)",
                      overlaying="y",
                      side="right"
                  ),
                  xaxis=dict(
                      title="Years",
                      showline=False,
                      showticklabels=True,
                      showgrid=True,
                  ),
                  legend=dict(x=0.029, y=1.038, font_size=10),
                  margin=dict(l=100, r=20, t=70, b=70),
                  paper_bgcolor='rgb(248, 248, 255)',
                  plot_bgcolor='rgb(248, 248, 255)',
              )

              annotations = []

              y_tp = np.round(y_population, decimals=2)

              # Adding labels
              for yd, xd in zip( y_tp, x ):
                  # labeling the Bar Population (Millions)
                  annotations.append(dict(xref='x1', 
                                          yref='y1',
                                          y=yd + 0.5, 
                                          x=xd,
                                          text=str(yd) + 'M',
                                          font=dict(family='Arial', size=12,
                                                    color='rgb(50, 171, 96)'),
                                          showarrow=False))

              fig.update_layout(annotations=annotations)

              st.plotly_chart(fig, use_container_width=True)
            
        def ExchangeRate():
            st.info("Exchange rate: Rwf per US dollar")
            ExchangeRwfUSD, ExchangeGrowthRate = st.columns(2)
            with ExchangeRwfUSD:
                fig = px.area(df_macro[8:], x="Years", y="Exchange rate: Rwf per US dollar", markers=True)
                fig.update_layout(title="Exchange rate: Rwf per US dollar",yaxis_title="Rwf per US dollar",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
                st.plotly_chart(fig, use_container_width=True)
            with ExchangeGrowthRate:
                selectedColumn=df_macro["Exchange Growth rate"]*100
                fig=go.Figure()
                fig.add_trace(go.Scatter(
                fill='tozeroy',
                x=df_macro["Years"],
                y=selectedColumn,
                mode='lines+markers+text',
                line_color='red'
                  
                ))
      

                fig.update_layout(title="Exchange growth rate: Rwf per US dollar",yaxis_title="Exchange Growth Rate (Percentage)",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
                st.plotly_chart(fig, use_container_width=True)
        population_growth_illustration()  
        ExchangeRate()
    
    def ExpenditureOnGDP():
    # Create a dataframe with the data from the image
      data = pd.DataFrame({
          'Year': expenditure_cp["Years"][8:],
          'Gross capital formation': expenditure_cp["Gross capital formation"][8:],
          'Exports G&S': expenditure_cp["Exports of goods & services"][8:],
          'Households': expenditure_cp["Households and NGOs"][8:],
          'Government':expenditure_cp["Government"][8:],
          'Imports G&S': expenditure_cp["Imports of goods & services"][8:],
          'GDP': expenditure_cp["Gross Domestic Product"][8:]
      })

      # Create the traces for the chart
      trace1 = go.Bar(x=data['Year'], y=data['Gross capital formation'], name='Gross capital formation', marker=dict(color='green'))
      trace2 = go.Bar(x=data['Year'], y=data['Exports G&S'], name='Exports G&S', marker=dict(color='orange'))
      trace3 = go.Bar(x=data['Year'], y=data['Households'], name='Households', marker=dict(color='rgb(40,79,141)'))
      trace4 = go.Bar(x=data['Year'], y=data['Government'], name='Government', marker=dict(color='yellow'))
      trace5 = go.Bar(x=data['Year'], y=data['Imports G&S'], name='Imports G&S', marker=dict(color='red'))
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

    # GDP Summary
    gdp_summary_cards()

    # GDP overview
    col1, col2 = st.columns(2)
    with col1:
        threeD_barchart()
    with col2:
        donut_chart()
    # gdp inflation
    st.markdown(""" 
      ##### <div style='margin-top:20px'>GDP By Expenditure</div>
    """,unsafe_allow_html=True )
    ExpenditureOnGDP()

    # gdp inflation
    st.markdown(""" 
      ##### <div style='margin-top:20px'>GDP Information For Inflation</div>
    """,unsafe_allow_html=True )
    nominal_and_real_gdp()

    # gdp population
    MemorandumItems()

    # Divider
    st.markdown("""---""")
  # GDP SUMMARY BASED ON YEAR
  def cpi_home():
    sheet1="rw"
    sheet2="urban1"
    sheet3="rural1"
    # Load the Excel file containing CPI data
    data1 = pd.read_excel('CPI.xlsx',sheet1)
    data2 = pd.read_excel('CPI.xlsx',sheet2)
    data3 = pd.read_excel('CPI.xlsx',sheet3)
    # Create a selectbox to choose the base year
    data1[['Year', 'Month', 'Date']] = pd.to_datetime(data1['YEAR'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d').str.split('-').tolist()
    
    # Solting Year
    sorted_year=sorted(data1['Year'].unique(), reverse=True)
    sorted_month=sorted(data1['Month'].unique(), reverse=True)
    
  
    # Configurable Year
    # select year configuration
    selectYear,selectMonth=st.columns(2)
    with selectYear:
      year  = st.selectbox(label="Select Year",options=sorted_year,key=11)
    with selectMonth:
      # Filter data based on selected year
      filtered_df = data1[data1['Year'] == year]
      # Extract unique months for the selected year
      unique_months = filtered_df['Month'].unique()
      
      # Create a selectbox for month selection
      selected_month = st.selectbox('Select Month:', options=unique_months)
      # Filter the data based on the selected month and date
    filtered_df_macro = data1[(data1['Year'] == year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column1 =filtered_df_macro['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
        # Filter the data based on the selected month and date
    filtered_df2 = data2[(data1['Year'] == year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column2 =filtered_df2['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
    # Filter the data based on the selected month and date
    filtered_df3 = data3[(data1['Year'] == year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column3 =filtered_df3['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
      # RULAR INFLATION
    annual_filtered = data3[(data1['Year'] == str(int(year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data3[(data1['Year'] == str(int(year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data3[(data1['Year'] == year) & (data1['Month'].astype(int) == int(selected_month)-1)]    
    #selected column

    annual_base_year = "{:.2f}".format(float(annual_filtered['GENERAL INDEX (CPI)']))
    monthly_base= "{:.2f}".format(float(monthly_filtered['GENERAL INDEX (CPI)']))
    annual_base_year = float(annual_base_year)
    current_year=float(selected_column3)
    monthly_base=float(monthly_base)
    current_year=np.round(current_year,decimals=1)
    annual_base_year=np.round(annual_base_year,decimals=1)
    rular_annual_inflation_rate=(current_year-annual_base_year)/annual_base_year*100
    rular_monthly_inflation_rate=(current_year-monthly_base)/monthly_base*100

    
    # URBAN INFLATION
    annual_filtered = data2[(data1['Year'] == str(int(year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data2[(data1['Year'] == str(int(year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data2[(data1['Year'] == year) & (data1['Month'].astype(int) == int(selected_month)-1)]  
    #selected column
    annual_base_year = "{:.2f}".format(float(annual_filtered['GENERAL INDEX (CPI)']))
    monthly_base= "{:.2f}".format(float(monthly_filtered['GENERAL INDEX (CPI)']))
    annual_base_year = float(annual_base_year)
    current_year=float(selected_column2)
    monthly_base=float(monthly_base)
    current_year=np.round(current_year,decimals=1)
    annual_base_year=np.round(annual_base_year,decimals=1)
    Urban_annual_inflation_rate=(current_year-annual_base_year)/annual_base_year*100
    Urban_monthly_inflation_rate=(current_year-monthly_base)/monthly_base*100

    
    #GENERAL INFLATION
    annual_filtered = data1[(data1['Year'] == str(int(year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data1[(data1['Year'] == str(int(year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data1[(data1['Year'] == year) & (data1['Month'].astype(int) == int(selected_month)-1)]  
  
    #selected column
    annual_base_year = float(annual_filtered['GENERAL INDEX (CPI)'])
    monthly_base=float(monthly_filtered['GENERAL INDEX (CPI)'])
    annual_base_year = float(annual_base_year)
    current_year=float(selected_column1)
    monthly_base=float(monthly_base)
    current_year=np.round(current_year,decimals=1)
    annual_base_year=np.round(annual_base_year,decimals=1)
    general_annual_inflation_rate=(current_year-annual_base_year)/annual_base_year*100
    general_monthly_inflation_rate=(current_year-monthly_base)/monthly_base*100
    
    #Rounding
    general_annual_inflation_rate1=np.round(general_annual_inflation_rate,decimals=1)
    general_monthly_inflation_rate1=np.round(general_monthly_inflation_rate,decimals=1)
    Urban_annual_inflation_rate=np.round(Urban_annual_inflation_rate,decimals=1)
    Urban_monthly_inflation_rate=np.round(Urban_monthly_inflation_rate,decimals=1)
    rular_annual_inflation_rate=np.round(rular_annual_inflation_rate,decimals=1)
    rular_monthly_inflation_rate=np.round(rular_monthly_inflation_rate,decimals=1)
  
    # GDP and CPI summary
    total1,total2,total3=st.columns(3,gap='large')
    with total1:
        st.metric(label=f" Overall Rwanda Index {selected_month} {year}",value=selected_column1)
        st.metric(label=f" Anually Inflation Rate {selected_month} {year}",value="",delta=f"{general_annual_inflation_rate1}%")
        st.metric(label=f" Monthly Inflation Rate {selected_month} {year}",value="",delta=f"{general_monthly_inflation_rate1}%")
    with total2:
        st.metric(label=f"Urban Index {selected_month} {year}",value=selected_column2)
        st.metric(label=f" Anually Inflation Rate  {selected_month} {year}",value="",delta=f"{Urban_annual_inflation_rate}%")
        st.metric(label=f" Monthly Inflation Rate {selected_month} {year}",value="",delta=f"{Urban_monthly_inflation_rate}%")
    with total3:
        st.metric(label=f"Rural Index {selected_month} {year}",value=selected_column3)
        st.metric(label=f" Anually Inflation Rate {selected_month} {year}",value="",delta=f"{rular_annual_inflation_rate}%")
        st.metric(label=f" Monthly Inflation Rate {selected_month} {year}",value="",delta=f"{rular_monthly_inflation_rate}%")
    # with total4:
    #     st.metric(label=f"Real GDP in {month} {year}",value=f"{7451.3344:,.0f}",delta="84 Billions")

    # with total5:
    #     st.metric(label=f"Total Population as in {month} {year}",value=5,delta="100%")
    
    # GDP Charts
    def categories():
     # Read the Excel file into a Pandas DataFrame
      df = pd.read_excel(excel_file, "urban1")

      # Convert the 'Year' column to datetime format
      df['YEAR'] = pd.to_datetime(df['YEAR'])

      # Get the last year from the data
      last_year = df['YEAR'].dt.year.max()
      st.write(last_year)
      # Filter data based on the last year
      filtered_df = df[df['YEAR'].dt.year == last_year]
      # Calculate the annual CPI for each category
      def calculate_annual_inflation(category):
          annual_cpi = []
          for year in filtered_df['YEAR'].dt.year.unique():
              year_data = filtered_df[filtered_df['YEAR'].dt.year == year][category]
              # Assuming monthly data, calculate the average CPI for the year
              average_cpi = np.mean(year_data)

              # Calculate annual inflation rate using the formula
              if year != filtered_df['YEAR'].dt.year.unique()[0]:
                  previous_year_data = filtered_df[filtered_df['YEAR'].dt.year == year - 1][category]
                  previous_average_cpi = np.mean(previous_year_data)

                  inflation_rate = (average_cpi - previous_average_cpi) / previous_average_cpi * 100
                  annual_cpi.append(inflation_rate)

          return annual_cpi

      # Calculate annual inflation rates for all categories
      category_columns = filtered_df.columns[1:]
      annual_inflation_rates = {}
      for category in category_columns:
          annual_inflation_rates[category] = calculate_annual_inflation(category)

      # Display the annual inflation rates in a table
      st.header('Annual Inflation Rates')
      st.table(annual_inflation_rates)

  
            
      allw,urbanw=st.columns(2)
      with allw:
        fig=go.Figure()
        fig.add_trace(go.Bar(
            orientation='h',        
            
        )
          )
        fig.update_layout(
            title='Overall Consumption in Rwanda'
        )
        st.plotly_chart(fig,use_container_width=True)
      with urbanw:
            fig11 = px.bar(weight2, 
                            y='Categories', 
                            x='Weights',
                            orientation="h", 
                            title='Consumption Trends in Urban Rwanda'
                            )
            fig11.update_layout(yaxis_title="Weights",legend=dict(yanchor="bottom", y=1, xanchor="right", x=0.5))
            st.plotly_chart(fig11,use_container_width=True)
    categories()
    #CPI Charts
    CPI_general()
    # Divider
    st.markdown("""---""")
  
  with tab1:
    gdp_home()
  with tab2:
    cpi_home()
  

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