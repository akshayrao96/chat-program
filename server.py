import threading
import socket

host = 'localhost'
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            if message.endswith('has left the chat.'):
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast(f'{name} has left the room!'.encode('utf-8'))
                names.remove(name)
                break
            else:
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
        client, address = server.accept()  # accepts connections from clients
        print(f'connection is established with {str(address)}')
        client.send('name?'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)
        print(f'Client is {name}'.encode('utf-8'))
        broadcast(f'{name} has joined the room!'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


if __name__ == "__main__":
    receive()
