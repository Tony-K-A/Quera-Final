import storage as db
import ui
from password_security import hash_password, is_password_hash, verify_password

AUTHORITY = {"admin": "admin", "coach": "coach", "member": "gym_user"}

class Authenticator:
    @staticmethod
    def login(role, label):
        print(f"\n--- {label} login ---")
        while True:
            username = ui.ask("Username")
            if username is None:
                return None
            password = ui.ask("Password", secret=True)
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
