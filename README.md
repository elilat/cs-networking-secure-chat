# Secure Multi-Client Chat Application

## Overview
This project implements a secure, multi-client chat application using Python. It features user authentication, end-to-end encryption, and a basic command system. The application consists of a server script and a client script, both utilizing sockets and SSL for secure communication. This project demonstrates advanced concepts in network programming, cryptography, and secure system design. It was chosen as my submission for the computer networks course in the MS Computer Science program at the Lebanese American University (LAU).

## Features
- User authentication with hashed passwords
- End-to-end encryption using RSA public-key cryptography
- Support for multiple concurrent clients
- Private messaging functionality (/whisper command)
- List of online users (/list command)
- Secure socket communication with SSL/TLS
- Broadcast messaging to all connected clients
- Error handling and graceful disconnection management

## Requirements
- Python 3.7+
- PyCryptodome library for cryptographic operations
- OpenSSL for generating SSL certificates
- Additional Python packages:
  - `socket` (built-in)
  - `ssl` (built-in)
  - `threading` (built-in)
  - `json` (built-in)
  - `hashlib` (built-in)
  - `base64` (built-in)
  - `getpass` (built-in)

## Installation

1. Ensure you have Python 3.7+ installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Install OpenSSL:
   - On macOS (using Homebrew): `brew install openssl`
   - On Ubuntu/Debian: `sudo apt-get install openssl`
   - On Windows: Download from [openssl.org](https://www.openssl.org/source/)

3. Clone the repository:
   ```sh
   git clone https://github.com/ellisisaac/cs-networking-secure-chat.git
   cd secure-chat-app
   ```

4. Set up a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

5. Install the required packages:
   ```sh
   pip install pycryptodome
   ```

6. Generate SSL certificates for the server:
   ```sh
   openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
   ```
   Follow the prompts to enter information for your self-signed certificate.

## Usage

1. Start the server:
   ```sh
   python server.py
   ```
   The server will start and listen for incoming connections on localhost:8443.

2. Run the client(s) in separate terminal windows:
   ```sh
   python client.py
   ```
   You can run multiple clients to simulate different users.

3. Follow the prompts to log in:
   • Enter a username (e.g., "alice" or "bob")
   • Enter the password (use "password" for the demo accounts)

4. Start chatting:
   • Type messages and press Enter to send to all users
   • Use commands for specific actions (see Commands section)

## Commands

• /whisper <username> <message>: Send a private message to a specific user
   Example: /whisper bob Hello, Bob! This is a private message.
• /list: Show a list of currently online users

## Security Features

• Password hashing: User passwords are hashed using SHA-256 before storage and transmission
• End-to-end encryption: All messages are encrypted using RSA public-key cryptography (2048-bit keys)
• SSL/TLS: All network communication is encrypted using SSL/TLS (TLS 1.2+)
• Secure key exchange: Public keys are exchanged securely during the connection process
• No plaintext storage: Passwords and messages are never stored in plaintext

## Limitations

• This application is a demonstration and should not be used in production environments without further security enhancements.
• User credentials are stored in memory and are lost when the server restarts.
• The RSA key generation process may be slow on some systems.
• The current implementation does not include perfect forward secrecy.
• There is no message persistence or offline message delivery.

## Troubleshooting

• If you encounter SSL certificate errors, ensure that you've correctly generated the SSL certificates and that they are in the same directory as the server script.
• If a client cannot connect, verify that the server is running and that you're using the correct hostname and port.
• For "Address already in use" errors, ensure no other instance of the server is running on the same port.
• If you experience slow performance, consider reducing the RSA key size (not recommended for production use).

## Security Considerations

• The self-signed SSL certificate should be replaced with a properly issued certificate for production use.
• Implement additional security measures such as rate limiting and input validation for production environments.
• Regularly update all dependencies to ensure you have the latest security patches.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project uses the PyCryptodome library for cryptographic operations.
OpenSSL is used for generating SSL certificates.
Inspired by various open-source chat applications and cryptography tutorials.
Special thanks to Dr. Haidar Harmanani of the Computer Science department at the Lebanese American University (LAU) for his invaluable support.

## Authors

Ellis Isaac @ellisisaac

For more detailed information about the project's architecture and implementation, please refer to the DOCUMENTATION.md file.