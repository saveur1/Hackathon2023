import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import plotly.graph_objs as go
import plotly.express as px
import streamlit_option_menu as om
from bisect import bisect_left
from datetime import datetime, timedelta

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

expenditure_c2017 = pd.read_excel('GDP.xlsx', sheet_name='expenditure_c2017')
expenditure_c2017 = expenditure_c2017.rename(columns=lambda x: x.strip())

expenditure_deflator = pd.read_excel('GDP.xlsx', sheet_name='expenditure_deflator')
expenditure_deflator = expenditure_deflator.rename(columns=lambda x: x.strip())

expenditure_cpper = pd.read_excel('GDP.xlsx', sheet_name='expenditure_cpper')
expenditure_cpper = expenditure_cpper.rename(columns=lambda x: x.strip())

expenditure_c2017per = pd.read_excel('GDP.xlsx', sheet_name='expenditure_c2017per')
expenditure_c2017per = expenditure_c2017per.rename(columns=lambda x: x.strip())

current_bf = pd.read_excel('GDP.xlsx', sheet_name='current_bf')
current_bf = current_bf.rename(columns=lambda x: x.strip())

current_perc = pd.read_excel('GDP.xlsx', sheet_name='current_perc')
current_perc = current_perc.rename(columns=lambda x: x.strip())

constant_2017 = pd.read_excel('GDP.xlsx', sheet_name='constant_2017')
constant_2017 = constant_2017.rename(columns=lambda x: x.strip())

constant_2017_perc = pd.read_excel('GDP.xlsx', sheet_name='constant_2017_perc')
constant_2017_perc = constant_2017_perc.rename(columns=lambda x: x.strip())

deflators_gdp = pd.read_excel('GDP.xlsx', sheet_name='deflators_gdp')
constant_gdp = deflators_gdp.rename(columns=lambda x: x.strip())


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

def ExpenditureOnGDP(data_df, data_title,data_range=[-5000, 20000],y_title=""):
# Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Year': data_df["Years"][8:],
        'Imports G&S': [-int(x) for x in data_df["Imports of goods & services"][8:]],
        'Gross capital formation': data_df["Gross capital formation"][8:],
        'Exports G&S': data_df["Exports of goods & services"][8:],
        'Households': data_df["Households and NGOs"][8:],
        'Government':data_df["Government"][8:],
        'GDP': data_df["Gross Domestic Product"][8:]
    })

    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Gross capital formation'], name='Gross capital formation', marker=dict(color='green'))
    trace2 = go.Bar(x=data['Year'], y=data['Exports G&S'], name='Exports G&S', marker=dict(color='orange'))
    trace3 = go.Bar(x=data['Year'], y=data['Households'], name='Households', marker=dict(color='rgba(40,79,141,0.8)'))
    trace4 = go.Bar(x=data['Year'], y=data['Government'], name='Government', marker=dict(color='yellow'))
    trace5 = go.Bar(x=data['Year'], y=data['Imports G&S'], name='Imports G&S', marker=dict(color='rgba(255, 77, 77,0.8)'))
    trace6 = go.Scatter(x=data['Year'], y=data['GDP'], name='GDP', line=dict(color='black'))

    # Create the layout for the chart
    layout = go.Layout(
        title=data_title,
        yaxis=dict(
            title= y_title,
            showgrid=False,
            showline=False,
            showticklabels=True,
            range=data_range,
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
        barmode='relative',
    )

    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace5, trace2, trace3, trace4, trace1, trace6], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
#                                       CONSUMER PRICE INDEX
# -------------------------------------------------------------------------------------------------------------

# Load the Excel workbook
excel_file = 'CPI.xlsx'

