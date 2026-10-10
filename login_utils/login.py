import json
from pathlib import Path

def show_menu():
    print("1.Gym manager login.")
    print("2.Gym coach login.")
    print("3.Gym user login.")
    print("4.Exit menu.")

def login(username, password, authority, status = None):
    file_path = Path(__file__).resolve().parent / "login_info.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            users = json.load(f)

    except FileNotFoundError:
        print(f"File does not exist: {file_path}")
        return False

    except json.JSONDecodeError:
        print("The login file does not contain valid JSON.")
        return False
    
    for user in users:
        if (user["username"] == username and user["password"] == password and user["authority"] == authority):
            if user["authority"] == "manager":
                return True
            if user["status"] == "active":
                return True 
    return False