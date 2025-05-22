import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

# Get keys from env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page config
st.set_page_config(
    page_title="Login | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)

# Custom CSS: Rubik font, larger text, better layout
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
    * {
        font-family: 'Rubik', sans-serif !important;
    }
    body {
        background-color: #F7F7F7;
        color: #333333;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(79, 109, 122, 0.1);
    }
    h1, h3, .stRadio, .stTextInput label {
        font-size: 1.5rem !important;
        text-align: right;
        direction: rtl;
    }
    .stButton>button {
        background-color: #A2D2FF;
        color: #333333;
        font-weight: bold;
        font-size: 1.2rem;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }
    .stButton>button:hover {
        background-color: #FF9E9E;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


_, _, col, _, _ = st.columns([1,1,1,1,1])
with col:
    st.image("./assets/brand/logo.png", width=200, use_container_width=False)
st.title("ברוכים הבאים לאסקי")

# Session defaults
if "role" not in st.session_state:
    st.session_state.role = "תלמיד"
if "name" not in st.session_state:
    st.session_state.name = ""

# Role selection (in Hebrew, larger)
st.markdown("### התחברות", unsafe_allow_html=True)
role = st.radio("", ["תלמיד", "מורה"], horizontal=True, label_visibility="collapsed")

# Input (username)
if role == "תלמיד":
    user_name = st.text_input("הכנס שם משתמש")
else:
    user_name = None

# Login button logic
if st.button("כניסה", use_container_width=True):
    st.session_state.role = role
    if role == "תלמיד":
        if not user_name.strip():
            st.error("אנא הכנס שם משתמש.")
        else:
            response = supabase.table("students").select("*").eq("user_name", user_name).execute()
            if response.data:
                student = response.data[0]
                st.session_state.name = student["user_name"]
                st.session_state.student_id = student["id"]
                st.session_state.class_id = student.get("class_id", "0")
            else:
                new_student = supabase.table("students").insert({
                    "user_name": user_name,
                    "class_id": "0"
                }).execute().data[0]
                st.session_state.name = new_student["user_name"]
                st.session_state.student_id = new_student["id"]
                st.session_state.class_id = new_student["class_id"]
            st.switch_page("pages/student.py")
    else:
        st.session_state.username = None
        st.switch_page("pages/teacher.py")