from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROK_API_KEY"))

def call_llm(messages, json_mode=False):
    params = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
    }

    if json_mode:
        params["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**params)
    return response.choices[0].message.content