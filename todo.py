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
        title = input("Assignment title: ")
        due = input("Due date and time (YYYY-MM-DD HH:MM): ")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Assignments (user_id, title, due_time)
            VALUES (?, ?, ?)
        """, (self.user_id, title, due))
        connection.commit()
        connection.close()
        print("Assignment added.")
    def add_meeting(self):
        title = input("Meeting title: ")
        time = input("Meeting time (YYYY-MM-DD HH:MM): ")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Meetings (user_id, title, meeting_time)
            VALUES (?, ?, ?)
        """, (self.user_id, title, time))
        connection.commit()
        connection.close()
        print("Meeting added.")
    def add_reminder(self):
        title = input("Reminder title: ")
        time = datetime.now().strftime("%Y-%m-%d %H:%M")  # Use current time or any placeholder
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
    def delete_item(self):
        print("\nDelete Item")
        print("1. Assignment")
        print("2. Meeting")
        print("3. Reminder")
        choice = input("Select type of task to delete: ")
        table = None
        time_col = None
        if choice == "1":
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
