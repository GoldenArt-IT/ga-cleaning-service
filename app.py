import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
# from upload_to_drive import upload_file_to_drive
import base64
from PIL import Image
import io

# — disable wrap on mobile and allow horizontal scroll —
st.markdown("""
<style>
  /* find every columns container and stop it from wrapping */
  div[data-testid="stHorizontalBlock"] > div {
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
  }
  /* give each column a minimum width so they don't all shrink to zero */
  div[data-testid="stHorizontalBlock"] > div > div {
    min-width: 120px;
  }
</style>
""", unsafe_allow_html=True)

# # — Inject CSS to hide the big drop‑zone and only show the small button —
# hide_dropzone = """
# <style>
#   /* remove the grey box around uploader */
#   section[data-testid="stFileUploadDropzone"] {
#     border: none !important;
#     background: transparent !important;
#     padding: 0 !important;
#     margin: 0 !important;
#   }
#   /* hide drag‑and‑drop instructions */
#   div[data-testid="stFileDropzoneInstructions"] {
#     display: none !important;
#   }
# </style>
# """
# st.markdown(hide_dropzone, unsafe_allow_html=True)  # :contentReference[oaicite:0]{index=0}

# — Load data from Google Sheets —
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=3000)
df = df.dropna(how="all")
# st.dataframe(df)

# — Title —
st.title("📲 GA TRADE-IN CALCULATOR")

# — Model selector —
model = st.selectbox("Select Model:", df["MODEL"])

# — Look up and display price & tier —
selected = df.loc[df["MODEL"] == model].iloc[0]
price_str = selected["PRICE VALUE"]
price = round(price_str, 2)
tier  = selected["VALUE TIER"]

col1, col2 = st.columns([1,1])
with col1:
    st.text_input("Price Value (RM)", value=price, disabled=True)
with col2:
   st.text_input("Value Tier",  value=tier,  disabled=True)

st.divider()

# — NCD scoring table (interactive) —
with st.expander("NCD Scoring Table"):
  st.subheader("NCD Scoring Table")
  requirements = [
      "Frame (Wood Structure)",
      "Sponge Condition",
      "Fabric / Leather Wear",
      "Fading / Discoloration",
      "Odor / Smoke / Pets",
      "Dent / Scratch / Stains",
      "Cushion Bounce",
      "Spring Noise / Sinking",
      "Leg Stability",
      "Overall Cleanliness",
  ]

  # # Header row
  # h0, h1, h2, h3, h4 = st.columns([4, 1, 1, 1, 1])
  # h0.markdown("**Requirement**")
  # h1.markdown("**Perfect (10)**")
  # h2.markdown("**Average (5)**")
  # h3.markdown("**Bad (0)**")
  # h4.markdown("**Upload**")

  # Rows with checkboxes + compact file uploader
  scores = {}
  upload = {}
  defaults = set(requirements[:1])

  for req in requirements:
      c0, c1, c2, c3, c4, c5, c6, c7 = st.columns([4, 1, 1, 1, 1, 1, 1, 1])
      c0.write(req)
      sel10 = c1.checkbox("Perfect (10 points)", value=(req in defaults),key=f"{req}_10")
      sel8  = c2.checkbox("Semi Perfect (8 points)", value=False, key=f"{req}_8")
      sel6  = c3.checkbox("Average (6 points)", value=False, key=f"{req}_6")
      sel4  = c4.checkbox("Below Average (4 points)", value=False, key=f"{req}_4")
      sel2  = c5.checkbox("Not Good (2 points)", value=False, key=f"{req}_2")
      sel0  = c6.checkbox("Bad (0 points)", value=False, key=f"{req}_0")
      sel_upload = c7.file_uploader(
          label="",
          type=["png", "jpg", "pdf"],
          key=f"{req}_upload",
          label_visibility="collapsed"
      )
      
      if sel_upload is not None:
         st.image(sel_upload)

      scores[req] = 10 if sel10 else 8 if sel8 else 6 if sel6 else 4 if sel4 else 2 if sel2 else 0
      upload[req] = sel_upload
      
      st.divider()

  total_ncd = sum(scores.values())
  # scores["Frame (Wood Structure)"]
  # upload["Frame (Wood Structure)"]
  # for req, file in upload.items():
  #   if file is not None and file.type.startswith("image/"):
  #       st.image(file, caption=req, use_column_width=True)

  st.markdown(f"**Total NCD Score: {total_ncd}**")

st.divider()

# — Main input panels —
seg1, seg2, seg3 = st.columns(3)
with seg1:
    year_purchased = float(st.text_input("YEAR OF PURCHASE (year)", value=11))

    select_year = df.loc[df["YEARS OF PURCHASED"] == year_purchased].iloc[0]
    select_year_trade_value = select_year["TRADE IN VALUE"]
    trade_value = price - (price/100) * select_year_trade_value

    trade_in_value = st.text_input("TRADE IN VALUE (RM)", round(trade_value, 2), disabled=True)
with seg2:
    st.text_input("NCD SCORE", value=str(total_ncd), disabled=True)

    ncd_score = df.loc[df["NCD SCORE"] == total_ncd].iloc[0]
    ncd_deduction_rates = ncd_score["NCD DEDUCT RATES"]

    ncd_deduction_value = trade_value/100 * ncd_deduction_rates

    ncd_deduction = st.text_input("NCD DEDUCTION", round(ncd_deduction_value, 2), disabled=True)
with seg3:
    select_bonus = select_year["ADDITIONAL DISCOUNTS"]
    bonus_years  = st.text_input("BONUS (loyal >10 yrs)", select_bonus, disabled=True)

    bonus_value = select_bonus * trade_value
    bonus_points = st.text_input("BONUS POINT", round(bonus_value, 2), disabled=True)

total_trade_in_value = round(trade_value - ncd_deduction_value + bonus_value, 2)

st.markdown(f"**TOTAL TRADE IN VALUE : RM {total_trade_in_value}**")

submitted = st.button("Save Trade-in Records")

if submitted:
  conn = st.connection("gsheets", type=GSheetsConnection)
  df_records = conn.read(worksheet="TRADE IN RECORDS", ttl=1)
  df_records = df_records.dropna(how="all")

  # st.write(df_records[:0])

  timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

  row_data = [timestamp, model, price, tier, year_purchased, trade_in_value, ncd_deduction_rates, ncd_deduction, bonus_years, bonus_points, total_trade_in_value]

  for field in requirements:
    score = scores.get(field, 0)
    file = upload.get(field)
    if file:
        img = Image.open(file)
        img = img.convert("RGB")  # Convert to RGB if not already in that mode
        img = img.resize((320, 240)) # Image resolution

        # ✅ Convert to byte stream
        buffered = io.BytesIO()
        img.save(buffered, format="WEBP", optimize=True, quality=95, subsampling=0, progressive=True)  # or "PNG"
        img_bytes = buffered.getvalue()

        # ✅ Convert to base64 string
        b64 = base64.b64encode(img_bytes).decode()
        image_url = f"data:image/jpeg;base64,{b64}"
    else:
        image_url = ""
    row_data.extend([score, image_url])

  new_index = df_records.index.max() + 1 if not df_records.empty else 0
  new_data = pd.DataFrame([row_data], columns=df_records.columns, index=[new_index])
  update_df = pd.concat([df_records, new_data], ignore_index=True)
  conn.update(worksheet="TRADE IN RECORDS", data=update_df)
  st.success("Record updated successfully.")

st.divider()
