# Created by Ellis Isaac
# This script implements a simple chat client with user authentication and encryption using SSL and RSA.
# The client connects to the server, authenticates the user, and sends/receives encrypted messages.

import socket
import ssl
import threading
import json
import getpass
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Function to receive and decrypt messages from the server
def receive_messages(sock, private_key):
    while True:
        try:
            data = sock.recv(1024).decode()  # Receive data from the server
            message = json.loads(data)
            if message['type'] == 'message':
                encrypted_message = base64.b64decode(message['content'])
                cipher = PKCS1_OAEP.new(private_key)
                decrypted_message = cipher.decrypt(encrypted_message).decode()  # Decrypt the message
                print(decrypted_message)
            elif message['type'] == 'error':
                print(f"Error: {message['content']}")
        except:
            print("An error occurred!")
            sock.close()
            break

# Function to start the client and connect to the server
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # In a real-world scenario, you should verify the server's certificate

    try:
        conn = context.wrap_socket(client, server_hostname='localhost')
        conn.connect(('localhost', 8443))  # Connect to the server
        print("Connected to server")

        # Authentication loop
        while True:
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            password_hash = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
            auth_data = json.dumps({"username": username, "password_hash": password_hash})
            conn.send(auth_data.encode())  # Send authentication data
            response = json.loads(conn.recv(1024).decode())
            if response['status'] == 'success':
                print(response['message'])
                break
            else:
                print(response['message'])

        # Generate RSA key pair and send public key to the server
        key = RSA.generate(2048)
        private_key = key
        public_key = key.publickey()
        conn.send(public_key.export_key().decode().encode())

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(conn, private_key))
        receive_thread.start()

        # Send messages to the server
        while True:
            message = input()
            if message.startswith('/'):  # Command messages
                conn.send(json.dumps({"type": "command", "content": message}).encode())
            else:  # Regular messages
                conn.send(json.dumps({"type": "message", "content": message}).encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    start_client()  # Start the client when the script is run
