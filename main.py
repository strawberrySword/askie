import streamlit as st

st.set_page_config( 
    page_title="Login | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)


st.title("👋 Welcome to Askie!")

# Session defaults
if "role" not in st.session_state:
    st.session_state.role = "student"
if "name" not in st.session_state:
    st.session_state.name = ""


# Actual Streamlit role selection (synced with the above manually)
role = st.radio("Role", ["student", "teacher"], horizontal=True, label_visibility="collapsed")

# Name input for students
if role == "student":
    name = st.text_input("Enter your name:")
else:
    name = None

# Login button
if st.button("Enter"):
    st.session_state.role = role
    st.session_state.name = name if name else ""

    if role == "student":
        if not name.strip():
            st.error("Please enter your name.")
        else:
            st.switch_page("pages/student.py")
    else:
        st.switch_page("pages/teacher.py")