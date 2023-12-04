# For use with login.py
import socket 
import sqlite3 
import hashlib
import threading


# Make the server a TCP internet socket
theServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost
theServer.bind(("localhost", 9998))

theServer.listen()

# Login attempt function
# c = client
def handle_connection(c):
    
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024)
    # Hash the password before comparing to db
    password = hashlib.sha256(password).hexdigest()

    # Connect to the db
    connection = sqlite3.connect("usercredentials.db")

    # Create cursor for interacting with db
    theCursor = connection.cursor()

    # Select any row where the username and password match the function inputs
    theCursor.execute("SELECT * FROM usercredentials WHERE username = ? AND password = ?", (username, password))

    # If the above query returns anything, that means correct credentials
    if (theCursor.fetchall()):
        # Login successful: insert code for what to do when login is successful
        print("Login success")
    else:
        # Login fail: insert code for what to do when login fails
        print("Login failure")
    
    # Close the connections
    theCursor.close()
    connection.close()

while True: 
    client, address = theServer.accept()
    threading.Thread(target=handle_connection, args=(client, )).start()
    