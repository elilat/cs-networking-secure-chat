# Secure Multi-Client Chat Application Documentation

## 1. Introduction
This secure multi-client chat application is designed to demonstrate various concepts in network programming, cryptography, and secure communication. It implements a client-server architecture with features such as user authentication, end-to-end encryption, and a basic command system. The application serves as an educational tool for understanding how to build secure networked applications and can be used as a foundation for more complex systems.

## 2. System Architecture

### 2.1 Server
The server is the central component of the application, responsible for:
- Accepting and managing client connections
- Authenticating users
- Routing messages between clients
- Handling commands
- Encrypting outgoing messages
- Managing the list of online users

The server uses a multi-threaded approach to handle multiple client connections simultaneously. Each client connection is managed in a separate thread, allowing for concurrent processing of client requests.

### 2.2 Client
The client is the user-facing component of the application, responsible for:
- Connecting to the server
- User authentication
- Generating and managing encryption keys
- Sending and receiving encrypted messages
- Handling user input and commands
- Decrypting incoming messages

The client uses a separate thread for receiving messages, allowing it to listen for incoming messages while simultaneously accepting user input.

## 3. Key Components

### 3.1 User Authentication
User authentication is implemented to ensure that only registered users can access the chat system. The process works as follows:

1. The server maintains a dictionary of registered users with their usernames and password hashes.
2. When a client connects, it prompts the user for a username and password.
3. The client hashes the password and sends the username and password hash to the server.
4. The server checks the provided credentials against its stored user data.
5. If the credentials are valid, the server allows the client to proceed; otherwise, it sends an authentication error.

### 3.2 Encryption
The application uses RSA public-key cryptography for end-to-end message encryption, ensuring that messages can only be read by their intended recipients. The encryption process works as follows:

1. When a client connects and authenticates, it generates an RSA key pair (public and private keys).
2. The client sends its public key to the server.
3. The server stores the public key associated with the client's user account.
4. When sending a message to a client, the server encrypts the message using the recipient's public key.
5. The client receives the encrypted message and decrypts it using its private key.

This approach ensures that even if the server is compromised, the attacker cannot read the contents of the messages without the clients' private keys.

### 3.3 SSL/TLS
All communication between the client and server is secured using SSL/TLS, providing an additional layer of security. This protects against eavesdropping and man-in-the-middle attacks on the network level. The SSL/TLS implementation:

1. Encrypts all data transmitted between the client and server.
2. Provides authentication of the server to the client.
3. Ensures the integrity of the transmitted data.

### 3.4 Command System
The application supports a basic command system, allowing users to perform special actions. The current implementation includes:

- `/whisper <username> <message>`: Sends a private message to a specific user.
- `/list`: Displays a list of currently online users.

The command system is extensible, allowing for easy addition of new commands in the future.

## 4. Code Explanation

### 4.1 Server (server.py)

#### Key Classes and Functions:

- `User` class:
  - Represents a user with attributes for username, password hash, public key, and connection.
  - Used to store and manage user data on the server.

- `handle_client(conn, addr)`:
  - Manages individual client connections.
  - Handles the authentication process.
  - Processes incoming messages and commands.
  - Routes messages to appropriate recipients.

- `broadcast(message, sender)`:
  - Sends a message to all connected clients except the sender.
  - Used for general chat messages and system announcements.

- `send_encrypted_message(user, message)`:
  - Encrypts a message using the recipient's public key.
  - Sends the encrypted message to the specified user.

- `start_server()`:
  - Initializes the server socket with SSL/TLS.
  - Listens for incoming connections.
  - Creates a new thread for each client connection.

### 4.2 Client (client.py)

#### Key Functions:

- `receive_messages(sock, private_key)`:
  - Runs in a separate thread.
  - Continuously listens for incoming messages from the server.
  - Decrypts messages using the client's private key.
  - Displays decrypted messages to the user.

- `start_client()`:
  - Manages the main client-side operations.
  - Connects to the server using SSL/TLS.
  - Handles user authentication.
  - Generates RSA key pair and sends the public key to the server.
  - Manages user input and sending of messages/commands.

## 5. Security Considerations

The application implements several security measures:

- Password hashing: Passwords are hashed before transmission and storage, protecting them even if the server data is compromised.
- End-to-end encryption: All messages are encrypted using RSA, ensuring that only the intended recipient can read them.
- SSL/TLS: All network communication is encrypted, protecting against network-level attacks.
- Server authentication: The SSL/TLS implementation authenticates the server to the client, preventing man-in-the-middle attacks.
- Separation of concerns: The server never stores or has access to clients' private keys, maintaining the integrity of the end-to-end encryption.

## 6. Limitations and Future Improvements

While the current implementation provides a solid foundation for a secure chat application, there are several areas for potential improvement:

- Persistent storage: Implement a secure database to store user credentials and message history.
- Improved key management: Implement key rotation and secure key storage mechanisms.
- Enhanced authentication: Add support for multi-factor authentication.
- File transfer: Implement secure file transfer functionality.
- Group chat: Add support for user-created chat rooms or channels.
- Offline messaging: Allow users to send messages to offline users, delivered upon their next login.
- GUI: Develop a graphical user interface for improved user experience.
- Push notifications: Implement push notifications for mobile clients.
- End-to-end encryption for metadata: Encrypt not just message content, but also metadata like recipient usernames.
- Perfect forward secrecy: Implement protocols like Double Ratchet for improved long-term security.

## 7. Conclusion

This secure multi-client chat application demonstrates key concepts in network programming, cryptography, and secure system design. It provides a practical example of how to implement user authentication, end-to-end encryption, and secure network communication. While it includes several important security features, it should be further enhanced before being considered for use in a production environment.

The modular design of the application allows for easy extension and improvement, making it an excellent starting point for more advanced secure communication systems. By studying and building upon this application, developers can gain valuable insights into the challenges and best practices of creating secure networked applications.

## Acknowledgements

Special thanks to Dr. Haidar Harmanani of the Computer Science department at the Lebanese American University (LAU) for his invaluable support.