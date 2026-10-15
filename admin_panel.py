import storage as db
import services as svc
import ui
import validators as v
from manage import Manage

CLASS_TYPES = ["gym", "crossfit", "fitness", "yoga"]
WEEKDAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
ROLE_LABEL = {"coach": "Coach", "gym_user": "Member"}

class AdminPanel:
    def __init__(self, admin):
        self.admin = admin
        self.manage = Manage()

    def run(self):
        actions = {
            "1": self.users_menu,
            "2": self.halls_menu,
            "3": self.classes_menu,
            "4": self.subscriptions_menu,
            "5": self.manage.show_reports,
        }
        while True:
            print(f"\n=== Manager panel ({self.admin['name']}) ===")
            Manage.show_panel()
            choice = input("Choice: ").strip()
            if choice == "6":
                print("Logged out.")
                return
            action = actions.get(choice)
            if action is None:
                print("Invalid choice, try again.")
                continue
            action()

    def users_menu(self):
        actions = [self.add_user, self.edit_user, self.toggle_user, self.view_users]
        while True:
            index = ui.choose("\n-- Users management --",
                              ["Add user", "Edit user", "Activate / deactivate user", "View users"])
            if index is None:
                return
            actions[index]()

    def _ask_existing_user(self):
        while True:
            username = ui.ask("Username")
            if username is None:
                return None
            user = svc.find_user(username)
            if user and user.get("authority") in ROLE_LABEL:
                return user
            print("No coach or member with that username.")

    def _ask_new_username(self):
        while True:
            username = ui.ask("Username", v.USERNAME_RE, v.USERNAME_ERROR)
            if username is None:
                return None
            if svc.find_user(username):
                print("This username is already taken.")
                continue
            return username

    def add_user(self):
        role = ui.choose("User type:", ["Coach", "Member"])
        if role is None:
            return
        name = ui.ask("Full name", v.NAME_RE, v.NAME_ERROR)
        if name is None:
            return
        username = self._ask_new_username()
        if username is None:
            return
        password = ui.ask("Password (needs a letter, a digit and @ or &)", Manage.is_valid_password,
                          "Password must contain an English letter, a digit and one of @ or &.")
        if password is None:
            return
        email = ui.ask("Email", Manage.is_valid_email, "Email must look like name@domain.com.")
        if email is None:
            return
        active = ui.choose_bool("Account status:")
        if active is None:
            return
        authority = ["coach", "gym_user"][role]
        self.manage.add_member(authority, name, username, password, email, active)

    def edit_user(self):
        user = self._ask_existing_user()
        if user is None:
            return
        field = ui.choose("Which field do you want to edit?", ["Name", "Password", "Email"])
        if field is None:
            return
        fields = [
            ("name", "New name", v.NAME_RE, v.NAME_ERROR),
            ("password", "New password", Manage.is_valid_password,
             "Password must contain an English letter, a digit and one of @ or &."),
            ("email", "New email", Manage.is_valid_email,
             "Email must look like name@domain.com."),
        ]
        section, prompt, check, error = fields[field]
        value = ui.ask(prompt, check, error)
        if value is None:
            return
        if self.manage.edit_member_info(section, value, user["username"]):
            print("User updated.")

    def toggle_user(self):
        user = self._ask_existing_user()
        if user is None:
            return
        active = ui.choose_bool("New account status:")
        if active is None:
            return
        if self.manage.edit_member_info("active_status", active, user["username"]):
            print(f"Account is now {'active' if active else 'inactive'}. No data was deleted.")

    def view_users(self):
        users = [u for u in db.load_json(db.USERS, []) if u.get("authority") in ROLE_LABEL]
        if not users:
            print("No users yet.")
        for user in users:
            print(f"Name     : {user.get('name')}")
            print(f"Username : {user.get('username')}")
            print(f"Role     : {ROLE_LABEL[user['authority']]}")
            print(f"Email    : {user.get('email')}")
            print(f"Status   : {'active' if user.get('active_status') is True else 'inactive'}")
            print("-" * 50)

    def halls_menu(self):
        actions = [self.add_hall, self.edit_hall, self.toggle_hall, self.manage.show_hall_info]
        while True:
            index = ui.choose("\n-- Halls management --",
                              ["Add hall", "Edit hall", "Activate / deactivate hall", "View halls"])
            if index is None:
                return
            actions[index]()

    def _choose_hall(self, title="Select a hall:", active_only=False):
        halls = [h for h in db.load_json(db.HALLS, [])
                 if not active_only or h.get("hall_status") is True]
        index = ui.choose(title, [f"{h['name']} (capacity {h['capacity']})" for h in halls])
        return None if index is None else halls[index]

    def _ask_new_hall_name(self):
        halls = db.load_json(db.HALLS, [])
        while True:
            name = ui.ask("Hall name", v.NAME_RE, v.NAME_ERROR)
            if name is None:
                return None
            if any(h["name"].lower() == name.lower() for h in halls):
                print("A hall with this name already exists.")
                continue
            return name

    def add_hall(self):
        name = self._ask_new_hall_name()
        if name is None:
            return
        capacity = ui.ask_int("Capacity")
        if capacity is None:
            return
        tools = ui.ask("Equipment (comma separated, e.g. treadmill, dumbbell, bike)", v.TOOLS_RE,
                       "Enter names separated by commas.")
        if tools is None:
            return
        active = ui.choose_bool("Hall status:")
        if active is None:
            return
        if self.manage.add_hall(name, capacity, tools, active):
            print("Hall added.")

    def edit_hall(self):
        hall = self._choose_hall()
        if hall is None:
            return
        field = ui.choose("Which field do you want to edit?", ["Name", "Capacity", "Equipment"])
        if field is None:
            return
        old_name = hall["name"]
        if field == 0:
            new_name = self._ask_new_hall_name()
            if new_name is None:
                return
            if self.manage.edit_hall_info(old_name, "name", new_name) is not False:
                print("Hall updated.")
        elif field == 1:
            classes = db.load_json(db.CLASSES, [])
            needed = max((c["capacity"] for c in classes if c.get("sport_hall") == old_name), default=1)
            while True:
                capacity = ui.ask_int("New capacity")
                if capacity is None:
                    return
                if capacity < needed:
                    print(f"A class in this hall needs capacity {needed}.")
                    continue
                break
            if self.manage.edit_hall_info(old_name, "capacity", capacity) is not False:
                print("Hall updated.")
        else:
            tools = ui.ask("New equipment (comma separated)", v.TOOLS_RE, "Enter names separated by commas.")
            if tools is None:
                return
            if self.manage.edit_hall_info(old_name, "tools", tools) is not False:
                print("Hall updated.")

    def toggle_hall(self):
        hall = self._choose_hall()
        if hall is None:
            return
        active = ui.choose_bool("New hall status:")
        if active is None:
            return
        if self.manage.edit_hall_info(hall["name"], "hall_status", active):
            print(f"Hall is now {'active' if active else 'inactive'}.")

    def classes_menu(self):
        actions = [self.add_class, self.edit_class, self.toggle_class, self.view_classes]
        while True:
            index = ui.choose("\n-- Classes management --",
                              ["Create class", "Edit class", "Activate / deactivate class", "View classes"])
            if index is None:
                return
            actions[index]()

    def _choose_class(self):
        classes = db.load_json(db.CLASSES, [])
        index = ui.choose("Select a class:", [c["title"] for c in classes])
        return None if index is None else classes[index]

    def _ask_new_class_title(self):
        classes = db.load_json(db.CLASSES, [])
        while True:
            title = ui.ask("Class title", v.NAME_RE, v.NAME_ERROR)
            if title is None:
                return None
            if any(c["title"].lower() == title.lower() for c in classes):
                print("A class with this title already exists.")
                continue
            return title

    def _choose_coach(self):
        coaches = svc.users_by_role("coach", active_only=True)
        index = ui.choose("Coach:", [f"{c['name']} ({c['username']})" for c in coaches])
        return None if index is None else coaches[index]["username"]

    def add_class(self):
        if not svc.users_by_role("coach", active_only=True):
            print("There is no active coach. Add a coach first.")
            return
        if not any(h.get("hall_status") is True for h in db.load_json(db.HALLS, [])):
            print("There is no active hall. Add a hall first.")
            return
        title = self._ask_new_class_title()
        if title is None:
            return
        type_index = ui.choose("Sport type:", CLASS_TYPES)
        if type_index is None:
            return
        coach = self._choose_coach()
        if coach is None:
            return
        hall = self._choose_hall("Hall:", active_only=True)
        if hall is None:
            return
        day_index = ui.choose("Day:", WEEKDAYS)
        if day_index is None:
            return
        time = ui.ask("Time (HH:MM, 24-hour)", v.TIME_RE, "Use 24-hour HH:MM, e.g. 18:30.")
        if time is None:
            return
        while True:
            capacity = ui.ask_int("Capacity")
            if capacity is None:
                return
            if capacity > hall["capacity"]:
                print(f"The hall holds only {hall['capacity']} people.")
                continue
            break
        if self.manage.add_class(title, CLASS_TYPES[type_index], coach, hall["name"],
                                 WEEKDAYS[day_index], time, capacity, True):
            print("Class created.")

    def edit_class(self):
        gym_class = self._choose_class()
        if gym_class is None:
            return
        title = gym_class["title"]
        field = ui.choose("Which field do you want to edit?",
                          ["Title", "Sport type", "Coach", "Hall", "Day", "Time", "Capacity"])
        if field is None:
            return
        pair = self._ask_class_value(field, gym_class)
        if pair is None:
            return
        key, value = pair
        if self.manage.edit_class_info(title, key, value):
            print("Class updated.")

    def _ask_class_value(self, field, gym_class):

        if field == 0:
            value = self._ask_new_class_title()
            return None if value is None else ("title", value)
        if field == 1:
            index = ui.choose("Sport type:", CLASS_TYPES)
            return None if index is None else ("class_type", CLASS_TYPES[index])
        if field == 2:
            value = self._choose_coach()
            return None if value is None else ("coach", value)
        if field == 3:
            hall = self._choose_hall("Hall:", active_only=True)
            return None if hall is None else ("sport_hall", hall["name"])
        if field == 4:
            index = ui.choose("Day:", WEEKDAYS)
            return None if index is None else ("class_date", WEEKDAYS[index])
        if field == 5:
            value = ui.ask("New time (HH:MM, 24-hour)", v.TIME_RE, "Use 24-hour HH:MM, e.g. 18:30.")
            return None if value is None else ("class_time", value)
        enrolled = len(svc.EnrollmentService.active_for_class(gym_class["title"]))
        while True:
            capacity = ui.ask_int("New capacity")
            if capacity is None:
                return None
            if capacity < enrolled:
                print(f"{enrolled} members are already enrolled.")
                continue
            return "capacity", capacity

    def toggle_class(self):
        gym_class = self._choose_class()
        if gym_class is None:
            return
        active = ui.choose_bool("New class status:")
        if active is None:
            return
        if self.manage.edit_class_info(gym_class["title"], "class_status", active):
            print(f"Class is now {'active' if active else 'inactive'}.")

    def view_classes(self):
        classes = db.load_json(db.CLASSES, [])
        if not classes:
            print("No classes yet.")
        for gym_class in classes:
            svc.print_class(gym_class)

    def subscriptions_menu(self):
        actions = [self.create_subscription, self.manage.show_payments, self.view_subscription_status]
        while True:
            index = ui.choose("\n-- Subscriptions and payments --",
                              ["Create subscription for a member", "View payments",
                               "View members' subscription status"])
            if index is None:
                return
            actions[index]()

    def create_subscription(self):
        members = svc.users_by_role("gym_user", active_only=True)
        member_index = ui.choose("Member:", [f"{m['name']} ({m['username']})" for m in members])
        if member_index is None:
            return
        keys = list(svc.PLANS)
        plan_index = ui.choose("Plan:", [f"{k} (standard price {svc.PLANS[k]['price']})" for k in keys])
        if plan_index is None:
            return
        amount = ui.ask_int("Amount paid")
        if amount is None:
            return
        self.manage.create_subscription(members[member_index]["username"], keys[plan_index], amount)

    def view_subscription_status(self):
        members = svc.users_by_role("gym_user")
        if not members:
            print("No members yet.")
        for member in members:
            print(f"Name     : {member['name']}")
            print(f"Username : {member['username']}")
            svc.SubscriptionService.print_status(member)
            print("-" * 50)
