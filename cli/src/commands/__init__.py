from builtins import input


def confirm(message="Confirm"):
    prompt = message + " [y/n]:\n"

    while True:
        ans = input(prompt)
        if ans not in ["y", "Y", "n", "N"]:
            print("please enter y or n.")
            continue
        if ans == "y" or ans == "Y":
            return True
        if ans == "n" or ans == "N":
            return False
