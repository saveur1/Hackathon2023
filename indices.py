import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set the page layout to wide
st.set_page_config(layout="wide")

def other_indices():
    # Load the Excel file
    excel_file_path = 'CPI.xlsx'
    sheet_name = 'other_indices1'
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    df[['Year', 'Month']] = pd.to_datetime(df['YEAR'], format='%Y-%m').dt.strftime('%Y-%m').str.split('-').tolist()

    # Assuming you have columns for the specified indices, update the column names accordingly
    imported_goods_column = 'Imported Goods Index'
    local_goods_column = 'Local Goods Index'
    fresh_products_column = 'Fresh Products index'
    energy_column = 'Energy index'
    general_excluding_fresh_energy_column = 'General Index excluding fresh Products and energy'

    # Convert 'Year' column to integer
    df['Year'] = df['Year'].astype(int)

    # Create dropdown for selecting year
    selected_year = st.selectbox('Select Year', sorted(df['Year'].unique(), reverse=True))

    # Filter unique months based on the selected year
    available_months = sorted(df[df['Year'] == selected_year]['Month'].unique(), key=lambda x: datetime.strptime(x, "%m").month, reverse=True)

    # Create dropdown for selecting month
    selected_month = st.selectbox('Select Month', available_months, format_func=lambda x: datetime.strptime(str(x), "%m").strftime("%B"))

    # Create a date column combining 'Year' and 'Month'
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')

    # Create a one-year range from the selected month and year
    end_date = datetime(selected_year, int(selected_month), 1)
    start_date = end_date - timedelta(days=365)
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Create the first line chart comparing Imported Goods and Local Goods
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[imported_goods_column],
                            mode='lines', name='Imported Goods Index', line=dict(color='red', width=2), marker=dict(size=6)))

    fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[local_goods_column],
                            mode='lines', name='Local Goods Index', line=dict(color='blue', width=2), marker=dict(size=6)))

    # Update layout for the first chart
    fig1.update_layout(title='Comparison of Imported Goods vs Local Goods',
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
    fig2.update_layout(title='Comparison of Fresh Products, Energy, and General Index (excluding Fresh Products and Energy)',
                    xaxis_title='Year-Month',
                    yaxis_title='CPI Index',
                    legend=dict(x=0, y=1.1, traceorder='normal'))

    # Organize the charts into two columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)

other_indices()
