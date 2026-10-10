import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"

class Manage:

    def __init__(self):
        pass

    @staticmethod
    def show_panel():
        print("1. Users management")
        print("2. Saloons management")
        print("3. Class management")
        print("4. Subscriptions and payments management")
        print("5. Show logs")
        print("6. Exit")

    def add_member(self, authority, name, username, password, email, active_status):
        if (authority == "coach" or authority == "gym_member"):
            try:
                with open("users.txt", "a") as f:
                    users = json.load(f)
            except FileNotFoundError:
                print(f"File does not exist: {file_path}")
                return False  
            else:
                user = {
                        'name' : name, 
                        'username' : username, 
                        'password' : password, 
                        'email' : email, 
                        'active_status' : active_status
                        }
                json.dump(user, f)

        else:
            raise ValueError("Not valid authority!")