import sqlite3
import sys
import random 
class User:
    def __init__(self, databaseName="todolist.db"):
        self.databaseName = databaseName
        self.loggedIn = False
        self.userID = ""
    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        try: 
            connection = sqlite3.connect(self.databaseName)
        except: 
            print("Failed database connection.")
            sys.exit()
        cursor = connection.cursor()
        query = "SELECT id, password FROM User WHERE username=?"
        data = (username,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        if(len(result == 0)):
            print("\nUsername or password is incorect.")
            self.userID = ""
            self.loggedIn = False
            return False
        id = result[0][0]
        token = result[0][1]
        cursor.close()
        connection.close()
        if password == token:
            print("\nLogging user in...")
            self.userID = id
            self.loggedIn = True
            return True
        else:
            print("\nUsername or password is incorect.")
            self.userID = ""
            self.loggedIn = False
            return False
    
    def logout(self):
        self.userID = ""
        self.loggedIn = False
        return False
    
    def createAccount(self):
        try: 
            connection = sqlite3.connect(self.databaseName)
        except: 
            print("Failed database connection.")
            sys.exit()
        cursor = connection.cursor()
        while(1):
            return 
    def getLoggedIn(self):
        return self.loggedIn
    def gerUserID(self):
        return self.userID