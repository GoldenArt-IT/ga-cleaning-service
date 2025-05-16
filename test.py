import streamlit as st
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io

# 1. Products & base prices
products = {"1 SEATER SOFA": 50.0, "2 SEATERS SOFA": 100.0, "3 SEATER SOFA": 150.0}

# 2. Pick item
item = st.selectbox("Pick item to service", list(products.keys()))

# 3. Section base price
base = products[item]
section_base = base / 4

# 4. Rate map
rate_map = {5:1.0, 4:1.2, 3:1.4, 2:1.6, 1:1.8}

# 5. Four columns: one per section :contentReference[oaicite:0]{index=0}
sec_names = ["Stain Level", "Discolor Level", "Scratch Level", "Other Substance Level"]
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
