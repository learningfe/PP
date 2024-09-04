import socket

class RoomUser:
    def __init__(self,username,nickname,ip,port,socket:socket.socket,room_id:int):
        self.username = username
        self.nickname = nickname
        self.ip = ip
        self.port = port
        self.socket = socket
        self.room_id = room_id