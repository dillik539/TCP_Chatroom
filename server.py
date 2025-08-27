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
This function sends the given message(in bytes) to every active clients
'''
def broadcast_message(message, sender = None):
    with lock:      #prevents race conditions while iterating
        for client in clients:
            try:
                if sender and client == sender:
                    continue        #skip the broadcast to the sender
                client.send(message)
            except:     #if sending fails, remove the broken socket and close it.
                idx = clients.index(client)
                client.close()
                clients.remove(client)
                name = clients_name.pop(idx)
                print(f'Removed dead client {name}')

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
            broadcast_message(f'{username}:{message.decode()}'.encode())
        except:
            with lock:      #makes thread safe
                if client in clients:
                    idx = clients.index(client)
                    clients.remove(client)
                    clients_name.pop(idx)
            broadcast_message(f'{username} left the chatroom!'.encode())
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
This function addresses how the received message is handled.
'''
def receive():
    while True:
        client, address = server.accept() #Blocks everything until a new TCP connection is accepted, and returns addresses and socket
        client.send('USERNAME'.encode())
        user = client.recv(1024).decode()
        client.send('PASSWORD'.encode())
        password = client.recv(1024).decode()
        clients.append(client) #TODO: Authenticate first and then append
        if authenticate(user, password):
            print(f'Connected with {user}')
            broadcast_message(f'{user} joined the chatroom!'.encode())
            client.send(f'Connected to the server!'.encode())
        else:
            #TODO: Address the auto registration feature here.
            add_user(user, password)
            # users_list[user] = password
            print(f'New user {user} joined!')
            client.send(f'Welcome to chatroom!'.encode())
            broadcast_message(f'New user {user} joined the chatroom!'.encode())

        thread = threading.Thread(target=manage_client, args=(client,))
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
            # line = file.readline()
            # while line:
            #     line = line.split(',')
            #     users_list[line[0].strip()] = line[1].strip()
            #     # users.append(line[0].strip())
            #     # passwords.append(line[1].strip())
            #     line = file.readline()
    except FileNotFoundError:
        print('No user file found! Starting with empty user list.')


if __name__ == '__main__':
    file_path = 'user_information.txt'
    print('Server is listening......')
    get_user_info(file_path)

    receive()

