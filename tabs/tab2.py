import streamlit as st
import functions.bq as bq

### initialize session state stuff
if 'my_dataframe' not in st.session_state:
    st.session_state.my_dataframe = None
if "choices" not in st.session_state:
    st.session_state.choices = []
if "category" not in st.session_state:
    st.session_state.category = []  # Change 'columns' to 'category'
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = None
if "my_dataframe_received" not in st.session_state:
    st.session_state.my_dataframe_received = False
######################################################

def tabs2():
    st.write("Hi")