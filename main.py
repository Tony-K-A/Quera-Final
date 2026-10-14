from manage_utils.manage import Manage
from login_utils.login import *

while True:

    show_menu_login()

    try:
        choice = int(input("Enter your choice: ").strip())
    except ValueError:
        print("\nPlease enter a valid number!\n")
        continue

    # Manager login section

    if choice == 1:
        auth = "manager"
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        if not login(username, password, auth):
            print("\nWrong inputs. Try again.\n")
            returning = input("Enter 0 to return to the main menu. Enter 1 to try again: ").strip()
            if returning == "1":
                continue
            else:
                break

        else:
            print("\nLogged in as manager.\n")
            m = Manage()

            while True:
                Manage.show_panel()

                try:
                    option = int(input("Enter your desired option: ").strip())
                except ValueError:
                    print("\nPlease enter a valid number!\n")
                    continue

                # User management section

                if option == 1:
                    while True:

                        show_manager_user_options()

                        try:
                            user_option = int(input("Enter your choice: ").strip())
                        except ValueError:
                            print("\nPlease enter a valid number!\n")
                            continue

                        if user_option == 1:

                            # Add user section

                            authority = input("Enter user authority (coach / gym_user): ").strip()
                            name = input("Enter user name: ").strip()
                            usernam = input("Enter username: ").strip()
                            passwor = input("Enter password: ").strip()
                            email = input("Enter user e-mail: ").strip()

                            if authority not in ["coach", "gym_user"]:
                                print("Invalid Authority!")
                            else:
                                m.add_member(authority, name, usernam, passwor, email, True)
                                print("User added successfully!" if True else "Failed to add user.")

                        elif user_option == 2:
                            # Edit User
                            usernam = input("Enter username to edit: ").strip()
                            print("What do you want to edit?")
                            print("1. name")
                            print("2. password")
                            print("3. email")
                            print("4. active_status")
                            edit_choice = input("Enter choice: ").strip()

                            section_map = {
                                "1": "name",
                                "2": "password",
                                "3": "email",
                                "4": "active_status"
                            }
                            section = section_map.get(edit_choice)

                            if not section:
                                print("Invalid selection!")
                            else:
                                if section == "active_status":
                                    amount = input("Enter new status (True/False): ").strip()
                                    amount = True if amount.lower() in ["true", "1", "yes"] else False
                                else:
                                    amount = input(f"Enter new {section}: ").strip()

                                result = m.edit_member_info(section, amount, usernam)
                                if result:
                                    print("User updated successfully!")
                                else:
                                    print("Failed to update user.")

                        elif user_option == 3:
                            # Show All Users
                            m.show_user_info()

                        elif user_option == 4:
                            # Activate / Deactivate
                            usernam = input("Enter username: ").strip()
                            status = input("Enter new status (True/False): ").strip()
                            active_status = True if status.lower() in ["true", "1", "yes"] else False
                            result = m.edit_member_info("active_status", active_status, usernam)
                            if result:
                                print(f"User status changed to {active_status}")
                            else:
                                print("Failed to change status.")

                        elif user_option == 5:
                            break

                        else:
                            print("Invalid option!")

                # Halls management section

                elif option == 2:
                    while True:
                        show_manager_hall_options()

                        try:
                            hall_option = int(input("Enter your choice: ").strip())
                        except ValueError:
                            print("\nPlease enter a valid number!\n")
                            continue

                        if hall_option == 1:
                            # Add Hall
                            name = input("Enter hall name: ").strip()
                            capacity = input("Enter capacity: ").strip()
                            tools = input("Enter tools (comma separated): ").strip()
                            status = input("Enter status (True/False): ").strip()

                            try:
                                capacity = int(capacity)
                            except ValueError:
                                print("Capacity must be a number!")
                                continue

                            hall_status = True if status.lower() in ["true", "1", "yes"] else False
                            result = m.add_hall(name, capacity, tools, hall_status)
                            if result:
                                print("Hall added successfully!")
                            else:
                                print("Failed to add hall.")

                        elif hall_option == 2:
                            # Edit Hall
                            name = input("Enter current hall name: ").strip()
                            print("What do you want to edit?")
                            print("1. name")
                            print("2. capacity")
                            print("3. tools")
                            print("4. hall_status")
                            edit_choice = input("Enter choice: ").strip()

                            choice_map = {
                                "1": "name",
                                "2": "capacity",
                                "3": "tools",
                                "4": "hall_status"
                            }
                            field = choice_map.get(edit_choice)

                            if not field:
                                print("Invalid selection!")
                            else:
                                if field == "capacity":
                                    try:
                                        new_value = int(input("Enter new capacity: ").strip())
                                    except ValueError:
                                        print("Capacity must be a number!")
                                        continue
                                elif field == "hall_status":
                                    val = input("Enter new status (True/False): ").strip()
                                    new_value = True if val.lower() in ["true", "1", "yes"] else False
                                else:
                                    new_value = input(f"Enter new {field}: ").strip()

                                m.edit_hall_info(name, field, new_value)
                                print("Hall updated!")

                        elif hall_option == 3:

                            m.show_hall_info()

                        elif hall_option == 4:
                            name = input("Enter hall name: ").strip()
                            status = input("Enter new status (True/False): ").strip()
                            hall_status = True if status.lower() in ["true", "1", "yes"] else False
                            m.edit_hall_info(name, "hall_status", hall_status)
                            print(f"Hall status changed to {hall_status}")

                        elif hall_option == 5:
                            break

                        else:
                            print("Invalid option!")

                # Class management section

                elif option == 3:
                    while True:

                        show_manager_class_options()

                        try:
                            class_option = int(input("Enter your choice: ").strip())
                        except ValueError:
                            print("\nPlease enter a valid number!\n")
                            continue

                        if class_option == 1:
                            # Add Class
                            print("Available types: gym, yoga, fitness, crossfit")
                            title = input("Enter class title: ").strip()
                            class_type = input("Enter class type: ").strip().lower()
                            coach_user = input("Enter coach username: ").strip()
                            hall = input("Enter hall name: ").strip()
                            date = input("Enter day (e.g. Monday): ").strip()
                            time = input("Enter time (e.g. 18:00): ").strip()
                            capacity = input("Enter capacity: ").strip()
                            status = input("Enter status (True/False): ").strip()

                            try:
                                capacity = int(capacity)
                            except ValueError:
                                print("Capacity must be a number!")
                                continue

                            class_status = True if status.lower() in ["true", "1", "yes"] else False
                            result = m.add_class(title, class_type, coach_user, hall, date, time, capacity, class_status)
                            if result:
                                print("Class added successfully!")
                            else:
                                print("Failed to add class. Check coach and hall.")

                        elif class_option == 2:
                            # Edit class
                            title = input("Enter current class title: ").strip()
                            print("What do you want to edit?")
                            print("1. title")
                            print("2. class_type")
                            print("3. coach")
                            print("4. sport_hall")
                            print("5. class_date")
                            print("6. class_time")
                            print("7. capacity")
                            print("8. class_status")
                            edit_choice = input("Enter choice: ").strip()

                            field_map = {
                                "1": "title",
                                "2": "class_type",
                                "3": "coach",
                                "4": "sport_hall",
                                "5": "class_date",
                                "6": "class_time",
                                "7": "capacity",
                                "8": "class_status"
                            }
                            field = field_map.get(edit_choice)

                            if not field:
                                print("Invalid selection!")
                            else:
                                if field == "capacity":
                                    try:
                                        new_value = int(input("Enter new capacity: ").strip())
                                    except ValueError:
                                        print("Capacity must be a number!")
                                        continue
                                elif field == "class_status":
                                    val = input("Enter new status (True/False): ").strip()
                                    new_value = True if val.lower() in ["true", "1", "yes"] else False
                                else:
                                    new_value = input("Enter new value: ").strip()

                                result = m.edit_class_info(title, field, new_value)
                                if result:
                                    print("Class updated successfully!")
                                else:
                                    print("Failed to update class.")

                        elif class_option == 3:
                            m.show_class_info()

                        elif class_option == 4:
                            title = input("Enter class title: ").strip()
                            status = input("Enter new status (True/False): ").strip()
                            class_status = True if status.lower() in ["true", "1", "yes"] else False
                            result = m.edit_class_info(title, "class_status", class_status)
                            if result:
                                print(f"Class status changed to {class_status}")
                            else:
                                print("Failed to change status.")

                        elif class_option == 5:
                            break

                        else:
                            print("Invalid option!")

                # Subscription section

                elif option == 4:
                    while True:
                        show_manager_subscription_options()

                        try:
                            sub_option = int(input("Enter your choice: ").strip())
                        except ValueError:
                            print("\nPlease enter a valid number!\n")
                            continue

                        if sub_option == 1:
                            # Make subscription

                            member_username = input("Enter member username: ").strip()
                            print("Available types: 1-month, 3-month, 6-month")
                            sub_type = input("Enter subscription type: ").strip()
                            amount = input("Enter amount: ").strip()

                            try:
                                amount = float(amount)
                            except ValueError:
                                print("Amount must be a number!")
                                continue

                            result = m.create_subscription(member_username, sub_type, amount)
                            if result:
                                print("Subscription created successfully!")

                        elif sub_option == 2:
                            # Show All Payments
                            m.show_payments()

                        elif sub_option == 3:
                            # Show Subscription Status
                            print("1. Show status of all members")
                            print("2. Show status of one member")
                            status_choice = input("Enter choice: ").strip()

                            if status_choice == "1":
                                m.show_subscription_status()
                            elif status_choice == "2":
                                member_username = input("Enter member username: ").strip()
                                m.show_subscription_status(member_username)
                            else:
                                print("Invalid choice!")

                        elif sub_option == 4:
                            break

                        else:
                            print("Invalid option!")

                # Reports section

                elif option == 5:

                    m.show_reports()

                # Exit manager section

                elif option == 6:
                    print("\nExiting manager section.")
                    break

                else:
                    print("Invalid option!")

    # -------------------- Coach Login --------------------
    elif choice == 2:
        print("\nCoach login is not implemented yet.")

    # -------------------- Member Login --------------------
    elif choice == 3:
        print("\nMember login is not implemented yet.")

    # -------------------- Exit --------------------
    elif choice == 4:
        print("\nExiting from program.")
        break

    else:
        print("\nInvalid choice! Please try again.")
