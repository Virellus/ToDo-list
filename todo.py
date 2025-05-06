import sqlite3
import sys
from datetime import datetime
class Manager:
    def __init__(self, user_id, databasename="todolist.db"):
        self.user_id = user_id
        self.databasename = databasename
    def _connect(self):
        connection = sqlite3.connect(self.databasename)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        return connection, cursor
    def add_assignment(self):
        title = input("Assignment title (or 0 to cancel): ")
        if title.strip() == "0":
            print("Cancelled.")
            return
        due = input("Due date and time (YYYY-MM-DD HH:MM) (or 0 to cancel): ")
        if due.strip() == "0":
            print("Cancelled.")
            return
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Assignments (user_id, title, due_time)
            VALUES (?, ?, ?)
        """, (self.user_id, title, due))
        connection.commit()
        connection.close()
        print("Assignment added.")
    def add_meeting(self):
        title = input("Meeting title (or 0 to cancel): ")
        if title.strip() == "0":
            print("Cancelled.")
            return
        time = input("Meeting time (YYYY-MM-DD HH:MM) (or 0 to cancel): ")
        if time.strip() == "0":
            print("Cancelled.")
            return
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Meetings (user_id, title, meeting_time)
            VALUES (?, ?, ?)
        """, (self.user_id, title, time))
        connection.commit()
        connection.close()
        print("Meeting added.")
    def add_reminder(self):
        title = input("Reminder title (or 0 to cancel): ")
        if title.strip() == "0":
            print("Cancelled.")
            return
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Reminders (user_id, title, reminder_time)
            VALUES (?, ?, ?)
        """, (self.user_id, title, time))
        connection.commit()
        connection.close()
        print("Reminder added.")
    def view_all(self):
        connection, cursor = self._connect()
        queries = [
            ("Assignments", "due_time"),
            ("Meetings", "meeting_time"),
            ("Reminders", None)
        ]
        for table, time_col in queries:
            print(f"\n{table}")
            if time_col:
                cursor.execute(f"SELECT title, {time_col} FROM {table} WHERE user_id=? ORDER BY {time_col}", (self.user_id,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        try:
                            dt = datetime.strptime(row[1], "%Y-%m-%d %H:%M")
                            formatted_time = dt.strftime("%b %d, %Y %I:%M %p")
                        except Exception:
                            formatted_time = row[1]
                        print(f"{row[0]}, {formatted_time}")
                else:
                    print("No tasks found.")
            else:
                cursor.execute(f"SELECT title FROM {table} WHERE user_id=?", (self.user_id,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        print(f"{row[0]}")
                else:
                    print("No tasks found.")
        connection.close()
    def view_items_by_type(self, table, time_col):
        conn, cursor = self._connect()
        if time_col:
            cursor.execute(f"SELECT id, title, description, {time_col}, completed FROM {table} WHERE user_id=? ORDER BY {time_col}", (self.user_id,))
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Title: {row[1]}, Due: {row[3]}, Completed: {"Made" if row[4] else "Not Made"}")
        else:
            cursor.execute(f"SELECT id, title, description, completed FROM {table} WHERE user_id=?", (self.user_id,))
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Title: {row[1]}, Completed: {"Made" if row[3] else "Not Made"}")
        conn.close()
    def wipe_user_data(self):
        confirm = input("Are you sure you want to wipe all your to-dos? (y/n): ").lower()
        if confirm != "y":
            print("Cancelled.")
            return
        connection, cursor = self._connect()
        cursor.execute("DELETE FROM Assignments WHERE user_id = ?", (self.user_id,))
        cursor.execute("DELETE FROM Meetings WHERE user_id = ?", (self.user_id,))
        cursor.execute("DELETE FROM Reminders WHERE user_id = ?", (self.user_id,))
        connection.commit()
        connection.close()
        print("All your tasks have been wiped.")
    def delete_item(self):
        print("\nDelete Item")
        print("0. Go Back")
        print("1. Assignment")
        print("2. Meeting")
        print("3. Reminder")
        choice = input("Select type of task to delete: ")
        table = None
        time_col = None
        if choice == "0":
            return
        elif choice == "1":
            table = "Assignments"
            time_col = "due_time"
        elif choice == "2":
            table = "Meetings"
            time_col = "meeting_time"
        elif choice == "3":
            table = "Reminders"
            time_col = "reminder_time"
        else:
            print("Invalid option.")
            return

        connection, cursor = self._connect()
        if time_col:
            cursor.execute(
                f"SELECT id, title, {time_col} FROM {table} WHERE user_id=? ORDER BY {time_col}",
                (self.user_id,)
            )
        else:
            cursor.execute(
                f"SELECT id, title FROM {table} WHERE user_id=?",
                (self.user_id,)
            )
        rows = cursor.fetchall()
        if not rows:
            print(f"No {table.lower()} to delete.")
            connection.close()
            return
        print(f"\nYour {table}:")
        for row in rows:
            if time_col:
                try:
                    formatted_time = datetime.strptime(row[2], "%Y-%m-%d %H:%M").strftime("%b %d, %Y %I:%M %p")
                except:
                    formatted_time = row[2]  # fallback
                print(f"ID: {row[0]}, Title: {row[1]}, Time: {formatted_time}")
            else:
                print(f"ID: {row[0]}, Title: {row[1]}")
        item_id = input("\nEnter the ID of the item to delete: ")
        cursor.execute(f"DELETE FROM {table} WHERE id=? AND user_id=?", (item_id, self.user_id))
        connection.commit()
        connection.close()
        print("Item deleted (if it existed).")
    def edit_item(self):
        item_types = {
            "1": ("Assignments", "due_time"),
            "2": ("Meetings", "meeting_time"),
            "3": ("Reminders", None)
        }

        print("\nEdit an Item:")
        print("0. Go Back")
        print("1. Assignment")
        print("2. Meeting")
        print("3. Reminder")
        choice = input("Choose item type to edit: ")
        if choice == "0":
            return
        if choice not in item_types:
            print("Invalid option.")
            return
        table, time_col = item_types[choice]
        connection, cursor = self._connect()
        print(f"\n{table}")
        if time_col:
            cursor.execute(f"SELECT id, title, {time_col} FROM {table} WHERE user_id = ?", (self.user_id,))
        else:
            cursor.execute(f"SELECT id, title FROM {table} WHERE user_id = ?", (self.user_id,))
        rows = cursor.fetchall()
        if not rows:
            print("No items found.")
            connection.close()
            return
        for row in rows:
            if time_col:
                print(f"ID: {row[0]}, Title: {row[1]}, Time: {row[2]}")
            else:
                print(f"ID: {row[0]}, Title: {row[1]}")

        item_id = input("Enter the ID of the item you want to edit (or 0 to go back): ")
        if item_id == "0":
            connection.close()
            return
        new_title = input("Enter new title: ")
        if time_col:
            new_time = input(f"Enter new time ({time_col}, format: YYYY-MM-DD HH:MM): ")
            cursor.execute(
                f"UPDATE {table} SET title = ?, {time_col} = ? WHERE id = ? AND user_id = ?",
                (new_title, new_time, item_id, self.user_id)
            )
        else:
            cursor.execute(
                f"UPDATE {table} SET title = ? WHERE id = ? AND user_id = ?",
                (new_title, item_id, self.user_id)
            )
        connection.commit()
        connection.close()
        print("Item updated successfully.")
    def auto_delete_expired_items(self):
        now = datetime.now()
        connection, cursor = self._connect()
        cursor.execute("""
            DELETE FROM Assignments 
            WHERE user_id = ? AND 
                datetime(due_time) < datetime(?,'-1 day')
        """, (self.user_id, now.strftime("%Y-%m-%d %H:%M")))
        cursor.execute("""
            DELETE FROM Meetings 
            WHERE user_id = ? AND 
                datetime(meeting_time) < datetime(?,'-1 day')
        """, (self.user_id, now.strftime("%Y-%m-%d %H:%M")))
        connection.commit()
        connection.close()