#### import libraries
import streamlit as st

### functions from other files
import functions.bq as bq
import tabs.tab1 as haben
import tabs.tab2 as brauchen

########################################################################################################################
# Set the page configuration
st.set_page_config(
    layout="centered",
    page_title="Lagerhaus | MitschHerzog",
    initial_sidebar_state="collapsed", #collapsed
    page_icon="🫙"
)
st.title("🍽️ Lagerhaus | Mitsch&Herzog")
st.write("Aktualisiere die Daten, indem du auf den Button drückst.")

########################################################################################################################
if "my_dataframe_received" not in st.session_state:
    st.session_state.my_dataframe_received = False

if st.button("Jetzt Daten aktualisieren"):
    st.session_state.my_dataframe, st.session_state.my_dataframe_received = bq.load_from_bq()

tab1, tab2 = st.tabs([
    "Wir haben...",
    "Wir brauchen..."
])

with tab1:
    haben.tab1()

with tab2:
    st.write("test")