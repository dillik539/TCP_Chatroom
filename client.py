import threading

from socket import *

host = 'localhost'
port_Number = 45673
client_address = (host, port_Number)
client = socket(AF_INET, SOCK_STREAM)
client.connect(client_address)

name = input('Enter username: ')
password = input('Enter password: ')


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'USERNAME':
                client.send(name.encode())
            elif message == 'PASSWORD':
                client.send(password.encode())
            else:
                print(message)
        except:
            print('An error occurred!')
            client.close()
            break


def write_message():
    while True:
        chat_message = f'{name}: {input()}'
        client.send(chat_message.encode())


if __name__ == '__main__':

    receive_message_thread = threading.Thread(target=receive_message)
    write_message_thread = threading.Thread(target=write_message)
    receive_message_thread.start()
    write_message_thread.start()
