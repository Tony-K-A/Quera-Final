
import storage as db
from password_security import hash_password

USERS = [
    {"name": "Manager", "authority": "admin", "username": "admin", "password": hash_password("Admin@123"),
     "email": "admin@gym.com", "active_status": True},
    {"name": "Sara Coach", "authority": "coach", "username": "coach1", "password": hash_password("Coach@123"),
     "email": "coach1@gym.com", "active_status": True},
    {"name": "Ali Coach", "authority": "coach", "username": "coach2", "password": hash_password("Coach@456"),
     "email": "coach2@gym.com", "active_status": True},
    {"name": "Mina Member", "authority": "gym_user", "username": "member1", "password": hash_password("Member@123"),
     "email": "member1@gym.com", "active_status": True},
    {"name": "Reza Member", "authority": "gym_user", "username": "member2", "password": hash_password("Member@456"),
     "email": "member2@gym.com", "active_status": True},
]

HALLS = [
    {"name": "Main Hall", "capacity": 30, "tools": ["treadmill", "dumbbell", "bike"], "hall_status": True},
    {"name": "Yoga Room", "capacity": 15, "tools": ["mat", "block"], "hall_status": True},
]

CLASSES = [
    {"title": "Morning Yoga", "class_type": "yoga", "coach": "coach1", "sport_hall": "Yoga Room",
     "class_date": "Saturday", "class_time": "08:00", "capacity": 15, "class_status": True},
    {"title": "Evening Crossfit", "class_type": "crossfit", "coach": "coach2", "sport_hall": "Main Hall",
     "class_date": "Monday", "class_time": "18:30", "capacity": 20, "class_status": True},
]

WALLETS = {"member1": 3_000_000, "member2": 0}

DEFAULT_FILES = {
    db.USERS: USERS,
    db.HALLS: HALLS,
    db.CLASSES: CLASSES,
    db.SUBSCRIPTIONS: [],
    db.PAYMENTS: [],
    db.ENROLLMENTS: [],
    db.WORKOUTS: [],
    db.WALLETS: WALLETS,
}

def ensure_data_files():
    for path, content in DEFAULT_FILES.items():
        if not path.exists():
            db.save_json(path, content)
    if not db.TRANSACTIONS.exists():
        db.TRANSACTIONS.touch()
    classes = db.load_json(db.CLASSES, [])
    if any("members" in gym_class for gym_class in classes):
        for gym_class in classes:
            gym_class.pop("members", None)
        db.save_json(db.CLASSES, classes)
    wallets = db.load_json(db.WALLETS, {})
    existing_usernames = set()
    for line in db.read_lines(db.TRANSACTIONS):
        parts = line.split("|", 5)
        if len(parts) == 6:
            existing_usernames.add(parts[1])
    for username, balance in wallets.items():
        if balance and username not in existing_usernames:
            db.append_line(db.TRANSACTIONS, "|".join([
                "OPENING-BALANCE", username, "opening_balance", str(balance),
                db.now_str(), "Opening wallet balance from initial data"
            ]))
