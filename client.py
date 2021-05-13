import socket
import pyaudio
import tkinter as tk
from tkinter import scrolledtext
import sys
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

# HOST = '127.0.0.1'
HOST = '65.1.163.34'    # The remote host
SEND_PORT = 7000              # The same port as used by the server
RECV_PORT = 8000

sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

p = pyaudio.PyAudio()
username, contact = "", ""


def recordAndSend(miniDisplay):
    sendSocket.connect((HOST, SEND_PORT))
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    miniDisplay.insert(tk.END, 'recording...\n')

    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        sendSocket.sendall(data)

    miniDisplay.insert(tk.END, 'sent successfully...\n')

    stream.stop_stream()
    stream.close()
    sendSocket.close()
    return


def receive(miniDisplay):
    miniDisplay.insert(tk.END, 'retreiving message...\n')
    recvSocket.connect((HOST, RECV_PORT))
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    output=True, frames_per_buffer=CHUNK)
    data = recvSocket.recv(1024)

    while data:
        stream.write(data)
        data = recvSocket.recv(1024)

    print("over")
    stream.stop_stream()
    stream.close()
    recvSocket.close()
    miniDisplay.insert(tk.END, 'Message played...\n')
    return


class page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (homePage, callPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(homePage)

    def show_frame(self, cont):
        if cont == homePage:
            self.title("Walkie-Talkie Homepage")
        else:
            self.title("Walkie-Talkie Calling Interface")
        frame = self.frames[cont]
        frame.tkraise()


class homePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_username = tk.Label(self, text="Username")
        label_contact = tk.Label(self, text="Contact")

        entry_username = tk.Entry(self)
        entry_contact = tk.Entry(self)

        label_username.grid(row=1, column=0, padx=10, pady=10)
        label_contact.grid(row=2, column=0, padx=10, pady=10)
        entry_username.grid(row=1, column=1, padx=10, pady=10)
        entry_contact.grid(row=2, column=1, padx=10, pady=10)

        connectBtn = tk.Button(self, text="Connect", width=10, background="white",
                               foreground="Black", command=lambda: connectBtn_clicked())
        connectBtn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        def connectBtn_clicked():
            global username, contact
            username = entry_username.get()
            contact = entry_contact.get()
            controller.show_frame(callPage)


class callPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        message_label = tk.Label(self, text="Status", font=("Arial,12"))
        message_label.grid(row=1, column=0, columnspan=3,
                           padx=10, pady=5, sticky="NSEW")

        miniDisplay = scrolledtext.ScrolledText(self, height=8, width=35,
                              bg="Grey", fg="White")
        miniDisplay.grid(row=4, column=0, rowspan=3,
                         columnspan=3, sticky="NSEW")

        var = tk.IntVar()
        sendRbtn = tk.Radiobutton(self, text="Send", variable=var, value=1,
                                  command=lambda: modeSelect())

        waitRbtn = tk.Radiobutton(self, text="Wait", variable=var, value=2,
                                  command=lambda: modeSelect())

        recvRbtn = tk.Radiobutton(self, text="receive", variable=var, value=3,
                                  command=lambda: modeSelect())

        sendRbtn.grid(row=8, column=0,padx=10, pady=5, sticky="nsew")
        waitRbtn.grid(row=8, column=1,padx=10, pady=5, sticky="nsew")
        recvRbtn.grid(row=8, column=2,padx=10, pady=5, sticky="nsew")

        disconnectBtn = tk.Button(
            self, text="Disconnect", width=10, command=lambda: disconnectBtn_clicked())
        disconnectBtn.grid(row=9, column=0, columnspan=2,
                           padx=10, pady=5, sticky="nsew")

        def modeSelect():
            if var.get() == 1:
                t = threading.Thread(target=recordAndSend, args = (miniDisplay, ))
                t.start()
            elif var.get() == 2:
                pass
            else:
                t = threading.Thread(target=receive, args = (miniDisplay, ))
                t.start()
        def disconnectBtn_clicked():
            sys.exit(0)


app = page()
app.mainloop()
