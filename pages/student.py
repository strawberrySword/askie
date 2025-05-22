# student.py
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config( 
    page_title="Characters | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)


# Alternative implementation using pure Streamlit (if the above doesn't work)
def create_simple_gallery():
    
    characters = [
        {"name": "Golda Meir", "image": "golda.png"},
        {"name": "David Ben-Gurion", "image": "david.png"},
        {"name": "Herzel", "image": "herzel.png"},
    ]
    
    cols = st.columns(3)
    
    for idx, char in enumerate(characters):
        col = cols[idx % 3]
        
        with col:
            # Make the image itself clickable using image click detection
            st.image("./assets/cards/"+char["image"], use_container_width=True)
            
            # Create an invisible button overlay for click detection
            if st.button(char["name"], key=f"chat_{idx}", help=f"Chat with {char['name']}", use_container_width=True):
                st.session_state.character = char["name"]
                st.switch_page("./pages/chat.py")




if __name__ == "__main__":
    # Use the fancy gallery if possible, fallback to simple version
    st.title("Character Gallery")
    st.write("Hover over characters to see descriptions, click to chat!")
    create_simple_gallery()