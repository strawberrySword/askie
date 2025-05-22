import streamlit as st
from supabase_utils import get_all_chats
import pandas as pd

st.set_page_config(page_title="Askie - Teacher Dashboard", layout="wide")
st.title("🧑‍🏫 Teacher Dashboard")

chats, students, messages, grades = get_all_chats()

# Link students to chats and grades
student_map = {s["id"]: s["username"] for s in students}
chat_map = {c["id"]: c["student_id"] for c in chats}

data = []
for grade in grades:
    chat_id = grade["chat_id"]
    student_id = chat_map.get(chat_id, "unknown")
    student_name = student_map.get(student_id, "unknown")

    data.append({
        "Student": student_name,
        "Score": grade["score"],
        "Answers": grade["answers"]
    })

df = pd.DataFrame(data)
st.dataframe(df)

# Class stats
st.subheader("📉 Class-Level Struggles")

q1_wrong = sum("rome" not in a["q1"].lower() for a in df["Answers"])
q2_wrong = sum("brutus" not in a["q2"].lower() for a in df["Answers"])
q3_wrong = sum("veni" not in a["q3"].lower() for a in df["Answers"])

st.write(f"❌ Question 1 missed by: {q1_wrong} students")
st.write(f"❌ Question 2 missed by: {q2_wrong} students")
st.write(f"❌ Question 3 missed by: {q3_wrong} students")
