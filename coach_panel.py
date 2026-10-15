import storage as db
import services as svc
import ui
import validators as v

class CoachPanel:
    def __init__(self, coach):
        self.coach = coach
        self.username = coach["username"]

    def run(self):
        actions = [self.view_classes, self.manage_plans]
        while True:
            index = ui.choose(f"\n=== Coach panel ({self.coach['name']}) ===",
                              ["View my classes", "Manage members' workout plans"],
                              back_label="Logout", back_last=True)
            if index is None:
                print("Logged out.")
                return
            actions[index]()

    def _my_classes(self):
        coach = svc.find_user(self.username)
        if coach is None or coach.get("active_status") is not True:
            return []
        return [c for c in db.load_json(db.CLASSES, [])
                if c.get("coach") == self.username and c.get("class_status") is True]

    def view_classes(self):
        classes = self._my_classes()
        if not classes:
            print("You have no classes assigned.")
        for gym_class in classes:
            svc.print_class(gym_class, show_members=True)

    def manage_plans(self):
        classes = self._my_classes()
        class_index = ui.choose("Select one of your classes:", [c["title"] for c in classes])
        if class_index is None:
            return
        title = classes[class_index]["title"]

        enrolled = svc.EnrollmentService.active_for_class(title)
        if not enrolled:
            print("No members are enrolled in this class yet.")
            return
        names = {u["username"]: u["name"] for u in db.load_json(db.USERS, [])}
        member_index = ui.choose("Select a member:", [
            f"{names.get(e['member_username'], '?')} ({e['member_username']})" for e in enrolled])
        if member_index is None:
            return
        self._plan_menu(title, enrolled[member_index]["member_username"])

    def _plan_menu(self, title, member):
        names = {u.get("username"): u.get("name", u.get("username")) for u in db.load_json(db.USERS, [])}
        member_label = f"{names.get(member, member)} ({member})"
        while True:
            index = ui.choose(f"\n-- Plan for {member_label} in '{title}' --",
                              ["View plan", "Add exercise", "Edit exercise"])
            if index is None:
                return
            if index == 0:
                self._show_plan(title, member)
            elif index == 1:
                exercise = self._ask_exercise()
                if exercise:
                    svc.WorkoutService.add_exercise(self.username, title, member, exercise)
            else:
                self._edit_exercise(title, member)

    def _show_plan(self, title, member):
        plan = svc.WorkoutService.get_plan(title, member)
        svc.WorkoutService.print_exercises(plan["exercises"] if plan else [])

    def _ask_exercise(self):
        name = ui.ask("Exercise name", lambda t: 1 <= len(t) <= 50, "Use 1-50 characters.")
        if name is None:
            return None
        sets = ui.ask_int("Number of sets", error="Sets must be a whole number greater than zero.")
        if sets is None:
            return None
        reps = ui.ask_int("Number of reps", error="Reps must be a whole number greater than zero.")
        if reps is None:
            return None
        rest = ui.ask_int("Rest time in seconds", v.NON_NEGATIVE_INT_RE,
                          "Enter 0 or a positive whole number.")
        if rest is None:
            return None
        description = ui.ask("Description (optional, press Enter to skip)",
                             lambda t: len(t) <= 200, "Use at most 200 characters.", allow_empty=True)
        if description is None:
            return None
        return {"name": name, "sets": sets, "reps": reps, "rest_seconds": rest, "description": description}

    def _edit_exercise(self, title, member):
        plan = svc.WorkoutService.get_plan(title, member)
        if not plan or not plan["exercises"]:
            print("This member has no exercises yet. Add one first.")
            return
        ex_index = ui.choose("Which exercise?", [e["name"] for e in plan["exercises"]])
        if ex_index is None:
            return
        fields = ["name", "sets", "reps", "rest_seconds", "description"]
        field_index = ui.choose("Which field?", ["Name", "Sets", "Reps", "Rest time (seconds)", "Description"])
        if field_index is None:
            return
        field = fields[field_index]
        if field == "name":
            value = ui.ask("New name", lambda t: 1 <= len(t) <= 50, "Use 1-50 characters.")
        elif field in ("sets", "reps"):
            value = ui.ask_int(f"New {field}", error=f"{field.capitalize()} must be greater than zero.")
        elif field == "rest_seconds":
            value = ui.ask_int("New rest time in seconds", v.NON_NEGATIVE_INT_RE,
                               "Enter 0 or a positive whole number.")
        else:
            value = ui.ask("New description", lambda t: len(t) <= 200, "Use at most 200 characters.",
                           allow_empty=True)
        if value is None:
            return
        svc.WorkoutService.update_exercise(self.username, title, member, ex_index, field, value)
