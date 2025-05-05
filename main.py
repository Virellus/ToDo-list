from user import *
from todo import *

def edit_menu(manager):
    while True:
        print("\nEdit Tasks:")
        print("0. Back to main Menu")
        print("1. Add Assignment")
        print("2. Add Meeting")
        print("3. Add Reminder")
        print("4. Delete and Item")
        print("5. Wipe all tasks")
        choice = input("Choose an Option: ")
        if choice == "0":
            break
        elif choice == "1":
            manager.add_asignment()
        elif choice == "2":
            manager.add_meeting()
        elif choice == "3":
            manager.add_reminder()
        elif choice == "4":
            manager.delete_item()
        elif choice == "5":
            manager.wipe_user_data()
        else:
            print("Invalid option. Try again.")
def main_menu(user):
    manager = Manager(user.getUserID())
    while True: 
        print("\nMain Menu")
        print("0. Logout")
        print("1. View All Tasks")
        print("2. Edit Tasks")
        choice = input("Choose an option: ")
        if choice == "0":
            user.logout()
            print("Logged out.")
            break
        elif choice == "1":
            manager.view_all()
        elif choice == "2":
            edit_menu(manager)
        else:
            print("Invalid option. Try again.")
def main():
    user = User()
    while True: 
        print("\nWelcome!")
        print("0. Exit")
        print("1. Log In")
        print("2. Create Account")
        choice = input("Choose an option: ")
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            if user.login():
                main_menu(user)
        elif choice == "2":
            user.createAccount()
        else:
            print("Invalid option. Try again")
if __name__ == "__main__":
    main()