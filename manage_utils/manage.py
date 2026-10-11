import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"
file_path_hall = Path(__file__).resolve().parent / "halls.json"

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
                try:
                    with open("halls.json", "r") as f:
                        halls = json.load(f)
                except FileNotFoundError:
                    print(f"File not found in path {file_path_hall}")
                    return False
                else:
                    for hall in halls:
                        if hall["name"] == name:
                            hall["name"] = new_amount
                            break
                        else:
                            pass
                    with open("halls.json", "w") as f:    
                        json.dump(halls, f, indent=4)

            case "capacity":

                try:
                    with open("halls.json", "r") as f:
                        halls = json.load(f)
                except FileNotFoundError:
                    print(f"File not found in path {file_path_hall}")
                    return False
                else:
                    for hall in halls:
                        if hall["name"] == name:
                            hall["capacity"] = new_amount
                            break
                        else:
                            pass
                    with open("halls.json", "w") as f:    
                        json.dump(halls, f, indent=4)

            case "tools":

                if isinstance(new_amount, str):
                    tools = [tool.strip() for tool in new_amount.split(",")]   
                try:
                    with open("halls.json", "r") as f:
                        halls = json.load(f)
                except FileNotFoundError:
                    print(f"File not found in path {file_path_hall}")
                    return False
                else:
                    for hall in halls:
                        if hall["name"] == name:
                            hall["tools"] = tools
                            break
                        else:
                            pass
                    with open("halls.json", "w") as f:    
                        json.dump(halls, f, indent=4)

            case "hall_status":

                try:
                    with open("halls.json", "r") as f:
                        halls = json.load(f)
                except FileNotFoundError:
                    print("File halls.json not found.")
                    return False
                for hall in halls:
                    if hall["name"] == name:
                        hall["hall_status"] = new_amount
                        break
                    else:
                        print("Name of the hall not found!")
                        return False
                with open("halls.json", "w") as f:
                    json.dump(halls, f, indent=4)
                return True

    # Show halls general info

    def show_hall_info(self):
        try:
            with open("halls.json", "r", encoding="utf-8") as f:
                halls = json.load(f)
        except FileNotFoundError:
            print(f"File not found in path: {file_path_hall}")
            return False
        else:
            for hall in halls:
                for key, value in hall.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")