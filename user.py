# ---------------- داده‌ها ----------------
members = {
    "sarax": {
        "name": "sara",
        "password": "4567",
        "email": "sara@gmail.com",
        "subscription_status": "active",
        "account_status": "active",
        "role": "member",
        "subscription_type": "1 months",
        "wallet_balance": 0,
        "start_date": "1402/05/11",
        "end_date": "1403/05/11",
        "enrolled_classes": [],
        "registrations": [
            {
                "class_name": "yoga",
                "register_date": "1403/07/20",
                "status": "active",
                "tracking_code": "REG_1001",
            },
        ],
    },
    "alirt6": {
        "name": "ali",
        "password": "1234",
        "email": "ali@gmail.com",
        "subscription_status": "active",
        "account_status": "active",
        "role": "coach",
        "subscription_type": "none",
        "wallet_balance": 0,
        "start_date": "1405/08/10",
        "end_date": "1406/08/10",
        "enrolled_classes": [],
        "registrations": [
            {
                "class_name": "pilates",
                "register_date": "1404/04/13",
                "status": "inactive",
                "tracking_code": "WE10",
            },
        ],
    },
    "arya56": {
        "name": "arya",
        "password": "8970",
        "email": "aryan@gmail.com",
        "subscription_status": "inactive",
        "account_status": "inactive",
        "role": "member",
        "subscription_type": "none",
        "wallet_balance": 0,
        "start_date": "1402/04/07",
        "end_date": "1403/04/07",
        "enrolled_classes": [],
        "registrations": [
            {
                "class_name": "fitness",
                "register_date": "1403/07/13",
                "status": "inactive",
                "tracking_code": "WE11",
            },
        ],
    },
}

classes = {
    "C101": {
        "title": "Gym Class",
        "class_type": "gym",
        "coach": "coach1",
        "sport_hall": "Persia",
        "class_date": "Tuesday",
        "class_time": "19:00",
        "capacity": 50,
        "remaining": 50,
        "class_status": True,
        "workout_plan": ["Warm up", "Deadlift", "Cool down"],
    },
    "C102": {
        "title": "Yoga",
        "class_type": "yoga",
        "coach": "coach2",
        "sport_hall": "Persia",
        "class_date": "Wednesday",
        "class_time": "18:00",
        "capacity": 20,
        "remaining": 20,
        "class_status": True,
        "workout_plan": ["Sun salutation", "Downward dog", "Relaxation"],
    },
    "C103": {
        "title": "Pilates",
        "class_type": "pilates",
        "coach": "coach3",
        "sport_hall": "Persia",
        "class_date": "Monday",
        "class_time": "18:00",
        "capacity": 15,
        "remaining": 15,
        "class_status": False,
        "workout_plan": ["Roll up", "Single leg stretch", "Spine stretch"],
    },
}
subscriptions = {
    "1": {"title": "1 months", "price": 100, "months": 1},
    "2": {"title": "3 months", "price": 250, "months": 3},
    "3": {"title": "6 months", "price": 450, "months": 6},
}


# ---------------- ورود ----------------
def login():
    attempts = 0
    while attempts < 3:
        user_name = input("please enter your username: ")
        password = input("please enter password: ")

        if (
            user_name in members
            and password == members[user_name]["password"]
            and members[user_name]["account_status"] == "active"
        ):
            print("successful")
            return user_name

        attempts += 1
        print("unsuccessful")
    return None


# ---------------- پنل عضو ----------------
def show_profile(username, member):
    print("name:", member["name"])
    print("username:", username)
    print("email:", member["email"])
    print("account status:", member["account_status"])
    print("subscription type:", member["subscription_type"])
    print("start date:", member["start_date"])
    print("end date:", member["end_date"])
    print("subscription status:", member["subscription_status"])


def show_classes():
    for class_id, class_info in classes.items():
        print("class id:", class_id)
        print("class:", class_info["title"])
        print("class_type:", class_info["class_type"])
        print("coach:", class_info["coach"])
        print("sport_hall:", class_info["sport_hall"])
        print("date:", class_info["class_date"])
        print("time:", class_info["class_time"])
        print("capacity:", class_info["capacity"])
        print("remaining:", class_info["remaining"])
        print("status:", class_info["class_status"])
        print()


def register_class(member):
    class_id = input("enter class id: ")
    if class_id not in classes:
        print("class not found")
    elif member["subscription_status"] != "active":
        print("your subscription is not active")
    elif classes[class_id]["class_status"] == False:
        print("this class is not active")
    elif classes[class_id]["remaining"] <= 0:
        print("this class is full")
    elif class_id in member["enrolled_classes"]:
        print("you are already registered in this class")
    else:
        classes[class_id]["remaining"] -= 1
        member["enrolled_classes"].append(class_id)
        print("registration successful")


def show_workout_plan():
    class_id = input("enter class id: ")
    if class_id in classes:
        print("workout plan for", classes[class_id]["title"])
        for exercise in classes[class_id]["workout_plan"]:
            print("-", exercise)
    else:
        print("class not found")


def cancel_registration(member):
    class_id = input("enter class id: ")
    if class_id not in member["enrolled_classes"]:
        print("you are not registered in this class")
    else:
        member["enrolled_classes"].remove(class_id)
        classes[class_id]["remaining"] += 1
        print("registration canceled")


def pay_subscription(member):
    for sub_key, sub_info in subscriptions.items():
        print(sub_key, sub_info["title"], sub_info["price"])
    sub_id = input("enter sub id: ")
    if sub_id not in subscriptions:
        print("Invalid subscription.")
    elif member["wallet_balance"] < subscriptions[sub_id]["price"]:
        print("Insufficient balance")
    else:
        member["wallet_balance"] -= subscriptions[sub_id]["price"]
        member["subscription_status"] = "active"
        member["subscription_type"] = subscriptions[sub_id]["title"]
        print("successful")


def member_panel(result):
    member = members[result]
    print("welcome")
    running = True
    while running:
        print("1.profile")
        print("2.wallet")
        print("3.classes")
        print("4.register class")
        print("5.workout plan")
        print("6.cancel registration")
        print("7.subscriptions")
        print("8.exit")
        choice = input("select an option: ")
        if choice == "1":
            show_profile(result, member)
        elif choice == "2":
            print("balance:", member["wallet_balance"])
        elif choice == "3":
            show_classes()
        elif choice == "4":
            register_class(member)
        elif choice == "5":
            show_workout_plan()
        elif choice == "6":
            cancel_registration(member)
        elif choice == "7":
            pay_subscription(member)
        elif choice == "8":
            running = False
        else:
            print("invalid option")


# ---------------- اجرا ----------------
def main():
    result = login()
    if result is not None and members[result]["role"] == "member":
        member_panel(result)
    else:
        print("login failed")


if __name__ == "main":
    main()
