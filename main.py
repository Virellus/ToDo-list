from user import *
from todo import *

def edit_menu(manager):
    while True:
        print("\nEdit Tasks:")
        print("1. Add Assignment")
        print("2. Add Meeting")
        print("3. Add Reminder")
        print("4. Delete and Item")
        print("5. Wipe all tasks")
        print("6. Back to main Menu")
        choice = input("Choose an Option: ")
        if choice == "1":
            manager.add_asignment()
        elif choice == "2":
            manager.add_meeting()
        elif choice == "3":
            manager.add_reminder()
        elif choice == "4":
            manager.delete_item()
        elif choice == "5":
            manager.wipe_user_data()
        elif choice == "6":
            break
        else:
            print("Invalid option. Try again.")
def main_menu(user):
    manager = Manager(user.getUserID())
    while True: 
        print("\nMain Menu")
        print("1. View All Tasks")
        print("2. Edit Tasks")
        print("3. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            manager.view_all()
        elif choice == "2":
            edit_menu(manager)
        elif choice == "3":
            user.logout()
            print("Logged out.")
        else:
            print("Invalid option. Try again.")
def main():
    user = User()
    while True: 
        print("\nWelcome!")
        print("1. Log In")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            if user.login():
                main_menu(user)
        elif choice == "2":
            user.createAccount()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again")
if __name == "__main__":
    main()