import json
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register_user(username, password, role):
    users = load_users()
    users[username] = {"password": password, "role": role}
    save_users(users)

def login_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None