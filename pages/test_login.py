import streamlit as st
import time

st.title("Test Login Page")

allowed_emails = ["store.goldenart@gmail.com", "sharul.ariffin13@gmail.com"]

# Check login
if st.button("🔐 Login with Google"):
    st.login("google")
if st.button("Logout"):
    st.toast("Successfully logged out.")
    time.sleep(3)
    st.logout()

    
if st.experimental_user.is_logged_in == False:
    st.stop()

# If logged in, check access
if st.experimental_user.email not in allowed_emails:
    st.error("Access denied. You’re not authorized to view this app.")
    st.stop()

# If passed, show the app
st.write(f"Hello, {st.experimental_user.name} ({st.experimental_user.email})")

st.json(st.experimental_user)