import sqlite3
import sys

try:
    connection = sqlite3.connect("todolist.db")
    print("Successful connection.")
except:
    print("Failed Connection.")
    sys.exit()
cursor = connection.cursor()
print()
print("Creating User table")
cursor = connection.cursor()
users = """CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);"""
cursor.execute(users)
print("Created User table.")
print()
print("Creating Assignments table")
asignments = """CREATE TABLE IF NOT EXISTS Assignments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
description TEXT,
due_time DATETIME NOT NULL,
completed BOOLEAN DEFAULT 0,
FOREIGN KEY(user_id) REFERENCES users(id)
);"""
cursor.execute(asignments)
print("Created Assignments table.")
print()
print("Creating Meetings table")
meetings = """CREATE TABLE IF NOT EXISTS meetings (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
description TEXT,
meeting_time DATETIME NOT NULL,
completed BOOLEAN DEFAULT 0,
FOREIGN KEY(user_id) REFERENCES users(id)
);"""
cursor.execute(meetings)
print("Created Meetings table.")
print()
print("Creating Reminders table")
reminders = """CREATE TABLE IF NOT EXISTS reminders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
description TEXT,
reminder_time DATETIME NOT NULL,
completed BOOLEAN DEFAULT 0,
FOREIGN KEY(user_id) REFERENCES users(id)
);"""
cursor.execute(reminders)
print("Created User table.")
print()
connection.commit()
print()
cursor.close()
connection.close()

