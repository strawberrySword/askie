import streamlit as st
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from module.charachtars import ConversationSession

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Character Chat | Askie",
    page_icon="./assets/brand/logo.png",
    layout="wide"
)

# Define state for application with conversation history

@st.cache_resource
def get_conversation_session(character_name):
    """Cache the conversation session for each character"""
    return ConversationSession(character_name)


def get_user_id():
    """Get or create a user ID for this session"""
    if "user_id" not in st.session_state:
        # In a real app, you'd have proper authentication
        # For now, we'll use a simple session-based ID
        import uuid
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id

def load_conversation_from_db(supabase: Client, user_id: str, character_name: str):
    """Load existing conversation from database"""
    if character_name.equals("David Ben-Gurion"):
        char_id = 0
    elif character_name.equals("Golda Meir"):
        char_id = 1
    elif character_name.equals("Herzel"):
        char_id = 2

    user_id = int(user_id)

    try:
        response = supabase.table("chats").select("*").eq("student_id", user_id).eq("character_id", char_id).execute()
        
        if response.data:
            # Get the conversation ID
            conversation_id = response.data[0]["id"]
            
            # Load messages for this conversation
            messages_response = supabase.table("messages").select("*").eq("chat_id", conversation_id).order("created_at").execute()
            
            messages = []
            for msg in messages_response.data:
                messages.append({
                    "role": msg["sender_role"],
                    "content": msg["content"],
                    "timestamp": msg["created_at"]
                })
            
            return conversation_id, messages
        else:
            # Create new conversation
            new_conversation = supabase.table("chats").insert({
                "student_id": user_id,
                "character_id": char_id,
                "created_at": datetime.now().isoformat()
            }).execute()
            
            return new_conversation.data[0]["id"], []
            
    except Exception as e:
        st.error(f"Error loading conversation: {e}")
        return None, []

def save_message_to_db(supabase: Client, conversation_id: str, role: str, content: str):
    """Save a message to the database"""
    try:
        supabase.table("messages").insert({
            "chat_id": int(conversation_id),
            "sender_role": role,
            "content": content,
            "created_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error saving message: {e}")
        return False
    

def simulate_typing(text, container, img_placeholder, name):
    """Simulate typing effect by revealing text character by character"""
    displayed_text = ""
    placeholder = container.empty()

    # Add some initial delay
    time.sleep(0.1)

    i = 0
    lastimg = 0

    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text + "▋")  # Add cursor

        if i % 5 == 0:
            imgname = name if lastimg != 0 else name+"2"
            img_placeholder.image(f"./assets/cards/{imgname}.png", use_container_width=True)
            lastimg = 1-lastimg

        # Variable speed typing - faster for spaces, slower for punctuation
        if char == ' ':
            time.sleep(0.01)  # Fast for spaces
        elif char in '.,!?;:':
            time.sleep(0.2)   # Pause at punctuation
        else:
            time.sleep(0.03)  # Normal speed for letters

        i += 1
    # Remove cursor and show final text
    placeholder.markdown(displayed_text)


def main():
    # Get keys from env
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    user_id = get_user_id()
    # Get the selected character from session state
    if "character" in st.session_state:
        selected_character = st.session_state.character

        with st.sidebar:
            imgname = selected_character.lower().split(' ')[0]
            img_placeholder = st.empty()
            img_placeholder.image(f"./assets/cards/{imgname}.png", use_container_width=True)

            st.success(f"Now chatting with: **{selected_character}**")

            # Add a back button
            if st.button("← Back to Gallery"):
                st.switch_page("./pages/student.py")

            # Add a quiz button
            if st.button("To quiz →"):
                st.switch_page("./pages/quiz.py")

        # Initialize conversation session for this character
        if f"session_{selected_character}" not in st.session_state:
            try:
                st.session_state[f"session_{selected_character}"] = get_conversation_session(
                    selected_character)
            except Exception as e:
                st.error(f"Error initializing character: {e}")
                return

        session = st.session_state[f"session_{selected_character}"]

        if f"conversation_id_{selected_character}" not in st.session_state:
            conversation_id, messages = load_conversation_from_db(supabase, user_id, selected_character)
            st.session_state[f"conversation_id_{selected_character}"] = conversation_id
            st.session_state[f"messages_{selected_character}"] = messages

        conversation_id = st.session_state[f"conversation_id_{selected_character}"]

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
            user_message = {"role": "user", "content": prompt}
            st.session_state[f"messages_{selected_character}"].append(user_message)

            save_message_to_db(supabase, conversation_id, "user", prompt)

            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # Get response from the character's RAG system
                response = session.ask(prompt)

                # Show typing effect
                with st.chat_message("assistant"):
                    typing_container = st.empty()

                    # Show typing indicator first
                    typing_container.markdown("*typing...*")
                    time.sleep(1)  # Brief pause before typing starts

                    # Simulate typing
                    simulate_typing(response, typing_container, img_placeholder, imgname)

                # Add character response to chat history AFTER typing is complete
                assistant_message = {"role": "assistant", "content": response}
                st.session_state[f"messages_{selected_character}"].append(assistant_message)

                # Save assistant message to database
                save_message_to_db(supabase, conversation_id, "assistant", response)

            except Exception as e:
                st.error(f"Error getting response: {e}")
                # Fallback response
                fallback_response = f"I'm sorry, I'm having trouble responding right now. Please try again."
                assistant_message = {"role": "assistant", "content": fallback_response}
                st.session_state[f"messages_{selected_character}"].append(assistant_message)

                # Save fallback message to database
                save_message_to_db(supabase, conversation_id, "assistant", fallback_response)

            # Rerun to update the chat display
            st.rerun()

    else:
        st.warning(
            "No character selected. Please go back to the gallery and select a character.")
        if st.button("Go to Gallery"):
            st.switch_page("student.py")


if __name__ == "__main__":
    main()
