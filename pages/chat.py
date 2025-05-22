# chat.py
import streamlit as st

# Set page config
st.set_page_config(page_title="Character Chat", layout="wide")

def main():
    st.title("Character Chat")
    
    # Get the selected character from session state
    if "character" in st.session_state:
        selected_character = st.session_state.character
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
                "Wizard Merlin": f"*adjusts pointed hat* Ah, young one, you seek wisdom? {prompt} is indeed a curious matter...",
                "Knight Arthur": f"*raises sword honorably* By the code of chivalry, I say {prompt} requires courage and honor!",
                "Rogue Shadow": f"*whispers from the shadows* {prompt}? Interesting... few know of such things...",
                "Elf Archer": f"*notches arrow gracefully* The forest spirits tell me that {prompt} is worth considering...",
                "Dragon Slayer": f"*hefts mighty weapon* {prompt}? Ha! I've faced fiercer challenges than that!",
                "Mystic Oracle": f"*gazes into crystal ball* The future reveals that {prompt} will lead to great changes..."
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