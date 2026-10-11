import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"
file_path_hall = Path(__file__).resolve().parent / "halls.json"

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
                    print(f"Username '{username}' already exists!")
                    return False
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

    # Module to show users information

    def show_user_info(self):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
                for user in users:
                    for key, value in user.items():
                        print(f"{key} : {value}")
        except FileNotFoundError:
            print(f"file does not exist in path {file_path}")
        else:
            for user in users:
                for key, value in user.items():
                    print(f"{key} : {value}")
                print("-------------------------------")

    # Add hall

    def add_hall(self, name, capacity, tools, hall_status):
        print("Enter tools in a sentence seperated by ','")
        if isinstance(tools, str):
            tools = [tool.strip() for tool in tools.split(",")]
        try:
            with open("halls.json", "r", encoding="utf-8") as f:
                halls = json.load(f)
        except FileNotFoundError:
            print(f"File not found in path: {file_path_hall}")
            return False
        else:
            hall = {
                "name" : name,
                "capacity" : capacity,
                "tools" : tools,
                "hall_status" : hall_status
            }
            halls.append(hall)
            try: 
                with open("halls.json", "w") as f:
                    json.dump(halls, f, indent=4)
            except FileNotFoundError:
                print(f"File not found in path: {file_path_hall}")
                return False

    # Edit hall information by taking name of the hall as a key

    def edit_hall_info(self, name, choice, new_amount):
        match choice:
            case "name":
                pass
            case "capacity":
                pass
            case "tools":
                pass
            case "hall_status":
                pass