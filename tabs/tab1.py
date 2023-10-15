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
        st.session_state.category = st.session_state.my_dataframe.groupby("category")["category"].apply(list).to_dict()
        st.session_state.choices = st.selectbox("Kategorie", st.session_state.category)
        st.session_state.filtered_df = st.session_state.my_dataframe[st.session_state.my_dataframe['category'] == st.session_state.choices]
        columns_to_drop = ["barcode", "category", "date"]
        new_column_order = ["name", "quantity", "amount", "brand"]
        column_name_mapping = {"name": "Produkt Name",
                               "quantity": "Menge",
                               "amount": "Anzahl",
                               "brand": "Marke"
                              }   
        st.session_state.filtered_df = st.session_state.filtered_df.drop(columns=columns_to_drop)
        st.session_state.filtered_df = st.session_state.filtered_df[new_column_order].rename(columns=column_name_mapping)
        st.session_state.filtered_df = st.session_state.filtered_df.reset_index(drop=True)
        st.dataframe(st.session_state.filtered_df)

        #st.session_state.category_sum = st.session_state.my_dataframe.groupby("category")["amount"].sum().reset_index()
        #st.session_state.category_sum['amount'] = st.session_state.category_sum['amount'].astype(int)


        # Now you can use 'category' as the x-axis values in st.bar_chart
        #st.subheader("Übersicht aller Kategorien")
        #st.bar_chart(st.session_state.category_sum, x="category", y="amount")
