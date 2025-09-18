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

---

## For Developers

### Project Structure

```
project_root/
│
├─ server.py          # Server-side Python code
├─ client.py          # Client-side Python code
├─ user_information.txt  # Stores username and hashed password
└─ README_combined.md  # This document
```

### Setup & Installation

1. Ensure Python 3.10+ is installed.
2. Install required packages:

```bash
pip install bcrypt
```

3. Ensure both `server.py` and `client.py` are in the same directory.

### Running the Server

```bash
python server.py
```

- The server listens on `localhost:45673` by default.
- It maintains a thread for each client connection.
- Loads existing user credentials from `user_information.txt`.

### Running the Client

```bash
python client.py
```

- Connects to the server and prompts for username/password.
- Spawns two threads: one for sending messages, one for receiving.

### Features

1. **Threaded client handling** - allows multiple clients to log in and chat simultaneously.
2. **Secure password storage** - uses bcrypt hashing for stored passwords.
3. **Public messaging** - broadcasts messages to all connected users.
4. **Direct messaging** - private messages using `/dm <username> <message>`.
5. **Automatic password migration** - legacy plaintext passwords are automatically hashed upon first login.

### Extending or Modifying the Application

- To change port or host, modify the `HOST` and `PORT` variables in `server.py` and `client.py`.
- To enhance security, consider adding SSL/TLS support.
- Additional commands can be implemented in `send_message()` (client) and `manage_client()` (server).
- To persist chat history, implement logging to a file in `manage_client()`.

---

## For Users

### Getting Started

1. Run the server (`server.py`) on a machine you have access to.
2. Run the client (`client.py`) on the same or another machine in your network.
3. Enter the server IP (`localhost` by default) and port (`45673` by default).

### Login & Registration

- If you are an existing user, enter your username and password.
- New users will be automatically registered, and passwords are securely stored.

### Public Chat

- Simply type your message and press Enter.
- Messages will be broadcast to all connected users.
- Format: `username: message`

### Direct Messaging

- Send a private message using:

```
/dm <username> <message>
```

- Example: `/dm Alice Hello, Alice!`
- The recipient will only see your private message.

### Commands

- `/quit` - Exit the chatroom.
- `/dm <username> <message>` - Send a private message.

### Exiting the Chat

- Type `/quit` and press Enter.
- The client will notify the server and close the connection safely.

---

End of README.
