import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json

# Convert Streamlit secret dict to string and then to credentials
creds_dict = dict(st.secrets["connections"]["gsheets"])
creds_json = json.loads(json.dumps(creds_dict))

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

client = gspread.authorize(credentials)
sheet = client.open("SOFA TRADE IN CHECKER").worksheet("CLEANING SERVICE RECORDS")
sheet.append_row(["meh", "test", "tets"]) # dummy row data
data = sheet.get_all_records()
st.dataframe(data)