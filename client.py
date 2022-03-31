import threading

from socket import *

host = 'localhost'
port_Number = 45673
client_address = (host, port_Number)
client = socket(AF_INET, SOCK_STREAM)
client.connect(client_address)

