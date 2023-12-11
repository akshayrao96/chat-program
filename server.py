import threading
import socket
import sys

# Initializes host, port, and server socket configurations
host = 'localhost'
port = 9001

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
            message = client.recv(1024).decode('utf-8')
            if message == "/quit":
                index = clients.index(client)
                name = names[index]
                broadcast(f"{name} has left the room!\n".encode('utf-8'))
                names.remove(name)
                clients.remove(client)
                client.close()
                break
            else:
                broadcast(message.encode('utf-8'))
        except Exception as e:
            index = clients.index(client)
            name = names[index]
            broadcast(f"{name} has left the room!\n".encode('utf-8'))
            names.remove(name)
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        print('Server is running..')
        client, address = server.accept()

        print(f'connection is established with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        if name.lower() in ['quit', 'q']:
            client.send('Server is shutting down'.encode('utf-8'))
            client.close()
            continue

        broadcast(f'{name} has joined the room!\n'.encode('utf-8'))

        names.append(name)
        clients.append(client)

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
