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

def register_user():
    payload = {
        "first_name": "Bode",
        "last_name": "Murairi",
        "username": "bodemurairi",
        "email_address": "b.murairi@alustudent.com"
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
    login_user(username="bodemurairi", api_key="pkey-860f44bf-cae2-4202-b5be-3de1c2338ba9")
