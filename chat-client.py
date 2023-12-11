import tkinter
import threading
import socket
import queue
from tkinter import simpledialog, scrolledtext, messagebox

host = 'localhost'
port = 9001


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.gui_done = False
        self.running = True
        self.msg_queue = queue.Queue()

        self.win = tkinter.Tk()

        self.win.configure(bg="turquoise")
        self.win.title("Chat Room Application")

        self.chat_label = tkinter.Label(
            self.win, text="A CS5700 Networking Chat Room!", bg="Khaki1", fg="#333333", borderwidth=2, relief="groove"
        )
        self.chat_label.config(font=("Calibri", 28, "bold"))
        # You might want to fill the label in the x direction for better appearance
        self.chat_label.pack(padx=20, pady=5, fill="x")

        self.text_area = scrolledtext.ScrolledText(
            self.win, bg="Khaki1", fg="#333333", highlightbackground="black", highlightthickness=1
        )
        # Expand and fill both directions for better appearance
        self.text_area.pack(padx=20, pady=5, expand=True, fill="both")
        self.text_area.config(state='disabled', font=("Calibri", 20))

        self.msg_label = tkinter.Label(
            self.win, text='Type Your Message Below', bg="Khaki1", fg="#333333", borderwidth=2, relief="groove"
        )
        self.msg_label.config(font=("Calibri", 28, "bold"))
        self.msg_label.pack(padx=20, pady=5, fill="x")

        self.input_area = tkinter.Text(
            self.win, height=3, bg="PeachPuff2", fg="#333333", highlightbackground="black", highlightthickness=1
        )
        self.input_area.pack(padx=20, pady=5, fill="x")
        self.input_area.config(font=("Calibri", 16))

        self.send_button = tkinter.Button(
            self.win, text="Send", command=self.write, bg="Khaki1", fg="#333333", highlightbackground="black", highlightthickness=1, borderwidth=2, relief="raised"
        )
        self.send_button.config(font=("Calibri", 26, "bold"))
        self.send_button.pack(padx=20, pady=5)

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.initialize_gui()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def initialize_gui(self):
        self.name = simpledialog.askstring(
            "Name", "Choose name", parent=self.win)
        self.gui_done = True
        self.win.after(500, self.check_queue)

    def write(self):
        message = self.input_area.get('1.0', 'end').strip()

        if message.lower() == "quit":
            self.socket.send("/quit".encode('utf-8'))
            self.stop()
        else:
            full_message = f"{self.name}: {message}"
            self.socket.send(full_message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.socket.close()
        self.win.destroy()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.socket.send(self.name.encode('utf-8'))
                else:
                    self.msg_queue.put(message)
            except ConnectionAbortedError:
                break
            except Exception as e:
                print("Error:", e)
                self.socket.close()
                break

    def check_queue(self):
        while not self.msg_queue.empty():
            message = self.msg_queue.get_nowait().strip()
            if message:
                self.text_area.config(state='normal')
                if not self.text_area.get('1.0', 'end-1c').endswith('\n'):
                    message = '\n' + message
                self.text_area.insert('end', message)
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
        if self.gui_done:
            self.win.after(500, self.check_queue)


if __name__ == "__main__":
    client = Client(host, port)
    tkinter.mainloop()
