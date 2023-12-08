# For use with login.py
import socket 
import sqlite3 
import hashlib
import threading


# Make the server a TCP internet socket
theServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost
theServer.bind(("localhost", 8997))

theServer.listen()

# For Bryan: add user credentials to sql database 
def add_user_to_db(username, password):
    # Connect to the database
    connection = sqlite3.connect("usercredentials.db")

    # Cursor for interacting with the database
    theCursor = connection.cursor()

    # hash the password prior to adding
    password = hashlib.sha256(password.encode()).hexdigest()

    # Insert into DB
    theCursor.execute("INSERT INTO usercredentials (username, password) VALUES (?, ?)", (username, password))

    # Save changes
    connection.commit()

# Login attempt function
def handle_connection(client):
    # Receive username from the client
    username = client.recv(1024).decode()

    # Send prompt for password
    client.send("Password: ".encode())

    # Receive password from the client
    password = client.recv(1024).decode()

    # Hash the password before comparing to db
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Connect to the db
    connection = sqlite3.connect("usercredentials.db")

    # Create cursor for interacting with db
    theCursor = connection.cursor()

    # Select any row where the username and password match the function inputs
    theCursor.execute("SELECT * FROM usercredentials WHERE username = ? AND password = ?", (username, hashed_password))

    print("test")
    # If the above query returns anything, that means correct credentials
    if theCursor.fetchall():
        # Login successful: insert code for what to do when login is successful
        print("Login success")
        client.send("Login success".encode())
    else:
        # Login fail: insert code for what to do when login fails
        print("Login failure")
        client.send("Login failure".encode())
    
    # Close the connections
    theCursor.close()
    connection.close()

while True: 
    client, address = theServer.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()