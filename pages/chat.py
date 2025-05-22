# chat.py
import streamlit as st

# Set page config
st.set_page_config(page_title="Character Chat", layout="wide")

def main():
    st.title("Character Chat")
    
    # Get the selected character from session state
    if "character" in st.session_state:
        selected_character = st.session_state.character

        with st.sidebar:
            imgname = selected_character.lower().split(' ')[0]
            st.image(f"./assets/cards/{imgname}.png", use_container_width=True)
            st.write(f"**{selected_character}**")


        st.success(f"Now chatting with: **{selected_character}**")
        
        # Add a back button
        if st.button("← Back to Gallery"):
            st.switch_page("./pages/student.py")
        
        st.divider()
        
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
            
            # Generate character response (you can customize this based on the character)
            character_responses = {
                "Golda Meir" : f'lmfao *smokes a cigar* "You know, {prompt} reminds me of the time I had to make a tough decision..."',
                "David Ben-Gurion": f"*leans back in chair* Ah, {prompt}... Sde boker is shit af man...",
                "Herzel" : f'Yo balcony vibes, {prompt}...',
            }
            
            response = character_responses.get(selected_character, f"{selected_character} says: That's an interesting point about {prompt}!")
            
            # Add character response to chat history
            st.session_state[f"messages_{selected_character}"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
    
    else:
        st.warning("No character selected. Please go back to the gallery and select a character.")
        if st.button("Go to Gallery"):
            st.switch_page("student.py")

if __name__ == "__main__":
    main()