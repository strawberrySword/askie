import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load env vars
load_dotenv()

st.set_page_config(
    page_title="Teacher | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Check access
if "role" not in st.session_state or st.session_state.role != "מורה":
    st.error("Access denied. Please log in as a teacher.")
    st.stop()

st.title("👨‍🏫 Teacher Page")
st.write("Welcome, Teacher!")

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("main.py")

# Student Dashboard Section
st.markdown("---")
st.header("📊 Student Dashboard")

# Fetch students data
try:
    response = supabase.table("students").select("*").execute()
    students = response.data
    
    if students:
        st.write(f"Total Students: {len(students)}")
        
        # Create columns for card layout (3 cards per row)
        cols_per_row = 3
        for i in range(0, len(students), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, student in enumerate(students[i:i+cols_per_row]):
                with cols[j]:
                    # Create a card using container and custom styling
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 10px 0;
                            background-color: #f9f9f9;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <h4 style="margin-bottom: 10px; color: #333;">👤 {student.get('user_name', 'Unknown User')}</h4>
                            <p style="color: #666; margin: 5px 0;"><strong>ID:</strong> {student.get('id', 'N/A')}</p>
                            <p style="color: #666; margin: 5px 0;"><strong>Status:</strong> Active</p>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("No students found in the database.")
        
except Exception as e:
    st.error(f"Error fetching student data: {str(e)}")

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)