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

# Function to get quiz scores for a student


def get_student_quiz_scores(student_id):
    try:
        # Get all quiz scores for this student
        quiz_response = supabase.table("quizzes").select(
            "character_id, score").eq("student_id", student_id).execute()
        quizzes = quiz_response.data

        quiz_scores = {}
        total_quizzes = len(quizzes)
        total_score = 0

        for quiz in quizzes:
            character_id = quiz['character_id']
            score = quiz['score']

            quiz_scores[str(character_id)] = score
            total_score += score

        # Ensure all three characters are represented
        for i in [0, 1, 2]:
            if str(i) not in quiz_scores:
                quiz_scores[str(i)] = None

        average_score = total_score / total_quizzes if total_quizzes > 0 else 0

        return quiz_scores, total_quizzes, average_score

    except Exception as e:
        st.error(f"Error fetching quiz scores: {str(e)}")
        return {}, 0, 0

# Function to get character analytics


def get_character_analytics():
    try:
        character_names = {
            0: "David Ben-Gurion",
            1: "Golda Meir",
            2: "Herzel"
        }

        character_stats = {}

        for char_id in [0, 1, 2]:
            # Get total chats for this character
            chats_response = supabase.table("chats").select(
                "id", count="exact").eq("character_id", char_id).execute()
            total_chats = chats_response.count or 0

            # Get all quiz scores for this character
            quiz_response = supabase.table("quizzes").select(
                "score").eq("character_id", char_id).execute()
            quizzes = quiz_response.data

            # Calculate average quiz score
            if quizzes:
                scores = [quiz['score'] for quiz in quizzes]
                avg_score = sum(scores) / len(scores)
                total_quizzes = len(scores)
            else:
                avg_score = 0
                total_quizzes = 0

            character_stats[char_id] = {
                'name': character_names[char_id],
                'total_chats': total_chats,
                'avg_quiz_score': avg_score,
                'total_quizzes': total_quizzes
            }

        return character_stats

    except Exception as e:
        st.error(f"Error fetching character analytics: {str(e)}")
        return {}


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

        # Create tabs for different sections
        tab1, tab2 = st.tabs(["💬 Chat Activity", "🎯 Quiz Scores"])

        with tab1:
            st.markdown("---")

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

        with tab2:
            st.markdown("---")

            # Get quiz scores
            with st.spinner("Loading quiz data..."):
                quiz_scores, total_quizzes, average_score = get_student_quiz_scores(
                    student.get('id'))

            if total_quizzes > 0:
                st.write(f"**Total Quizzes Completed:** {total_quizzes}")
                st.write(f"**Average Score:** {average_score:.1f}%")
                st.markdown("**Scores by Character:**")

                # Display each character's quiz score
                col1, col2, col3 = st.columns(3)

                with col1:
                    score = quiz_scores['0']
                    if score is not None:
                        st.markdown("**David Ben-Gurion**")
                        st.progress(score / 100, text=f"{score}%")
                        if average_score > 0:
                            delta = score - average_score
                            delta_color = "green" if delta >= 0 else "red"
                            st.markdown(
                                f"<span style='color: {delta_color}; font-size: 0.8em;'>Δ {delta:+.1f}%</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**David Ben-Gurion**")
                        st.info("No quiz taken")

                with col2:
                    score = quiz_scores['1']
                    if score is not None:
                        st.markdown("**Golda Meir**")
                        st.progress(score / 100, text=f"{score}%")
                        if average_score > 0:
                            delta = score - average_score
                            delta_color = "green" if delta >= 0 else "red"
                            st.markdown(
                                f"<span style='color: {delta_color}; font-size: 0.8em;'>Δ {delta:+.1f}%</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**Golda Meir**")
                        st.info("No quiz taken")

                with col3:
                    score = quiz_scores['2']
                    if score is not None:
                        st.markdown("**Herzel**")
                        st.progress(score / 100, text=f"{score}%")
                        if average_score > 0:
                            delta = score - average_score
                            delta_color = "green" if delta >= 0 else "red"
                            st.markdown(
                                f"<span style='color: {delta_color}; font-size: 0.8em;'>Δ {delta:+.1f}%</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**Herzel**")
                        st.info("No quiz taken")

                # Add a visual representation of scores
                st.markdown("---")
                st.markdown("**Quiz Performance Overview:**")

                # Create a simple bar chart data
                chart_data = []
                character_names = ["David Ben-Gurion", "Golda Meir", "Herzel"]

                for i, name in enumerate(character_names):
                    score = quiz_scores[str(i)]
                    if score is not None:
                        chart_data.append({"Character": name, "Score": score})

                if chart_data:
                    import pandas as pd
                    df = pd.DataFrame(chart_data)
                    # Create a chart with y-axis from 0 to 100
                    st.bar_chart(df.set_index(
                        "Character"), y_label="Score (%)", height=400, use_container_width=True)

                    # Set the y-axis range to 0-100 by creating a custom chart
                    chart = st.empty()
                    with chart.container():
                        # Add a note about the percentage scale
                        st.caption(
                            "📊 Quiz scores are displayed as percentages (0-100%)")

            else:
                st.info("This student hasn't completed any quizzes yet.")

        if st.button("Close", type="primary"):
            del st.session_state.selected_student
            st.rerun()

    show_student_modal()

