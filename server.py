import threading
from socket import *

host = 'localhost'

port = 45673

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))

server.listen()

users_list = {}
clients = []
clients_name = []

users = []
passwords = []


def broadcast_message(message):
    for client in clients:
        client.send(message)


def manage_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast_message(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            client_name = clients_name[index]
            clients_name.remove(client_name)
            broadcast_message(f'{client_name} left the chatroom!'.encode())
            break


def authenticate(user, password):
    for u, p in users_list.items():
        if user == u and password == p:
            return True
        else:
            return False


def receive():
    while True:
        client, address = server.accept()
        client.send('USERNAME'.encode())
        user = client.recv(1024).decode()
        client.send('PASSWORD'.encode())
        password = client.recv(1024).decode()
        if authenticate(user, password):
            print(f'Connected with {user}')
            broadcast_message(f'{user} joined the chatroom!'.encode())
            client.send(f'Connected to the server!'.encode())
        else:
            users_list[user] = password
            print(f'New user {user} joined!')
            client.send(f'Welcome to chatroom!'.encode())
            broadcast_message(f'New user {user} joined the chatroom!'.encode())
        print(f'The new user is {user}')
        print(f'The new password is {password}')
        print('The new user list is', users_list)
        thread = threading.Thread(target=manage_client, args=(client,))
        thread.start()


def get_user_info(path):
    try:
        with open(path) as file:
            line = file.readline()
            while line:
                line = line.split(',')
                users_list[line[0].strip()] = line[1].strip()
                # users.append(line[0].strip())
                # passwords.append(line[1].strip())
                line = file.readline()
    except:
        print('File not found!')


if __name__ == '__main__':
    file_path = 'user_information.txt'
    print('Server is listening......')
    get_user_info(file_path)
    print('Users List\n')
    print(users, '\n')
    print('Passwords List\n')
    print(passwords, '\n')
    print(users_list)

    receive()

