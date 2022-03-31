import threading
from socket import *

host = '127.0.0.1'

port = 45673

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))

server.listen()

clients_IP = []
clients_name = []


def broadcast_message(message):
    for IPs in clients_IP:
        IPs.send(message)


def manage_client(client_ip):
    while True:
        try:
            message = client_ip.recv(1024)
            broadcast_message(message)
        except:
            index = clients_IP.index(client_ip)
            clients_IP.remove(client_ip)
            client_ip.close()
            client_name = clients_name(index)
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
        clients_IP.append(client)
        print(f'This is {name}')
        broadcast_message(f'{name} joined the chatroom!'.encode())
        client.send(f'Connected to the chatroom!'.encode())

        thread = threading.Thread(target=manage_client)
        thread.start()


if __name__ == '__main__':

    print('Server is listening......')

    receive()
