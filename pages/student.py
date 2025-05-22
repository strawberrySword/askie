# student.py
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config( 
    page_title="Characters | Askie",
    page_icon="./assets/brand/logo.png",
    layout="centered"
)


# Custom CSS for gallery styling
st.markdown("""
<style>
.gallery-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
}

.gallery-item {
    position: relative;
    cursor: pointer;
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.gallery-item:hover {
    transform: scale(1.05);
}

.gallery-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}

.gallery-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    color: white;
    padding: 15px;
    transform: translateY(100%);
    transition: transform 0.3s ease;
}

.gallery-item:hover .gallery-overlay {
    transform: translateY(0);
}

.gallery-text {
    font-size: 16px;
    font-weight: bold;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)


# Alternative implementation using pure Streamlit (if the above doesn't work)
def create_simple_gallery():
    
    characters = [
        {"name": "Golda Meir", "image": "bob.png"},
        {"name": "David Ben-Gurion", "image": "krabs.png"},
        {"name": "Herzel", "image": "pat.png"},
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

