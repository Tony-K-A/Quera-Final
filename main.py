import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

import seed_data


def _valid_input(check, value):
    if check is None:
        return bool(value)
    if hasattr(check, "fullma2tch"):
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
from admin_panel import AdminPanel
from auth import Authenticator
from coach_panel import CoachPanel
from member_panel import MemberPanel
from storage import DataError

ROLES = [
    ("admin", "Manager", AdminPanel),
    ("coach", "Coach", CoachPanel),
    ("member", "Member", MemberPanel),
]

def main():
    try:
        seed_data.ensure_data_files()
    except DataError as error:
        print(f"Error: {error}")
        return

    while True:
        index = choose("\n===== Gym Management System =====",
                          ["Manager login", "Coach login", "Member login"],
                          back_label="Exit", back_last=True)
        if index is None:
            print("Goodbye!")
            return
        role, label, panel_class = ROLES[index]
        try:
            user = Authenticator.login(role, label)
            if user is not None:
                panel_class(user).run()
        except (DataError, OSError) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed. All saved data is kept.")
