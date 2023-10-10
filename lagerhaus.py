#### import libraries
import streamlit as st

### functions from other files
import functions.bq as bq

########################################################################################################################
# Set the page configuration
st.set_page_config(
    layout="centered",
    page_title="Lagerhaus | MitschHerzog",
    initial_sidebar_state="collapsed", #collapsed
    page_icon="🫙"
)
########################################################################################################################

tab1, tab2, tab3 = st.tabs([
    "Tab 1",
    "Tab 2", 
    "Tab 3"
])

with tab1:
    if st.button("Warehouse Daten abfragen"):
        bq.load_from_bq()