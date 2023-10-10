import pandas_gbq
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import streamlit as st
import json


bq = "adroit-medium-379911.privat_lagerbestand.lagerbestand_pi"

data = {
    "type": "service_account",
    "project_id": st.secrets["service_account"]["project_id"],
    "private_key_id": st.secrets["service_account"]["private_key_id"],
    "private_key": st.secrets["service_account"]["private_key"],
    "client_email": st.secrets["service_account"]["client_email"],
    "client_id": st.secrets["service_account"]["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["service_account"]["client_x509_cert_url"],
    "universe_domain": "googleapis.com"
}
service_account_json = json.dumps(data, indent=4)
service_account_info = json.loads(service_account_json)
current_date = datetime.now().strftime("%Y-%m-%d")

credentials = service_account.Credentials.from_service_account_info(service_account_info)

def load_from_bq():
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    query = f"""
    SELECT *
    FROM `adroit-medium-379911.privat_lagerbestand.lagerbestand_pi`
    """
    df = pd.read_gbq(query, project_id="adroit-medium-379911", credentials=credentials)
    st.write(df)