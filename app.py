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
def load_data(data, ttl, header_first_row=True):
    df = conn.read(worksheet=data, ttl=ttl)
    df = df.dropna(how="all")
    if header_first_row == True:
        df = pd.DataFrame(df.values[1:], columns=df.iloc[0])
    return df

def load_data_ALWAYS_RELOAD(data, ttl, header_first_row=True):
    df = conn.read(worksheet=data, ttl=ttl)
    df = df.dropna(how="all")
    if header_first_row == True:
        df = pd.DataFrame(df.values[1:], columns=df.iloc[0])
    return df


def load_records(data, ttl):
    df = conn.read(worksheet=data, ttl=ttl)
    df = df.dropna(how="all")
    return df

df = load_data("SETTING", 3000, False)
df_arrangement = load_data_ALWAYS_RELOAD("RECORDS", 20, True) # load records from ga cleaning service - arrangement
df_arrangement = df_arrangement.query("`CLEANING SERVICE` == 'ON PROGRESS'")

# session states
defaults = {
    "product": df["PRODUCT TYPE"].iloc[0],
    "quantity": 1,
    "Stain Rating": 4,
    "Discolor Rating": 4,
    "Scratch Rating": 4,
    "Other Substance Rating": 4
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Pick item
customer = st.selectbox("Select customer", df_arrangement["CUST NAME"].unique(), key="customer")
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
rate_map_1 = {1:1, 2:1.1, 3:1.2}
rate_map_2 = {"LEVEL 1":1, "LEVEL 2":1.06, "LEVEL 3":1.13, "LEVEL 4":1.2}
rate_map_3 = {"LIKE NEW":1, "GRED A":1.06, "GRED B":1.13, "GRED C":1.2}
rate_map_4 = {"30 MIN - 1 JAM":1, "1 JAM - 2 JAM":1.06, "2 JAM - 4 JAM":1.13, "4 JAM":1.2}

# Section selection
sec_names = ["SKALA KEKOTORAN", "TAHAP KEKOTORAN", "KONDISI BARANG", "MASA SIAP SERVICE"]
cols = st.columns(4)

# scores = {}
# for col, sec in zip(cols, sec_names):
#     with col:
#         # horizontal=True makes options row-aligned :contentReference[oaicite:1]{index=1}
#         scores[sec] = st.radio(
#             sec.capitalize(), 
#             options=[4,3,2,1], 
#             index=0, 
#             horizontal=True, 
#             key=sec
#         )

with cols[0]:
    score_1 = st.radio(
        sec_names[0], 
        options=[1, 2, 3],
        index=0, 
        horizontal=True
    )
with cols[1]:
    score_2 = st.radio(
        sec_names[1], 
        options=["LEVEL 1", "LEVEL 2", "LEVEL 3", "LEVEL 4"],
        index=0, 
        horizontal=True
    )
with cols[2]:
    score_3 = st.radio(
        sec_names[2], 
        options=["LIKE NEW", "GRED A", "GRED B", "GRED C"],
        index=0, 
        horizontal=True
    )
with cols[3]:
    score_4 = st.radio(
        sec_names[3], 
        options=["30 MIN - 1 JAM", "1 JAM - 2 JAM", "2 JAM - 4 JAM", "4 JAM"],
        index=0, 
        horizontal=True
    )

total_rate_score = rate_map_1[score_1] + rate_map_2[score_2] + rate_map_3[score_3] + rate_map_4[score_4]

total_1 = rate_map_1[score_1] * section_base
total_2 = rate_map_2[score_2] * section_base
total_3 = rate_map_3[score_3] * section_base
total_4 = rate_map_4[score_4] * section_base



# Total price
total = total_1 + total_2 + total_3 + total_4


# Display
st.divider()

# Display layout
if products == "CARPET":
    st.subheader("Cleaning Service Layout")
    df_type = load_data("SETTING", 3000, False)
    df_type = df_type.query("`TYPE` == 'CARPET'")
    df_type = df_type[["TYPE", "LEVEL", "LANGKAH"]]
    st.table(df_type)

elif products.startswith("M"):
    st.subheader("Cleaning Service Layout")
    df_type = load_data("SETTING", 3000, False)
    df_type = df_type.query("`TYPE` == 'BED'")
    df_type = df_type[["TYPE", "LEVEL", "LANGKAH"]]
    st.table(df_type)

else:
    st.subheader("Cleaning Service Layout")
    df_type = load_data("SETTING", 3000, False)
    df_type = df_type.loc[(df_type["TYPE"] == "ALL TYPE") & (df_type["LEVEL"] == score_2)]
    df_type = df_type[["TYPE", "LEVEL", "LANGKAH"]]
    st.table(df_type)

col1, col2 = st.columns([1,1])
col1.metric("Cleaning price", f"RM {round(total, 1):.2f}")
# col2.metric("Cleaning price (after tax)", f"RM {round(total*1.1, 1):.2f}")

def save_and_clear():
    df_records = load_records("CLEANING RECORDS", 1)
    new_index = df_records.index.max() + 1 if not df_records.empty else 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row_data = {
        "TIMESTAMP": timestamp,
        "CUSTOMER NAME": customer,
        "PRODUCT": products,
        "BASE PRICE PER SECTION": section_base,
        "PRODUCT UNIT": product_unit,
        "MULTIPLIER": product_multiplier,
        "SCORE": total_rate_score,
        "TOTAL PRICE": round(total, 1)
    }

    new_data = pd.DataFrame([row_data], columns=df_records.columns, index=[new_index])
    df_records = pd.concat([df_records, new_data], ignore_index=True) 
    conn.update(worksheet="CLEANING RECORDS", data=df_records)

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
