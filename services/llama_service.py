import requests

def get_llama_reply(message: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3",
        "prompt": message,
        "stream": False
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data["response"]
