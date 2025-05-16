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
products = st.selectbox("Pick type of products to service", df["PRODUCT TYPE"])

# 3. Section base price
product_price = df.loc[df["PRODUCT TYPE"] == products].iloc[0]["PRODUCT SERVICE PRICE"]
section_base = product_price / 4

# 4. Rate map
rate_map = {5:1.0, 4:1.2, 3:1.4, 2:1.6, 1:1.8}

# 5. Section selection
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

# 6. Total price
total = sum(section_base * rate_map[s] for s in scores.values())

# 7. Display
st.metric("Cleaning price", f"RM {total:.2f}")
