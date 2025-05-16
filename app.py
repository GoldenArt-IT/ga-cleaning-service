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

@st.cache_data(ttl=3000)
def load_data(data, ttl):
    df = conn.read(worksheet=data, ttl=ttl)
    df = df.dropna(how="all")
    return df

def load_records(data, ttl):
    df = conn.read(worksheet=data, ttl=ttl)
    df = df.dropna(how="all")
    return df

df = load_data("DATA", 3000)

# session state
defaults = {
    "product": df["PRODUCT TYPE"].iloc[0],
    "quantity": 1,
    "Stain Rating": 5,
    "Discolor Rating": 5,
    "Scratch Rating": 5,
    "Other Substance Rating": 5
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Pick item
products = st.selectbox("Select product to service", df["PRODUCT TYPE"].unique(), key="product")
product_row = df.query("`PRODUCT TYPE` == @products").squeeze() # get the row of the selected product

# Create a control statement if the user selects a product
product_multiplier = 1 # default value
product_unit = "N/A" # default value

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
col1.metric("Cleaning price", f"RM {round(total, 1):.2f}")
col2.metric("Cleaning price (after tax)", f"RM {round(total*1.1, 1):.2f}")

def save_and_clear():
    df_records = load_records("CLEANING SERVICE RECORDS", 1)
    new_index = df_records.index.max() + 1 if not df_records.empty else 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row_data = {
        "Timestamp": timestamp,
        "Product": products,
        "Base price per section": section_base,
        "Product Unit": product_unit,
        "Multiplier": product_multiplier,
        "Rate map": rate_map,
        "Scores": scores,
        "Total price": round(total, 1),
        "Total price (after tax)": round(total * 1.1, 1)
    }

    new_data = pd.DataFrame([row_data], columns=df_records.columns, index=[new_index])
    df_records = pd.concat([df_records, new_data], ignore_index=True) 
    conn.update(worksheet="CLEANING SERVICE RECORDS", data=df_records)

    for k, v in defaults.items():
        st.session_state[k] = v
    st.success("Cleaning records saved successfully!")

submitted = st.button("Save cleaning records", on_click=save_and_clear)


# Uncomment the following lines to see the debug information
# st.write("Selected Product:", products)
# st.write("Base price per section:", section_base)
# st.write("Product Unit:", product_unit)
# st.write("Multiplier:", product_multiplier)
# st.write("Rate map:", rate_map)
# st.write("Scores:", scores)
# st.write("Total price:", round(total, 1))
# st.write("Total price (after tax):", round(total * 1.1, 1))
