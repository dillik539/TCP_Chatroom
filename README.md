<!-- @format -->

# TCP Chat Application

This README provides guidance for both **developers** and **end-users** of the TCP chat application.

---

## Table of Contents

1. [Overview](#overview)
2. [For Developers](#for-developers)

   - [Project Structure](#project-structure)
   - [Setup & Installation](#setup--installation)
   - [Running the Server](#running-the-server)
   - [Running the Client](#running-the-client)
   - [Features](#features)
   - [Testing](#testing)
   - [Extending or Modifying the Application](#extending-or-modifying-the-application)

3. [For Users](#for-users)

   - [Getting Started](#getting-started)
   - [Login & Registration](#login--registration)
   - [Public Chat](#public-chat)
   - [Direct Messaging](#direct-messaging)
   - [Commands](#commands)
   - [Exiting the Chat](#exiting-the-chat)

---

## Overview

A multi-user TCP chat application implemented in Python. The application supports:

- Secure authentication using bcrypt password hashing
- Public chat (broadcast messages to all users)
- Direct messaging (private one-to-one messages)
- Simultaneous multiple client connections with threaded handling
- **Unit testing support** with `unittest`

---

## For Developers

### Project Structure

```
project_root/
│
├─ server.py             # Server-side Python code
├─ client.py             # Client-side Python code
├─ user_information.txt  # Stores username and hashed password
├─ test_server.py        # Unit tests for server functions
├─ test_users.txt        # Test-specific user credentials (created during tests)
└─ README.md             # This document
```

---

### Setup & Installation

1. Ensure Python 3.10+ is installed.
2. Install required packages:

```bash
pip install bcrypt
```

3. Ensure both `server.py` and `client.py` are in the same directory.

---

### Running the Server

```bash
python server.py
```

- The server listens on `localhost:45673` by default.
- It maintains a thread for each client connection.
- Loads existing user credentials from `user_information.txt`.

---

### Running the Client

```bash
python client.py
```

- Connects to the server and prompts for username/password.
- Spawns two threads: one for sending messages, one for receiving.

---

### Features

1. **Threaded client handling** – multiple clients can log in and chat simultaneously.
2. **Secure password storage** – bcrypt hashing ensures no plaintext passwords are stored.
3. **Public messaging** – broadcasts messages to all connected users.
4. **Direct messaging** – private messages using `/dm <username> <message>`.
5. **Automatic password migration** – legacy plaintext passwords are automatically hashed upon first login.
6. **Unit tests** – validate authentication, user registration, and direct messaging functionality.

---

### Testing

Run the unit tests with:

```bash
python -m unittest test_server.py
```

#### What’s tested:

- `add_user_hashed()` – verifies bcrypt is used and no plaintext passwords are stored.
- `authenticate()` – checks correct password, wrong password, and non-existent user cases.
- `manage_private_message()` – validates direct messaging (success & user not found).

> Tests use a `DummySocket` class to simulate sending/receiving without real network connections.
> Test users are stored in **test_users.txt** (separate from production `user_information.txt`).

---

### Extending or Modifying the Application

- To change port or host, modify the `HOST` and `PORT` variables in both `server.py` and `client.py`.
- For enhanced security, consider adding SSL/TLS support.
- Additional commands can be added inside `send_message()` (client) or `manage_client()` (server).
- To persist chat history, implement logging in `manage_client()`.

---

## For Users

### Getting Started

1. Run the server (`server.py`).
2. Run the client (`client.py`) on the same or another machine in your network.
3. Enter the server IP (`localhost` by default) and port (`45673` by default).

---

### Login & Registration

- If you are an existing user, enter your username and password.
- New users will be automatically registered, with passwords securely stored using bcrypt.

---

### Public Chat

- Type your message and press Enter.
- Messages will be broadcast to all connected users.
- Format:

```
username: message
```

---

### Direct Messaging

- Send a private message using:

```
/dm <username> <message>
```

- Example:

```
/dm Alice Hello, Alice!
```

- Only Alice will see the private message.

---

### Commands

- `/quit` – Exit the chatroom.
- `/dm <username> <message>` – Send a private message.

---

### Exiting the Chat

- Type `/quit` and press Enter.
- The client will notify the server and close the connection safely.

---

End of README.
