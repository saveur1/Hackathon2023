import streamlit as st
import plotly.express as px
import pandas as pd

# Load the data into a Pandas DataFrame
df = pd.DataFrame({
    "Years": [2017, 2018, 2019, 2020, 2021, 2022],
    "Agriculture": [10, 12, 15, 18, 22, 26],
    "Industry": [20, 22, 25, 28, 32, 36],
    "Services": [30, 33, 36, 39, 43, 47],
    "GDP": [60, 67, 78, 85, 97, 111]
})

# Calculate the percentage change in GDP
df["Percentage Change"] = df["GDP"].pct_change() * 100

# Create a line chart using Plotly Express
fig = px.line(df, x="Years", y="Percentage Change", color="Industry", line_shape="linear")

# Update the chart layout
fig.update_layout(
    title="Percentage Change in GDP by Sector",
    xaxis_title="Years",
    yaxis_title="Percentage Change",
    legend_title="Sector",
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
