import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"


class Manage:

    def __init__(self):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.file= json.load(f)        
            except FileNotFoundError:
                    raise FileNotFoundError (f"File does not exist: {file_path}")

    @staticmethod
    def show_panel():
        print("1. Users management")
        print("2. Saloons management")
        print("3. Class management")
        print("4. Subscriptions and payments management")
        print("5. Show logs")
        print("6. Exit")

    # Module to add members both coach and gym members

    def add_member(self, authority, name, username, password, email, active_status):
        if (authority == "coach"):
                if any(coach.get("username") == username for coach in self.file):
                    raise ValueError(f"Username '{username}' already exists!")
                coach = {
                        'name' : name,
                        'authority' : authority, 
                        'username' : username, 
                        'password' : password, 
                        'email' : email, 
                        'active_status' : active_status
                        }
                self.file.append(coach)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.file, f, indent=4)
                return True
        elif (authority == "gym_user"):
                if any(coach.get("username") == username for coach in self.file):
                    raise ValueError(f"Username '{username}' already exists!")
                coach = {
                    'authority' : authority,
                    'name' : name, 
                    'username' : username, 
                    'password' : password, 
                    'email' : email, 
                    'active_status' : active_status
                    }
                self.file.append(coach)
                with open(file_path, "w") as f:
                    json.dump(self.file, f, indent=4)
                return True
        else:
            print("Invalid authority! ")
            return False

    # Module to edit user info including "name" - "email" - "password" - "active_status"

    def edit_member_info(self, section, amount, username):

        match section:
            case "name":
                    found=False
                    for user in self.file:
                        if(user['username'] == username):
                            user['name'] = amount
                            found=True
                            break
                    if not found:
                            print("Username not found.")
                            return False
                    with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(self.file, f, indent=4)
                    return True
            case "password":
                    found=False    
                    for user in self.file:
                        if(user['username'] == username):
                            user['password'] = amount
                            found=True
                            break
                    if not found:
                            print("Username not found.")
                            return False
                    with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(self.file, f, indent=4)
                    return True
            case "email":
                    found=False  
                    for user in self.file:
                        if(user['username'] == username):
                            user["email"] = amount
                            found=True 
                            break
                    if not found:
                            print("Username not found.")
                            return False
                    with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(self.file, f, indent=4)
                    return True
            case "active_status":
                    found=False  
                    for user in self.file:
                        if(user['username'] == username):
                            user["active_status"] = amount
                            found=True 
                            break
                    if not found:
                            print("Username not found.")
                            return False
                    with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(self.file, f, indent=4)
                    return True
    # Module to show users information

    def show_user_info(self):
                for user in self.file:
                    for key, value in user.items():
                        print(f"{key} : {value}")
                    print("-------------------------------")

    