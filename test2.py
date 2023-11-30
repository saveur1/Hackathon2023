import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Set the page layout to wide
st.set_page_config(layout="wide")

# Load the Excel file
excel_file_path = 'CPI.xlsx'
sheet_name = 'urban_inflation'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
df[['Year', 'Month', 'Date']] = pd.to_datetime(df['YEAR'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d').str.split('-').tolist()

# Create a selectbox for the month
selected_month = st.selectbox("Select Month", df['Month'].unique())

# Create a selectbox for the year
selected_year = st.selectbox("Select Year", df['Year'].unique())

# Filter the DataFrame based on the user's selection
filtered_df = df[(df['Month'] == selected_month) & (df['Year'] == selected_year)]

# Sort the DataFrame by the values of the selected column (e.g., 'Meat')
filtered_df = filtered_df.sort_values(by='Meat', ascending=True)  # Change 'Meat' to your desired column

# Display the filtered DataFrame
st.write(f"Data for {selected_month} {selected_year}:")
st.write(filtered_df)

# Calculate Annual Inflation Rate
cpi_beginning_year = filtered_df.iloc[0]['CPI']
cpi_end_year = filtered_df.iloc[-1]['CPI']
annual_inflation_rate = ((cpi_end_year - cpi_beginning_year) / cpi_beginning_year) * 100

# Display Annual Inflation Rate
st.write(f"Annual Inflation Rate for {selected_month} {selected_year}: {annual_inflation_rate:.2f}%")

# Plotly Go Bar Chart with horizontal orientation
fig = go.Figure()

# Select all columns for the x-axis except 'Year', 'Month', and 'Date'
x_columns = [col for col in df.columns if col not in ['Year', 'Month', 'Date', 'YEAR']]

# Set color and text color
bar_color = '#00724c'  # Dark green color
text_color = 'white'
text_font_size = 14  # Adjust font size as needed

for column in x_columns:
    fig.add_trace(go.Bar(
        x=filtered_df[column],  # X-axis will be the current column
        y=filtered_df['Year'],  # Y-axis will be 'Year'
        name=column,
        hoverinfo='text+x',
        orientation='h',  # Set orientation to horizontal
        marker=dict(color=bar_color),  # Set color for all bars
        text=filtered_df[column].apply(lambda x: f'{x:.2f}%'),  # Display percentages in the bar
        textposition='inside',  # Display text inside the bars
        textfont=dict(color=text_color, size=text_font_size),  # Set text color and font size
    ))

fig.update_layout(
    barmode='group',  # Change to 'stack' if you want stacked bars
    title=f'Inflation Rate Chart for {selected_month} {selected_year}',
    xaxis=dict(title='Percentage Change Rate (%)'),  # Set x-axis title
    plot_bgcolor='white',
    yaxis=dict(title='Category'),
    showlegend=False,
    margin=dict(l=50, r=50, t=50, b=50),  # Set margins to increase padding
)

# Display the Plotly Go Bar Chart
st.plotly_chart(fig)
