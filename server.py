import threading
from socket import *

host = 'localhost'

port = 45673

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))

server.listen()

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


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('NAME'.encode())
        name = client.recv(1024).decode()
        clients_name.append(name)
        clients.append(client)
        print(f'The nickname is {name}')
        broadcast_message(f'{name} joined the chatroom!'.encode())
        client.send(f'Connected to the server!'.encode())

        thread = threading.Thread(target=manage_client, args=(client,))
        thread.start()


def get_user_info(path):
    try:
        with open(path) as file:
            line = file.readline()
            while line:
                line = line.split(',')
                users.append(line[0].strip())
                passwords.append(line[1].strip())
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
    print(passwords)

    receive()
