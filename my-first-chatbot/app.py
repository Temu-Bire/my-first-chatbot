# app.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # Add current directory to path
import streamlit as st
from src.chatbot import chat
from src.memory import init_memory, clear_memory, get_memory
from src.prompt_lab import run_multiple

st.set_page_config(page_title="AI App", layout="wide")

st.title("🤖 AI Chatbot + Prompt Playground")

# Initialize memory
init_memory()

# Sidebar
mode = st.sidebar.selectbox("Select Mode", ["Chatbot", "Prompt Playground"])

if mode == "Chatbot":
    st.subheader("💬 Chatbot")

    user_input = st.text_input("Type your message")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Send"):
            if user_input:
                response = chat(user_input)

    with col2:
        if st.button("Clear Chat"):
            clear_memory()

    # Display chat
    messages = get_memory()

    for msg in messages[1:]:  # skip system message
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {msg['content']}")

elif mode == "Prompt Playground":
    st.subheader("🧪 Prompt Engineering Playground")

    input_text = st.text_area("Input Text")

    col1, col2, col3 = st.columns(3)

    with col1:
        prompt1 = st.text_area("Prompt 1")
    with col2:
        prompt2 = st.text_area("Prompt 2")
    with col3:
        prompt3 = st.text_area("Prompt 3")

    if st.button("Run Prompts"):
        outputs = run_multiple([prompt1, prompt2, prompt3], input_text)

        st.write("### Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Output 1")
            st.write(outputs[0])

        with col2:
            st.write("Output 2")
            st.write(outputs[1])

        with col3:
            st.write("Output 3")
            st.write(outputs[2])