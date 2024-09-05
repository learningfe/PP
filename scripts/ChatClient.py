import socket
from SocketWrapper import SocketWrapper

def test():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('127.0.0.1',12345))
    Client = SocketWrapper(client)

    while True:
        message = input("input:")
        if message:
            Client.send(message)
            response = Client.recv()
            print(response)
        else:
            break

if __name__ == "__main__":
    test()