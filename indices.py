import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set the page layout to wide
st.set_page_config(layout="wide")
excel_file = 'CPI.xlsx'

def urban_indices2():
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
                            value=(default_start_year, int(df['Year'].max())))

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
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)

urban_indices2()
