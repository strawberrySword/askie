import streamlit as st

st.set_page_config( 
    page_title="Teacher | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)

# Check access
if "role" not in st.session_state or st.session_state.role != "teacher":
    st.error("Access denied. Please log in as a teacher.")
    st.stop()

st.title("👨‍🏫 Teacher Page")
st.write("Welcome, Teacher!")

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("main.py")