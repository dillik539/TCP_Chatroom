<!-- @format -->

TCP Chat Application

This README provides guidance for both developers and end-users of the TCP chat application.

#TODO: Table of contents here

Overview

A multi-user TCP chat application implemented in Python. The application supports:

- Secure authentication using bcrypt password hashing
- Public chat (broadcast message to all users)
- Direct message (one-to-one messages)
- Simultaneous multiple client connections with threaded handling

**\*** For Developers\*\*\*
Project Structure
project_root/
|
|- server.py #server-side Python code
|- client.py #client-side Python code
|- user_information.txt #Stores username and hashed password
|- README.md #This file

Setup and Installation:

1. Ensure Python 3.10+ is installed
2. Install required packages:
   pip install bcrypt
3. Ensure both server.py and client.py are in the same directory

Running the Server:
python server.py
