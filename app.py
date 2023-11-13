import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.graph_objs as go
import plotly.express as px
import streamlit_option_menu as om
st.set_page_config(page_title="GDP&CPI Dashboard",layout="wide",page_icon="🇷🇼")
st.title("""NISR GDP & CPI Dashboard""")

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#                          GROSS DOMESTIC PRODUCT AT MACRO ECCONOMIC LEVEL
# -------------------------------------------------------------------------------------------------------------
#load excel file
df1=pd.read_excel('GDP.xlsx', sheet_name='macro_economic')
df1 = df1.rename(columns=lambda x: x.strip())

#Macro Economic Table
def MacroTable():
    with st.expander("Rwanda's GDP Macroeconomic Aggregates: A Historical Perspective from 1999 to 2022 Table"):
        showData = st.multiselect('Filter: ', df1.columns, default=[
                            "Years", "GDP at current prices", "Growth rate-cp", "Growth rate", "Implicit GDP deflator", "Growth rate-d", "GDP per head (in '000 Rwf)", "GDP per head (in current US dollars)"])
        st.dataframe(df1[showData],use_container_width=True)

def gdps_trends_chart():
    selected_columns = st.multiselect("Filters:", df1.columns, default=[
            "GDP at current prices", "GDP at constant 2017 prices"])
    fig = px.line(df1, x="Years", y=selected_columns)
    fig.update_layout(title="Charting Rwanda's Economic Rise: A Line Graph Perspective on GDP from 1999 to 2022",yaxis_title="in billion Rwf",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
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
        legend=dict(yanchor="bottom", y=-0.8, xanchor="center", x=0.5),
        annotations=[dict(text='Frw '+str(df1["GDP at current prices"][23])+' billion', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # Create the figure and plot it using Streamlit
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
 

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

def expanditure_on_gdp():
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
        yaxis=dict(title='in billion Rwf', range=[-5000, 19000]),
        barmode='stack'
    )

    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def MacroEconomicHome():
    st.subheader(":house: Rwanda's GDP Macroeconomic Aggregates")
    st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

    MacroTable()
    
    # GDPs Trending Chart
    gdps_trends_chart()

    st.subheader(""" 
    Rwanda's GDP Highlights in 2022: A Visual Representation
    """)

    col1,col2 = st.columns((2))
    with col1:
        donut_chart()
    with col2:
        barchart_with_line()

    st.subheader("Expenditure on GDP (Billion Frw)")
    expanditure_on_gdp()
    
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
  table1,table1A,table2=st.columns(3)
  table2A,table2B,table3=st.columns(3)
  

  with table1:
    st.subheader("Table 1")
    st.caption("Gross Domestic product by Kind of Activity at current prices ( in billion Rwf)")
    with st.expander("Expand"):
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
    with st.expander("Expand"):
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
    with st.expander("Expand"):
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
    with st.expander("Expand"):
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
    with st.expander("Expand"):
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
    with st.expander("Expand"):
      # Create a multiselect widget
      selected_columns6 = st.multiselect('Filter: ',df6.columns,default=["YEAR","GROSS DOMESTIC PRODUCT (GDP)","INDUSTRY","SERVICES","TAXES LESS SUBSIDIES ON PRODUCTS"],key=6)

      # Convert the Year column to datetime format
      df6["YEAR"] = pd.to_datetime(df6["YEAR"], format="%Y")

      # Format the Year column as YYYY
      df6["YEAR"] = df6["YEAR"].dt.strftime("%Y")
      # Display the filtered DataFrame in Streamlit
      st.dataframe(df6,use_container_width=True)
    
  
  ## Graph
  st.subheader("GDP by Kind of Activity Charts")
  column_names = df1.columns.tolist()
  column_names.remove('YEAR')

  graph1,graph1A=st.columns(2)
  graph2,graph2A=st.columns(2)
  graph2B,graph3=st.columns(2)
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
   st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
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


# ALL RWANDA
def Urban():
  # Select the worksheet you want to display
  sheet_name = 'urban1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.subheader("Urban CPI in Rwanda: 2009 to 2022")
  st.info("Base: 2014; Reference: February 2014=100")
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
  with st.expander("""Urban CPI in Rwanda: 2009 to 2022 TABLE"""):  
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
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
  with st.expander("""Rural CPI in Rwanda: 2009 to 2022 TABLE"""):  
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

  fig = px.line(df, x='YEAR', y=selected_columns, title='Unveiling Rural Consumption Dynamics in Rwanda: A Focus on CPI Trends from 2009 to 2022')
  fig.update_layout(yaxis_title="Percentage",legend=dict(yanchor="bottom", y=-1, xanchor="center", x=0.5))
  st.plotly_chart(fig,use_container_width=True)
# ALL RWANDA

def Other_Indices():
  # Select the worksheet you want to display
  sheet_name = 'other_indices1'

   # Read the worksheet into a Pandas DataFrame
  df = pd.read_excel(excel_file, sheet_name)


  st.subheader("Other indices CPI in Rwanda: 2009 to 2022, Urban only")
  st.info("Base: 2014; Reference: February 2014=100")
  st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
  

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
  
def Deflator():
     st.info("Deflator")
     
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
    # Display CPI dashboard attributes
    st.sidebar.header("CPI Dashboard")
    with st.sidebar:
       selected= om.option_menu(
          menu_title=None,
          options=["Weights","All Rwanda","Urban","Rural","Other_Indices"],
          icons=["house","wallet-fill","view-stacked","three-dots","card-text"],
          menu_icon="cast",
          default_index = 0
       )
    if selected=="Weights":
       weights()
    if selected=="All Rwanda":
      all()
    if selected=="Urban":
       Urban()
    if selected=="Rural":
       Rural()
    if selected=="Other_Indices":
       Other_Indices()
    

def gdp_dashboard():
    # Display GDP dashboard option
    with st.sidebar:
       selected= om.option_menu(
          menu_title=None,
          options=["Macro economic aggregates","GDP BY Kind of activity","Deflator"],
          icons=["house","wallet-fill","view-stacked","three-dots","card-text"],
          menu_icon="cast",
          default_index = 0
       )
    if selected=="Macro economic aggregates":
       MacroEconomicHome()   
    if selected=="GDP BY Kind of activity":
       kindOfActivity()
    if selected=="Deflator":
       Deflator()


st.sidebar.image("logo/logo2.png")

st.sidebar.header("Dashboard Selection")
dashboard_selection = st.sidebar.radio("Select Dashboard", ["GDP","CPI"])

if dashboard_selection == "CPI":
    cpi_dashboard()
elif dashboard_selection == "GDP":
    gdp_dashboard()
else:
    st.sidebar.write("Please select a dashboard.")
# Copyright notice
st.markdown("Copyright (c) 2023 methode TWIZEYIMANA & Saveur BIKORIMANA")