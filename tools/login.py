import sqlite3
import hashlib

# Installing an sqlite extension is reccommended for working on this


# Set up connection to sqlite database
connection = sqlite3.connect("usercredentials.db")

# Set up cursor
theCursor = connection.cursor()

# Initialize database if not already existing
# Three columns: id, user, password

theCursor.execute("""
CREATE TABLE IF NOT EXISTS usercredentials(
                  id INTEGER PRIMARY KEY,
                  username VARCHAR(255) NOT NULL, 
                  password VARCHAR(255) NOT NULL
)
""")

# Example credentials
# In database, store username and a hashed password converted to hex
exampleUsername1, examplePassword1 = "lucas123", hashlib.sha256("password123".encode()).hexdigest()

# Insert sample data
theCursor.execute("INSERT INTO usercredentials (username, password) VALUES (?, ?)", (exampleUsername1, examplePassword1))

# Actually send/save the data
connection.commit()