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

# Function to get message counts for a student


def get_student_message_counts(student_id):
    try:
        # Get all chats for this student
        chats_response = supabase.table("chats").select(
            "id, character_id").eq("student_id", student_id).execute()
        chats = chats_response.data

        message_counts = {}
        total_messages = 0

        for chat in chats:
            chat_id = chat['id']
            character_id = chat['character_id']

            # Get message count for this chat
            messages_response = supabase.table("messages").select(
                "id", count="exact").eq("chat_id", chat_id).execute()
            message_count = messages_response.count or 0

            # Map character_id to character name
            message_counts[str(character_id)] = message_count
            total_messages += message_count

        # Ensure all three characters are represented
        for i in [0, 1, 2]:
            if str(i) not in message_counts:
                message_counts[str(i)] = 0

        return message_counts, total_messages

    except Exception as e:
        st.error(f"Error fetching message counts: {str(e)}")
        return {}, 0


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

                        # Add button to view student details
                        if st.button(f"View Details", key=f"btn_{student.get('id')}", use_container_width=True):
                            # Store selected student in session state for modal
                            st.session_state.selected_student = student
    else:
        st.info("No students found in the database.")

except Exception as e:
    st.error(f"Error fetching student data: {str(e)}")

# Modal for student details
if "selected_student" in st.session_state and st.session_state.selected_student:
    student = st.session_state.selected_student

    @st.dialog(f"Student Details: {student.get('user_name', 'Unknown User')}")
    def show_student_modal():
        st.write(f"**Student ID:** {student.get('id')}")
        st.write(f"**Username:** {student.get('user_name', 'Unknown User')}")

        st.markdown("---")
        st.subheader("💬 Chat Activity")

        # Get message counts
        with st.spinner("Loading chat data..."):
            message_counts, total_messages = get_student_message_counts(
                student.get('id'))

        if total_messages > 0:
            st.write(f"**Total Messages:** {total_messages}")
            st.markdown("**Messages by Character:**")

            # Display each character's message count
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="David Ben-Gurion",
                    value=message_counts['0']
                )

            with col2:
                st.metric(
                    label="Golda Meir",
                    value=message_counts['1']
                )

            with col3:
                st.metric(
                    label="Herzel",
                    value=message_counts['2']
                )
        else:
            st.info("This student hasn't started any conversations yet.")

        if st.button("Close", type="primary"):
            del st.session_state.selected_student
            st.rerun()

    show_student_modal()

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)
