import json
import uuid
from pathlib import Path
from datetime import datetime, date
from .Bank import API

# Shared JSON files (same directory as this module)
BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "users.json"
SUBSCRIPTIONS_FILE = BASE_DIR / "subscriptions.json"
PAYMENTS_FILE = BASE_DIR / "payments.json"
CLASSES_FILE = BASE_DIR / "classes.json"
HALLS_FILE = BASE_DIR / "halls.json"
ENROLLMENTS_FILE = BASE_DIR / "class_enrollments.json"
MEMBERS_FILE = BASE_DIR / "members.json"
TRAINING_FILE = BASE_DIR / "training_plan.json"
TRANSACTIONS_DIR = BASE_DIR / "transactions"


class Member:

    def __init__(self, name, username, password, email, sub_type="", start_date="", end_date="", status="no_subscription", active_status=True):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.sub_type = sub_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.active_status = active_status

    def __str__(self):
        status = "Active" if self.active_status else "Inactive"
        return (
            f"Name: {self.name}\n"
            f"Username: {self.username}\n"
            f"Email: {self.email}\n"
            f"Subscription type: {self.sub_type or 'No subscription'}\n"
            f"Start date: {self.start_date or 'Not specified'}\n"
            f"End date: {self.end_date or 'Not specified'}\n"
            f"Subscription status: {self.status or 'No subscription'}\n"
            f"Account status: {status}"
        )

    # ---------- JSON helpers ----------
    @staticmethod
    def _load_json(path, default=None):
        if default is None:
            default = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    @staticmethod
    def _save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_users():
        return Member._load_json(USERS_FILE, [])

    @staticmethod
    def load_subscriptions():
        return Member._load_json(SUBSCRIPTIONS_FILE, [])

    @staticmethod
    def save_subscriptions(data):
        Member._save_json(SUBSCRIPTIONS_FILE, data)

    @staticmethod
    def load_payments():
        return Member._load_json(PAYMENTS_FILE, [])

    @staticmethod
    def save_payments(data):
        Member._save_json(PAYMENTS_FILE, data)

    @staticmethod
    def load_members():
        return Member._load_json(MEMBERS_FILE, [])

    @staticmethod
    def save_members(data):
        Member._save_json(MEMBERS_FILE, data)

    @staticmethod
    def setup_members():
        """Sync members.json from users.json + subscriptions.json"""
        users = Member.load_users()
        subscriptions = Member.load_subscriptions()
        members = []

        for user in users:
            if user.get("authority") != "gym_user":
                continue
            member = user.copy()
            member["amount"] = 0
            member["sub_type"] = ""
            member["start_date"] = ""
            member["end_date"] = ""
            member["status"] = "no_subscription"

            for sub in subscriptions:
                if sub.get("member_username") == user.get("username"):
                    member["amount"] = sub.get("amount", 0) if "amount" in member else member.get("amount", 0)
                    member["sub_type"] = sub.get("sub_type", "")
                    member["start_date"] = sub.get("start_date", "")
                    member["end_date"] = sub.get("end_date", "")
                    member["status"] = sub.get("status", "no_subscription")
                    break
            members.append(member)

        Member.save_members(members)
        print("Members initialized successfully.")

    # ---------- Login ----------
    @staticmethod
    def login():
        while True:
            print("\n===== Member Login =====")
            print("1. Login")
            print("2. Back")
            choice = input("Choose an option: ").strip()

            if choice == "2":
                return None

            if choice != "1":
                print("Invalid option.")
                continue

            username = input("Username: ").strip()
            password = input("Password: ").strip()

            users = Member.load_users()
            found = None
            for user in users:
                if user.get("username") == username and user.get("authority") == "gym_user":
                    found = user
                    break

            if found is None:
                print("Member not found.")
                if input("Try again? (1=yes, other=no): ").strip() != "1":
                    return None
                continue

            if password != found.get("password"):
                print("Incorrect password.")
                if input("Try again? (1=yes, other=no): ").strip() != "1":
                    return None
                continue

            if not found.get("active_status"):
                print("Account is inactive. You cannot login.")
                continue

            print("Login successful!")
            # Ensure members.json is up to date
            Member.setup_members()
            return found

    # ---------- Profile ----------
    @staticmethod
    def show_profile(username):
        members = Member.load_members()
        member_data = next((m for m in members if m.get("username") == username), None)
        users = Member.load_users()
        user_data = next((u for u in users if u.get("username") == username), None)

        if not user_data:
            print("Member not found.")
            return

        profile = Member(
            name=user_data.get("name", ""),
            username=user_data.get("username", ""),
            password=user_data.get("password", ""),
            email=user_data.get("email", ""),
            sub_type=(member_data or {}).get("sub_type", ""),
            start_date=(member_data or {}).get("start_date", ""),
            end_date=(member_data or {}).get("end_date", ""),
            status=(member_data or {}).get("status", "no_subscription"),
            active_status=user_data.get("active_status", False)
        )
        print("\n===== Profile =====")
        print(profile)

    # ---------- Wallet ----------
    @staticmethod
    def show_wallet_balance(username):
        members = Member.load_members()
        for member in members:
            if member.get("username") == username:
                print(f"\nWallet balance: {member.get('amount', 0):,} Toman")
                return
        print("Member not found.")

    @staticmethod
    def save_transaction(username, transaction_type, amount, description, tracking_number):
        TRANSACTIONS_DIR.mkdir(parents=True, exist_ok=True)
        transaction_file = TRANSACTIONS_DIR / f"{username}.txt"
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(transaction_file, "a", encoding="utf-8") as f:
            f.write(
                f"Type: {transaction_type}\n"
                f"Amount: {amount:,} Toman\n"
                f"Date: {transaction_date}\n"
                f"Description: {description}\n"
                f"Tracking: {tracking_number}\n"
                f"{'-' * 40}\n"
            )

    @staticmethod
    def show_transaction_history(username):
        transaction_file = TRANSACTIONS_DIR / f"{username}.txt"
        if not transaction_file.exists():
            print("No transactions found.")
            return
        with open(transaction_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            print("No transactions found.")
            return
        print("\n===== Transaction History =====")
        print(content)

    @staticmethod
    def charge_wallet(username):
        members = Member.load_members()
        found = next((m for m in members if m.get("username") == username), None)
        if not found:
            print("Member not found.")
            return

        try:
            amount = int(input("Enter charge amount (Toman): ").strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            card = input("Card number (16 digits): ").strip()
            exp_month = int(input("Expiration month (1-12): ").strip())
            exp_year = int(input("Expiration year (e.g. 1405): ").strip())
            password = input("Card password (6 digits): ").strip()
            cvv2 = input("CVV2 (3 digits): ").strip()

            api = API()
            payment_id = api.pay(card, exp_month, exp_year, password, cvv2, amount)
        except ValueError as e:
            print(f"Payment failed: {e}")
            return
        except Exception as e:
            print(f"Error: {e}")
            return

        found["amount"] = found.get("amount", 0) + amount
        Member.save_members(members)
        Member.save_transaction(username, "Wallet charge", amount, "Charged by card", payment_id)
        print("Wallet charged successfully.")
        print(f"New balance: {found['amount']:,} Toman")
        print(f"Tracking number: {payment_id}")

    @staticmethod
    def add_months(start, months):
        month = start.month + months
        year = start.year
        while month > 12:
            month -= 12
            year += 1
        day = min(start.day, 28)
        return date(year, month, day)

    @staticmethod
    def pay_for_subscription(username):
        members = Member.load_members()
        found = next((m for m in members if m.get("username") == username), None)
        if not found:
            print("Member not found.")
            return

        print("\nSubscription Plans:")
        print("1. 1-month  - 2,000,000 Toman")
        print("2. 3-month  - 5,400,000 Toman")
        print("3. 6-month  - 10,000,000 Toman")
        print("4. Back")

        choice = input("Choose: ").strip()
        plans = {
            "1": ("1-month", 1, 2000000),
            "2": ("3-month", 3, 5400000),
            "3": ("6-month", 6, 10000000),
        }
        if choice == "4":
            return
        if choice not in plans:
            print("Invalid choice.")
            return

        sub_type, months, price = plans[choice]
        balance = found.get("amount", 0)
        if balance < price:
            print(f"Insufficient balance. Required: {price:,}  Available: {balance:,}")
            return

        today = date.today()
        start_date = today
        if found.get("status") == "active" and found.get("end_date"):
            try:
                current_end = date.fromisoformat(found["end_date"])
                if current_end >= today:
                    start_date = current_end
            except ValueError:
                pass

        end_date = Member.add_months(start_date, months)
        tracking = "SUB-" + uuid.uuid4().hex[:12].upper()

        found["amount"] = balance - price
        found["sub_type"] = sub_type
        found["start_date"] = start_date.isoformat()
        found["end_date"] = end_date.isoformat()
        found["status"] = "active"
        found["tracking_number"] = tracking

        # Also update subscriptions.json for manager reports
        subscriptions = Member.load_subscriptions()
        for sub in subscriptions:
            if sub.get("member_username") == username and sub.get("status") == "active":
                sub["status"] = "expired"
        subscriptions.append({
            "member_username": username,
            "member_name": found.get("name", ""),
            "sub_type": sub_type,
            "amount": price,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": "active",
            "tracking_number": tracking
        })
        Member.save_subscriptions(subscriptions)

        payments = Member.load_payments()
        payments.append({
            "member_username": username,
            "member_name": found.get("name", ""),
            "sub_type": sub_type,
            "amount": price,
            "payment_date": today.isoformat(),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "tracking_number": tracking
        })
        Member.save_payments(payments)
        Member.save_members(members)
        Member.save_transaction(username, "Subscription payment", price, f"Purchased {sub_type}", tracking)

        print("\nSubscription payment successful!")
        print(f"Type: {sub_type} | Paid: {price:,} | Remaining: {found['amount']:,}")
        print(f"Start: {found['start_date']} | End: {found['end_date']}")
        print(f"Tracking: {tracking}")

    # ---------- Classes ----------
    @staticmethod
    def check_active_subscription(username):
        members = Member.load_members()
        today = date.today()
        for member in members:
            if member.get("username") == username and member.get("status") == "active":
                end_text = member.get("end_date", "")
                if not end_text:
                    return False
                try:
                    return date.fromisoformat(end_text) >= today
                except ValueError:
                    return False
        return False

    @staticmethod
    def show_available_classes():
        classes = Member._load_json(CLASSES_FILE, [])
        halls = Member._load_json(HALLS_FILE, [])
        enrollments = Member._load_json(ENROLLMENTS_FILE, [])

        print("\n===== Available Classes =====")
        found = False
        for gym_class in classes:
            if not gym_class.get("class_status"):
                continue
            hall_ok = any(
                h.get("name") == gym_class.get("sport_hall") and h.get("hall_status")
                for h in halls
            )
            if not hall_ok:
                continue

            registered = sum(
                1 for e in enrollments
                if e.get("class_title") == gym_class.get("title") and e.get("status") == "active"
            )
            capacity = gym_class.get("capacity", 0)
            remaining = capacity - registered
            if remaining <= 0:
                continue

            found = True
            print("-" * 40)
            print(f"Title      : {gym_class.get('title')}")
            print(f"Sport      : {gym_class.get('class_type')}")
            print(f"Coach      : {gym_class.get('coach')}")
            print(f"Hall       : {gym_class.get('sport_hall')}")
            print(f"Day        : {gym_class.get('class_date')}")
            print(f"Time       : {gym_class.get('class_time')}")
            print(f"Capacity   : {capacity}")
            print(f"Remaining  : {remaining}")

        if not found:
            print("No available classes found.")

    @staticmethod
    def register_for_class(username):
        if not Member.check_active_subscription(username):
            print("You need an active subscription to register.")
            return

        Member.show_available_classes()
        title = input("\nEnter class title to register: ").strip()

        classes = Member._load_json(CLASSES_FILE, [])
        selected = next((c for c in classes if c.get("title") == title), None)
        if not selected:
            print("Class not found.")
            return
        if not selected.get("class_status"):
            print("This class is not active.")
            return

        halls = Member._load_json(HALLS_FILE, [])
        hall_ok = any(
            h.get("name") == selected.get("sport_hall") and h.get("hall_status")
            for h in halls
        )
        if not hall_ok:
            print("The hall is not active.")
            return

        enrollments = Member._load_json(ENROLLMENTS_FILE, [])
        for e in enrollments:
            if e.get("username") == username and e.get("class_title") == title and e.get("status") == "active":
                print("You are already registered in this class.")
                return

        registered = sum(
            1 for e in enrollments
            if e.get("class_title") == title and e.get("status") == "active"
        )
        if registered >= selected.get("capacity", 0):
            print("This class is full.")
            return

        new_enrollment = {
            "username": username,
            "class_title": title,
            "registration_date": str(date.today()),
            "status": "active",
            "tracking_number": uuid.uuid4().hex[:12].upper()
        }
        enrollments.append(new_enrollment)
        Member._save_json(ENROLLMENTS_FILE, enrollments)
        print("Registration completed.")
        print(f"Tracking number: {new_enrollment['tracking_number']}")

    @staticmethod
    def cancel_class_registration(username):
        enrollments = Member._load_json(ENROLLMENTS_FILE, [])
        print("\nYour active registrations:")
        active = [e for e in enrollments if e.get("username") == username and e.get("status") == "active"]
        if not active:
            print("No active registrations.")
            return
        for e in active:
            print(f"  - {e.get('class_title')}")

        title = input("Enter class title to cancel: ").strip()
        found = False
        for e in enrollments:
            if e.get("username") == username and e.get("class_title") == title and e.get("status") == "active":
                e["status"] = "inactive"
                found = True
                break

        if found:
            Member._save_json(ENROLLMENTS_FILE, enrollments)
            print("Registration cancelled (record kept as inactive).")
        else:
            print("Active registration not found.")

    # ---------- Training plan ----------
    @staticmethod
    def show_training_plan(username):
        plans = Member._load_json(TRAINING_FILE, [])
        for plan in plans:
            if plan.get("username") == username:
                exercises = plan.get("exercises", [])
                if not exercises:
                    print("No exercises in your training plan.")
                    return
                print("\n===== My Training Plan =====")
                for ex in exercises:
                    print(f"\nExercise   : {ex.get('name', 'N/A')}")
                    print(f"Sets       : {ex.get('sets', 'N/A')}")
                    print(f"Reps       : {ex.get('repetitions', 'N/A')}")
                    print(f"Rest time  : {ex.get('rest_time', 'N/A')}")
                    print(f"Description: {ex.get('description', 'N/A')}")
                return
        print("No training plan found for this member.")

    # ---------- Panel ----------
    @staticmethod
    def show_panel():
        print("\n===== Member Panel =====")
        print("1. Profile and subscription")
        print("2. Wallet and payments")
        print("3. Classes")
        print("4. Training plan")
        print("5. Exit")

    @staticmethod
    def run_panel(user):
        username = user.get("username")
        while True:
            Member.show_panel()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                Member.show_profile(username)

            elif choice == "2":
                while True:
                    print("\n===== Wallet =====")
                    print("1. View balance")
                    print("2. Charge wallet")
                    print("3. Transaction history")
                    print("4. Pay / Renew subscription")
                    print("5. Back")
                    w = input("Choose: ").strip()
                    if w == "1":
                        Member.show_wallet_balance(username)
                    elif w == "2":
                        Member.charge_wallet(username)
                    elif w == "3":
                        Member.show_transaction_history(username)
                    elif w == "4":
                        Member.pay_for_subscription(username)
                    elif w == "5":
                        break
                    else:
                        print("Invalid option.")

            elif choice == "3":
                while True:
                    print("\n===== Classes =====")
                    print("1. Show available classes")
                    print("2. Register for a class")
                    print("3. Cancel registration")
                    print("4. Back")
                    c = input("Choose: ").strip()
                    if c == "1":
                        Member.show_available_classes()
                    elif c == "2":
                        Member.register_for_class(username)
                    elif c == "3":
                        Member.cancel_class_registration(username)
                    elif c == "4":
                        break
                    else:
                        print("Invalid option.")

            elif choice == "4":
                Member.show_training_plan(username)

            elif choice == "5":
                print("Logging out from Member panel...")
                return

            else:
                print("Invalid option.")