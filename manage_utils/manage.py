import json
from pathlib import Path
import re

file_path = Path(__file__).resolve().parent / "users.json"
file_path_hall = Path(__file__).resolve().parent / "halls.json"
file_path_classes = Path(__file__).resolve().parent / "classes.json"

class Manage:

    def __init__(self):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.file= json.load(f)        
            except FileNotFoundError:
                    raise FileNotFoundError (f"File does not exist: {file_path}")
            try:
                with open(file_path_hall, "r", encoding="utf-8") as f:
                    self.halls = json.load(f)
            except FileNotFoundError:
                    raise FileNotFoundError(f"File not found in path: {file_path_hall}")
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
                if re.fullmatch(email,r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]+{2,})") and re.fullmatch(password,r"(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+"):
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
                else:
                    print("invalid email or password")
                    return False
        elif (authority == "gym_user"):
                if any(coach.get("username") == username for coach in self.file):
                    raise ValueError(f"Username '{username}' already exists!")
                if re.fullmatch(email,r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]+{2,})") and re.fullmatch(password,r"(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+") :
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
                    print("invalid email or password")
                    return False
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
                if re.fullmatch(section,r"(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+"):
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
                else:
                    print("invalid email")
                    return False
            case "email":
                if re.fullmatch(section,r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]+{2,})"): 
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
                else:
                    print("invalid email")
                    return False
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
            hall = {
                "name" : name,
                "capacity" : capacity,
                "tools" : tools,
                "hall_status" : hall_status
            }
            self.halls.append(hall) 
            with open(file_path_hall, "w") as f:
                json.dump(self.halls, f, indent=4)
    # Edit hall information by taking name of the hall as a key

    def edit_hall_info(self, name, choice, new_amount):
        match choice:
            case "name":
                    found=False
                    for hall in self.halls:
                        if hall["name"] == name:
                            hall["name"] = new_amount
                            found=True
                            break
                    if not found:
                            print("hall didn't found!")
                            return False
                    with open(file_path_hall, "w") as f:    
                        json.dump(self.halls, f, indent=4)
                    return True

            case "capacity":
                    found=False
                    for hall in self.halls:
                        if hall["name"] == name:
                            hall["capacity"] = new_amount
                            found=True
                            break
                    if not found:
                          print("hall didn't found!")
                          return False
                    with open(file_path_hall, "w") as f:    
                        json.dump(self.halls, f, indent=4)
                    return True

            case "tools":
                found=False
                if isinstance(new_amount, str):
                    tools = [tool.strip() for tool in new_amount.split(",")]   
                for hall in self.halls:
                        if hall["name"] == name:
                            hall["tools"] = tools
                            found=True
                            break
                if not found:
                    print("hall didn't found!")
                    return False
                with open(file_path_hall, "w") as f:    
                    json.dump(self.halls, f, indent=4)
                return True

            case "hall_status":
                found=False
                for hall in self.halls:
                    if hall["name"] == name:
                        hall["hall_status"] = new_amount
                        found=True
                        break
                if not found:
                    print("Name of the hall not found!")
                    return False
                with open(file_path_hall, "w") as f:
                    json.dump(self.halls, f, indent=4)
                return True

    # Show halls general info

    def show_hall_info(self):
            for hall in self.halls:
                for key, value in hall.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Classes Section
    # Add classes

    def add_class(self, name, class_type, coach_user, hall, date, time, capacity):
        class_types = ["gym", "crossfit", "fitness", "yoga"]
        if class_type in class_types:
            pass
        else:
            print("Mentioned class type is not valid! ")
            return False
    
        try:
            with open("classes.json", "r") as f:
                classes = json.load(f)
        except FileNotFoundError:
            print(f"File not found in path {file_path_classes}")
        else:
            h = open("halls.json", "r")
            c = open("users.json", "r")
            halls = json.load(h)
            coaches = json.load(c)

            hall_key = 0
            coach_key = 0

            for hal in halls:
                for key, value in hal.items():
                    if hal[key] == hall:
                        if hal["hall_status"] == True:
                            hall_key = 1
                for coach in coaches:
                    for key, value in coach.items():
                        if coach[key] == coach_user:
                            if coach["active_status"] == True:
                                coach_key = 1

                if (coach_key == 1 and hall_key == 1):
                    clas = {
                        "title" : name,
                        "class_type" : class_type,
                        "coach" : coach_user,
                        "sport_hall" : hall,
                        "class_date" : date,
                        "class_time" : time,
                        "capacity" : capacity
                    }
                    classes.append(clas)
                else:
                    if coach_key != 1:
                        print("Coach status is not active! ")
                        return False
                    else:
                        print("Hall status in not active!")
                        return False

        finally:
            with open("classes.json", "w") as f:
                json.dump(classes, f, indent=4)
            h.close()
            c.close()

