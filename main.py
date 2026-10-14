import login_utils.login as log
from login_utils.login import login
from manage_utils.manage import Manage

"""
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
        m = Manage()

# Create subscription
        m.create_subscription("TC140", "3-month", 1500000)

# View payments
        m.show_payments()

# View status of all members
        m.show_subscription_status()

# View status of one member
        m.show_subscription_status("ali123")

# Reports
        m.show_reports()