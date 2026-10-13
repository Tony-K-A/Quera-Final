import json
from pathlib import Path

file_path = Path(__file__).resolve().parent / "users.json"
file_path_hall = Path(__file__).resolve().parent / "halls.json"
file_path_classes = Path(__file__).resolve().parent / "classes.json"

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
                coaches = [] 
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
            except OSError as e:
                print(f"Could now save users: {e}")
                return False

        elif (authority == "gym_user"):
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    coaches = json.load(f)
            except FileNotFoundError:
                coaches = []  
            else:
                if any(coach.get("username") == username for coach in coaches):
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
                coaches.append(coach)
                try: 
                    with open("users.json", "w") as f:
                        json.dump(coaches, f, indent=4)
                except OSError as e:
                    print(f"Could not save users: {e}")
                    return False
                return True
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
                            pass
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except OSError:
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
                            pass
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except OSError:
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
                            pass
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except OSError:
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
                            pass
                    try:
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, indent=4)
                    except OSError:
                        return False
                return True
            case wrong:
                print("Invalid selection! ")
                return False

    # Module to show users information

    def show_user_info(self):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            print(f"file does not exist in path {file_path}")
            return False
        else:
            for user in users:
                for key, value in user.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Add hall

    def add_hall(self, name, capacity, tools, hall_status):

        if isinstance(tools, str):
            tools = [tool.strip() for tool in tools.split(",")]

        try:
            with open("halls.json", "r", encoding="utf-8") as f:
                halls = json.load(f)
                print("try 1 ok")

        except FileNotFoundError:
            print(f"Halls.json not found in path {file_path_hall}")
            halls = []

        else:
            hall = {
                    "name": name,
                "capacity": capacity,
                "tools": tools,
                "hall_status": hall_status
            }

            halls.append(hall)
            print("hall appended")
            try:
                with open("halls.json", "w", encoding="utf-8") as f:
                    json.dump(halls, f, indent=4)
                    print("hall dumped")
            except OSError:
                return False
            return True

    # Edit hall information by taking name of the hall as a key

    def edit_hall_info(self, name, choice, new_amount):
        match choice:
            case "name":
                try:
                    with open("halls.json", "r", encoding="utf-8") as f:
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
                    with open("halls.json", "w", encoding="utf-8") as f:    
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
                        pass
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

    # Classes Section
    # Add classes

    def add_class(self, name, class_type, coach_user, hall, date, time, capacity, status):
        class_types = ["gym", "crossfit", "fitness", "yoga"]

        if class_type not in class_types:
            print("Mentioned class type is not valid!")
            return False

        try:
            with open("classes.json", "r", encoding="utf-8") as f:
                classes = json.load(f)
        except FileNotFoundError:
            print("File not found: classes.json")
            return False
        except json.JSONDecodeError:
            print("classes.json contains invalid JSON!")
            return False

        try:
            with open("halls.json", "r", encoding="utf-8") as h:
                halls = json.load(h)

            with open("users.json", "r", encoding="utf-8") as c:
                coaches = json.load(c)

        except FileNotFoundError:
            print("Hall or User file not found!")
            return False
        except json.JSONDecodeError:
            print("halls.json or users.json contains invalid JSON!")
            return False

        hall_key = 0
        coach_key = 0

        for hal in halls:
            if hal["name"] == hall:
                if hal["hall_status"] is True:
                    hall_key = 1
                break

        for coach in coaches:
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

        classes.append(clas)

        try:
            with open("classes.json", "w", encoding="utf-8") as f:
                json.dump(classes, f, indent=4)
        except OSError:
            print("Could not save the class!")
            return False

        return True


    # Edit Classes info


    def edit_class_info(self, name, edit_item, item_value):


        try:
            with open("classes.json", "r", encoding="utf-8") as f:
                classes = json.load(f)
        except FileNotFoundError:
            print("File not found: classes.json")
            return False

        editable_items = [
            "title", "class_type", "coach", "sport_hall",
            "class_date", "class_time", "capacity", "class_status"
        ]

        if edit_item not in editable_items:
            print("Invalid item to edit!")
            return False

        # Find the class by its current title
        target_class = None

        for clas in classes:
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
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
            except FileNotFoundError:
                print("Users file not found!")
                return False
            except json.JSONDecodeError:
                print("users.json contains invalid JSON!")
                return False

            coach_found = False

            for user in users:
                if user.get("username") == item_value:
                    if user.get("authority") != "coach":
                        print("Selected user is not a coach!")
                        return False

                    if user.get("active_status") is not True:
                        print("Coach status is not active!")
                        return False

                    coach_found = True
                    break

            if not coach_found:
                print("Coach not found!")
                return False

    # Validate sport hall
        if edit_item == "sport_hall":
            try:
                with open("halls.json", "r", encoding="utf-8") as f:
                    halls = json.load(f)
            except FileNotFoundError:
                print("Halls file not found!")
                return False
            except json.JSONDecodeError:
                print("halls.json contains invalid JSON!")
                return False

            hall_found = False
            selected_hall = None

            for hall in halls:
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

            try:
                with open("halls.json", "r", encoding="utf-8") as f:
                    halls = json.load(f)
            except FileNotFoundError:
                print("Halls file not found!")
                return False
            except json.JSONDecodeError:
                print("halls.json contains invalid JSON!")
                return False

            current_hall = next(
                (hall for hall in halls
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

        try:
            with open("classes.json", "w", encoding="utf-8") as f:
                json.dump(classes, f, indent=4, ensure_ascii=False)
        except OSError:
            print("Could not save the class information!")
            return False

        return True

    # Show classes

    def show_class_info(self):
        try:
            with open("classes.json", "r") as f:
                classes = json.load(f)
        except FileNotFoundError:
            print(f"File not found in path {file_path_classes}")
            return False
        else:
            for clas in classes:
                for key, value in clas.items():
                    print(f"{key} : {value}")
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")