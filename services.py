import uuid
from pathlib import Path
from datetime import date, datetime, timedelta

import bank_gateway
import storage as db

DATE_FMT = "%Y-%m-%d"

PLANS = {
    "1-month": {"days": 30, "price": 500000},
    "3-month": {"days": 90, "price": 1000000},
    "6-month": {"days": 180, "price": 2000000},
}

def _snapshot_files(paths):
    snapshots = {}
    for path in paths:
        path = Path(path)
        snapshots[path] = path.read_bytes() if path.exists() else None
    return snapshots

def _restore_files(snapshots):
    errors = []
    for path, content in snapshots.items():
        try:
            if content is None:
                path.unlink(missing_ok=True)
            else:
                temp = path.with_name(path.name + ".rollback.tmp")
                temp.write_bytes(content)
                temp.replace(path)
        except OSError as error:
            errors.append(f"{path.name}: {error}")
    if errors:
        raise db.DataError("Rollback could not restore all data files: " + "; ".join(errors))

def new_tracking_number():
    return uuid.uuid4().hex[:8].upper()

def find_user(username):
    users = db.load_json(db.USERS, [])
    for user in users:
        if user.get("username") == username:
            return user
    return None

def find_class(title):
    classes = db.load_json(db.CLASSES, [])
    for gym_class in classes:
        if gym_class.get("title") == title:
            return gym_class
    return None

def users_by_role(authority, active_only=False):
    result = []
    for user in db.load_json(db.USERS, []):
        if user.get("authority") != authority:
            continue
        if active_only and user.get("active_status") is not True:
            continue
        result.append(user)
    return result

def print_class(gym_class, show_members=False):
    title = gym_class.get("title")
    remaining = EnrollmentService.remaining(gym_class)
    users = {u.get("username"): u.get("name", u.get("username")) for u in db.load_json(db.USERS, [])}
    coach_name = users.get(gym_class.get("coach"), gym_class.get("coach"))

    if gym_class.get("class_status") is True:
        status = "active"
    else:
        status = "inactive"

    print(f"Title            : {title}")
    print(f"Sport            : {gym_class.get('class_type')}")
    print(f"Coach            : {coach_name}")
    print(f"Hall             : {gym_class.get('sport_hall')}")
    print(f"Day and time     : {gym_class.get('class_date')} {gym_class.get('class_time')}")
    print(f"Total capacity   : {gym_class.get('capacity')}")
    print(f"Remaining        : {remaining}")
    print(f"Status           : {status}")

    if show_members:
        print(f"Enrolled members : {members_text(title)}")
    print("-" * 50)

def members_text(title):

    names = {}
    for user in db.load_json(db.USERS, []):
        names[user["username"]] = user["name"]

    texts = []
    for enrollment in EnrollmentService.active_for_class(title):
        username = enrollment["member_username"]
        texts.append(f"{names.get(username, '?')} ({username})")

    if not texts:
        return "none"
    return ", ".join(texts)

