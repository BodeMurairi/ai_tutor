import requests

BASE_URL = "http://localhost:5000"


def ask_chat(message: str, token: str, session_id: str = None):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id

    response = requests.post(url=f"{BASE_URL}/chat/", json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data.get("response", ""))
    return data

def register_user():
    payload = {
        "first_name": "Bode",
        "last_name": "Murairi",
        "username": "bodemurairi3",
        "email_address": "bodemurairi@gmail.com"
        }
    response = requests.post(url=f"{BASE_URL}/auth/register", json=payload)
    response.raise_for_status()
    data = response.json()
    print(data)
    return data


def login_user(username: str, api_key: str):
    payload = {
        "username": username,
        "api_key": api_key
        }
    response = requests.post(url=f"{BASE_URL}/auth/login", json=payload)
    response.raise_for_status()
    data = response.json()
    print(data)
    return data


if __name__ == "__main__":
    username = "bodemurairi3"
    api_key = "pkey-7d0face9-be87-4b28-abf5-1c606340f39f"
    login_data = login_user(username=username, api_key=api_key)
    token = login_data["jwt"]
    is_running = True
    while is_running:
        message = input("Ask your question!\n")
        ask_chat(message=message, token=token)
