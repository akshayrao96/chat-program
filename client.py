import threading
import socket

host = 'localhost'
port = 9000

name = input('Choose username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'name?':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = input("")
        if message.lower() in ['q', 'quit']:
            client.send(f'{name} has left the chat.'.encode('utf-8'))
            client.close()
            break
        else:
            client.send(f'{name}: {message}'.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
