import socket

class SocketWrapper(socket.socket):
    def __init__(self,socket:socket.socket):
        self.socket = socket

    def send(self,message:str):
        self.socket.sendall(message.encode("utf-8"))

    def recv(self):
        return self.socket.recv(1024).decode('utf-8')

    def close(self):
        self.socket.close()