# ALL RWANDA
def all():
    st.subheader("Rwanda's CPI from 2009 to 2023")
    st.info("Base: 2014; Reference: February 2014=100")
    # Select the worksheet you want to display
    sheet_name = 'rw'
    
    # Read the worksheet into a Pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name)
    with st.expander("""Rwanda's CPI from 2009 to 2023 TABLE"""):  
        # Create a multiselect widget
        selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"])

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

    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df[['Year', 'Month']] = pd.to_datetime(df['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()

    # Assuming you have columns for the specified indices, update the column names accordingly
    item1 = 'Food and non-alcoholic beverages'
    item2 = 'Housing, water, electricity, gas and other fuel'
    item3 = 'Transport'
    item4 = 'Restaurants and hotels'

    # Convert 'Year' column to integer
    df['Year'] = df['Year'].astype(int)

    # Set the default slider value to start at the year 2017
    default_start_year = 2017
    x_axis_range = st.slider('Select Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), 
                            value=(default_start_year, int(df['Year'].max())),key=25)

    # Filter the DataFrame based on the selected range
    filtered_df = df[(df['Year'] >= x_axis_range[0]) & (df['Year'] <= x_axis_range[1])]

    # Create the first line chart comparing Imported Goods and Local Goods
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item1],
                            mode='lines', name='Food and non-alcoholic beverages', line=dict(color='red', width=2), marker=dict(size=6)))

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item2],
                            mode='lines', name='Housing, water, electricity, gas and other fuel', line=dict(color='blue', width=2), marker=dict(size=6)))

    # Update layout for the first chart
    fig1.update_layout(title='Food and non-alcoholic beverages and Housing, water, electricity, gas and other fuel',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Create the second line chart comparing Fresh Products Index, Energy Index, and General Index excluding Fresh Products and Energy
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item3],
                            mode='lines', name='Transport', line=dict(color='green', width=2), marker=dict(size=6)))

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item4],
                            mode='lines', name='Restaurants and hotels', line=dict(color='orange', width=2), marker=dict(size=6)))


    # Update layout for the second chart
    fig2.update_layout(title='Transport, and Restaurants and hotels',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Organize the charts into two columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1,use_container_width=True)
    col2.plotly_chart(fig2,use_container_width=True)


# URBAN SECTOR
def Urban():
    # Select the worksheet you want to display
    sheet_name = 'urban1'

    # Read the worksheet into a Pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name)


    st.subheader("Urban CPI in Rwanda: 2009 to 2023")
    st.info("Base: 2014; Reference: February 2014=100")
        
    with st.expander("""Urban CPI in Rwanda: 2009 to 2023 TABLE"""):  
        # Create a multiselect widget
        selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"],key=22)

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

    sheet_name = 'urban1'
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df[['Year', 'Month']] = pd.to_datetime(df['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()

    # Assuming you have columns for the specified indices, update the column names accordingly
    item1 = 'Food and non-alcoholic beverages'
    item2 = 'Housing, water, electricity, gas and other fuel'
    item3 = 'Transport'
    item4 = 'Restaurants and hotels'

    # Convert 'Year' column to integer
    df['Year'] = df['Year'].astype(int)

    # Set the default slider value to start at the year 2017
    default_start_year = 2017
    x_axis_range = st.slider('Select Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), 
                            value=(default_start_year, int(df['Year'].max())),key=36)

    # Filter the DataFrame based on the selected range
    filtered_df = df[(df['Year'] >= x_axis_range[0]) & (df['Year'] <= x_axis_range[1])]

    # Create the first line chart comparing Imported Goods and Local Goods
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item1],
                            mode='lines', name='Food and non-alcoholic beverages', line=dict(color='red', width=2), marker=dict(size=6)))

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item2],
                            mode='lines', name='Housing, water, electricity, gas and other fuel', line=dict(color='blue', width=2), marker=dict(size=6)))

    # Update layout for the first chart
    fig1.update_layout(title='Food and non-alcoholic beverages and Housing, water, electricity, gas and other fuel',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Create the second line chart comparing Fresh Products Index, Energy Index, and General Index excluding Fresh Products and Energy
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item3],
                            mode='lines', name='Transport', line=dict(color='green', width=2), marker=dict(size=6)))

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item4],
                            mode='lines', name='Restaurants and hotels', line=dict(color='orange', width=2), marker=dict(size=6)))


    # Update layout for the second chart
    fig2.update_layout(title='Transport, and Restaurants and hotels',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Organize the charts into two columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1,use_container_width=True)
    col2.plotly_chart(fig2,use_container_width=True)


