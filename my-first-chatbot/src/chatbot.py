from .llm import call_llm
from .memory import get_memory, add_user_message, add_bot_message

def chat(user_input):
    add_user_message(user_input)

    messages = get_memory()
    response = call_llm(messages)

    add_bot_message(response)

    return response