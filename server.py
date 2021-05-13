import socket
import threading

frames = []           #list to store the received chunks of data

HOST = '0.0.0.0'
RECV_PORT = 7000
SEND_PORT = 8000
recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvSocket.bind((HOST, RECV_PORT))
sendSocket.bind((HOST, SEND_PORT))
recvSocket.listen(100)
sendSocket.listen(100)


def receiveAudio():
    global frames
    while True:
        conn, addr = recvSocket.accept()             # busy waiting funciton till client connects to the server
        print('recieving from', addr)

        data = conn.recv(1024)

        while data:
            frames.append(data)
            data = conn.recv(1024)

        print('message stored')


def sendAudio():
    global frames
    while True:
        conn, addr = sendSocket.accept()                  # busy waiting funciton till client connects to the server
        print('sending to', addr)
        conn.sendall(b''.join(frames))
        conn.close()
        frames = []
        print('Sent')


t1 = threading.Thread(target=receiveAudio)
t2 = threading.Thread(target=sendAudio)

t1.start()
t2.start()

t1.join()
t2.join()
