import streamlit as st
from stt_component import voice_input

st.set_page_config(page_title="Askie - Voice Input", layout="centered")
st.title("🎙️ Speak Hebrew with Askie")

st.markdown("Click the mic and speak in Hebrew:")

transcript = voice_input()

if transcript:
    st.success("📝 Transcription:")
    st.markdown(f"**{transcript}**")
