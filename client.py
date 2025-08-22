'''
This is a client side TCP chat program which connects to the server,
authenticates with username and password, and allows the user to run multiple
tasks (receiving and sending message) from and to other users/server
at the same time using threads.
'''

import threading

from socket import * #allows low-level networking (TCP/UDP) capabilities.
'''set up the client'''
def connect_to_server():
    server_ip = input("Enter server IP address (default: localhost): ") or "localhost"
    server_port = int(input("Enter server port (default: 45673): ") or 45673)
    server = (server_ip, server_port)
    client_socket = socket(AF_INET,SOCK_STREAM) #TCP socket
    client_socket.connect(server) #connects to server
    return client_socket #returns socket for further use

# host = 'localhost'   #server's IP
# port_Number = 45673    #server's port where it listens for message
# client_address = (host, port_Number)   #This is server, not to confuse with client.

# #create a TCP socket using IPV4
# client = socket(AF_INET, SOCK_STREAM)

# #connect socket (client's) to the server
# client.connect(client_address)

name = input('Enter username: ')
password = input('Enter password: ')

'''
This defines how client handles message received from the server. This
constantly wait for the data from the server, receives bytes in chunk(1024),
and decode to plain string.
'''
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

'''
This function continuously takes input from the user, encode it as byte
and sends it to the server
'''
def write_message():
    while True:
        chat_message = f'{name}: {input()}'
        client.send(chat_message.encode())


if __name__ == '__main__':

    receive_message_thread = threading.Thread(target=receive_message)
    write_message_thread = threading.Thread(target=write_message)
    receive_message_thread.start()
    write_message_thread.start()
