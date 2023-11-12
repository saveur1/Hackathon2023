import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time

st.set_page_config(page_title="NISR Analysis",page_icon="🌍",layout="wide")
st.title(":house: NISR Dashboard")
st.markdown("<style>div.block-container{padding-top:1.5rem;}</style>", unsafe_allow_html=True)

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def expanditure_on_gdp_chart():
    # Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Year': [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        'Gross capital formation': [3.5, 4.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5],
        'Exports G&S': [2.5, 3.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5],
        'Households': [1.5, 2.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5],
        'Government': [0.5, 1.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5],
        'Imports G&S': [1.5, 2.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5],
        'GDP': [1.5, 2.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5]
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
        yaxis=dict(title='Thousands of Dollars', range=[0, 100]),
        barmode='stack'
    )

    # Create the figure and plot it using Plotly
    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6], layout=layout)
    st.plotly_chart(fig, use_container_width=True)
    
 
#load excel file
df1=pd.read_excel('Tutorial Spread.xlsx', sheet_name='Sheet1')
df1 = df1.rename(columns=lambda x: x.strip())


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
    # Create a dataframe with the data from the image
    data = pd.DataFrame({
        'Year': df1["Years"][18:],
        'Agriculture': [x*100 for x in df1['Agriculture'][18:]],
        'Industry': [x*100 for x in df1['Industry'][18:]],
        'Services': [x*100 for x in df1['Services'][18:]],
        'Adjustments': [x*100 for x in df1['Adjustments'][18:]],
    })

    # Create the traces for the chart
    trace1 = go.Bar(x=data['Year'], y=data['Agriculture'], name='Agriculture')
    trace2 = go.Bar(x=data['Year'], y=data['Industry'], name='Industry')
    trace3 = go.Bar(x=data['Year'], y=data['Services'], name='Services')
    trace4 = go.Bar(x=data['Year'], y=data['Adjustments'], name='Adjustments')

    # Create the layout for the chart
    layout = go.Layout(
        title='Value Added by Agriculture, Industry and Services',
        xaxis=dict(title='Years'),
        yaxis=dict(title='Percentage Change', range=[-7.5, 60]),
        barmode='group'
    )

    # Create the figure and plot it using Streamlit
    fig = go.Figure(data=[trace1, trace2, trace3,trace4], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def MacroTable():
    # Expanding Table
    with st.expander("GDP Summary Table"):
        showData = st.multiselect('Filter: ', df1.columns, default=[
                            "Years", "GDP at current prices", "Growth rate-cp", "Growth rate", "Implicit GDP deflator", "Growth rate-d", "GDP per head (in '000 Rwf)", "GDP per head (in current US dollars)"])
        st.dataframe(df1[showData],use_container_width=True)



#side bar
st.sidebar.image("logo/logo2.png")

#switcher
st.sidebar.header("GDP Filters")



def MacroEconomicHome():
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


MacroEconomicHome()
#theme
hide_st_style="""

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""



