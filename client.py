import socket
import threading
from time import sleep


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(True)

    s.connect(('127.0.0.1', 7777))

    msg = input()

    while msg != 'exit':
        s.send(msg.encode())

        data = s.recv(1024)

        print(data.decode())
        msg = input()
