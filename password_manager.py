import pickle
import os
import time
import ctypes
import sys
import random
# os.system("cls")


def is_admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


if not is_admin():
    print("You need to be admin to run this program!")
    time.sleep(2)
    os._exit(0)
    # # Re-run the program with admin rights
    # ctypes.windll.shell32.ShellExecuteW(
    #     None, "runas", sys.executable, " ".join(sys.argv), None, 1)


password_entered = False


# make sure files and directorys exists
os.system("cd %CD%")

if not os.path.exists("data"):
    os.mkdir("data")

try:
    with open("data/login_password.data", "rb") as f:
        pickle.load(f)
    with open("data/passwords.data", "rb") as f:
        pickle.load(f)
except:
    with open("data/login_password.data", "wb") as f:
        pickle.dump("admin", f)
    with open("data/passwords.data", "wb") as f:
        pickle.dump([], f)


def pause():
    os.system("pause")

# login to application


def enter_password():
    password = input(
        "Enter password to login and confirm you have permission: ")
    with open("data/login_password.data", "rb") as f:
        if password == pickle.load(f):
            print("Done!")
            password_entered = True
        else:
            print("Wrong!")
            time.sleep(2)
            os._exit(0)
    return password_entered


password_entered = enter_password()
if password_entered != True:
    password_entered = enter_password()
    enter_password()


def add_password():
    # add new password to passwords list
    with open("data/passwords.data", "rb") as f:
        passwords_list = pickle.load(f)
    with open("data/passwords.data", "wb") as f:
        # get password
        password_to_save = input(
            "Enter your password that you like to save: ")

        password_name_to_save = input(
            "Enter password name to find it easily: ")

        # encrypt password
        password_to_save_ascii = ""
        password_to_save_ascii_list = []
        for i in password_to_save:
            password_to_save_ascii += str(ord(i))
            password_to_save_ascii_list.append(str(ord(i)))

        password_name_to_save_ascii = ""
        password_name_to_save_ascii_list = []
        for i in password_name_to_save:
            password_name_to_save_ascii += str(ord(i))
            password_name_to_save_ascii_list.append(str(ord(i)))

        # append to full list
        password_full = {"name": password_name_to_save,
                         "password": password_to_save_ascii,
                         "list_password_ascii": password_to_save_ascii_list,
                         "list_password_name_ascii": password_name_to_save_ascii_list}
        passwords_list.append(password_full)
        pickle.dump(passwords_list, f)


def remove_password():
    # remove password from passwords list
    print("Note: You can find passwords by name in \"show passwords\" command")
    password_name_to_remove = input("Enter password name to remove: ")
    with open("data/passwords.data", "rb") as f:
        passwords_list = pickle.load(f)
        if password_name_to_remove == "*":
            passwords_list.clear()
        else:
            for i in passwords_list:
                if i[list(i.keys())[0]] == password_name_to_remove:
                    passwords_list.remove(i)
                    break
    with open("data/passwords.data", "wb") as f:
        pickle.dump(passwords_list, f)


def show_passwords():
    # show all passwords list
    with open("data/passwords.data", "rb") as f:
        passwords_list = pickle.load(f)
        for i in passwords_list:
            # set password variables
            password_name = i["name"]
            password_password = i["password"]
            password_ascii_list = i["list_password_ascii"]
            password_name_ascii_list = i["list_password_name_ascii"]

            # decrypt password variables
            password_password_encrypted = ""
            for i in password_ascii_list:
                password_password_encrypted += chr(int(i))

            password_name_encrypted = ""
            for i in password_name_ascii_list:
                password_name_encrypted += chr(int(i))

            # print password name and orginal password
            print("Name: {}\nPassword: {}\n".format(
                password_name_encrypted, password_password_encrypted))
    pause()


def change_login_pass():

    # change login password
    old_password = input("Enter your old password: ")
    with open("data/login_password.data", "rb") as f:
        if old_password == pickle.load(f):
            new_password = input("Enter your new password: ")
            with open("data/login_password.data", "wb") as f:
                pickle.dump(new_password, f)
        else:
            print("Wrong!")
            time.sleep(2)


def generate_password(length, has_numbers, has_lower, has_upper, has_symbols):
    char = []
    if has_numbers:
        for i in numbers:
            char.append(i)
    if has_lower:
        for i in alpha_lower:
            char.append(i)
    if has_upper:
        for i in alpha_upper:
            char.append(i)
    if has_symbols:
        for i in symbols:
            char.append(i)

    password = random.choices(char, k=length)
    pass_save = ""
    for i in password:
        pass_save += str(i)

    return pass_save


while True:
    if password_entered:
        choices_to_select = """
        [1] Add new password
        [2] Delete a password
        [3] Show all passwords
        [4] Change login password
        [5] Generate a strong password
        [6] Exit
        """
        print(choices_to_select)
        choice = input("[?]: ")
    if choice == "1":
        add_password()
    elif choice == "2":
        remove_password()
    elif choice == "3":
        show_passwords()
    elif choice == "4":
        change_login_pass()
    elif choice == "5":
        os.system("cls")

        print("We recommend you to use a password with at least 8 characters, with at least one number, one lowercase letter, one uppercase letter, and one symbol. \n")

        numbers = list("0123456789")
        alpha_lower = list("abcdefghijklmnopqrstuvwxyz")
        alpha_upper = ""
        for i in alpha_lower:
            alpha_upper += i.upper()
        symbols = list("!@#$%^&*()_+")

        alpha_upper = list(alpha_upper)

        length = int(input("How long do you want your password to be? "))
        has_numbers = input("Do you want to include numbers? (y/n) ").lower()
        has_lower = input(
            "Do you want to include lowercase letters? (y/n) ").lower()
        has_upper = input(
            "Do you want to include uppercase letters? (y/n) ").lower()
        has_symbols = input("Do you want to include symbols? (y/n) ").lower()

        has_numbers = True if has_numbers == "y" else False
        has_lower = True if has_lower == "y" else False
        has_upper = True if has_upper == "y" else False
        has_symbols = True if has_symbols == "y" else False

        generated_pass = generate_password(
            length, has_numbers, has_lower, has_upper, has_symbols)
        print("\nYour Password is: \n", generated_pass)
        
        pause()
        # add_generated_password = input(
        #     "Do you want to add this generated password to list of your passwords in this app? (y/n) ")
        # if add_generated_password.lower() == "y":
        #     add_password(generated_pass)
        #     print("Done!")
        #     pause()

    elif choice == "6":
        os._exit(0)
    else:
        print("Wrong choice!")
        time.sleep(2)
        os.system("cls")
        print(choices_to_select)

    os.system("cls")
