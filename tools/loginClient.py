import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9998))

def attemptLogin(username, password):
    # Send the username to the server
    client.send(username.encode())

    # Receive the password prompt from the server
    password_prompt = client.recv(1024).decode()
    print(password_prompt)

    # Send the password to the server
    client.send(password.encode())

    # Receive and print the result from the server
    result = client.recv(1024).decode()
    print(result)

# Example usage
attemptLogin("lucas123", "password123")

# Close the client socket when done
client.close()