# ALL RWANDA
def Rural():
    # Select the worksheet you want to display
    sheet_name = 'rural1'

    # Read the worksheet into a Pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name)


    st.subheader("Rural CPI in Rwanda: 2009 to 2023)")
    st.info("Base: 2014; Reference: February 2014=100")
    
    with st.expander("""Rural CPI in Rwanda: 2009 to 2023 TABLE"""):  
        # Create a multiselect widget
        selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","GENERAL INDEX (CPI)","Food and non-alcoholic beverages","Alcoholic beverages and tobacco","Clothing and footwear","Housing, water, electricity, gas and other fuel","Furnishing, household and equipment","Health"],key=24)

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

    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df[['Year', 'Month']] = pd.to_datetime(df['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()

    # Assuming you have columns for the specified indices, update the column names accordingly
    item1 = 'Food and non-alcoholic beverages'
    item2 = 'Housing, water, electricity, gas and other fuel'
    item3 = 'Alcoholic beverages and tobacco'
    item4 = 'Restaurants and hotels'

    # Convert 'Year' column to integer
    df['Year'] = df['Year'].astype(int)

    # Set the default slider value to start at the year 2017
    default_start_year = 2017
    x_axis_range = st.slider('Select Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), 
                            value=(default_start_year, int(df['Year'].max())),key=65)

    # Filter the DataFrame based on the selected range
    filtered_df = df[(df['Year'] >= x_axis_range[0]) & (df['Year'] <= x_axis_range[1])]

    # Create the first line chart comparing Imported Goods and Local Goods
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item1],
                            mode='lines', name='Food and non-alcoholic beverages', line=dict(color='red', width=2), marker=dict(size=6)))

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item2],
                            mode='lines', name='Housing, water, electricity, gas and other fuel', line=dict(color='blue', width=2), marker=dict(size=6)))

    # Update layout for the first chart
    fig1.update_layout(title='Food and non-alcoholic beverages and Housing, water, electricity, gas and other fuel',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Create the second line chart comparing Fresh Products Index, Energy Index, and General Index excluding Fresh Products and Energy
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item3],
                            mode='lines', name='Alcoholic beverages and tobacco', line=dict(color='green', width=2), marker=dict(size=6)))

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[item4],
                            mode='lines', name='Restaurants and hotels', line=dict(color='orange', width=2), marker=dict(size=6)))


    # Update layout for the second chart
    fig2.update_layout(title='Alcoholic beverages and tobacco, and Restaurants and hotels',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))  # Set y to 1 to move legend to the top and x to 0 for left alignment

    # Organize the charts into two columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1,use_container_width=True)
    col2.plotly_chart(fig2,use_container_width=True)

# Other indices function
def Other_Indices():
    # Select the worksheet you want to display
    sheet_name = 'other_indices1'

    # Read the worksheet into a Pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name)


    st.subheader("Other indices CPI in Rwanda: 2009 to 2023, Urban only")
    st.info("Base: 2014; Reference: February 2014=100")
        
    

    with st.expander("""Other indices CPI in Rwanda: 2009 to 2023 TABLE"""):  
        # Create a multiselect widget
        selected_columns = st.multiselect('Filter: ',df.columns,default=["YEAR","Local Goods Index","Imported Goods Index","Fresh Products index","Energy index","General Index excluding fresh Products and energy"])
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

    df[['Year', 'Month']] = pd.to_datetime(df['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()

    # Assuming you have columns for the specified indices, update the column names accordingly
    imported_goods_column = 'Imported Goods Index'
    local_goods_column = 'Local Goods Index'
    fresh_products_column = 'Fresh Products index'
    energy_column = 'Energy index'
    general_excluding_fresh_energy_column = 'General Index excluding fresh Products and energy'

    # Convert 'Year' column to integer
    df['Year'] = df['Year'].astype(int)

    # Set the default slider value to start at the year 2017
    default_start_year = 2017
    x_axis_range = st.slider('Select Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), 
                            value=(default_start_year, int(df['Year'].max())))

    # Filter the DataFrame based on the selected range
    filtered_df = df[(df['Year'] >= x_axis_range[0]) & (df['Year'] <= x_axis_range[1])]

    # Create the first line chart comparing Imported Goods and Local Goods
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[imported_goods_column],
                            mode='lines', name='Imported Goods Index', line=dict(color='red', width=2), marker=dict(size=6)))

    fig1.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[local_goods_column],
                            mode='lines', name='Local Goods Index', line=dict(color='blue', width=2), marker=dict(size=6)))

    # Update layout for the first chart
    fig1.update_layout(title='Comparison of Imported Goods vs Local Goods',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))

    # Create the second line chart comparing Fresh Products Index, Energy Index, and General Index excluding Fresh Products and Energy
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[fresh_products_column],
                            mode='lines', name='Fresh Products Index', line=dict(color='green', width=2), marker=dict(size=6)))

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], y=filtered_df[energy_column],
                            mode='lines', name='Energy Index', line=dict(color='orange', width=2), marker=dict(size=6)))

    fig2.add_trace(go.Scatter(x=filtered_df['Year'].astype(str) + '-' + filtered_df['Month'], 
                            y=filtered_df[general_excluding_fresh_energy_column],
                            mode='lines', name='General Index excluding Fresh Products and Energy',
                            line=dict(color='purple', width=2), marker=dict(size=6)))

    # Update layout for the second chart
    fig2.update_layout(title='Comparison of Fresh Products, Energy, and General Index (excluding Fresh Products and Energy)',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1, traceorder='normal'))

    # Organize the charts into two columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)

