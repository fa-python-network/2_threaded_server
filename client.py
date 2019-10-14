import socket
import re 
from time import sleep

while True:
	port = int(input('укажите порт в диапазоне 1024-65535: \n'))
	if 1024<= port <= 65535:
		break
	else:
		print('ошибка, введите порт снова')

while True: 
	ip= input("введите ip или _ для localhost: \n")
	if ip ==' ':
		ip= 'localhost'
		break
	elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) == None:
		print('введите снова')
	else:
		break

sock = socket.socket()
sock.setblocking(1)
sock.connect((ip, int(port)))


aut = sock.recv(1024).decode()
print(aut)
if aut[0]=="g":  #проверка пароля у известного пользователя
	passwd=input()
	sock.send(passwd.encode())
	print(sock.recv(1024).decode())

if aut[0]=="i":  #ввод и отправка данных по новому пользователю
	name = input()
	sock.send(name.encode())
	print(sock.recv(1024).decode())
	passwd = input()
	sock.send(passwd.encode())

while True:  
	msg = input("input a massage: ")
	if msg == "exit":
		sock.close()
		print('stop')
		break
	sock.send(msg.encode())
	data = sock.recv(1024)


