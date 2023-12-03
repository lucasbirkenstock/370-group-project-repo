# For use with login.py
import socket 
import sqlite3 
import hashlib
import threading

# Make the server a TCP internet socket
theServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost
theServer.bind(("localhost", 9999))

theServer.listen()

def handle_connection(username, password):
    # Hash the password before comparing to db
    password = hashlib.sha256(password).hexdigest()

    # Connect to the db
    connection = sqlite3.connect("usercredentials.db")

    # Create cursor for interacting with db
    theCursor = connection.cursor()


    theCursor.execute("SELECT * FROM usercredentials WHERE username = ? AND password = ?", (username, password))

    # If the above query returns anything, that means correct credentials
    if (theCursor.fetchall()):
        # Login successful: insert code for what to do when login is successful
        print("Login success")
    else:
        # Login fail: insert code for what to do when login fails
        print("Login failure")