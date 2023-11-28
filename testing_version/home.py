import streamlit as st
import streamlit_option_menu as opt

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

with st.sidebar:
#     st.markdown("""
# # Welcome to Flat Iron School
#                 This is where future begin
# """)
    home_selected = opt.option_menu("",["Home"], 
                icons=['house', 'gear'], default_index=-1,key="gdp_options")
    with st.expander("GDP"):
        gdp_selected = opt.option_menu("",["Home", 'Settings'], 
                icons=['house', 'gear'], default_index=-1,key="gdp_options")

        # if selected == "Home":
        #     st.write("home is where the heart is")
        # else:
        #     st.write("settings is my bettings")
    with st.expander("CPI"):
        cpi_selected = opt.option_menu("",["Home", 'Settings'], 
                icons=['house', 'gear'], default_index=-1,key="cpi_options")

        # if selected == "Home":
        #     st.write("home is where the heart is")
        # else:
        #     st.write("settings is my bettings")