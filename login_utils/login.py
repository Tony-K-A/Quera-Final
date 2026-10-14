import json
from pathlib import Path

def login(username, password, authority, status = None):
    file_path = Path(__file__).resolve().parent / "login_info.json"

    try:
        with open("users.json", "r", encoding="utf-8") as f:
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

def show_menu_login():
    print("\n===== Gym Management System =====")
    print("1. Manager Login")
    print("2. Coach Login")
    print("3. Member Login")
    print("4. Exit")
    print()

def show_manager_user_options():
    print("\n===== Users Management =====")
    print("1. Add User (Coach / Member)")
    print("2. Edit User")
    print("3. Show All Users")
    print("4. Activate / Deactivate User")
    print("5. Back")
    print()

def show_manager_hall_options():
    print("\n===== Halls Management =====")
    print("1. Add Hall")
    print("2. Edit Hall")
    print("3. Show All Halls")
    print("4. Activate / Deactivate Hall")
    print("5. Back")
    print()

def show_manager_class_options():
    print("\n===== Classes Management =====")
    print("1. Add Class")
    print("2. Edit Class")
    print("3. Show All Classes")
    print("4. Activate / Deactivate Class")
    print("5. Back")
    print()

def show_manager_subscription_options():
    print("\n===== Subscriptions & Payments =====")
    print("1. Create Subscription for a Member")
    print("2. Show All Payments")
    print("3. Show Subscription Status")
    print("4. Back")
    print("=" * 35)
