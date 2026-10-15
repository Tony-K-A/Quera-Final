import getpass

from validators import POSITIVE_INT_RE

CANCEL = "/back"

def _is_valid(check, text):
    if check is None:
        return bool(text)
    if hasattr(check, "fullmatch"):
        return bool(check.fullmatch(text))
    return bool(check(text))

def ask(prompt, check=None, error="Invalid input, please try again.", secret=False, allow_empty=False):

    reader = getpass.getpass if secret else input
    while True:
        raw = reader(f"{prompt} ({CANCEL} to cancel): ")
        if raw.strip().lower() == CANCEL:
            return None
        text = raw.strip()
        if text == "" and allow_empty and raw == "":
            return ""
        if raw != text:
            print(error)
            continue
        if _is_valid(check, text):
            return text
        print(error)

def ask_int(prompt, check=POSITIVE_INT_RE, error="Please enter a positive whole number."):

    text = ask(prompt, check, error)
    return None if text is None else int(text)

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
        raw = input("Choice: ").strip()
        if raw == back_key:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print("Invalid choice, try again.")

def choose_bool(prompt="Status:", true_label="Active", false_label="Inactive"):
    index = choose(prompt, [true_label, false_label])
    return None if index is None else index == 0

def pause():
    input("\nPress Enter to continue...")
