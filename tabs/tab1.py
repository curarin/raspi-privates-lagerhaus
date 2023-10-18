import streamlit as st
import functions.bq as bq
import pandas as pd

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
if "category_sum" not in st.session_state:
    st.session_state.category_sum = None
######################################################

def tab1():
    if st.session_state.my_dataframe_received == False:
        st.write("Nothing to see...")
    if st.session_state.my_dataframe_received == True:

        ### Filter Dataframe by Product Category
        category = my_dataframe.groupby("category")["category"].apply(list).to_dict() #hier
        choices = ("Kategorie", category) #hier
        filtered_df = my_dataframe[my_dataframe['category'] == choices] #hier
        columns_to_drop = ["barcode", "category", "date"]
        new_column_order = ["name", "quantity", "amount", "brand"]
        column_name_mapping = {"name": "Produkt Name",
                               "quantity": "Menge",
                               "amount": "Anzahl",
                               "brand": "Marke"
                              }   
        filtered_df = filtered_df.drop(columns=columns_to_drop) #hier
        filtered_df = filtered_df[new_column_order].rename(columns=column_name_mapping) #hier
        filtered_df = filtered_df.reset_index(drop=True) #hier
        st.dataframe(filtered_df) #hier
