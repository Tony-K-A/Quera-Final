from login_utils.login import *
from manage_utils.manage import Manage


# User selection in match. Authority is adjusted to the type of user.

while True:

    show_menu_login()

    choice = int(input())

    if choice == 1:
        auth = "manager"
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        if not login(username, password, auth):
            print("\nWrong inputs. Try again.\n")

        else:
            print("\nLogged in as manager. \n")
            
            while True:
                Manage.show_panel()

                option = int(input("Enter your desired option: "))

                if option == 1:
                    m = Manage()
                    show_manager_user_options()
                    user_option = int(input())

                    if user_option == 1:
                        authority = input("Enter user authority: ").strip()
                        name = input("Enter user name: ")
                        usernam = input("Enter username: ").strip()
                        passwor = input("Enter password: ").strip()
                        email = input("Enter user e-mail: ").strip()

                        if authority not in ["coach", "gym_user"]:
                            print("Invalid Authority! ")
                        else:
                            m.add_member()
                        

                    elif user_option == 2:
                        pass

                    elif user_option == 3:
                        m.show_user_info()
                elif option == 2:
                    pass

                elif option == 3:
                    pass

                elif option == 4:
                    pass

                elif option == 5:
                    pass

                elif option == 6:
                    break
            

    elif choice == 2:
        pass

    elif choice == 3:
        pass

    elif choice == 4:
        break

