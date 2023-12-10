import tkinter
import threading
import socket
import queue
from tkinter import simpledialog, scrolledtext, messagebox

host = 'localhost'
port = 9000


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
        self.win.configure(bg="khaki1")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Calibri", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(
            self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Calibri", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(
            self.win, text="Send", command=self.write)
        self.send_button.config(font=("Calibri", 12))
        self.send_button.pack(padx=20, pady=5)

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.initialize_gui()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def initialize_gui(self):
        self.name = simpledialog.askstring(
            "Name", "Choose username", parent=self.win)
        self.gui_done = True
        self.win.after(500, self.check_queue)

    def write(self):
        message = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        self.socket.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.socket.close()
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
            message = self.msg_queue.get_nowait()
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
        if self.gui_done:
            self.win.after(500, self.check_queue)


if __name__ == "__main__":
    client = Client(host, port)
    tkinter.mainloop()
