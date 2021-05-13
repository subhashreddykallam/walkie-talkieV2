import socket
import pyaudio
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "server_output.wav"
frames = []

p = pyaudio.PyAudio()

HOST = '0.0.0.0'                 # Symbolic name meaning all available interfaces
RECV_PORT = 5000              # Arbitrary non-privileged port
SEND_PORT = 6000
recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvSocket.bind((HOST, RECV_PORT))
sendSocket.bind((HOST, SEND_PORT))
recvSocket.listen(100)
sendSocket.listen(100)

def recieveAudio():
    global frames
    while True:
        conn, addr = recvSocket.accept()
        print('recieving from', addr)

        data = conn.recv(1024)

        while data:
            frames.append(data)
            data = conn.recv(1024)
        
        print('message stored')

def sendAudio():
    global frames
    while True:
        conn, addr = sendSocket.accept()
        print('sending to', addr)
        conn.sendall(b''.join(frames))
        conn.close()
        frames = []
        print('Sent')

t1 = threading.Thread(target=recieveAudio)
t2 = threading.Thread(target=sendAudio)

t1.start()
t2.start()

t1.join()
t2.join()