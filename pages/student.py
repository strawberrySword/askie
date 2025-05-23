# student.py
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config( 
    page_title="Characters | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)

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
    h3, .stRadio, .stTextInput label {
        font-size: 2.5rem !important;
        text-align: right;
        direction: rtl;
    }
    h1{
        font-size: 4rem !important;
        text-align: right;
        direction: rtl;        
    }
    .stButton > button {
    background-color: #A2D2FF !important;
    color: #333333 !important;
    font-weight: bold !important;
    font-size: 2rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    border: none !important;
    }
    .stButton>button:hover {
        background-color: #FF9E9E;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Alternative implementation using pure Streamlit (if the above doesn't work)
def create_simple_gallery():
    
    characters = [
    {"name": "Golda Meir", "display_name": "גולדה מאיר", "image": "golda.png"},
    {"name": "David Ben-Gurion", "display_name": "דוד בן-גוריון", "image": "david.png"},
    {"name": "Herzel", "display_name": "בנימין זאב הרצל", "image": "herzel.png"},
    ]
    
    cols = st.columns(3)
    
    for idx, char in enumerate(characters):
        col = cols[idx % 3]
        
        with col:
            # Make the image itself clickable using image click detection
            st.image("./assets/cards/"+char["image"], use_container_width=True)
            
            # Create an invisible button overlay for click detection
            if st.button(char["display_name"], key=f"chat_{idx}", help=f"להתחיל שיחה עם  {char['display_name']}", use_container_width=True):
                st.session_state.character = char["name"]
                st.switch_page("./pages/chat.py")




if __name__ == "__main__":
    # Use the fancy gallery if possible, fallback to simple version
    st.markdown("""
    <h1 style='text-align: right; direction: rtl; font-size: 2.5rem;'>גלריית דמויות</h1>
    <p style='text-align: right; direction: rtl; font-size: 1.3rem;'>תבחרו דמות ותתחילו לצ׳וטט</p>
    """, unsafe_allow_html=True)
    create_simple_gallery()