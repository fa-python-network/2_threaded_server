import socket
import logging
from time import sleep

sock = socket.socket()
sock.setblocking(1)

port = 9090
hostname = 'localhost'

sock.connect((hostname, port))

#Взаимодействие с сервером

while True:
	sock.settimeout(1)
	server_msg = sock.recv(16384).decode()
	print(server_msg)
	answ = input()
	sock.send(answ.encode())

sock.close()