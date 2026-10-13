import re
import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"
file_path_hall = Path(__file__).resolve().parent / "halls.json"
file_path_classes = Path(__file__).resolve().parent / "classes.json"
def checking_json_files(path):
        if not path.exists():
            with open(path,"w",encoding="utf-8") as f:
                json.dump([],f)
                return []
        else:
            try:
                with open(path,"r",encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"{path} contains invalid JSON!")
                return False
class Manage:
    def __init__(self):
            self.users=checking_json_files(file_path)
            self.halls=checking_json_files(file_path_hall)
            self.classes=checking_json_files(file_path_classes)  
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
                if any(coach.get("username") == username for coach in self.users):
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
                self.users.append(coach)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.users, f, indent=4)
                return True
        elif (authority == "gym_user"):
                if any(coach.get("username") == username for coach in self.users):
                    print(f"Username {username} already exists! ")
                    return False
                coach = {
                    'authority' : authority,
                    'name' : name, 
                    'username' : username, 
                    'password' : password, 
                    'email' : email, 
                    'active_status' : active_status

                    }
                self.users.append(coach)
                with open(file_path, "w") as f:
                        json.dump(self.users, f, indent=4)
                return True
        else:
            print("Invalid authority! ")
            return False

    # Module to edit user info including "name" - "email" - "password" - "active_status"

    def edit_member_info(self, section, amount, username):
        def checking_username():
            found=False
            for user in self.users:
                if(user['username'] == username):
                        user[section] = amount
                        found=True
                        break
            if not found:
                print(f"{username} did'nt found")
                return False
            with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.users, f, indent=4)
            return True 
        match section:
            case "name":
                return checking_username()
            case "password":
                if re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+",amount):
                    return checking_username()
                else:
                    print("password is invalid")
                    return False          
            case "email":
                if re.fullmatch(r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]{2,})+",amount):
                    return checking_username()
                else:
                    print("email is invalid")
                    return False    
            case "active_status":
                if amount==True or amount==False:
                    return checking_username()
                else:
                    print("invalid active_status")
            case _:
                print("Invalid selection! ")
                return False
    # Module to show users information

    def show_user_info(self):
            for user in self.users:
                for key, value in user.items():
                    print(f"{key} : {value}")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Add hall

    def add_hall(self, name, capacity, tools, hall_status):

        if isinstance(tools, str):
            tools = [tool.strip() for tool in tools.split(",")]
            hall = {
                    "name": name,
                "capacity": capacity,
                "tools": tools,
                "hall_status": hall_status
            }
            self.halls.append(hall)
            print("hall appended")
            with open(file_path_hall, "w", encoding="utf-8") as f:
                    json.dump(self.halls, f, indent=4)
                    print("hall dumped")
        else:
            print("enter tools in a sentence seperated by ',' ")
            return False
            
        return True
        
    # Edit hall information by taking name of the hall as a key

    def edit_hall_info(self, name, choice, new_amount):
        def checking_halls():
            found=False
            for hall in self.halls:
                if hall["name"] == name:
                    hall[choice] = new_amount
                    found=True
                    break
            if not found:
                print(f"{name} did'nt found")
                return False
            with open(file_path_hall, "w", encoding="utf-8") as f:    
                    json.dump(self.halls, f, indent=4)
            return True
        match choice:
            case "name":
                return checking_halls()
            case "capacity":
                return checking_halls()
            case "tools":
                if isinstance(new_amount, str):
                    new_amount = [tool.strip() for tool in new_amount.split(",")]   
                    return checking_halls()
                else:
                    print("enter tools in a sentence seperated by ',' ")
                    return False
            case "hall_status":
                return checking_halls()
            case _:
                print("invalid choice !")
                return False

    # Show halls general info

    def show_hall_info(self):
            for hall in self.halls:
                for key, value in hall.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Classes Section
    # Add classes

    def add_class(self, name, class_type, coach_user, hall, date, time, capacity, status):
        class_types = ["gym", "crossfit", "fitness", "yoga"]

        if class_type not in class_types:
            print("Mentioned class type is not valid!")
            return False
        hall_key = 0
        coach_key = 0

        for hal in self.halls:
            if hal["name"] == hall:
                if hal["hall_status"] is True:
                    hall_key = 1
                break

        for coach in self.users:
            if coach["username"] == coach_user:
                if coach["active_status"] is True:
                    coach_key = 1
                break

        if coach_key != 1:
            print("Coach not found or coach status is not active!")
            return False

        if hall_key != 1:
            print("Hall not found or hall status is not active!")
            return False

        clas = {
            "title": name,
            "class_type": class_type,
            "coach": coach_user,
            "sport_hall": hall,
            "class_date": date,
            "class_time": time,
            "capacity": capacity,
            "class_status": status
        }

        self.classes.append(clas)
        with open(file_path_classes, "w", encoding="utf-8") as f:
                json.dump(self.classes, f, indent=4)
        return True

    # Edit Classes info


    def edit_class_info(self, name, edit_item, item_value):

        editable_items = [
            "title", "class_type", "coach", "sport_hall",
            "class_date", "class_time", "capacity", "class_status"
        ]

        if edit_item not in editable_items:
            print("Invalid item to edit!")
            return False

        # Find the class by its current title
        target_class = None

        for clas in self.classes:
            if clas["title"] == name:
                target_class = clas
                break

        if target_class is None:
            print("Class not found!")
            return False

    # Validate class type
        if edit_item == "class_type":
            class_types = ["gym", "crossfit", "fitness", "yoga"]

            if item_value not in class_types:
                print("Mentioned class type is not valid!")
                return False

    # Validate coach
        if edit_item == "coach":

            coach_found = False

            for user in self.users:
                if user.get("username") == item_value:
                    if user.get("authority") != "coach":
                        print("Selected user is not a coach!")
                        return False

                    elif user.get("active_status") is not True:
                        print("Coach status is not active!")
                        return False

                    coach_found = True
                    break

            if not coach_found:
                print("Coach not found!")
                return False

    # Validate sport hall
        if edit_item == "sport_hall":

            hall_found = False
            selected_hall = None

            for hall in self.halls:
                if hall.get("name") == item_value:
                    if hall.get("hall_status") is not True:
                        print("Hall is not active!")
                        return False

                    selected_hall = hall
                    hall_found = True
                    break

            if not hall_found:
                print("Sport hall not found!")
                return False

        # Ensure the class capacity fits in the selected hall
            if target_class.get("capacity", 0) > selected_hall.get("capacity", 0):
                print("Class capacity exceeds hall capacity!")
                return False

    # Validate capacity
        if edit_item == "capacity":
            if type(item_value) is not int or item_value <= 0:
                print("Capacity must be a positive integer!")
                return False

            current_hall = next(
                (hall for hall in self.halls
                 if hall.get("name") == target_class.get("sport_hall")),
                None
            )

            if current_hall is None:
                print("Current sport hall not found!")
                return False

            if item_value > current_hall.get("capacity", 0):
                print("Class capacity exceeds hall capacity!")
                return False

    # Validate class status
        if edit_item == "class_status":
            if type(item_value) is not bool:
                print("Class status must be True or False!")
                return False

    # Apply the change
        target_class[edit_item] = item_value
        with open("classes.json", "w", encoding="utf-8") as f:
                json.dump(self.classes, f, indent=4, ensure_ascii=False)
        return True

    # Show classes

    def show_class_info(self):
            for clas in self.classes:
                for key, value in clas.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
