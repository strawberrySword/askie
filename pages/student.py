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

def create_gallery():
    # Sample gallery data - replace with your actual data
    gallery_items = [
        {
            "image_url": "https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Character+1",
            "character": "Wizard Merlin",
            "description": "Ancient wizard with mystical powers"
        },
        {
            "image_url": "https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text=Character+2", 
            "character": "Knight Arthur",
            "description": "Noble knight of the round table"
        },
        {
            "image_url": "https://via.placeholder.com/300x200/45B7D1/FFFFFF?text=Character+3",
            "character": "Rogue Shadow",
            "description": "Stealthy assassin from the shadows"
        },
        {
            "image_url": "https://via.placeholder.com/300x200/96CEB4/FFFFFF?text=Character+4",
            "character": "Elf Archer",
            "description": "Swift archer with keen eyes"
        },
        {
            "image_url": "https://via.placeholder.com/300x200/FFEAA7/000000?text=Character+5",
            "character": "Dragon Slayer",
            "description": "Fearless warrior who hunts dragons"
        },
        {
            "image_url": "https://via.placeholder.com/300x200/DDA0DD/000000?text=Character+6",
            "character": "Mystic Oracle",
            "description": "Seer who knows the future"
        }
    ]
    
    st.title("Character Gallery")
    st.write("Hover over characters to see descriptions, click to chat!")
    
    # Create columns for gallery layout
    cols = st.columns(3)  # Adjust number of columns as needed
    
    for idx, item in enumerate(gallery_items):
        col = cols[idx % 3]  # Cycle through columns
        
        with col:
            # Display clickable image with custom HTML for hover effect
            html_content = f"""
            <div class="gallery-item" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{item['character']}'}}, '*')">
                <img src="{item['image_url']}" alt="{item['character']}" class="gallery-image">
                <div class="gallery-overlay">
                    <p class="gallery-text">{item['character']}</p>
                    <p style="font-size: 12px; margin: 5px 0 0 0;">{item['description']}</p>
                </div>
            </div>
            """
            
            # Create the HTML component with click handling
            clicked_character = html(html_content, height=220, key=f"gallery_{idx}")
            
            # Check if this item was clicked
            if clicked_character == item['character']:
                st.session_state.character = item['character']
                st.switch_page("chat.py")

# Alternative implementation using pure Streamlit (if the above doesn't work)
def create_simple_gallery():
    
    characters = [
        {"name": "Wizard Merlin", "image": "bob.png"},
        {"name": "Knight Arthur", "image": "krabs.png"},
        {"name": "Rogue Shadow", "image": "pat.png"},
        {"name": "Elf Archer", "image": "squid.jpg"},
    ]
    
    cols = st.columns(2)
    
    for idx, char in enumerate(characters):
        col = cols[idx % 2]
        
        with col:
            # Make the image itself clickable using image click detection
            clicked = st.image("./assets/cards/"+char["image"], caption=char["name"], use_container_width=True)
            
            # Create an invisible button overlay for click detection
            if st.button(f"🎭", key=f"chat_{idx}", help=f"Chat with {char['name']}"):
                st.session_state.character = char["name"]
                st.switch_page("./pages/chat.py")

if __name__ == "__main__":
    # Use the fancy gallery if possible, fallback to simple version
    try:
        create_gallery()
    except:
        create_simple_gallery()

