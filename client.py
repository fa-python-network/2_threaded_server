import socket
import logging
from time import sleep

sock = socket.socket()
sock.setblocking(1)

port = 9090
hostname = 'localhost'

sock.connect((hostname, port))

#Получение "приветственного" сообщения от сервера/запрос имени

data = sock.recv(1024).decode()
print(data)

login = input()
sock.send(login.encode())

data = sock.recv(1024).decode()

if data == "Придумайте логин: ":

	login = input()
	sock.send(login.encode())
	print(sock.recv(1024).decode())
	password = input()
	sock.send(password.encode())
	print(sock.recv(1024).decode())
	
else:

	password = input()
	sock.send(password.encode())
	answ = sock.recv(1024).decode()
	print(answ + '\n')


answ = sock.recv(1024).decode()
print(answ)

#Отправка сообщений

msg = ""
while True:
	msg = input()
	if msg == "exit":
		sock.send(("Клиент разорвал соединение \n").encode())
		break
	sock.send(msg.encode())
	
sock.close()