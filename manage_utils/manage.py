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

    # Module to add members both coach and gym members

    def add_member(self, authority, name, username, password, email, active_status):
        if (authority == "coach"):
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    coaches = json.load(f)
                    
            except FileNotFoundError:
                print(f"File does not exist: {file_path}")
                return False  
            else:
                if any(coach.get("username") == username for coach in coaches):
                    raise ValueError(f"Username '{username}' already exists!")
                coach = {
                        'name' : name,
                        'authority' : authority, 
                        'username' : username, 
                        'password' : password, 
                        'email' : email, 
                        'active_status' : active_status
                        }
                coaches.append(coach)
            try: 
                with open("users.json", "w", encoding="utf-8") as f:
                    json.dump(coaches, f, indent=4)
            except FileNotFoundError:
                print(f"File does not exist: {file_path}")
                return False

        elif (authority == "gym_user"):
            try:
                with open("users.json", "r") as f:
                    coaches = json.load(f)
            except FileNotFoundError:
                print(f"File does not exist: {file_path}")
                return False  
            else:
                if any(coach.get("username") == username for coach in coaches):
                    raise ValueError(f"Username '{username}' already exists!")
                coach = {
                    'authority' : authority,
                    'name' : name, 
                    'username' : username, 
                    'password' : password, 
                    'email' : email, 
                    'active_status' : active_status
                    }
                coaches.append(coach)
                try: 
                    with open("users.json", "w") as f:
                        json.dump(coaches, f, indent=4)
                except FileNotFoundError:
                    print(f"File does not exist: {file_path}")
                    return False
        else:
            print("Invalid authority! ")
            return False

    # Module to edit user info including "name" - "email" - "password" - "active_status"

    def edit_member_info(self, section, amount, username):

        match section:

            case "name":

                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    print(f"File does not exist: {file_path}")
                    return False  
                else:
                    for user in users:
                        if(user['username'] == username):
                            user['name'] = amount
                            break
                        else:
                            print("Username not found.")
                            return False
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except FileNotFoundError:
                        print(f"File does not exist: {file_path}")
                        return False
                return True
            
            case "password":

                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    print(f"File does not exist: {file_path}")
                    return False  
                else:
                    for user in users:
                        if(user['username'] == username):
                            user['password'] = amount
                            break
                        else:
                            print("Username not found.")
                            return False
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except FileNotFoundError:
                        print(f"File does not exist: {file_path}")
                        return False
                return True    

            case "email":
                
                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    print(f"File does not exist: {file_path}")
                    return False  
                else:
                    for user in users:
                        if(user['username'] == username):
                            user["email"] = amount
                            break
                        else:
                            print("Username not found.")
                            return False
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except FileNotFoundError:
                        print(f"File does not exist: {file_path}")
                        return False
                return True      

            case "active_status":

                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    print(f"File does not exist: {file_path}")
                    return False  
                else:
                    for user in users:
                        if(user['username'] == username):
                            user["active_status"] = amount
                            break
                        else:
                            print("Username not found.")
                            return False
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except FileNotFoundError:
                        print(f"File does not exist: {file_path}")
                        return False
                return True
            