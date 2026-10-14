# ---------------- data----------------
import json

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

members = data["members"]
classes = data["classes"]
subscription = data["subscription"]


# ---------------- ----------------
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
    for sub_key, sub_info in subscription.items():
        print(sub_key, sub_info["title"], sub_info["price"])
    sub_id = input("enter sub id: ")
    if sub_id not in subscription:
        print("Invalid subscription.")
    elif member["wallet_balance"] < subscription[sub_id]["price"]:
        print("Insufficient balance")
    else:
        member["wallet_balance"] -= subscription[sub_id]["price"]
        member["subscription_status"] = "active"
        member["subscription_type"] = subscription[sub_id]["title"]
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
