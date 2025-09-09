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

'''
This defines how client handles message received from the server. This
constantly wait for the data from the server, receives bytes in chunk(1024),
and decode to plain string and display to the user.
'''
def receive_message(client):
    '''
    Continuously listen for messages from the server and display them.
    '''
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except:
            print('Connection error! Closing client.')
            client.close()
            break

'''
This function continuously takes input from the user, encode it as byte
and sends it to the server
'''
def send_message(client, username):
    '''
    Continuously read user input and send it to the server.
    '''
    while True:
        chat_message = input()

        if chat_message.strip().lower() =='/quit':
            #notifies server before closing
            try:
                client.send(f'{username} has left the chat.'.encode())
            except:
                pass
            client.close()
            print('You have left the chatroom. Goodbye!')
            break
        #checks if it is a direct message
        try:
            if chat_message.strip().lower().startswith('/dm'):
                #sends the message as-is. Leave parsing in the hands of server
                client.send(chat_message.encode())
            else:
                client.send(f'{username}:{chat_message}'.encode())
        except:
            print('Error sending message. Closing client.')
            client.close()
            break

def main():
    client = connect_to_server()

    #handle login procedure
    server_msg = client.recv(1024).decode()
    if server_msg == "USERNAME":
        username = input('Enter username: ')
        client.send(username.encode())
    
    server_msg = client.recv(1024).decode()
    if server_msg == "PASSWORD":
        password = input('Enter password: ')
        client.send(password.encode())

    #Start threads for async send/receive
    recv_thread = threading.Thread(target=receive_message, args = (client,))
    send_thread = threading.Thread(target=send_message, args=(client, username))
    
    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()

if __name__ == '__main__':

    main()
