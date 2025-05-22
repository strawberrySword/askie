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
    user_name = st.text_input("Enter your user_name:")
else:
    user_name = None

# Login button
if st.button("Enter"):
    st.session_state.role = role

    if role == "student":
        if not user_name.strip():
            st.error("Please enter a user name.")
        else:
            # Check if student exists
            response = supabase.table("students").select("*").eq("user_name", user_name).execute()

            if response.data:
                student = response.data[0]
                st.session_state.name = student["user_name"]
                st.session_state.student_id = student["id"]
                st.session_state.class_id = student.get("class_id", "0")
            else:
                # Create new student
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