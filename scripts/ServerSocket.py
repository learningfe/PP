import socket
from config import HOST,PORT,BACKLOG

class ServerSocket(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET,socket.SOCK_STREAM)

        self.bind((HOST,PORT))

        self.listen(BACKLOG)