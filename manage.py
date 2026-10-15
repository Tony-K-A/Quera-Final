import re
from datetime import date

import storage as db
import services as svc
from password_security import hash_password

class Manage:
    CLASS_TYPES = {"gym", "crossfit", "fitness", "yoga"}

    @staticmethod
    def show_panel():
        print("1. Users management")
        print("2. Saloons management")
        print("3. Class management")
        print("4. Subscriptions and payments management")
        print("5. Show reports")
        print("6. Exit")

    @staticmethod
    def is_valid_password(password):
        return (isinstance(password, str) and len(password) >= 8 and not any(ch.isspace() for ch in password)
                and re.search(r"[A-Za-z]", password) and re.search(r"\d", password)
                and re.search(r"[@&]", password))

    @staticmethod
    def is_valid_email(email):
        if not isinstance(email, str) or email != email.strip() or len(email) > 254:
            return False
        if any(ch.isspace() for ch in email) or email.count("@") != 1:
            return False
        local, domain = email.split("@")
        if not local or len(local) > 64 or local.startswith(".") or local.endswith(".") or ".." in local:
            return False
        if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+", local):
            return False
        labels = domain.split(".")
        if len(labels) < 2 or any(not label or len(label) > 63 for label in labels):
            return False
        if any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", label) for label in labels):
            return False
        return len(labels[-1]) >= 2

    @staticmethod
    def _snapshot(paths):
        return {path: path.read_bytes() if path.exists() else None for path in paths}

    @staticmethod
    def _rollback(snapshots):
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
            raise db.DataError("Rollback failed: " + "; ".join(errors))

    def add_member(self, authority, name, username, password, email, active_status):
        if not self.is_valid_password(password):
            print("Invalid password. Use at least 8 characters, a letter, a digit and @ or &, without spaces.")
            return False
        if not self.is_valid_email(email):
            print("Invalid email address.")
            return False
        if authority not in ("coach", "gym_user"):
            print("Invalid authority.")
            return False
        users = db.load_json(db.USERS, [])
        if any(u.get("username", "").casefold() == username.casefold() for u in users):
            print(f"Username '{username}' already exists!")
            return False
        users.append({"name": name, "authority": authority, "username": username,
                      "password": hash_password(password), "email": email, "active_status": bool(active_status)})
        db.save_json(db.USERS, users)
        print("User added successfully!")
        return True

    def edit_member_info(self, section, amount, username):
        allowed = {"name", "password", "email", "active_status"}
        if section not in allowed:
            print("Invalid selection!")
            return False
        if section == "password" and not self.is_valid_password(amount):
            print("Invalid password. Use at least 8 characters, a letter, a digit and @ or &, without spaces.")
            return False
        if section == "email" and not self.is_valid_email(amount):
            print("Invalid email address.")
            return False
        users = db.load_json(db.USERS, [])
        user = next((u for u in users if u.get("username") == username), None)
        if user is None:
            print(f"User '{username}' not found.")
            return False
        was_active = user.get("active_status") is True
        user[section] = hash_password(amount) if section == "password" else amount
        if section == "active_status" and was_active and amount is False:
            snapshots = self._snapshot((db.USERS, db.CLASSES, db.ENROLLMENTS))
            try:
                if user.get("authority") == "coach":
                    classes = db.load_json(db.CLASSES, [])
                    affected_titles = set()
                    for gym_class in classes:
                        if gym_class.get("coach") == username:
                            gym_class["class_status"] = False
                            affected_titles.add(gym_class.get("title"))
                    db.save_json(db.CLASSES, classes)
                    enrollments = db.load_json(db.ENROLLMENTS, [])
                    for enrollment in enrollments:
                        if enrollment.get("class_title") in affected_titles and enrollment.get("status") == "active":
                            enrollment["status"] = "inactive"
                            enrollment["withdrawn_date"] = date.today().strftime("%Y-%m-%d")
                    db.save_json(db.ENROLLMENTS, enrollments)
                elif user.get("authority") == "gym_user":
                    enrollments = db.load_json(db.ENROLLMENTS, [])
                    for enrollment in enrollments:
                        if enrollment.get("member_username") == username and enrollment.get("status") == "active":
                            enrollment["status"] = "inactive"
                            enrollment["withdrawn_date"] = date.today().strftime("%Y-%m-%d")
                    db.save_json(db.ENROLLMENTS, enrollments)
                db.save_json(db.USERS, users)
            except Exception:
                self._rollback(snapshots)
                raise
        else:
            db.save_json(db.USERS, users)
        return True

    def add_hall(self, name, capacity, tools, hall_status):
        if isinstance(tools, str):
            tools = [tool.strip() for tool in tools.split(",") if tool.strip()]
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            print("Hall capacity must be a positive integer.")
            return False
        halls = db.load_json(db.HALLS, [])
        if any(h.get("name", "").casefold() == name.casefold() for h in halls):
            print("A hall with this name already exists.")
            return False
        halls.append({"name": name, "capacity": capacity, "tools": tools, "hall_status": bool(hall_status)})
        db.save_json(db.HALLS, halls)
        return True

    def edit_hall_info(self, name, choice, new_amount):
        if choice not in ("name", "capacity", "tools", "hall_status"):
            print("Invalid selection!")
            return False
        halls = db.load_json(db.HALLS, [])
        hall = next((h for h in halls if h.get("name") == name), None)
        if hall is None:
            print("Hall not found!")
            return False
        if choice == "capacity":
            if not isinstance(new_amount, int) or isinstance(new_amount, bool) or new_amount <= 0:
                print("Capacity must be a positive integer.")
                return False
            classes = db.load_json(db.CLASSES, [])
            needed = max((c.get("capacity", 0) for c in classes if c.get("sport_hall") == name), default=0)
            if new_amount < needed:
                print(f"Hall capacity cannot be below an assigned class capacity ({needed}).")
                return False
        if choice == "name":
            if any(h.get("name", "").casefold() == str(new_amount).casefold() and h is not hall for h in halls):
                print("A hall with this name already exists.")
                return False
            snapshots = self._snapshot((db.HALLS, db.CLASSES))
            try:
                hall["name"] = new_amount
                classes = db.load_json(db.CLASSES, [])
                for gym_class in classes:
                    if gym_class.get("sport_hall") == name:
                        gym_class["sport_hall"] = new_amount
                db.save_json(db.CLASSES, classes)
                db.save_json(db.HALLS, halls)
            except Exception:
                self._rollback(snapshots)
                raise
            return True
        if choice == "tools" and isinstance(new_amount, str):
            new_amount = [tool.strip() for tool in new_amount.split(",") if tool.strip()]
        if choice == "hall_status" and new_amount is False:
            snapshots = self._snapshot((db.HALLS, db.CLASSES, db.ENROLLMENTS))
            try:
                hall[choice] = new_amount
                classes = db.load_json(db.CLASSES, [])
                affected_titles = set()
                for gym_class in classes:
                    if gym_class.get("sport_hall") == name:
                        gym_class["class_status"] = False
                        affected_titles.add(gym_class.get("title"))
                enrollments = db.load_json(db.ENROLLMENTS, [])
                for enrollment in enrollments:
                    if enrollment.get("class_title") in affected_titles and enrollment.get("status") == "active":
                        enrollment["status"] = "inactive"
                        enrollment["withdrawn_date"] = date.today().strftime("%Y-%m-%d")
                db.save_json(db.CLASSES, classes)
                db.save_json(db.ENROLLMENTS, enrollments)
                db.save_json(db.HALLS, halls)
            except Exception:
                self._rollback(snapshots)
                raise
            return True
        hall[choice] = new_amount
        db.save_json(db.HALLS, halls)
        return True

    @staticmethod
    def _class_conflicts(candidate, classes, ignore_title=None):
        for other in classes:
            if other.get("title") == ignore_title:
                continue
            if other.get("class_date") != candidate.get("class_date") or other.get("class_time") != candidate.get("class_time"):
                continue
            if other.get("class_status") is not True:
                continue
            if other.get("sport_hall") == candidate.get("sport_hall"):
                return "Another active class already uses this hall at that time."
            if other.get("coach") == candidate.get("coach"):
                return "This coach already has another active class at that time."
        return None

    def add_class(self, name, class_type, coach_user, hall, day, time, capacity, status):
        if class_type not in self.CLASS_TYPES:
            print("Mentioned class type is not valid!")
            return False
        classes = db.load_json(db.CLASSES, [])
        halls = db.load_json(db.HALLS, [])
        users = db.load_json(db.USERS, [])
        selected_hall = next((h for h in halls if h.get("name") == hall and h.get("hall_status") is True), None)
        coach = next((u for u in users if u.get("username") == coach_user and u.get("authority") == "coach" and u.get("active_status") is True), None)
        if not selected_hall:
            print("Hall not found or inactive.")
            return False
        if not coach:
            print("Coach not found or inactive.")
            return False
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0 or capacity > selected_hall.get("capacity", 0):
            print("Class capacity must be positive and fit the hall.")
            return False
        if any(c.get("title", "").casefold() == name.casefold() for c in classes):
            print("A class with this title already exists.")
            return False
        candidate = {"title": name, "class_type": class_type, "coach": coach_user, "sport_hall": hall,
                     "class_date": day, "class_time": time, "capacity": capacity,
                     "class_status": bool(status)}
        conflict = self._class_conflicts(candidate, classes)
        if conflict:
            print(conflict)
            return False
        classes.append(candidate)
        db.save_json(db.CLASSES, classes)
        return True

    def edit_class_info(self, name, edit_item, item_value):
        allowed = {"title", "class_type", "coach", "sport_hall", "class_date", "class_time", "capacity", "class_status"}
        if edit_item not in allowed:
            print("Invalid item to edit!")
            return False
        classes = db.load_json(db.CLASSES, [])
        target = next((c for c in classes if c.get("title") == name), None)
        if target is None:
            print("Class not found!")
            return False
        candidate = dict(target)
        candidate[edit_item] = item_value
        if edit_item == "title" and any(c.get("title", "").casefold() == str(item_value).casefold() and c is not target for c in classes):
            print("A class with this title already exists.")
            return False
        if edit_item == "class_type" and item_value not in self.CLASS_TYPES:
            print("Mentioned class type is not valid!")
            return False
        if edit_item == "coach":
            coach = next((u for u in db.load_json(db.USERS, []) if u.get("username") == item_value and u.get("authority") == "coach" and u.get("active_status") is True), None)
            if not coach:
                print("Coach not found or inactive.")
                return False
        if edit_item == "sport_hall":
            hall = next((h for h in db.load_json(db.HALLS, []) if h.get("name") == item_value and h.get("hall_status") is True), None)
            if not hall:
                print("Hall not found or inactive.")
                return False
            if candidate.get("capacity", 0) > hall.get("capacity", 0):
                print("Class capacity exceeds hall capacity!")
                return False
        if edit_item == "capacity":
            if not isinstance(item_value, int) or isinstance(item_value, bool) or item_value <= 0:
                print("Capacity must be a positive integer!")
                return False
            hall = next((h for h in db.load_json(db.HALLS, []) if h.get("name") == candidate.get("sport_hall")), None)
            enrolled = len(svc.EnrollmentService.active_for_class(name))
            if hall is None or item_value > hall.get("capacity", 0) or item_value < enrolled:
                print("Capacity must fit the hall and current active enrollment count.")
                return False
        if edit_item == "class_status" and type(item_value) is not bool:
            print("Class status must be True or False!")
            return False
        if candidate.get("class_status") is True:
            coach = next((u for u in db.load_json(db.USERS, []) if u.get("username") == candidate.get("coach") and u.get("authority") == "coach" and u.get("active_status") is True), None)
            hall = next((h for h in db.load_json(db.HALLS, []) if h.get("name") == candidate.get("sport_hall") and h.get("hall_status") is True), None)
            if coach is None or hall is None:
                print("A class cannot be active unless its coach and hall are active.")
                return False
            conflict = self._class_conflicts(candidate, classes, ignore_title=name)
            if conflict:
                print(conflict)
                return False
        if edit_item == "title" and item_value != name:
            snapshots = self._snapshot((db.CLASSES, db.ENROLLMENTS, db.WORKOUTS))
            try:
                target["title"] = item_value
                enrollments = db.load_json(db.ENROLLMENTS, [])
                workouts = db.load_json(db.WORKOUTS, [])
                for record in enrollments + workouts:
                    if record.get("class_title") == name:
                        record["class_title"] = item_value
                db.save_json(db.ENROLLMENTS, enrollments)
                db.save_json(db.WORKOUTS, workouts)
                db.save_json(db.CLASSES, classes)
            except Exception:
                self._rollback(snapshots)
                raise
            return True
        target[edit_item] = item_value
        db.save_json(db.CLASSES, classes)
        return True

    def create_subscription(self, member_username, sub_type, amount):
        return svc.SubscriptionService.create_admin_subscription(member_username, sub_type, amount)

    def show_hall_info(self):
        halls = db.load_json(db.HALLS, [])
        if not halls:
            print("No halls found.")
            return False
        for hall in halls:
            print(f"Name: {hall.get('name')} | Capacity: {hall.get('capacity')} | Status: {'active' if hall.get('hall_status') else 'inactive'}")
        return True

    def show_payments(self):
        payments = db.load_json(db.PAYMENTS, [])
        if not payments:
            print("No payments recorded.")
            return False
        for payment in payments:
            print(f"Member: {payment.get('member_name')} ({payment.get('member_username')})")
            print(f"Subscription: {payment.get('sub_type')} | Amount: {payment.get('amount')}")
            print(f"Payment date: {payment.get('payment_date')} | Tracking: {payment.get('tracking_number')}")
            print("-" * 50)
        return True

    def show_reports(self):
        users = db.load_json(db.USERS, [])
        classes = db.load_json(db.CLASSES, [])
        payments = db.load_json(db.PAYMENTS, [])
        print("\n========== Gym Reports ==========")
        print(f"Active members: {sum(1 for u in users if u.get('authority') == 'gym_user' and u.get('active_status') is True)}")
        print(f"Active coaches: {sum(1 for u in users if u.get('authority') == 'coach' and u.get('active_status') is True)}")
        print(f"Active classes: {sum(1 for c in classes if c.get('class_status') is True)}")
        print(f"Total payments: {len(payments)}")
        print(f"Total revenue: {sum(float(p.get('amount', 0)) for p in payments)}")
        return True
