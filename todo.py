import sqlite3
import sys
from datetime import datetime
class Manager:
    def __init__(self, user_id, databaseName="todolist.db")
        self.user_id = user_id
        self.databaseName = databaseName
    def _connect(self):
        connection = sqlite3.connect(self.db_name)
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
        pass
    def delete_i