import streamlit as st
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from module.charachtars import ConversationSession

if __name__ == '__main__':

    # Get keys from env
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


    # Define questions and answers
    all_questions ={
        "David Ben-Gurion": [    
            {
                "question": "מה היה שמו המלא של דוד בן גוריון בלידתו?",
                "answers": ["דוד גרין", "דוד לוי", "דוד בלוך", "דוד ויינר"],
                "correct": "דוד גרין"
            },
            {
                "question": "באיזו שנה הכריז דוד בן גוריון על הקמת מדינת ישראל?",
                "answers": ["1948", "1950", "1947", "1949"],
                "correct": "1948"
            },
            {
                "question": "מאיזו מדינה עלה דוד בן גוריון לארץ ישראל?",
                "answers": ["פולין", "רוסיה", "רומניה", "גרמניה"],
                "correct": "פולין"
            },
            {
                "question": "מה היה תפקידו הראשון של בן גוריון בממשלת ישראל?",
                "answers": ["ראש ממשלה ושר הביטחון", "נשיא", "שר החוץ", "ראש עיריית תל אביב"],
                "correct": "ראש ממשלה ושר הביטחון"
            },
            {
                "question": "בן גוריון פרש לחיי שקט היכן?",
                "answers": ["שדה בוקר", "ראש פינה", "מצפה רמון", "ירוחם"],
                "correct": "שדה בוקר"
            }],
        "Golda Meir": [
            {
                "question": "באיזו מדינה נולדה גולדה מאיר?",
                "answers": ["אוקראינה", "ארצות הברית", "רוסיה", "פולין"],
                "correct": "אוקראינה"
            },
            {
                "question": "מה היה שמה בלידה של גולדה מאיר?",
                "answers": ["גולדה מבוביץ'", "גולדה ויינשטיין", "גולדה לוי", "גולדה פרידמן"],
                "correct": "גולדה מבוביץ'"
            },
            {
                "question": "מה היה תפקידה הראשון של גולדה מאיר בממשלת ישראל?",
                "answers": ["שרת העבודה", "שרת החוץ", "ראש הממשלה", "שרת הפנים"],
                "correct": "שרת העבודה"
            },
            {
                "question": "איזו מלחמה התרחשה בתקופת כהונתה של גולדה מאיר כראש ממשלה?",
                "answers": ["מלחמת יום הכיפורים", "מלחמת ששת הימים", "מלחמת לבנון הראשונה", "מלחמת העצמאות"],
                "correct": "מלחמת יום הכיפורים"
            },
            {
                "question": "גולדה מאיר הייתה האישה הראשונה שכיהנה כ...",
                "answers": ["ראש ממשלת ישראל", "יושבת ראש הכנסת", "נשיאת המדינה", "שגרירה באו\"ם"],
                "correct": "ראש ממשלת ישראל"
            }],
        "Herzel": [
            {
                "question": "מה היה שמו המלא של בנימין זאב הרצל?",
                "answers": ["תאודור בנימין זאב הרצל", "הרמן זאב הרצל", "מרדכי זאב הרצל", "יוסף בנימין הרצל"],
                "correct": "תאודור בנימין זאב הרצל"
            },
            {
                "question": "באיזו מדינה נולד הרצל?",
                "answers": ["אוסטריה", "הונגריה", "גרמניה", "שווייץ"],
                "correct": "הונגריה"
            },
            {
                "question": "מהו שם ספרו המפורסם של הרצל?",
                "answers": ["מדינת היהודים", "העם היהודי", "שיבת ציון", "תקוותינו"],
                "correct": "מדינת היהודים"
            },
            {
                "question": "היכן נערך הקונגרס הציוני הראשון שיזם הרצל?",
                "answers": ["באזל", "וינה", "ירושלים", "ברלין"],
                "correct": "באזל"
            },
            {
                "question": "באיזו שנה נפטר הרצל?",
                "answers": ["1904", "1917", "1898", "1920"],
                "correct": "1904"
            }]}

    # Page config
    st.set_page_config(
        page_title="Quiz | Askie",
        page_icon="./assets/brand/logo.png",
        layout="centered"
    )


    questions = all_questions[st.session_state.character]


    st.title(f"Quiz time! 🎉 ({st.session_state.character})")

    # Store selected answers
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(questions)
        st.session_state.attempted = [False] * len(questions)
        st.session_state.first_try_correct = [False] * len(questions)


    for i, q in enumerate(questions):
        st.subheader(f"{i+1}: {q['question']}")

        cols = st.columns(len(q['answers']))
        for idx, ans in enumerate(q['answers']):
            key = f"q{i}_a_{ans}"
            if cols[idx].button(ans, key=key):
                if not st.session_state.attempted[i]:
                    st.session_state.responses[i] = ans
                    st.session_state.attempted[i] = True
                    if ans == q['correct']:
                        st.session_state.first_try_correct[i] = True

        # Show if the answer was correct
        if st.session_state.responses[i] is not None:
            if st.session_state.responses[i] == q['correct']:
                st.success("✅ כל הכבוד!")
            else:
                st.error(f"❌ טעות. התשובה הנכונה היא: {q['correct']}")




    st.write("<br>"*3, unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        if st.button('Back to Chat', use_container_width=True):
            st.switch_page("./pages/chat.py")
    with c2:
        if st.button('Back to Gallery', use_container_width=True):
            me = st.session_state.student_id
            st.session_state.clear()
            st.session_state.student_id = me
            st.switch_page("./pages/student.py")


    # Calculate success rate on first tries
    correct_first_tries = sum(st.session_state.first_try_correct)
    total_questions = len(questions)
    if total_questions > 0:
        percentage = round((correct_first_tries / total_questions) * 100)
        st.markdown(f"### הצלחה בניסיון ראשון: {correct_first_tries} מתוך {total_questions} ({percentage}%) 🎯")




    def get_user_id():
        """Get or create a user ID for this session"""
        if "student_id" not in st.session_state:
            st.session_state.student_id = 0
        return st.session_state.student_id


    def insert_quiz_result(student_id, character_id, score):
        supabase.table("quizzes").insert({
            "student_id": student_id,
            "character_id": character_id,
            "score": score
        }).execute()



    user_id = get_user_id()
    name2id = {
        "David Ben-Gurion": 0,
        "Golda Meir": 1,
        "Herzel": 2
    }
    char_id = name2id[st.session_state.character]


    attempted_all = True
    for i, q in enumerate(questions):
        if not st.session_state.attempted[i]:
            attempted_all = False
            break

    try:
        if attempted_all: insert_quiz_result(user_id, char_id, percentage)
    except: pass