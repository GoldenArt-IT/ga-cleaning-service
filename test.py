import streamlit as st
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io

st.title("🧼 GA CLEANING SERVICE")

# Load data from Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=3000)
df = df.dropna(how="all")

# Pick item
products = st.selectbox("Select product to service", df["PRODUCT TYPE"])
product_row = df.query("`PRODUCT TYPE` == @products").squeeze() # get the row of the selected product

# Create a control statement if the user selects a product
product_multiplier = 1 # default value
product_types = ["CARPET", "CURTAIN CLEANING", "OFFICE CARPET", "DINING CHAIR", "OFFICE CHAIR"] # product types that require a multiplier
if products in product_types:
    product_unit = product_row.get("PRODUCT UNIT") 
    product_multiplier = st.number_input(f" The {product_unit} for this product?")

# Section base price
product_price = product_row.get("PRODUCT SERVICE PRICE")
section_base = product_price * product_multiplier / 4

# Rate map
rate_map = {5:1.0, 4:1.2, 3:1.4, 2:1.6, 1:1.8}

# Section selection
sec_names = ["Stain Rating", "Discolor Rating", "Scratch Rating", "Other Substance Rating"]
cols = st.columns(4)

scores = {}
for col, sec in zip(cols, sec_names):
    with col:
        # horizontal=True makes options row-aligned :contentReference[oaicite:1]{index=1}
        scores[sec] = st.radio(
            sec.capitalize(), 
            options=[5,4,3,2,1], 
            index=0, 
            horizontal=True, 
            key=sec
        )

# Total price
total = sum(section_base * rate_map[s] for s in scores.values())

# Display
st.divider()
col1, col2 = st.columns([1,1])
col1.metric("Cleaning price", f"RM {total:.2f}")
col2.metric("Cleaning price (after tax)", f"RM {total*1.1:.2f}")
