import streamlit as st
import numpy as np
import time
st.selectbox('Select your favorite fruit:', [('apple', 'Apple'), ('banana', 'Banana'), ('orange', 'Orange')], key='fruit')

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep()
    st.success("Done!")
    
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)
