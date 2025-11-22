import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ai(prompt: str, model: str = "mistral:latest"):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code != 200:
        return f"Error: {response.text}"
    
    return response.json().get("response", "")
