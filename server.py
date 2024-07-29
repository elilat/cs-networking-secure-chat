# Created by Ellis Isaac
# This script implements a simple chat server with user authentication and encryption using SSL and RSA. 
# Users can send messages to the chat room or use commands to whisper to other users or list online users.

import socket
import ssl
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Class representing a user
class User:
    def __init__(self, username, password_hash):
        self.username = username  # Username of the user
        self.password_hash = password_hash  # Hashed password for authentication
        self.public_key = None  # RSA public key for message encryption
        self.connection = None  # Connection socket

# Dictionary to store users with their credentials
users = {
    "alice": User("alice", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),  # password: password
    "bob": User("bob", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8")  # password: password
}

# Function to handle each client connection
def handle_client(conn, addr):
    user = None  # Initialize the user as None
    try:
        # Authentication loop
        while not user:
            auth_data = json.loads(conn.recv(1024).decode())  # Receive authentication data
            username = auth_data['username']
            password_hash = auth_data['password_hash']
            if username in users and users[username].password_hash == password_hash:
                user = users[username]
                user.connection = conn
                conn.send(json.dumps({"status": "success", "message": "Authentication successful"}).encode())
            else:
                conn.send(json.dumps({"status": "error", "message": "Invalid credentials"}).encode())

        # Receive and set user's public key
        public_key_data = conn.recv(1024).decode()
        user.public_key = RSA.import_key(public_key_data)

        print(f"User {user.username} connected from {addr}")
        broadcast(f"User {user.username} has joined the chat", user)  # Notify other users

        while True:
            data = conn.recv(1024).decode()  # Receive messages from the user
            if not data:
                break
            message = json.loads(data)
            if message['type'] == 'command':
                handle_command(message, user, conn)  # Handle commands like /whisper or /list
            else:
                print(f"Message from {user.username}: {message['content']}")
                broadcast(f"{user.username}: {message['content']}", user)  # Broadcast messages to other users
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        if user:
            del users[user.username]  # Remove the user from the users dictionary
            broadcast(f"User {user.username} has left the chat", user)  # Notify other users
        conn.close()
        print(f"Connection from {addr} closed")

# Function to handle specific commands
def handle_command(message, user, conn):
    if message['content'].startswith('/whisper'):
        parts = message['content'].split(maxsplit=2)
        if len(parts) == 3:
            target_username = parts[1]
            content = parts[2]
            if target_username in users:
                send_encrypted_message(users[target_username], f"[Whisper from {user.username}] {content}")
            else:
                conn.send(json.dumps({"type": "error", "content": "User not found"}).encode())
    elif message['content'] == '/list':
        online_users = ', '.join(users.keys())
        conn.send(json.dumps({"type": "message", "content": f"Online users: {online_users}"}).encode())

# Function to broadcast messages to all users except the sender
def broadcast(message, sender):
    for username, user in users.items():
        if user != sender:
            send_encrypted_message(user, message)

# Function to send encrypted messages to a specific user
def send_encrypted_message(user, message):
    if user.public_key and user.connection:
        try:
            cipher = PKCS1_OAEP.new(user.public_key)
            encrypted_message = cipher.encrypt(message.encode())
            user.connection.send(json.dumps({"type": "message", "content": base64.b64encode(encrypted_message).decode()}).encode())
        except Exception as e:
            print(f"Error sending message to {user.username}: {e}")
    else:
        print(f"Cannot send encrypted message to {user.username}: Missing public key or connection")

# Function to start the server and listen for incoming connections
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8443))  # Bind to localhost on port 8443
    server.listen(5)  # Listen for up to 5 connections
    print("Server started, waiting for connections...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Load SSL certificate and key

    while True:
        client, addr = server.accept()  # Accept new connections
        try:
            conn = context.wrap_socket(client, server_side=True)  # Wrap the connection with SSL
            thread = threading.Thread(target=handle_client, args=(conn, addr))  # Start a new thread for the client
            thread.start()
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            client.close()

if __name__ == "__main__":
    start_server()  # Start the server when the script is run
