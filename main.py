import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

import seed_data
import ui
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
        index = ui.choose("\n===== Gym Management System =====",
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
