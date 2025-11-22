# Simple in-memory chat history

chat_history = []

def add_message(role, content):
    message = {"role": role, "content": content}
    chat_history.append(message)
    return message

def get_history():
    return chat_history

def clear_history():
    chat_history.clear()
