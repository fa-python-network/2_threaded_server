import socket
import threading
sock = socket.socket()
isnal = 0
try:
	sock.connect(('localhost', int(input('Введите порт: '))))
	isnal = 1
except:
	print('Неправильный порт')
	
nal = sock.recv(1024).decode()
if isnal == 0:
	nal = 'nothing'
if nal == 'YES':
	print('Вы есть в базе')
else:
	print('Вас нет в базе')
right = 1
if nal == 'YES':
	password = input('Введите пароль: ')
	sock.send(password.encode('utf-8'))
	if (sock.recv(1024).decode()) == 'Пароль верен':
		print('Пароль верен')
	else:
		print('Пароль не верен')
		right = 0
else:
	login = input('Введите логин: ')
	sock.send(login.encode('utf-8'))
	password = input('Введите пароль: ')
	sock.send(password.encode('utf-8'))
5

def reader():
	right = 1
	while right:
		msg = (sock.recv(1024).decode())
		if msg != 'exit':
			print(msg)
		else:
			break


s1 = threading.Thread(target = reader)
s1.setDaemon(True)
s1.start()
if right:
	print('Можешь писать')
while right:
	msg = input()
	if msg != 'exit':
		sock.send((msg).encode('utf-8'))
	else:
		sock.send((msg).encode('utf-8'))
		right = 0

sock.close()

