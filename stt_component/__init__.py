import streamlit.components.v1 as components

def voice_input():
    component = components.declare_component("voice_input", path="./stt_component")
    result = component()
    if result and "transcript" in result:
        return result["transcript"]
    return None
