import json
import calendar
import uuid

from pathlib import Path
from datetime import datetime, date
from .Bank import API

users_file_path = Path(__file__).resolve().parent.parent / "users.json"
subscriptions_file_path = Path(__file__).resolve().parent.parent / "subscriptions.json"
file_path_payments = Path(__file__).resolve().parent.parent / "payments.json"
classes_file_path = Path(__file__).resolve().parent.parent / "classes.json"
enrollments_file_path = Path(__file__).resolve().parent.parent / "class_enrollments.json"
member_file_path = Path(__file__).resolve().parent / "member.json"
training_file_path = (Path(__file__).resolve().parent / "training_plan.json")


class Member:

    def __init__(self, name, username, password, email, sub_type, start_date, end_date, status, active_status=True, ):
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
        sub_type = self.sub_type or "No subscription"
        start_date = self.start_date or "Not specified"
        end_date = self.end_date or "Not specified"
        subscription_status = self.status or "No subscription"

        return (f"Name: {self.name}\n"
                f"Username: {self.username}\n"
                f"Email: {self.email}\n"
                f"Subscription type: {sub_type}\n"
                f"Subscription start date: {start_date}\n"
                f"Subscription end date: {end_date}\n"
                f"Subscription status: {subscription_status}\n"
                f"Account status: {status}"
                )

    @staticmethod
    def load_users():
        import json
        from pathlib import Path

        file_path = Path(__file__).resolve().parent.parent / "users.json"

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def load_subscriptions():
        import json
        from pathlib import Path

        users_file_path = Path(__file__).resolve().parent.parent / "subscriptions.json"

        with open(users_file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_subscriptions(subscriptions):
        import json
        from pathlib import Path

        subscriptions_file_path = Path(__file__).resolve().parent.parent / "subscriptions.json"

        with open(subscriptions_file_path, "w", encoding="utf-8") as file:
            json.dump(subscriptions, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_payments():
        if not file_path_payments.exists():
            return []

        with open(file_path_payments, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_payments(payments):
        with open(file_path_payments, "w", encoding="utf-8") as file:
            json.dump(payments, file, indent=4, ensure_ascii=False)


    @staticmethod
    def load_members():
        if not member_file_path.exists():
            return []

        with open(member_file_path, "r", encoding="utf-8") as file:
            return json.load(file)


    @staticmethod
    def save_members(members):
        with open(member_file_path, "w", encoding="utf-8") as file:
            json.dump(members, file, indent=4, ensure_ascii=False)

    @staticmethod
    def setup_members():
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
            member["status"] = "inactive"

            for sub in subscriptions:
                if sub.get("member_username") == user.get("username"):
                    member["amount"] = sub.get("amount", 0)
                    member["sub_type"] = sub.get("sub_type", "")
                    member["start_date"] = sub.get("start_date", "")
                    member["end_date"] = sub.get("end_date", "")
                    member["status"] = sub.get("status", "inactive")
                    break

            members.append(member)

        Member.save_members(members)
        print("Members initialized successfully.")

    @staticmethod
    def login():
        while True:
            print("\n   Member Login   ")
            print("1. Login")
            print("2. Back")

            choice = input("Choose an option: ")

            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")

                users = Member.load_users()
                found_member = None

                for user in users:
                    if username == user.get("username"):
                        if user.get("authority") == "gym_user":
                            found_member = user
                            break

                if found_member is None:
                    print("Member not found")
                    
                    print("1 Try again")

                    retry_choice = input("Choose an option: ")

                    if retry_choice == "1":
                        continue

                    else:
                        print("Invalid option. Returning to login.")
                        continue

                if password == found_member.get("password"):
                    if found_member.get("active_status"):
                        print("Login successful")
                        return found_member
                    else:
                        print("Account is inactive")
                        continue

                else:
                    print("Incorrect password")

                    print("1 Try again")

                    retry_choice = input("Choose an option: ")

                    if retry_choice == "1":
                        continue

                    else:
                        print("Invalid option. Returning to login.")
                        continue

            elif choice == "2":
                return "back"

            else:
                print("Invalid option. Please try again.")

    @staticmethod
    def show_profile(username):
        users = Member.load_users()
        members = Member.load_members()

        users = None
        member_data = None

        for item in members:
            if item.get("username") == username:
                if item.get("authority") == "gym_user":
                    users = item
                    break

        if users is None:
            print("Member not found.")
            return
        
        for item in members:
            if item.get("username") == username:
                member_data = item
                break

        if member_data is None:
            member_data = {}


        profile = Member(
            name=users.get("name", ""),
            username=users.get("username", ""),
            password=users.get("password", ""),
            email=users.get("email", ""),
            sub_type=member_data.get("sub_type", ""),
            start_date=member_data.get("start_date", ""),
            end_date=member_data.get("end_date", ""),
            status=member_data.get("status", "inactive"),
            active_status=users.get("active_status", False)
        )


        print(profile)
    print("Member not found")

    @staticmethod
    def show_wallet_balance(username):
        members = Member.load_members()

        for member in members:
            if member.get("username") == username:
                balance = member.get("amount", 0)
                print(f"\namount: {balance:,} Toman")
                return

        print("Member not found.")


    @staticmethod
    def charge_wallet(username):
        members = Member.load_members()
        found_member = None

        for member in members:
            if member.get("username") == username:
                found_member = member
                break

        if found_member is None:
            print("Member Not Found")
            return

        try:
            amount = int(input("Enter charge amount in Toman: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            card = input("Card number (16 digits): ").strip()
            exp_month = int(input("Expiration month (1-12): "))
            exp_year = int(input("Expiration year: "))
            password = input("Card password (6 digits): ").strip()
            cvv2 = input("CVV2 (3 digits): ").strip()

            api = API()
            payment_id = api.pay(card, exp_month, exp_year, password, cvv2, amount)

        except ValueError as error:
            print(f"Payment failed: {error}")
            return

        found_member["amount"] = found_member.get("amount", 0) + amount

        Member.save_members(members)

        Member.save_transaction(username, "Wallet charge", amount, "Wallet charged by card", payment_id)

        print("Wallet charged successfully.")
        print(f"New balance: {found_member['amount']:,} Toman")
        print(f"Tracking number: {payment_id}")

            
    @staticmethod
    def save_transaction(username, transaction_type, amount, description, tracking_number):
        transaction_dir = Path(__file__).resolve().parent / "transactions"
        transaction_dir.mkdir(parents=True, exist_ok=True)

        transaction_file = transaction_dir / f"{username}.txt"
        transaction_date = datetime.now().astimezone().isoformat(timespec="seconds")

        with open(transaction_file, "a", encoding="utf-8") as file:
            file.write(f"Transaction type: {transaction_type}\n" f"Amount: {amount:,} Toman\n" f"Date: {transaction_date}\n" f"Description: {description}\n" f"Tracking number: {tracking_number}\n" f"{'-' * 40}\n")

    
    @staticmethod
    def show_transaction_history(username):
        transaction_dir = Path(__file__).resolve().parent / "transactions"
        transaction_file = transaction_dir / f"{username}.txt"

        if not transaction_file.exists():
            print("No transactions found.")
            return

        with open(transaction_file, "r", encoding="utf-8") as file:
            history = file.read()

        if not history.strip():
            print("No transactions found.")
            return

        print("\n   Transaction History   ")
        print(history)


    @staticmethod
    def add_months(start_date, months):
        month = start_date.month + months
        year = start_date.year

        while month > 12:
            month -= 12
            year += 1

        day = start_date.day

        if day > 28:
            day = 28

        return date(year, month, day)


    @staticmethod
    def pay_for_subscription(username):
        members = Member.load_members()

        found_member = None

        for member in members:
            if member["username"] == username:
                found_member = member
                break

        if found_member is None:
            print("Member subscription record not found.")
            return

        print("\nSubscription Plans:")
        print("1. Monthly - 2,000,000 Toman")
        print("2. Quarterly - 5,400,000 Toman")
        print("3. Semiannual - 10,000,000 Toman")
        print("4. Back")

        choice = input("Choose a subscription: ")

        if choice == "4":
            return

        if choice == "1":
            sub_type = "1-month"
            months = 1
            price = 2000000

        elif choice == "2":
            sub_type = "3-month"
            months = 3
            price = 5400000

        elif choice == "3":
            sub_type = "6-month"
            months = 6
            price = 10000000

        else:
            print("Invalid subscription choice.")
            return

        balance = found_member.get("amount", 0)

        if balance < price:
            print("Insufficient wallet balance.")
            print("Required:", price, "Toman")
            print("Available:", balance, "Toman")
            return

        today = date.today()
        start_date = today

        if found_member.get("status") == "active":
            end_text = found_member.get("end_date")

            if end_text:
                try:
                    current_end = date.fromisoformat(end_text)

                    if current_end >= today:
                        start_date = current_end

                except ValueError:
                    print("Invalid existing subscription end date.")
                    return

        end_date = Member.add_months(start_date, months)

        tracking_number = "SUB-" + uuid.uuid4().hex[:12].upper()

        found_member["amount"] = balance - price
        found_member["sub_type"] = sub_type
        found_member["start_date"] = start_date.isoformat()
        found_member["end_date"] = end_date.isoformat()
        found_member["status"] = "active"
        found_member["tracking_number"] = tracking_number

        payments = Member.load_payments()

        payment = {
            "member_username": username,
            "member_name": found_member.get("member_name", ""),
            "sub_type": sub_type,
            "amount": price,
            "payment_date": today.isoformat(),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "tracking_number": tracking_number
        }

        payments.append(payment)

        Member.save_members(members)
        Member.save_payments(payments)

        description = "Purchased or renewed " + sub_type + " subscription"

        Member.save_transaction(username,"Subscription payment", price, description, tracking_number)

        print("\nSubscription payment successful.")
        print("Subscription:", sub_type)
        print("Paid:", price, "Toman")
        print("Remaining wallet balance:", found_member["amount"], "Toman")
        print("Start date:", found_member["start_date"])
        print("End date:", found_member["end_date"])
        print("Tracking number:", tracking_number)


    @staticmethod
    def show_available_classes():
        file = open(classes_file_path, "r", encoding="utf-8")
        classes = json.load(file)
        file.close()

        halls_file_path = Path(__file__).resolve().parent.parent / "halls.json"

        file = open(halls_file_path, "r", encoding="utf-8")
        halls = json.load(file)
        file.close()

        enrollments = []

        if enrollments_file_path.exists():
            file = open(enrollments_file_path, "r", encoding="utf-8")
            enrollments = json.load(file)
            file.close()

        found_class = False

        print("\nAvailable Classes")

        for gym_class in classes:

            if gym_class["class_status"] == False:
                continue

            hall_found = False

            for hall in halls:
                if hall["name"] == gym_class["sport_hall"]:
                    if hall["hall_status"] == True:
                        hall_found = True

                    break

            if hall_found == False:
                continue

            registered_count = 0

            for enrollment in enrollments:
                if enrollment["class_title"] == gym_class["title"]:
                    if enrollment["status"] == "active":
                        registered_count = registered_count + 1

            capacity = gym_class["capacity"]
            remaining_capacity = capacity - registered_count

            if remaining_capacity > 0:
                found_class = True

                print("-------------------------")
                print("Title:", gym_class["title"])
                print("Sport:", gym_class["class_type"])
                print("Coach:", gym_class["coach"])
                print("Hall:", gym_class["sport_hall"])
                print("Day:", gym_class["class_date"])
                print("Time:", gym_class["class_time"])
                print("Total capacity:", capacity)
                print("Remaining capacity:", remaining_capacity)

        if found_class == False:
            print("No available classes found.")


    @staticmethod
    def check_active_subscription(username):
        members = Member.load_members()
        today = date.today()

        for member in members:
            if member.get("username") == username:
                if member["status"] == "active":
                    end_text = member.get("end_date", "")
                    
                    if not end_text:
                        return False
                    try:
                        return date.fromisoformat(end_text) >= today
                    except ValueError:
                        return False
        return False

    @staticmethod
    def register_for_class(username):
        
        if Member.check_active_subscription(username) == False:
            print("You need an active subscription.")
            return

        file = open(classes_file_path, "r", encoding="utf-8")
        classes = json.load(file)
        file.close()

        Member.show_available_classes()

        title = input("Enter class title: ")

        selected_class = None

        for gym_class in classes:
            if gym_class["title"] == title:
                selected_class = gym_class
                break

        if selected_class is None:
            print("Class not found.")
            return

        if selected_class["class_status"] == False:
            print("This class is not active.")
            return
        
        halls_file_path = Path(__file__).resolve().parent.parent / "halls.json"

        file = open(halls_file_path, "r", encoding="utf-8")
        halls = json.load(file)
        file.close()

        hall_found = False

        for hall in halls:
            if hall["name"] == selected_class["sport_hall"]:
                if hall["hall_status"] == True:
                    hall_found = True
                break

        if hall_found == False:
            print("The hall is not active.")
            return

        file = open(enrollments_file_path, "r", encoding="utf-8")
        enrollments = json.load(file)
        file.close()

        for enrollment in enrollments:
            if enrollment["username"] == username:
                if enrollment["class_title"] == title:
                    if enrollment["status"] == "active":
                        print("You are already registered.")
                        return

        registered_count = 0

        for enrollment in enrollments:
            if enrollment["class_title"] == title:
                if enrollment["status"] == "active":
                    registered_count += 1

        if registered_count >= selected_class["capacity"]:
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

        file = open(enrollments_file_path, "w", encoding="utf-8")
        json.dump(enrollments, file, indent=4, ensure_ascii=False)
        file.close()

        print("Registration completed.")
        print("Tracking number:", new_enrollment["tracking_number"])


    @staticmethod
    def cancel_class_registration(username):
        file = open(enrollments_file_path, "r", encoding="utf-8")
        enrollments = json.load(file)
        file.close()

        found_registration = False

        print("\nYour active registrations:")

        for enrollment in enrollments:
            if enrollment["username"] == username:
                if enrollment["status"] == "active":
                    print(enrollment["class_title"])

        title = input("Enter class title to cancel: ")

        for enrollment in enrollments:
            if enrollment["username"] == username:
                if enrollment["class_title"] == title:
                    if enrollment["status"] == "active":
                        enrollment["status"] = "inactive"
                        found_registration = True
                        break

        if found_registration == True:
            file = open(enrollments_file_path, "w", encoding="utf-8")
            json.dump(enrollments, file, indent=4, ensure_ascii=False)
            file.close()

            print("Registration cancelled.")
        else:
            print("Active registration not found.")


    @staticmethod
    def show_training_plan(username):
        training_file_path = (Path(__file__).resolve().parent / "training_plan.json")

        if not training_file_path.exists():
            print("Training plan is not available.")
            return

        with open(training_file_path, "r", encoding="utf-8") as file:
            training_plans = json.load(file)

        for plan in training_plans:
            if plan.get("username") == username:
                exercises = plan.get("exercises", [])

                if not exercises:
                    print("No exercises found in your training plan.")
                    return

                print("\n    My Training Plan    ")

                for exercise in exercises:
                    print(f"\nExercise: {exercise.get('name', 'N/A')}")
                    print(f"Sets: {exercise.get('sets', 'N/A')}")
                    print(f"Repetitions: " f"{exercise.get('repetitions', 'N/A')}")
                    print(f"Rest time: " f"{exercise.get('rest_time', 'N/A')}")
                    print(f"Description: " f"{exercise.get('description', 'N/A')}")

                return

        print("No training plan found for this member.")


    @staticmethod
    def show_panel():
        print("\n Gym User Panel")
        print("1 Profile and subscription")
        print("2 Wallet and payments")
        print("3 Classes")
        print("4 Training plan")
        print("5 Exit")


    @staticmethod
    def run_panel(users):
        while True:
            Member.show_panel()

            choice = input("chois an option: ")

            if choice == "1":
                Member.show_profile(users["username"])

                print("Profile and subscription")
            elif choice == "2":
                while True:
                    print("\n Wallet Status")
                    print("1 View Inventory")
                    print("2 Charge wallet")
                    print("3 Transaction history")
                    print("4 Pay for / Renew subscription")
                    print("5 Back")

                    wallet_choice = input("Choose an option: ")

                    if wallet_choice == "1":
                        Member.show_wallet_balance(users["username"])
                    elif wallet_choice == "2":
                        try:
                            Member.charge_wallet(users["username"])
                        except Exception as error:
                            print(error)

                    elif wallet_choice == "3":
                        Member.show_transaction_history(users["username"])
                    elif wallet_choice == "4":
                         Member.pay_for_subscription(users["username"])
                    elif wallet_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again")

            elif choice == "3":
                while True:
                    print("\nClasses Menu")
                    print("1. Show available classes")
                    print("2. Register for a class")
                    print("3. Cancel registration")
                    print("4. Back")

                    class_choice = input("Choose an option: ")

                    if class_choice == "1":
                        Member.show_available_classes()

                    elif class_choice == "2":
                        Member.register_for_class(users["username"])

                    elif class_choice == "3":
                        Member.cancel_class_registration(users["username"])

                    elif class_choice == "4":
                        break

                    else:
                        print("Invalid option.")

            elif choice =="4":
                Member.show_training_plan(users["username"])
            elif choice == "5":
                print("Logging out...")
                return "Exit"
                
            else:
                print("Invalid option. Please try again")                  