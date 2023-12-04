import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

def attemptLogin(username, password):  
    client.send(username.encode())
    client.send(password.encode())
    # Print login fail or success from loginServer
    print(client.recv(1024).decode())

attemptLogin("lucas123", "password123")
