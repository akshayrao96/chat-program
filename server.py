import threading
import socket
import sys

# Initializes host, port, and server socket configurations
host = 'localhost'
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))

server.listen()

clients = []
names = []


# Sends all connected client a message


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
            names.remove(name)
            break


def receive():
    while True:
        print('Server is running..')
        client, address = server.accept()

        print(f'connection is established with {str(address)}')

        client.send('name?'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        if name.lower() == 'quit' or name.lower() == 'q':
            break

        names.append(name)
        clients.append(client)

        broadcast(f'{name} has joined the room!\n'.encode('utf-8'))

        client.send('you are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

    for client in clients:
        client.send('Server has shut down'.encode('utf-8'))
        client.close()

    server.close()
    print("Server has shut down successfully")
    sys.exit


if __name__ == "__main__":
    receive()
