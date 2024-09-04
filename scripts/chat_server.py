import socket
import threading
import CommandParser
import Room
import RoomUser
import RoomManager

HOST = '0.0.0.0'
PORT = 12345

class ChatServer:   
    def init_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST,PORT))
        self.server.listen(5)
        print(f"listenning port: {PORT}")

        self.roomManager = RoomManager()
        self.roomManager.add_room(Room(0,"Waiting Room"))
        self.commandParser = CommandParser()

    def handle_single_client(self,room_user:RoomUser):
        while True:
            try:
                message = room_user.socket.recv(1024).decode('utf-8')
                #如果是命令交由commandParser处理
                self.commandParser.parse(message)
            except TimeoutError and OSError:
                continue
            if message == 'exit':
                break
        # remove user from room
        room = RoomManager.get_room(room_user.room_id)
        room.remove_user(room_user)

    def handle_clients(self,server:socket):
        while True:
            client_socket,address = server.accept()
            t = threading.Thread(target=self.check_login,args=(client_socket,address,))
            t.start()

    def check_login(self,client_socket:socket.socket,address):
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            user_name = ""
            nickname = ""
            if self.commandParser.parse(command):
                break
            #login后退出循环，进入handle_single_client
        t = threading.Thread(target=self.handle_single_client,args=(RoomUser(user_name,nickname,address[0],address[1],client_socket,0),))
        t.start()
        
    def broadcast(room_id:int,message:str):
        room = RoomManager.get_room(room_id)
        if room:
            for user in room.users:
                user.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    pass