#Dashboards
def cpi_dashboard():
    st.title("CPI Dashboard")
    # Create the navigation bar
    tab2,tab3, tab4,tab5 = st.tabs(["All Rwanda","Urban", "Rural","Other Indices"])

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
    with tab5:
        Other_Indices()
        
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
                    title="Percentages(%)",
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
        #### <div style="margin-top:40px">GDP at constant 2017 prices from 2007 to 2022</div>
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
                title='GDP growth rate at constant 2017 prices from 2007 to 2022',
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
        #### <div style="margin-top:40px">GDP Deflators [2017=100] prices from 2007 to 2022</div>
        """,unsafe_allow_html=True)
                
        def agriculture_deflators_chart():
            x = deflators_gdp["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=deflators_gdp["Export crops"][8:],
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
                y=deflators_gdp["Food crops"][8:],
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
                  y=deflators_gdp["Livestock & livestock products"][8:],
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
                  y=deflators_gdp["Fishing"][8:],
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
                  y=deflators_gdp["Forestry"][8:],
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
                    title="Agriculture Deflators",
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
            y_cp = deflators_gdp["GROSS DOMESTIC PRODUCT (GDP)"][8:]

            x = deflators_gdp["Years"][8:]


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
                title='GDP Deflators at [2017 = 100] from 2007 to 2022',
                yaxis=dict(
                    title="GDP Deflators",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[0,int(deflators_gdp["GROSS DOMESTIC PRODUCT (GDP)"].max())+20],
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
                                        y=yd + 10, 
                                        x=xd,
                                        text="{:,}".format(yd),
                                        font=dict(family='Arial', size=12,
                                                  color='rgb(50, 171, 96)'),
                                        showarrow=False))

            fig.update_layout(annotations=annotations)

            st.plotly_chart(fig, use_container_width=True)
        def industry_deflators_chart():
            x = deflators_gdp["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=deflators_gdp["Mining & quarrying"][8:],
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
                y=deflators_gdp["TOTAL MANUFACTURING"][8:],
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
                  y=deflators_gdp["Electricity"][8:],
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
                  y=deflators_gdp["Water & waste management"][8:],
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
                  y=deflators_gdp["Construction"][8:],
                  marker=dict(
                      color='rgba(50, 171, 96, 0.6)',
                      line=dict(
                          color='rgba(50, 171, 96, 1.0)',
                          width=2),
                  ),
                  name='Construction',
            ))

            fig.update_layout(
                title='INDUSTRY Deflators from 2007 to 2022',
                yaxis=dict(
                    title="Industry Deflators",
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
            x = deflators_gdp["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=deflators_gdp["TRADE &TRANSPORT"][8:],
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
                y=deflators_gdp["OTHER SERVICES"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.6)',
                    line=dict(
                        color='rgba(40,79,141,1.0)',
                        width=2),
                ),
                name='Other Services',
            ))

            fig.update_layout(
                title='SERVICES Deflators from 2007 to 2022',
                yaxis=dict(
                    title="Services Deflators",
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
            x = deflators_gdp["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=deflators_gdp["TAXES LESS SUBSIDIES ON PRODUCTS"][8:],
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
                    title="Taxes Deflators",
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
    def expenditure_on_gdp():
        st.markdown(""" 
        #### <div style="margin-top:20px">GDP at Current Price from 2007 to 2022</div>
        """,unsafe_allow_html=True)

        def total_expenditure_chart(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=data_df["Government"][8:],
                  marker=dict(
                      color='yellow'
                  ),
                  name='Government',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=data_df["Households and NGOs"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.9)'
                ),
                name='Households and NGOs',
            ))

            fig.update_layout(
                title= data_title,
                yaxis=dict(
                    title="Expenditure in Billions",
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
        def capital_formation_chart(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=data_df["Change in inventories"][8:],
                marker=dict(
                    color='rgb(255, 77, 77)'
                ),
                name='Change in inventories',
            ))

            fig.add_trace(go.Bar(
                  x=x,
                  y=data_df["Gross fixed capital formation"][8:],
                  marker=dict(
                      color='green'
                  ),
                  name='Gross fixed capital formation',
            ))
            
            fig.update_layout(
                title= data_title,
                yaxis=dict(
                    title="Expenditure in Billions",
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
                barmode = "relative"
              )

            st.plotly_chart(fig, use_container_width=True)      
        def exportgs_chart(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating two subplots
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=data_df["Export Goods (fob)"][8:],
                marker=dict(
                    color='rgb(255, 77, 77)'
                ),
                name='Export Goods (fob)',
            ))

            fig.add_trace(go.Bar(
                  x=x,
                  y=data_df["Export Services"][8:],
                  marker=dict(
                      color='green'
                  ),
                  name='Export Services',
            ))
            
            fig.update_layout(
                title= data_title,
                yaxis=dict(
                    title="Exports in Billions",
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
                barmode = "relative"
              )

            st.plotly_chart(fig, use_container_width=True)      
        
        def importgs_chart(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                  x=x,
                  y=data_df["Import Goods (fob)"][8:],
                  marker=dict(
                      color='orange'
                  ),
                  name='Import Goods',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=data_df["Import Services"][8:],
                marker=dict(
                    color='rgba(40,79,141,0.9)'
                ),
                name='Import Services',
            ))

            fig.update_layout(
                title= data_title,
                yaxis=dict(
                    title="Imports in Billions(Rwf)",
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
        def percent_eco_change_chart(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Total final consumption expenditure"][8:]],
                marker=dict(
                    color='green',
                ),
                name='Total final consumption expenditure',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Gross capital formation"][8:]],
                marker=dict(
                    color='rgb(255, 77, 77)'
                ),
                name='Gross capital formation',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Resource balance"][8:]],
                marker=dict(
                    color='rgba(40,79,141,1)'
                ),
                name='Import - Exports',
            ))

            fig.update_layout(
                title=data_title,
                yaxis=dict(
                    title="Percentages(%)",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[-20,100],
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
        def expenditures_growth_rates(data_df, data_title):
            x = data_df["Years"][8:]

            # Creating Figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Total final consumption expenditure"][8:]],
                marker=dict(
                    color='green',
                ),
                name='Total final consumption expenditure',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Gross capital formation"][8:]],
                marker=dict(
                    color='orange'
                ),
                name='Gross capital formation',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Exports of goods & services"][8:]],
                marker=dict(
                    color='rgba(40,79,141,1)'
                ),
                name='Exports of goods & services',
            ))
            fig.add_trace(go.Bar(
                x=x,
                y=[x*100 for x in data_df["Imports of goods & services"][8:]],
                marker=dict(
                    color='rgb(255, 77, 77)'
                ),
                name='Imports of goods & services',
            ))
            fig.add_trace(go.Scatter(
                x=x,
                y=[x*100 for x in data_df["Gross Domestic Product"][8:]],
                marker=dict(
                    color='rgb(5, 1, 21)'
                ),
                name='Gross Domestic Product',
            ))

            fig.update_layout(
                title=data_title,
                yaxis=dict(
                    title="Percentages(%)",
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    range=[-20,50],
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
        def gdp_deflators_chart(data_df,data_title,column="Gross Domestic Product"):
            y_cp = data_df[column][8:]

            x = data_df["Years"][8:]


            # Creating Figure Handle
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, 
                y=y_cp,
                mode='lines+markers',
                line_color='rgb(40,79,141)',
                name='GDP Deflator',
            ))

            fig.update_layout(
                title = data_title,
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

            st.plotly_chart(fig, use_container_width=True)
        # GDP Aggregate
        ExpenditureOnGDP(expenditure_cp, "Proportions of GDP and Percentage Change in GDP")
        
        # Expenditure and Capital Formation
        expenditure, capital=st.columns(2)
        with expenditure:
            total_expenditure_chart(expenditure_cp,"Total final consumption expenditure from 2007 to 2022")
        with capital:
            capital_formation_chart(expenditure_cp,"Gross capital formation from 2007 to 2022")

        # Exports and Imports
        export_gs, import_gs=st.columns(2)
        with export_gs:
            exportgs_chart(expenditure_cp, "Exports of goods & services from 2007 to 2022")
        with import_gs:
            importgs_chart(expenditure_cp, "Imports of goods & services from 2007 to 2022")
            
        st.markdown(""" 
        ###### Percentage Contribution of Sectors to GDP
        """,unsafe_allow_html=True)
        percent_eco_change_chart(expenditure_cpper,"Percentatage Value of Expenditures from 2007 to 2022")


        st.markdown(""" 
        #### <div style="margin-top:20px">GDP at Constant 2017 Price from 2007 to 2022</div>
        """,unsafe_allow_html=True)
        ExpenditureOnGDP(expenditure_c2017, "Proportions of GDP and Percentage Change in GDP")

        # Expenditure and Capital Formation
        expenditure, capital=st.columns(2)
        with expenditure:
            total_expenditure_chart(expenditure_c2017,"Total final consumption expenditure from 2007 to 2022")
        with capital:
            capital_formation_chart(expenditure_c2017,"Gross capital formation from 2007 to 2022")

        # Exports and Imports
        export_gs, import_gs=st.columns(2)
        with export_gs:
            exportgs_chart(expenditure_c2017, "Exports of goods & services from 2007 to 2022")
        with import_gs:
            importgs_chart(expenditure_c2017, "Imports of goods & services from 2007 to 2022")
            
        st.markdown(""" 
        ###### Growth rates of Expenditures from 2007 to 2022
        """,unsafe_allow_html=True)
        expenditures_growth_rates(expenditure_c2017per,"Growth Rates of Expenditures from 2007 to 2022")


        st.markdown(""" 
        #### <div style="margin-top:20px">GDP Deflators at 2017 = 100 from 2007 to 2022</div>
        """,unsafe_allow_html=True)
        # GDP Aggregate
        ExpenditureOnGDP(expenditure_deflator, "GDP Deflators and Deflators on Expenditures",[0,500])
        
        # Expenditure and Capital Formation
        expenditure, capital=st.columns(2)
        with expenditure:
            gdp_deflators_chart(expenditure_deflator,"Total final consumption Deflator from 2007 to 2022","Total final consumption expenditure")
        with capital:
            gdp_deflators_chart(expenditure_deflator,"Capital formation Deflators from 2007 to 2022","Gross capital formation")

        # Exports and Imports
        export_gs, import_gs=st.columns(2)
        with export_gs:
            gdp_deflators_chart(expenditure_deflator, "Exports of goods & services from 2007 to 2022","Exports of goods & services")
        with import_gs:
            gdp_deflators_chart(expenditure_deflator, "Imports of goods & services from 2007 to 2022","Imports of goods & services")
    st.title("GDP Dashboard")
    # Display GDP dashboard option
    tab1, tab2 = st.tabs(["Economic Activities","Expenditure on GDP"])
    # Display GDP dashboard attributes
    with tab1:
       economic_activities()
    with tab2:
      expenditure_on_gdp()

def home_dashboard():
    
  st.title("GDP and CPI Dashboard")
  tab1,tab2=st.tabs(["GDP","CPI"])
  # GDP SUMMARY BASED ON YEAR
  def gdp_home():
    
    st.markdown("""
