import socket
import threading
import os

HOST = '116.62.152.206'
PORT = 12345
ChatLog = []
nickname = ""
is_exit = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_server(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.settimeout(0.5)
    return s

def write(socket):
    while True:
        input_content = input()
        if input_content == 'exit':
            socket.close()
            global is_exit
            is_exit = True
            break
        message = f'{nickname}:{input_content}'
        socket.send(message.encode('utf-8'))

def print_chatlog():
    for message in ChatLog:
        print(message)
    
def receive(socket):
    while not is_exit:
        try:
            message = socket.recv(1024).decode('utf-8')
        except TimeoutError and OSError:
            continue
        ChatLog.append(message)
        clear_screen()
        print_chatlog()

if __name__ == "__main__":
    nickname = input("Choose a nickname: ")
    s = connect_server(HOST,PORT)

    NICKNAME_INIT = f'nickname:{nickname}'
    s.sendall(NICKNAME_INIT.encode('utf-8'))
    receive_thread = threading.Thread(target=receive,args=(s,))
    receive_thread.start()

    write_thread = threading.Thread(target=write,args=(s,))
    write_thread.start()