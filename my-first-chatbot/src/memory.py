import streamlit as st

SYSTEM_PROMPT = {
    "role": "system",
    "content": "Always respond ONLY in Amharic or English mixed with Amharic."
}

def init_memory():
    if "messages" not in st.session_state:
        st.session_state.messages = [SYSTEM_PROMPT]

def get_memory():
    return st.session_state.messages

def add_user_message(text):
    st.session_state.messages.append({"role": "user", "content": text})

def add_bot_message(text):
    st.session_state.messages.append({"role": "assistant", "content": text})

def clear_memory():
    st.session_state.messages = [SYSTEM_PROMPT]