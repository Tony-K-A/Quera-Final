import re

import storage as db
import services as svc
import ui
import validators as v

class MemberPanel:
    def __init__(self, member):
        self.username = member["username"]

    def run(self):
        actions = [self.profile, self.wallet_menu, self.classes_menu, self.workout_plan]
        while True:
            index = ui.choose("\n=== Member panel ===",
                              ["Profile and subscription status", "Wallet", "Classes", "Workout plan"],
                              back_label="Logout", back_last=True)
            if index is None:
                print("Logged out.")
                return
            actions[index]()

    def profile(self):
        user = svc.find_user(self.username)
        print(f"Name           : {user.get('name')}")
        print(f"Username       : {user.get('username')}")
        print(f"Email          : {user.get('email')}")
        print(f"Account status : {'active' if user.get('active_status') is True else 'inactive'}")
        svc.SubscriptionService.print_status(user)

    def wallet_menu(self):
        actions = [self.show_balance, self.charge_wallet, self.show_transactions, self.buy_subscription]
        while True:
            index = ui.choose("\n-- Wallet --", ["View balance", "Charge wallet", "View transactions",
                                                  "Buy or renew subscription"])
            if index is None:
                return
            actions[index]()

    def show_balance(self):
        print(f"Current balance: {svc.WalletService.balance(self.username)}")

    def charge_wallet(self):
        amount = ui.ask_int("Amount to add")
        if amount is None:
            return
        card = ui.ask("Card number (16 digits)", v.CARD_RE, "Card number must be exactly 16 digits.")
        if card is None:
            return
        month = ui.ask_int("Expiry month (1-12)", re.compile(r"[1-9]|1[0-2]"), "Month must be 1-12.")
        if month is None:
            return
        year = ui.ask_int("Expiry year (Jalali, e.g. 1405)", re.compile(r"14\d\d"), "Enter a 4-digit year like 1405.")
        if year is None:
            return
        bank_pass = ui.ask("Card password (6 digits)", re.compile(r"\d{6}"), "Password must be 6 digits.", secret=True)
        if bank_pass is None:
            return
        cvv2 = ui.ask("CVV2 (3 digits)", re.compile(r"\d{3}"), "CVV2 must be 3 digits.", secret=True)
        if cvv2 is None:
            return
        svc.WalletService.charge(self.username, amount, card, month, year, bank_pass, cvv2)

    def show_transactions(self):
        rows = svc.WalletService.transactions(self.username)
        if not rows:
            print("No transactions yet.")
        for row in rows:
            print(f"Type        : {row['type']}")
            print(f"Amount      : {row['amount']}")
            print(f"Date        : {row['date']}")
            print(f"Description : {row['description']}")
            print(f"Tracking no.: {row['tracking']}")
            print("-" * 50)

    def buy_subscription(self):
        keys = list(svc.PLANS)
        index = ui.choose("Choose a plan:", [
            f"{k} - {svc.PLANS[k]['price']} ({svc.PLANS[k]['days']} days)" for k in keys])
        if index is None:
            return
        svc.WalletService.buy_subscription(self.username, keys[index])

    def classes_menu(self):
        actions = [self.view_classes, self.enroll, self.withdraw, self.my_enrollments]
        while True:
            index = ui.choose("\n-- Classes --", ["View available classes", "Enroll in a class",
                                                   "Withdraw from a class", "My enrollments"])
            if index is None:
                return
            actions[index]()

    def _active_classes(self):
        return [c for c in db.load_json(db.CLASSES, []) if c.get("class_status") is True]

    def view_classes(self):
        classes = self._active_classes()
        if not classes:
            print("No classes are open right now.")
        for gym_class in classes:
            svc.print_class(gym_class)

    def enroll(self):
        classes = self._active_classes()
        labels = [f"{c['title']} ({c['class_date']} {c['class_time']}, "
                  f"{svc.EnrollmentService.remaining(c)} places left)" for c in classes]
        index = ui.choose("Choose a class:", labels)
        if index is None:
            return
        svc.EnrollmentService.enroll(self.username, classes[index]["title"])

    def withdraw(self):
        active = svc.EnrollmentService.active_for_member(self.username)
        index = ui.choose("Withdraw from which class?", [e["class_title"] for e in active])
        if index is None:
            return
        svc.EnrollmentService.withdraw(self.username, active[index]["class_title"])

    def my_enrollments(self):
        records = [e for e in db.load_json(db.ENROLLMENTS, []) if e.get("member_username") == self.username]
        if not records:
            print("You have not enrolled in any class yet.")
        for record in records:
            print(f"Class        : {record['class_title']}")
            print(f"Enrolled on  : {record['enrolled_date']}")
            print(f"Status       : {record['status']}")
            print(f"Tracking no. : {record['tracking_number']}")
            print("-" * 50)

    def workout_plan(self):
        plans = svc.WorkoutService.plans_for_member(self.username)
        if not plans:
            print("Your coach has not created a workout plan for you yet.")
        users = {u.get("username"): u.get("name", u.get("username")) for u in db.load_json(db.USERS, [])}
        for plan in plans:
            print(f"\nClass: {plan['class_title']} (coach: {users.get(plan.get('coach'), plan.get('coach'))})")
            svc.WorkoutService.print_exercises(plan["exercises"])
