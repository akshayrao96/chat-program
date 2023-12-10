import socket
import select
from server.model import ClientList, MessageList

import socket
import select
from server.model import ClientList, MessageList


class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.client_list = ClientList()
        self.inputs = [self.socket]
        self.outputs = []
        self.message_buffer = MessageList()

    def run(self):
        print(f"Server is running on {self.host}:{self.port}")
        try:
            while True:
                readable, writable, exceptional = select.select(
                    self.inputs, self.outputs, self.inputs)

                for s in readable:
                    if s is self.socket:
                        # Accept new connection
                        connection, client_address = s.accept()
                        print(f"New connection from {client_address}")
                        connection.setblocking(0)
                        self.inputs.append(connection)
                        # You could add a welcome message or send client number here
                        self.client_list.add(
                            f"Client{len(self.inputs) - 1}", connection)
                    else:
                        data = s.recv(1024)
                        if data:
                            print(
                                f"Received data: {data.decode()} from {s.getpeername()}")
                            self.message_buffer.add(data.decode())
                            if s not in self.outputs:
                                self.outputs.append(s)
                        else:
                            print(f"Closing connection to {s.getpeername()}")
                            if s in self.outputs:
                                self.outputs.remove(s)
                            self.inputs.remove(s)
                            s.close()

                            self.client_list.drop_by_connection(s)

                for s in writable:
                    try:
                        next_msg = self.message_buffer.get_next_message()
                        if next_msg:
                            s.send(next_msg.encode())
                    except Exception as e:
                        print(f"Sending message failed: {e}")

                for s in exceptional:
                    self.inputs.remove(s)
                    if s in self.outputs:
                        self.outputs.remove(s)
                    s.close()
                    self.client_list.drop_by_connection(s)
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            self.exit()

    def exit(self):
        for s in self.inputs:
            s.close()
        self.socket.close()
