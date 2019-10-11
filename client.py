import socket
from threading import Thread

def update_chat():
	while True:
		answer = sock.recv(1024)
		print(f'\n',answer.decode())

ip = 'localhost'
port = 9100

sock = socket.socket()

sock.connect((ip,port))

print('Подключились к серверу чата')

username = ""
password = ""

while not username:
	username = input('Введите Ваше имя: ')

sock.send(username.encode())
answer = sock.recv(1024)

if answer.decode() == 'reg_req':
	#registation required
	print('Такого пользователя ещё нет! Запускается процесс регистрации!')
	print(f'Регистрируемое имя: {username}')
	while not password:
		password = input('Придумайте пароль:')
	sock.send(password.encode())
	answer = sock.recv(1024)
	if answer.decode() == 'reg_end':
		print('Регистрация завершена! Перезапустите программу!')
else:
	password = input('Ваш пароль от аккаунта: ')
	sock.send(password.encode())
	answer = sock.recv(1024)
	if answer.decode() == 'valid':
		Thread(target=update_chat,args=()).start()
		while True:
			msg = input('Ваше сообщение: ')
			if msg == 'exit':
				sock.send('exit_cmd'.encode())
				break
			sock.send(msg.encode())
	else:
		print('Введен неверный пароль!')

print("Подключение закрыто!")
sock.close()

