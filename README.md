# Chat Application - CS5700 Fundamentals of Networking

## Overview

This project is a chat application developed as part of the CS5700 - Fundamentals of Networking course. It's designed to explore client-server socket connections in Python, demonstrating the application of TCP/IP networking concepts. The project consists of three main components: `server.py`, `client.py`, and `chat-client.py`, each playing a vital role in the chat system.

## Repository Link

[GitHub Repository](https://github.com/akshayrao96/chat-program)

## Features

- **Server (`server.py`)**: Configured to listen on port 9000, handles incoming client connections, and broadcasts messages to all connected clients.
- **Client (`client.py`)**: A basic client implementation that establishes a connection with the server and manages communication.
- **Chat Client (`chat-client.py`)**: An advanced version of the client with a graphical user interface, offering a real-world chat application experience.

## Installation

1. Clone the repository: `git clone https://github.com/akshayrao96/chat-program.git`
2. Navigate to the project directory: `cd chat-program`

## Usage

- To start the server: `python server.py`
- To run the basic client: `python client.py`
- To use the chat client with GUI: `python chat-client.py`

## Application and Significance

This chat application provides a functional demonstration of a chat room where a server hosts multiple clients. It's significant in understanding how data is transmitted over networks and the complexities involved in instant messaging systems.

## Implementation and Testing

- The application was developed and tested in phases, focusing initially on server stability and basic client-server communication.
- Both client and server are designed to be multithreaded for efficient handling of multiple connections.
- GUI development was carried out using Tkinter, enhancing the user experience.

## Sources and Resources

- Python Socket Programming: [Real Python](https://realpython.com/python-sockets/), [Python Documentation](https://docs.python.org/3/howto/sockets.html)
- Tkinter Documentation: [Tkinter Library](https://docs.python.org/3/library/tk.html)
