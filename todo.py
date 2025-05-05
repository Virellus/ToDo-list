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
        description = input("Description: ")
        due = input("Due date and time (YYYY-MM-DD HH:MM): ")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Assignments (user_id, title, description, due_time)
            VALUES (?, ?, ?, ?)
        """, (self.user_id, title, description, due))
        connection.commit()
        connection.close()
        print("Assignment added.")
    def add_meeting(self):
        title = input("Meeting title: ")
        description = input("Description: ")
        time = input("Meeting time (YYYY-MM-DD HH:MM): ")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Meetings (user_id, title, description, meeting_time)
            VALUES (?, ?, ?, ?)
        """, (self.user_id, title, description, time))
        connection.commit()
        connection.close()
        print("Assignment added.")
    def add_reminder(self):
        title = input("Reminder title: ")
        description = input("Description: ")
        connection, cursor = self._connect()
        cursor.execute(""" 
            INSERT INTO Assignments (user_id, title, description)
            VALUES (?, ?, ?)
        """, (self.user_id, title, description))
        connection.commit()
        connection.close()
        print("Reminder added.")
    def view_all(self):
        connection, cursor = self._connect()
        queries = [
            ("Assignments" ,"due_time"),
            ("Meetings", "meeting_time"),
            ("Reminders", None)
        ]
        for table, time_col in queries:
            print(f"\n{table}")
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