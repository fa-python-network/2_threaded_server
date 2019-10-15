import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
sock.connect(('localhost', 9093))

msg = input()

while msg != "exit":
    sock.send(msg.encode())

    data = sock.recv(1024)

    print(data.decode())
    msg = input()

sock.close()