# Character Dashboard Section
st.markdown("---")
st.header("🎭 Character Dashboard")

try:
    with st.spinner("Loading character analytics..."):
        character_stats = get_character_analytics()

    if character_stats:
        # Create three columns for character cards
        col1, col2, col3 = st.columns(3)

        columns = [col1, col2, col3]

        for i, (char_id, stats) in enumerate(character_stats.items()):
            with columns[i]:
                # Create character card
                st.markdown(f"""
                <div style="
                    border: 2px solid #4CAF50;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    text-align: center;
                ">
                    <h4 style="margin-bottom: 15px; color: #2E7D32; font-size: 1.2em;">
                        {stats['name']}
                    </h4>
                </div>
                """, unsafe_allow_html=True)

                # Display metrics
                st.metric(
                    label="💬 Total Chats",
                    value=stats['total_chats']
                )

                if stats['total_quizzes'] > 0:
                    st.metric(
                        label="🎯 Avg Quiz Score",
                        value=f"{stats['avg_quiz_score']:.1f}%"
                    )
                    st.caption(
                        f"Based on {stats['total_quizzes']} quiz{'zes' if stats['total_quizzes'] != 1 else ''}")
                else:
                    st.metric(
                        label="🎯 Avg Quiz Score",
                        value="No data"
                    )
                    st.caption("No quizzes completed yet")

        # Summary statistics
        st.markdown("---")
        st.subheader("📊 Overall Character Performance")

        total_chats = sum(stats['total_chats']
                          for stats in character_stats.values())
        characters_with_quizzes = [
            stats for stats in character_stats.values() if stats['total_quizzes'] > 0]

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.metric(
                label="Total Chats Across All Characters",
                value=total_chats
            )

        with summary_col2:
            if characters_with_quizzes:
                overall_avg = sum(
                    stats['avg_quiz_score'] for stats in characters_with_quizzes) / len(characters_with_quizzes)
                st.metric(
                    label="Overall Average Quiz Score",
                    value=f"{overall_avg:.1f}%"
                )
            else:
                st.metric(
                    label="Overall Average Quiz Score",
                    value="No data"
                )

        with summary_col3:
            total_quizzes = sum(stats['total_quizzes']
                                for stats in character_stats.values())
            st.metric(
                label="Total Quizzes Completed",
                value=total_quizzes
            )

        # Character comparison chart
        if characters_with_quizzes:
            st.markdown("---")
            st.subheader("📈 Character Quiz Performance Comparison")

            import pandas as pd

            # Prepare data for chart
            chart_data = []
            for stats in character_stats.values():
                if stats['total_quizzes'] > 0:
                    chart_data.append({
                        "Character": stats['name'],
                        "Average Score": stats['avg_quiz_score'],
                        "Total Quizzes": stats['total_quizzes']
                    })

            if chart_data:
                df = pd.DataFrame(chart_data)

                # Create two columns for different visualizations
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.markdown("**Average Quiz Scores**")
                    st.bar_chart(df.set_index("Character")[
                                 "Average Score"], height=300)

                with chart_col2:
                    st.markdown("**Total Quiz Activity**")
                    st.bar_chart(df.set_index("Character")[
                                 "Total Quizzes"], height=300)

                st.caption(
                    "📊 Performance metrics help identify which characters are most engaging for students")

    else:
        st.info("No character data available.")

except Exception as e:
    st.error(f"Error loading character dashboard: {str(e)}")


# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)
