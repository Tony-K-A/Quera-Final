import login_utils.login as log
from login_utils.login import login
from manage_utils.manage import Manage


log.show_menu()

login_choice = int(input())

# User selection in match. Authority is adjusted to the type of user.

match login_choice: 

    case 1:
        authority = "manager"
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login(username, password, authority):
                print(f"Wellcome {authority}!\nLogged in successfully!")
                break
            print("Not logged in! Try again")
    case 2:
        authority = "coach"
    case 3:
        authority = "gym_user"
    case 4:
        exit()
"""
authority = 'manager'
match authority:
    case "manager":
        manager = Manage()

        manager.show_panel()

   """     