class SubscriptionService:
    @staticmethod
    def latest(username):
        subs = [s for s in db.load_json(db.SUBSCRIPTIONS, []) if s.get("member_username") == username]
        return max(subs, key=lambda s: s.get("end_date", ""), default=None)

    @staticmethod
    def status(username):
        subscriptions = db.load_json(db.SUBSCRIPTIONS, [])
        member_subscriptions = [s for s in subscriptions if s.get("member_username") == username]
        sub = max(member_subscriptions, key=lambda s: s.get("end_date", ""), default=None)
        if sub is None:
            return "no_subscription", None
        try:
            end = datetime.strptime(sub["end_date"], DATE_FMT).date()
        except (KeyError, ValueError):
            status = "expired"
        else:
            status = "active" if end >= date.today() else "expired"
        if sub.get("status") != status:
            sub["status"] = status
            db.save_json(db.SUBSCRIPTIONS, subscriptions)
        return status, sub

    @staticmethod
    def print_status(user):
        status, sub = SubscriptionService.status(user["username"])
        print(f"Subscription status : {status}")
        if sub:
            print(f"Subscription type   : {sub.get('sub_type')}")
            print(f"Start date          : {sub.get('start_date')}")
            print(f"End date            : {sub.get('end_date')}")

    @staticmethod
    def append_records(username, plan_key, amount, subscriptions, payments, tracking=None):
        plan = PLANS.get(plan_key)
        user = find_user(username)
        if plan is None or user is None or user.get("authority") != "gym_user" or user.get("active_status") is not True:
            raise ValueError("Invalid plan or active member.")
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValueError("Payment amount must be positive.")
        current = max((s for s in subscriptions if s.get("member_username") == username),
                      key=lambda s: s.get("end_date", ""), default=None)
        renewing = False
        if current is not None:
            try:
                renewing = datetime.strptime(current["end_date"], DATE_FMT).date() >= date.today()
            except (KeyError, ValueError):
                renewing = False
        start = datetime.strptime(current["end_date"], DATE_FMT).date() if renewing else date.today()
        end = start + timedelta(days=plan["days"])
        start_text, end_text = start.strftime(DATE_FMT), end.strftime(DATE_FMT)
        tracking = tracking or new_tracking_number()
        for sub in subscriptions:
            if sub.get("member_username") == username and sub.get("status") == "active":
                sub["status"] = "expired"
        subscriptions.append({
            "member_username": username, "member_name": user.get("name"), "sub_type": plan_key,
            "amount": amount, "start_date": start_text, "end_date": end_text,
            "status": "active", "tracking_number": tracking,
        })
        payments.append({
            "member_username": username, "member_name": user.get("name"), "sub_type": plan_key,
            "amount": amount, "payment_date": date.today().strftime(DATE_FMT),
            "start_date": start_text, "end_date": end_text, "tracking_number": tracking,
        })
        return tracking, start_text, end_text

    @staticmethod
    def create_admin_subscription(username, plan_key, amount):
        subscriptions = db.load_json(db.SUBSCRIPTIONS, [])
        payments = db.load_json(db.PAYMENTS, [])
        tracking = new_tracking_number()
        tracking, start_text, end_text = SubscriptionService.append_records(
            username, plan_key, amount, subscriptions, payments, tracking)
        paths = (db.SUBSCRIPTIONS, db.PAYMENTS)
        snapshots = _snapshot_files(paths)
        try:
            db.save_json(db.SUBSCRIPTIONS, subscriptions)
            db.save_json(db.PAYMENTS, payments)
        except Exception:
            _restore_files(snapshots)
            raise
        print(f"Subscription created successfully: {start_text} to {end_text}. Tracking number: {tracking}")
        return True

