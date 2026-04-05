import streamlit as st
from groq import Groq
from typing import Any, List, Dict, cast

# ----------------- CONFIG -----------------
st.set_page_config(page_title="My Amharic Chatbot", page_icon="🇪🇹")
st.title("🤖 My First LLM Chatbot")
st.caption("Powered by Llama 3 on Groq • Made by you!")

# ----------------- CONFIG -----------------
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_HISTORY = 10

# ----------------- API KEY -----------------
if "groq_key" not in st.session_state:
    key = st.text_input("Paste your Groq API key:", type="password")
    if key:
        st.session_state.groq_key = key
        st.success("Key saved!")
        st.rerun()
    st.stop()

# Initialize client
client = Groq(api_key=st.session_state.groq_key)

# ----------------- MEMORY -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- SIDEBAR -----------------
language_mode = st.sidebar.radio(
    "Chat in:",
    ["English + Amharic", "Only Amharic"]
)

# ----------------- SYSTEM PROMPT -----------------
def get_system_prompt(mode: str) -> str:
    if mode == "Only Amharic":
        return "Respond only in Amharic. Be clear and helpful."
    return "Respond in both English and Amharic clearly."

system_prompt = get_system_prompt(language_mode)

# ----------------- DISPLAY CHAT -----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------- CHAT INPUT -----------------
if prompt := st.chat_input("እንዴት ነህ? Ask me anything..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Limit memory (important for performance)
    st.session_state.messages = st.session_state.messages[-MAX_HISTORY:]

    # Prepare API messages
    api_messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    # ----------------- AI RESPONSE -----------------
    with st.chat_message("assistant"):
        with st.spinner("እያሰብኩ ነው... Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=cast(Any, api_messages),
                    temperature=0.7,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )