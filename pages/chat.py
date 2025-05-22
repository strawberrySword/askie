import streamlit as st
import time

# Set page config
st.set_page_config( 
    page_title="Character Chat | Askie",
    page_icon="./assets/brand/logo.png",
    layout="wide"
)


def simulate_typing(text, container):
    """Simulate typing effect by revealing text character by character"""
    displayed_text = ""
    placeholder = container.empty()
    
    # Add some initial delay
    time.sleep(0.1)
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text + "▋")  # Add cursor
        
        # Variable speed typing - faster for spaces, slower for punctuation
        if char == ' ':
            time.sleep(0.01)  # Fast for spaces
        elif char in '.,!?;:':
            time.sleep(0.2)   # Pause at punctuation
        else:
            time.sleep(0.03)  # Normal speed for letters
    
    # Remove cursor and show final text
    placeholder.markdown(displayed_text)

def main():

    # Get the selected character from session state
    if "character" in st.session_state:
        selected_character = st.session_state.character

        with st.sidebar:
            imgname = selected_character.lower().split(' ')[0]
            st.image(f"./assets/cards/{imgname}.png", use_container_width=True)
            st.success(f"Now chatting with: **{selected_character}**")
            
            # Add a back button
            if st.button("← Back to Gallery"):
                st.switch_page("./pages/student.py")
            
        # Chat interface
        st.subheader(f"Conversation with {selected_character}")
        
        # Initialize chat history if it doesn't exist
        if f"messages_{selected_character}" not in st.session_state:
            st.session_state[f"messages_{selected_character}"] = []
        
        # Display chat messages
        for message in st.session_state[f"messages_{selected_character}"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input(f"Say something to {selected_character}..."):
            # Add user message to chat history
            st.session_state[f"messages_{selected_character}"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            character_responses = {
                "Golda Meir" : f'תשובה של גולדה מאיר',
                "David Ben-Gurion": f"תשובה של דוד בן גוריון",
                "Herzel" : f'תשובה של הרצל',
            }
            
            response = character_responses.get(selected_character, f"{selected_character} says: That's an interesting point about {prompt}!")
            
            # Show typing effect
            with st.chat_message("assistant"):
                typing_container = st.empty()
                
                # Show typing indicator first
                typing_container.markdown("*typing...*")
                time.sleep(1)  # Brief pause before typing starts
                
                # Simulate typing
                simulate_typing(response, typing_container)
            
            # Add character response to chat history AFTER typing is complete
            st.session_state[f"messages_{selected_character}"].append({"role": "assistant", "content": response})
            
            # Rerun to update the chat display
            st.rerun()
    
    else:
        st.warning("No character selected. Please go back to the gallery and select a character.")
        if st.button("Go to Gallery"):
            st.switch_page("student.py")

if __name__ == "__main__":
    main()