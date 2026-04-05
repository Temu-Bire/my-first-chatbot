from typing import cast

import streamlit as st
from groq import Groq

# ----------------- CONFIG -----------------
st.set_page_config(page_title="My Amharic Chatbot", page_icon="🇪🇹")
st.title("🤖 My First LLM Chatbot")
st.caption("Powered by Llama 3 on Groq • Made by you!")

# Get API key from secrets or input (for safety)
if "groq_key" not in st.session_state:
    key= st.text_input("Paste your Groq API key here:", type="password")
    if key:
        st.session_state.groq_key = key
        st.success("Key saved!")
        st.rerun()

client = Groq(api_key=st.session_state.groq_key)

# ----------------- MEMORY -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------- LANGUAGE CHALLENGE -----------------
language_mode = st.sidebar.radio(
    "Chat in:",
    ["English + Amharic", "Only Amharic"]
)

system_prompt = "You are a helpful assistant."
if language_mode == "Only Amharic":
    system_prompt = "You are a helpful assistant. ALWAYS answer ONLY in Amharic (አማርኛ). Never use English unless the user asks."
else:
    system_prompt = "You are a helpful assistant. Answer in Amharic or English+Amharic. Use Amharic script (አማርኛ) as much as possible."

# ----------------- CHAT INPUT -----------------
if prompt := st.chat_input("እንዴት ነህ? Ask me anything..."):
    
    # Add user message to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare messages for the API (with system prompt + memory)
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Call Groq API
    with st.chat_message("assistant"):
        with st.spinner("እያሰብኩ ነው... Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",   # very good model in 2026
                messages=cast(list, api_messages),
                temperature=0.7,
                max_tokens=1024
            )
            answer = response.choices[0].message.content
            
            st.markdown(answer)
    
    # Add assistant answer to memory
    st.session_state.messages.append({"role": "assistant", "content": answer})