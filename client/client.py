import socket
import select
from client.model import MessageList


class Client:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.message_list = MessageList()
        self.running = True

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def receive_messages(self):
        while self.running:
            ready_to_read, _, _ = select.select([self.socket], [], [], 0.1)
            for sock in ready_to_read:
                data = sock.recv(1024)
                if data:
                    print(f"Received: {data.decode()}")
                else:
                    print("Server closed the connection")
                    self.running = False
                    break

    def run(self):
        try:
            # Start listening for messages from the server
            print("Connected to the server. Type your messages below:")
            while self.running:
                message = input("Enter message: ")
                if message.lower() == 'quit':
                    self.running = False
                else:
                    self.send_message(message)
                    self.receive_messages()
        except KeyboardInterrupt:
            print("Client interrupted.")
        finally:
            self.exit()

    def exit(self):
        self.socket.close()
        print("Connection closed.")
