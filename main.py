from manage_utils.manage import Manage
from login_utils.login import (
    login, show_menu_login,
    show_manager_user_options, show_manager_hall_options,
    show_manager_class_options, show_manager_subscription_options
)
from coach import Coach
from gym_user.member import Member

while True:
    show_menu_login()
    try:
        choice = int(input("Enter your choice: ").strip())
    except ValueError:
        print("Please enter a valid number!")
        continue

    # ========== MANAGER ==========
    if choice == 1:
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()
        if not login(username, password, "manager"):
            print("Wrong inputs.")
            if input("Try again? (1=yes): ").strip() != "1":
                continue
            continue

        print("\nLogged in as manager.")
        m = Manage()
        while True:
            Manage.show_panel()
            try:
                option = int(input("Option: ").strip())
            except ValueError:
                print("Invalid number!")
                continue

            if option == 1:  # Users
                while True:
                    show_manager_user_options()
                    try: uo = int(input("Choice: ").strip())
                    except: continue
                    if uo == 1:
                        auth = input("authority (coach/gym_user): ").strip()
                        name = input("name: ").strip()
                        un = input("username: ").strip()
                        pw = input("password: ").strip()
                        em = input("email: ").strip()
                        if auth in ("coach", "gym_user"):
                            m.add_member(auth, name, un, pw, em, True)
                        else:
                            print("Invalid authority")
                    elif uo == 2:
                        un = input("username to edit: ").strip()
                        print("1.name 2.password 3.email 4.active_status")
                        sc = input("field: ").strip()
                        sm = {"1":"name","2":"password","3":"email","4":"active_status"}
                        sec = sm.get(sc)
                        if not sec: print("Invalid"); continue
                        if sec == "active_status":
                            val = input("True/False: ").strip().lower() in ("true","1","yes")
                        else:
                            val = input(f"new {sec}: ").strip()
                        print("OK" if m.edit_member_info(sec, val, un) else "Failed")
                    elif uo == 3:
                        m.show_user_info()
                    elif uo == 4:
                        un = input("username: ").strip()
                        st = input("True/False: ").strip().lower() in ("true","1","yes")
                        print("OK" if m.edit_member_info("active_status", st, un) else "Failed")
                    elif uo == 5:
                        break

            elif option == 2:  # Halls
                while True:
                    show_manager_hall_options()
                    try: ho = int(input("Choice: ").strip())
                    except: continue
                    if ho == 1:
                        name = input("name: ").strip()
                        try: cap = int(input("capacity: ").strip())
                        except: print("number!"); continue
                        tools = input("tools (comma): ").strip()
                        st = input("status True/False: ").strip().lower() in ("true","1","yes")
                        print("OK" if m.add_hall(name, cap, tools, st) else "Failed")
                    elif ho == 2:
                        name = input("current name: ").strip()
                        print("1.name 2.capacity 3.tools 4.hall_status")
                        fc = input("field: ").strip()
                        fm = {"1":"name","2":"capacity","3":"tools","4":"hall_status"}
                        field = fm.get(fc)
                        if not field: continue
                        if field == "capacity":
                            try: nv = int(input("new: ").strip())
                            except: continue
                        elif field == "hall_status":
                            nv = input("True/False: ").strip().lower() in ("true","1","yes")
                        else:
                            nv = input("new: ").strip()
                        m.edit_hall_info(name, field, nv)
                        print("Updated")
                    elif ho == 3:
                        m.show_hall_info()
                    elif ho == 4:
                        name = input("name: ").strip()
                        st = input("True/False: ").strip().lower() in ("true","1","yes")
                        m.edit_hall_info(name, "hall_status", st)
                        print("Status changed")
                    elif ho == 5:
                        break

            elif option == 3:  # Classes
                while True:
                    show_manager_class_options()
                    try: co = int(input("Choice: ").strip())
                    except: continue
                    if co == 1:
                        print("types: gym yoga fitness crossfit")
                        title = input("title: ").strip()
                        ctype = input("type: ").strip().lower()
                        coach = input("coach username: ").strip()
                        hall = input("hall: ").strip()
                        day = input("day: ").strip()
                        time = input("time: ").strip()
                        try: cap = int(input("capacity: ").strip())
                        except: continue
                        st = input("status True/False: ").strip().lower() in ("true","1","yes")
                        print("OK" if m.add_class(title, ctype, coach, hall, day, time, cap, st) else "Failed")
                    elif co == 2:
                        title = input("current title: ").strip()
                        print("1.title 2.class_type 3.coach 4.sport_hall 5.class_date 6.class_time 7.capacity 8.class_status")
                        fc = input("field: ").strip()
                        fm = {"1":"title","2":"class_type","3":"coach","4":"sport_hall",
                            "5":"class_date","6":"class_time","7":"capacity","8":"class_status"}
                        field = fm.get(fc)
                        if not field: continue
                        if field == "capacity":
                            try: nv = int(input("new: ").strip())
                            except: continue
                        elif field == "class_status":
                            nv = input("True/False: ").strip().lower() in ("true","1","yes")
                        else:
                            nv = input("new: ").strip()
                        print("OK" if m.edit_class_info(title, field, nv) else "Failed")
                    elif co == 3:
                        m.show_class_info()
                    elif co == 4:
                        title = input("title: ").strip()
                        st = input("True/False: ").strip().lower() in ("true","1","yes")
                        print("OK" if m.edit_class_info(title, "class_status", st) else "Failed")
                    elif co == 5:
                        break

            elif option == 4:  # Subscriptions
                while True:
                    show_manager_subscription_options()
                    try: so = int(input("Choice: ").strip())
                    except: continue
                    if so == 1:
                        mu = input("member username: ").strip()
                        print("1-month / 3-month / 6-month")
                        st = input("type: ").strip()
                        try: amt = float(input("amount: ").strip())
                        except: continue
                        m.create_subscription(mu, st, amt)
                    elif so == 2:
                        m.show_payments()
                    elif so == 3:
                        print("1.All 2.One")
                        sc = input("Choice: ").strip()
                        if sc == "1": m.show_subscription_status()
                        elif sc == "2":
                            mu = input("username: ").strip()
                            m.show_subscription_status(mu)
                    elif so == 4:
                        break

            elif option == 5:
                m.show_reports()

            elif option == 6:
                print("Logout manager.")
                break
            else:
                print("Invalid option!")

    # ========== COACH ==========
    elif choice == 2:
        user_data = Coach.login()
        if user_data:
            coach = Coach(
                username=user_data.get("username"),
                name=user_data.get("name", ""),
                password=user_data.get("password", ""),
                email=user_data.get("email", ""),
                is_active=user_data.get("active_status", True)
            )
            coach.run_panel()

    # ========== MEMBER ==========
    elif choice == 3:
        user_data = Member.login()
        if user_data:
            Member.run_panel(user_data)

    # ========== EXIT ==========
    elif choice == 4:
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")
