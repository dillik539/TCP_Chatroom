import threading
from socket import *

HOST = 'localhost'      #server listens only on local machine
PORT = 45673

server = socket(AF_INET, SOCK_STREAM)       #server socket (TCP-IP, IPV4)
server.bind((HOST, PORT))
server.listen()     #puts the server socket in listening mode

print(f'Server started on {HOST}:{PORT},waiting for connections.....')

users_list = {}         #dictionary (username, password) loaded from locally stored file
clients = []        #list of active client sockets
clients_name = []       #list of usernames corresponding to client sockets
lock = threading.Lock()     #This ensures safe access from multiple threads.
users = []      #list to capture only users
passwords = []      #list to capture only passwords

'''
This function sends the given message(in bytes) to every active clients.
It allows the developer whether to broadcast the message back to the sender
or not to broadcast to the sender simply by switching include_sender
parameter to True/False.

:param message: message to send (in bytes)
:param sender: the client socket that sends the message
:param include_sender: sends the message back to sender, if this is set to True
'''
def broadcast_message(message, sender = None, include_sender = False):
    with lock:      #prevents race conditions while iterating
        for client in clients:
            try:
                #skip the sender if include_sender is set to False
                if not include_sender and sender and client == sender:
                    continue        #skip the broadcast to the sender
                client.send(message)
            except:     #if sending fails, remove the broken socket and close it.
                idx = clients.index(client)
                client.close()
                clients.remove(client)
                name = clients_name.pop(idx)
                print(f'Removed disconnected client {name}')

'''
This function continuously loops to receive message from the client,
broadcast the received message to all other clients, and in case any 
socket becomes inactive, removes that socket and associated username
from the lists.
'''
def manage_client(client, username):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise ConnectionError
            #Broadcast to others and optionally back to sender too. change include_sender to false if you don't want to echo back to sender.
            broadcast_message(f'{message.decode()}'.encode(),sender = client, include_sender=True)
        except:
            with lock:      #makes thread safe
                if client in clients:
                    idx = clients.index(client)
                    clients.remove(client)
                    clients_name.pop(idx)
            #notifies only others that the user has left       
            broadcast_message(f'{username} left the chatroom!'.encode(), sender = client, include_sender=False)
            
            print(f'{username} disconnected.')
            client.close()
            break

'''
This function authenticates the user with the (username, password) combination
'''
def authenticate(user, password):
    return users_list.get(user) == password

'''
This function adds user (username, password) combination to the file
'''
def add_user(name, password):
    path = 'user_information.txt'
    with open(path, 'a') as file:
        #TODO: Encrypt/hash the plain text password for more security
        file.write(name + ',' + password + '\n')
    users_list[name] = password     #updates in-memory dictionary of userlist

'''
This function manages authentication and launching client management
for each new connection in its own thread so that each user
can type in username and password simultenously instead of waiting for
one client to be authenticated.
'''

def manage_new_client(client, address):
    try:
        print(f'Incoming connection from {address}')

        #Ask client for login information
        client.send('USERNAME'.encode())
        user = client.recv(1024).decode().strip()
        client.send('PASSWORD'.encode())
        password = client.recv(1024).decode().strip()
        
        with lock:
            if authenticate(user, password):
                print(f'{user} authenticated successfully!')
            else:
                #TODO: Address the auto registration feature here.
                add_user(user, password)
                client.send('Welcome new user!'.encode())
                print(f'Registered new user {user}.')
            clients.append(client)
            clients_name.append(user)

        #notifies only other clients about new user
        broadcast_message(f'{user} joined the chatroom!'.encode(),sender = client, include_sender= False)
    
        #sends a direct welcome message to just this client.
        client.send(f'Welcome, {user}! You are now connected.'.encode())

        #switch to chat management
        manage_client(client, user)

    except Exception as e:
        print(f'Error occured while handling client {address}: {e}')
        client.close()

'''
This function addresses how the received message is handled.
Each new connection is handled seperately in its own thread.
'''

def receive():
    while True:
        client, address = server.accept()

        #starts a new thread that handle this client's authentication and chat management.
        thread = threading.Thread(target=manage_new_client, args=(client,address),daemon=True)
        thread.start()

'''
This function loads users from the file to the in-memory state list
'''
def get_user_info(path):
    try:
        with open(path) as file:
            for line in file:
                if "," in line:
                    user, pwd = line.strip().split(",", 1)
                    users_list[user] = pwd
    except FileNotFoundError:
        print('No user file found! Starting with empty user list.')


if __name__ == '__main__':
    file_path = 'user_information.txt'
    get_user_info(file_path)

    receive()

