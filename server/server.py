import threading
import socket

host = 'localhost'
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
names = []

# Broadcasts messages to all clients


def broadcast(message):
    for client in clients:
        client.send(message)

# Handles clients connections


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} has left the room!'.encode())
            names.remove[name]
            break


def receive():
    while True:
        print('Server is running..')
        client, address = server.accept()  # accepts connections from clients