class WalletService:
    @staticmethod
    def balance(username):
        return db.load_json(db.WALLETS, {}).get(username, 0)

    @staticmethod
    def _record(username, kind, amount, description, tracking=None):
        tracking = tracking or new_tracking_number()
        db.append_line(db.TRANSACTIONS, "|".join(
            [tracking, username, kind, str(amount), db.now_str(), description]))
        return tracking

    @staticmethod
    def transactions(username):
        keys = ("tracking", "username", "type", "amount", "date", "description")
        rows = []
        for line in db.read_lines(db.TRANSACTIONS):
            parts = line.split("|", 5)
            if len(parts) == 6 and parts[1] == username:
                rows.append(dict(zip(keys, parts)))
        return rows

    @staticmethod
    @db.log_action("wallet_charge")
    def charge(username, amount, card, exp_month, exp_year, bank_password, cvv2):
        user = find_user(username)
        if user is None or user.get("authority") != "gym_user" or user.get("active_status") is not True:
            print("Only active members can charge a wallet.")
            return False
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            print("Amount must be a positive whole number.")
            return False
        try:
            bank_gateway.pay(card, exp_month, exp_year, bank_password, cvv2, amount)
        except (ValueError, TypeError):
            print("Card validation failed. Your wallet was not charged.")
            return False
        wallets = db.load_json(db.WALLETS, {})
        wallets[username] = wallets.get(username, 0) + amount
        paths = (db.WALLETS, db.TRANSACTIONS)
        snapshots = _snapshot_files(paths)
        try:
            db.save_json(db.WALLETS, wallets)
            tracking = WalletService._record(username, "charge", amount, "Wallet top-up by card")
        except Exception:
            _restore_files(snapshots)
            raise
        print(f"Wallet charged with {amount}. Tracking number: {tracking}")
        return True

    @staticmethod
    @db.log_action("buy_subscription")
    def buy_subscription(username, plan_key):
        plan = PLANS.get(plan_key)
        user = find_user(username)
        if plan is None or user is None or user.get("authority") != "gym_user" or user.get("active_status") is not True:
            print("Invalid plan or inactive member.")
            return False

        wallets = db.load_json(db.WALLETS, {})
        balance = wallets.get(username, 0)
        if balance < plan["price"]:
            print(f"Insufficient balance. Price: {plan['price']}, your balance: {balance}.")
            return False

        subscriptions = db.load_json(db.SUBSCRIPTIONS, [])
        payments = db.load_json(db.PAYMENTS, [])
        tracking = new_tracking_number()
        tracking, start_text, end_text = SubscriptionService.append_records(
            username, plan_key, plan["price"], subscriptions, payments, tracking)
        renewing = SubscriptionService.status(username)[0] == "active"
        wallets[username] = balance - plan["price"]

        paths = (db.SUBSCRIPTIONS, db.PAYMENTS, db.TRANSACTIONS, db.WALLETS)
        snapshots = _snapshot_files(paths)
        try:
            db.save_json(db.SUBSCRIPTIONS, subscriptions)
            db.save_json(db.PAYMENTS, payments)
            WalletService._record(username, "payment", plan["price"],
                                  f"{'Renewal' if renewing else 'Purchase'} of {plan_key} subscription", tracking)
            db.save_json(db.WALLETS, wallets)
        except Exception:
            _restore_files(snapshots)
            raise

        print(f"Subscription {'renewed' if renewing else 'created'}: {start_text} to {end_text}.")
        print(f"Tracking number: {tracking}. New balance: {wallets[username]}")
        return True

class EnrollmentService:
    @staticmethod
    def active_for_class(title, enrollments=None):
        if enrollments is None:
            enrollments = db.load_json(db.ENROLLMENTS, [])
        active_members = {u.get("username") for u in db.load_json(db.USERS, [])
                          if u.get("authority") == "gym_user" and u.get("active_status") is True}
        return [e for e in enrollments if e.get("class_title") == title
                and e.get("status") == "active" and e.get("member_username") in active_members]

    @staticmethod
    def active_for_member(username):
        user = find_user(username)
        if user is None or user.get("authority") != "gym_user" or user.get("active_status") is not True:
            return []
        return [e for e in db.load_json(db.ENROLLMENTS, [])
                if e.get("member_username") == username and e.get("status") == "active"]

    @staticmethod
    def remaining(gym_class):
        return gym_class.get("capacity", 0) - len(EnrollmentService.active_for_class(gym_class.get("title")))

    @staticmethod
    @db.log_action("enroll")
    def enroll(username, title):
        if SubscriptionService.status(username)[0] != "active":
            print("You need an active subscription to enroll in a class.")
            return False
        gym_class = find_class(title)
        if gym_class is None:
            print("Class not found.")
            return False
        if gym_class.get("class_status") is not True:
            print("This class is inactive and cannot be joined.")
            return False
        user = find_user(username)
        coach = find_user(gym_class.get("coach"))
        hall = next((h for h in db.load_json(db.HALLS, []) if h.get("name") == gym_class.get("sport_hall")), None)
        if user is None or user.get("authority") != "gym_user" or user.get("active_status") is not True:
            print("Only active members can enroll.")
            return False
        if coach is None or coach.get("authority") != "coach" or coach.get("active_status") is not True:
            print("This class's coach is inactive.")
            return False
        if hall is None or hall.get("hall_status") is not True:
            print("This class's hall is inactive.")
            return False

        enrollments = db.load_json(db.ENROLLMENTS, [])
        if any(e.get("member_username") == username for e in EnrollmentService.active_for_class(title, enrollments)):
            print("You are already enrolled in this class.")
            return False
        if gym_class.get("capacity", 0) - len(EnrollmentService.active_for_class(title, enrollments)) <= 0:
            print("This class is full.")
            return False

        tracking = new_tracking_number()
        enrollments.append({
            "tracking_number": tracking, "class_title": title, "member_username": username,
            "enrolled_date": date.today().strftime(DATE_FMT), "status": "active",
        })
        db.save_json(db.ENROLLMENTS, enrollments)
        print(f"Enrolled in '{title}'. Tracking number: {tracking}")
        return True

    @staticmethod
    @db.log_action("withdraw")
    def withdraw(username, title):
        enrollments = db.load_json(db.ENROLLMENTS, [])
        record = next((e for e in enrollments if e.get("member_username") == username
                       and e.get("class_title") == title and e.get("status") == "active"), None)
        if record is None:
            print("You have no active enrollment in that class.")
            return False
        record["status"] = "inactive"
        record["withdrawn_date"] = date.today().strftime(DATE_FMT)
        db.save_json(db.ENROLLMENTS, enrollments)
        print(f"You have withdrawn from '{title}'.")
        return True

