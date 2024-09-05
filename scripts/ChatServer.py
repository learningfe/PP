import socket
from SocketWrapper import SocketWrapper
import threading
from ServerSocket import ServerSocket 
from Parser import *
from RequestHandler import RequestHandler

class ChatServer:   
    def init_server(self):
        self.Server = ServerSocket()
        self.Parser = Parser()
        self.RequestHandler = RequestHandler(self.Server)

    def handle_single_client(self,client:SocketWrapper):
        while True:
            message = client.recv()
            if message:
                try:
                    parsed_data = self.Parser.parse(message)
                except UnknownCommandError:
                    continue
                except ParameterError:
                    continue
                request_id = parsed_data[0]
                print(self.RequestHandler.handle_request(client,request_id,**parsed_data[1]))
            else:
                break
        client.close()

    def handle_clients(self,server:socket):
        while True:
            client_socket,address = server.accept()
            client = SocketWrapper(client_socket)

            print(f"connection from {address}")
            t = threading.Thread(target=self.handle_single_client,args=(client,))
            t.start()


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.init_server()
    chat_server.handle_clients(chat_server.Server)