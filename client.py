import socket
from time import sleep
sock = socket.socket()
users = {}
k = False
while not k:
    try:
        print("Host:")
        host = input()
        if host == "":
            host = 'localhost'
        print("Port:")
        port = input()
        if port == "":
            port = 9090

        sock.connect((host, int(port)))
        print("Введите сообщение")
        print("Для выхода введите exit")
        msg = input()
        while msg != 'exit':
            sock.send(msg.encode())
            msg = input()
            data = sock.recv(1024)
            print(data.decode())
        k=True
    except KeyboardInterrupt:
        break
sock.close()