#### <div style="margin-top:20px">GDP Summary</div>
""",unsafe_allow_html=True)
    
    df_selection=df_macro
    df_selection = df_selection.rename(columns=lambda x: x.strip())
    year = st.selectbox("Select Year", options=df_selection["Years"][2:].iloc[::-1])
    
    # Gdp Summary Function
    def gdp_summary_cards():
        exp_years = [int(x) for x in df_macro["Years"]]
        
        def get_index(item, arr):
           return bisect_left(arr, item)
        
        def get_value(table_column):
           return df_macro[table_column][get_index(year, exp_years)]
        
        # GDP and CPI summary
        total1,total2,total3,total4,total5=st.columns(5, gap='small')
        with total1:
            st.metric(label=f"GDP per Capita in { year }",value=f"""{ "{:,}".format(get_value("GDP per head (in '000 Rwf)")) }k""", delta=f"""{ '{:,}'.format(int(get_value("GDP per head (in '000 Rwf)")) -  df_macro["GDP per head (in '000 Rwf)"][int(get_index(year, exp_years))-1]) }k Rwf""")

        with total2:
            st.metric(label=f"Gross National Income in { year }",value=f"{ '{:,}'.format(get_value('Gross National Income')) }B", delta=f"""{ '{:,}'.format(int(get_value("Gross National Income")) -  df_macro["Gross National Income"][int(get_index(year, exp_years))-1]) }B Rwf""")

        with total3:
            st.metric(label=f"GDP at current price in { year }",value=f"{ '{:,}'.format(get_value('GDP at current prices')) }B",delta=f"{ np.round(get_value('GDP Growth rate at current prices')*100,decimals=2) }%")

        with total4:
            st.metric(label=f"GDP at constantant 2017 in { year }",value=f"{ '{:,}'.format(get_value('GDP at constant 2017 prices'))}B",delta=f"{ np.round(get_value('GDP Growth rate at constant 2017 prices')*100,decimals=2) }%")

        with total5:
            st.metric(label=f"Total Population as in { year }",value='{:,}'.format(get_value("Total population (millions)"))+"M", delta=f"{ np.round(get_value('Population Growth rate')*100,decimals=2) }%")
    
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
                      mode="lines+markers",
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
    ExpenditureOnGDP(expenditure_cp, "Proportions of GDP and Percentage Change in GDP")

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
    data1[['Year', 'Month']] = pd.to_datetime(data1['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()
    # Filter unique months based on the selected year

    # Create dropdown for selecting month

    # Solting Year
    sorted_year=sorted(data1['Year'].unique(), reverse=True)
    sorted_month=sorted(data1['Month'].unique(), reverse=True)
    
    st.info("Base: 2014; Reference: February 2014=100")
    # Configurable Year
    # select year configuration
    selectYear,selectMonth=st.columns(2)
    with selectYear:
       selected_year = st.selectbox('Select Year', sorted(data1['Year'].unique(), reverse=True))
    with selectMonth:
      available_months = sorted(data1[data1['Year'] == selected_year]['Month'].unique(), key=lambda x: datetime.strptime(x, "%m").month, reverse=True)
      selected_month = st.selectbox('Select Month', available_months, format_func=lambda x: datetime.strptime(str(x), "%m").strftime("%B"))
      
      # Filter data based on selected year
      filtered_df = data1[data1['Year'] == selected_year]
      # Extract unique months for the selected year
      unique_months = filtered_df['Month'].unique()
      
      # Create a selectbox for month selection
      # Filter the data based on the selected month and date
    filtered_df_macro = data1[(data1['Year'] == selected_year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column1 =filtered_df_macro['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
        # Filter the data based on the selected month and date
    filtered_df2 = data2[(data1['Year'] == selected_year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column2 =filtered_df2['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
    # Filter the data based on the selected month and date
    filtered_df3 = data3[(data1['Year'] == selected_year) & (data1['Month'] == selected_month)]
    #selected column
    selected_column3 =filtered_df3['GENERAL INDEX (CPI)'].to_string(index=False, header=False)
    
      # RULAR INFLATION
    annual_filtered = data3[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data3[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data3[(data1['Year'] == selected_year) & (data1['Month'].astype(int) == int(selected_month)-1)]    
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
    annual_filtered = data2[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data2[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data2[(data1['Year'] == selected_year) & (data1['Month'].astype(int) == int(selected_month)-1)]  
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
    annual_filtered = data1[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'] == selected_month)]
    if selected_month=="01":

      monthly_filtered = data1[(data1['Year'] == str(int(selected_year)-1)) & (data1['Month'].astype(int) == 12)]
    else:
      monthly_filtered = data1[(data1['Year'] == selected_year) & (data1['Month'].astype(int) == int(selected_month)-1)]  
  
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
    value1=float(selected_column1)
    value2=float(selected_column2)
    value3=float(selected_column3)
    value1= np.round(value1, decimals=2)
    value2= np.round(value2, decimals=2)
    value3= np.round(value3, decimals=2)
    # GDP and CPI summary
    total1,total2,total3=st.columns(3,gap='large')
    with total1:
        st.metric(label=f" Overall Rwanda Index {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value=value1)
        st.metric(label=f" Anually Inflation Rate {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{general_annual_inflation_rate1}%")
        st.metric(label=f" Monthly Inflation Rate {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{general_monthly_inflation_rate1}%")
    with total2:
        st.metric(label=f"Urban Index {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value=value2)
        st.metric(label=f" Anually Inflation Rate  {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{Urban_annual_inflation_rate}%")
        st.metric(label=f" Monthly Inflation Rate {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{Urban_monthly_inflation_rate}%")
    with total3:
        st.metric(label=f"Rural Index {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value=value3)
        st.metric(label=f" Anually Inflation Rate {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{rular_annual_inflation_rate}%")
        st.metric(label=f" Monthly Inflation Rate {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",value="",delta=f"{rular_monthly_inflation_rate}%")
    def general_indices():
        # Load the Excel file
        sheet_name = 'General indices'
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        # Assuming you have columns for the specified indices, update the column names accordingly
        all_rwanda = 'All Rwanda'
        Urban = 'Urban'
        Rular = 'Rular'

        # Convert 'Year' column to integer
        data1['Year'] = data1['Year'].astype(int)

        # Create a date column combining 'Year' and 'Month'
        df['Date'] = pd.to_datetime(data1['Year'].astype(str) + '-' + data1['Month'].astype(str), format='%Y-%m')

        # Create a one-year range from the selected month and year
        end_date = datetime(int(selected_year), int(selected_month), 1)
        start_date = end_date - timedelta(days=365)
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Create the first line chart comparing Imported Goods and Local Goods
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[all_rwanda],
                                mode='lines+markers', name='All Rwanda', line=dict(color='green', width=3), marker=dict(size=8)))

        fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[Urban],
                                mode='lines+markers', name='Urban', line=dict(color='orange', width=3), marker=dict(size=8)))

        fig2.add_trace(go.Scatter(x=filtered_df['Date'], 
                                y=filtered_df[Rular],
                                mode='lines+markers', name='Rural',
                                line=dict(color='purple', width=3), marker=dict(size=6)))

        # Update layout for the second chart
        fig2.update_layout(title=f"Rwanda's inflation year on year in {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",
                        xaxis_title='Year-Month',
                        yaxis_title='CPI Index',
                        legend=dict(x=0, y=1.1, traceorder='normal'))

        # Organize the charts into two columns
        st.plotly_chart(fig2,use_container_width=True)
    general_indices() 
    def other_indicesHome():
  
        sheet_name = 'other_indices1'
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Assuming you have columns for the specified indices, update the column names accordingly
        imported_goods_column = 'Imported Goods Index'
        local_goods_column = 'Local Goods Index'
        fresh_products_column = 'Fresh Products index'
        energy_column = 'Energy index'
        general_excluding_fresh_energy_column = 'General Index excluding fresh Products and energy'

        # Convert 'Year' column to integer
        data1['Year'] = data1['Year'].astype(int)

        # Create dropdown for selecting year

        # Create a date column combining 'Year' and 'Month'
        df['Date'] = pd.to_datetime(data1['Year'].astype(str) + '-' + data1['Month'].astype(str), format='%Y-%m')

        # Create a one-year range from the selected month and year
        end_date = datetime(int(selected_year), int(selected_month), 1)
        start_date = end_date - timedelta(days=365)
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Create the first line chart comparing Imported Goods and Local Goods
        fig1 = go.Figure()

        fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[imported_goods_column],
                                mode='lines', name='Imported Goods Index', line=dict(color='red', width=2), marker=dict(size=6)))

        fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[local_goods_column],
                                mode='lines', name='Local Goods Index', line=dict(color='blue', width=2), marker=dict(size=6)))

        # Update layout for the first chart
        fig1.update_layout(title=f"Comparison of Imported Goods vs Local Goods {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",
                        xaxis_title='Year-Month',
                        yaxis_title='CPI Index',
                        legend=dict(x=0, y=1, traceorder='normal'))

        # Create the second line chart comparing Fresh Products Index, Energy Index, and General Index excluding Fresh Products and Energy
        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[fresh_products_column],
                                mode='lines', name='Fresh Products Index', line=dict(color='green', width=2), marker=dict(size=6)))

        fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[energy_column],
                                mode='lines', name='Energy Index', line=dict(color='orange', width=2), marker=dict(size=6)))

        fig2.add_trace(go.Scatter(x=filtered_df['Date'], 
                                y=filtered_df[general_excluding_fresh_energy_column],
                                mode='lines', name='General Index excluding Fresh Products and Energy',
                                line=dict(color='purple', width=2), marker=dict(size=6)))

        # Update layout for the second chart
        fig2.update_layout(title=f"Comparison of Fresh Products, Energy, and General Index (less Fresh Products and Energy) {datetime.strptime(selected_month, '%m').strftime('%B')} {selected_year}",
                        xaxis_title='Year-Month',
                        yaxis_title='CPI Index',
                        legend=dict(x=0, y=1.1, traceorder='normal'))

        # Organize the charts into two columns
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig1,use_container_width=True)
        col2.plotly_chart(fig2,use_container_width=True)

    other_indicesHome()
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
    options=["Home","GDP","CPI"],
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
st.text("Data Source: national institute of statistics of rwanda")
st.markdown("<div style='font-style:italic;text-align:center'>Copyright (c) 2023 Methode & Saveur</div>",unsafe_allow_html=True)