class WorkoutService:
    @staticmethod
    def _find(plans, title, member_username):
        return next((p for p in plans if p.get("class_title") == title
                     and p.get("member_username") == member_username), None)

    @staticmethod
    def get_plan(title, member_username):
        return WorkoutService._find(db.load_json(db.WORKOUTS, []), title, member_username)

    @staticmethod
    def plans_for_member(member_username):
        active_titles = {e.get("class_title") for e in EnrollmentService.active_for_member(member_username)}
        return [p for p in db.load_json(db.WORKOUTS, [])
                if p.get("member_username") == member_username and p.get("class_title") in active_titles]

    @staticmethod
    def can_edit(coach_username, title, member_username):
        gym_class = find_class(title)
        coach = find_user(coach_username)
        if (gym_class is None or gym_class.get("coach") != coach_username
                or gym_class.get("class_status") is not True
                or coach is None or coach.get("active_status") is not True):
            return False
        return any(e.get("member_username") == member_username
                   for e in EnrollmentService.active_for_class(title))

    @staticmethod
    def _valid(exercise):
        return (bool(str(exercise.get("name", "")).strip())
                and isinstance(exercise.get("sets"), int) and exercise["sets"] > 0
                and isinstance(exercise.get("reps"), int) and exercise["reps"] > 0
                and isinstance(exercise.get("rest_seconds"), int) and exercise["rest_seconds"] >= 0)

    @staticmethod
    @db.log_action("workout_add")
    def add_exercise(coach_username, title, member_username, exercise):
        if not WorkoutService.can_edit(coach_username, title, member_username):
            print("You can only manage plans for members of your own classes.")
            return False
        if not WorkoutService._valid(exercise):
            print("Invalid exercise data (sets and reps must be greater than zero).")
            return False
        plans = db.load_json(db.WORKOUTS, [])
        plan = WorkoutService._find(plans, title, member_username)
        if plan is None:
            plan = {"class_title": title, "member_username": member_username,
                    "coach": coach_username, "exercises": []}
            plans.append(plan)
        plan["exercises"].append(exercise)
        db.save_json(db.WORKOUTS, plans)
        print("Exercise added.")
        return True

    @staticmethod
    @db.log_action("workout_edit")
    def update_exercise(coach_username, title, member_username, index, field, value):
        if not WorkoutService.can_edit(coach_username, title, member_username):
            print("You can only manage plans for members of your own classes.")
            return False
        plans = db.load_json(db.WORKOUTS, [])
        plan = WorkoutService._find(plans, title, member_username)
        if plan is None or not 0 <= index < len(plan["exercises"]):
            print("Exercise not found.")
            return False
        updated = dict(plan["exercises"][index], **{field: value})
        if not WorkoutService._valid(updated):
            print("Invalid exercise data (sets and reps must be greater than zero).")
            return False
        plan["exercises"][index] = updated
        db.save_json(db.WORKOUTS, plans)
        print("Exercise updated.")
        return True

    @staticmethod
    def print_exercises(exercises):
        if not exercises:
            print("  (no exercises yet)")
        for number, ex in enumerate(exercises, 1):
            print(f"  {number}. {ex['name']} - {ex['sets']} sets x {ex['reps']} reps, "
                  f"rest {ex['rest_seconds']}s")
            if ex.get("description"):
                print(f"     Note: {ex['description']}")
