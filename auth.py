import storage as db
from password_security import hash_password, is_password_hash, verify_password


def _valid_input(check, value):
    if check is None:
        return bool(value)
    if hasattr(check, "fullmatch"):
        return bool(check.fullmatch(value))
    return bool(check(value))

def ask(prompt, check=None, error="Invalid input, please try again.", secret=False, allow_empty=False):
    import getpass
    reader = getpass.getpass if secret else input
    while True:
        raw = reader(f"{prompt} (/back to cancel): ")
        if raw.strip().lower() == "/back":
            return None
        value = raw.strip()
        if value == "" and allow_empty and raw == "":
            return ""
        if raw != value:
            print(error)
        elif _valid_input(check, value):
            return value
        else:
            print(error)

def ask_int(prompt, check=None, error="Please enter a positive whole number."):
    import re
    if check is None:
        check = re.compile(r"[1-9]\d*")
    value = ask(prompt, check, error)
    return None if value is None else int(value)

def choose(title, options, back_label="Back", back_last=False):
    if not options:
        print("Nothing available to select.")
        return None
    print(title)
    for number, option in enumerate(options, 1):
        print(f"{number}. {option}")
    back_key = str(len(options) + 1) if back_last else "0"
    print(f"{back_key}. {back_label}")
    while True:
        value = input("Choice: ").strip()
        if value == back_key:
            return None
        if value.isdigit() and 1 <= int(value) <= len(options):
            return int(value) - 1
        print("Invalid choice, try again.")

def choose_bool(prompt="Status:", true_label="Active", false_label="Inactive"):
    index = choose(prompt, [true_label, false_label])
    return None if index is None else index == 0

AUTHORITY = {"admin": "admin", "coach": "coach", "member": "gym_user"}

class Authenticator:
    @staticmethod
    def login(role, label):
        print(f"\n--- {label} login ---")
        while True:
            username = ask("Username")
            if username is None:
                return None
            password = ask("Password", secret=True)
            if password is None:
                return None
            user = Authenticator._find(role, username, password)
            if user is None:
                print("Invalid username or password. Try again.")
            elif user.get("active_status") is not True:
                print("This account is inactive. Please contact the manager.")
            else:
                print(f"Welcome, {user.get('name')}!")
                return user

    @staticmethod
    def _find(role, username, password):
        users = db.load_json(db.USERS, [])
        for user in users:
            if user.get("username") != username or user.get("authority") != AUTHORITY[role]:
                continue
            stored = user.get("password", "")
            if (verify_password(password, stored) if is_password_hash(stored) else password == stored):
                if not is_password_hash(stored):
                    user["password"] = hash_password(password)
                    db.save_json(db.USERS, users)
                return user
        return None
