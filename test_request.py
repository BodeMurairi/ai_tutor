import requests

BASE_URL = "http://localhost:5000"


def ask_chat(message: str, session_id: str = None):
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id

    response = requests.post(url=f"{BASE_URL}/chat", json=payload)
    response.raise_for_status()
    data = response.json()
    print(data.get("response", ""))
    return data


if __name__ == "__main__":
    result = ask_chat("Hello! I want to learn about Python")
    session_id = result.get("session_id")

    # Follow-up using the same session
    ask_chat("What are Python data types?", session_id=session_id)
    ask_chat()