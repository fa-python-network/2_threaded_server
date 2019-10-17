import socket       #сам сокет
import pickle       #получаем историю чата
from threading import Thread        #потоки для обновления окна чата

def update_chat():      #получение новых сообщений
	global username
	historychat = sock.recv(10240);
	historychat = pickle.loads(historychat)
	print(historychat)
	while True:
		answer = sock.recv(1024)
		if '@'+username in answer.decode().split():
			print("*** ВАС УПОМЯНУЛИ ***")
			print(f'\n',answer.decode())
		else:
			print(f'\n',answer.decode())

ip = 'localhost'
port = 9100

sock = socket.socket()

sock.connect((ip,port))

print('Подключились к серверу чата')

username = ""
password = ""

while not username:     #непустое поле
	username = input('Введите Ваше имя: ')

sock.send(username.encode())
answer = sock.recv(1024)

if answer.decode() == 'reg_req':        #если нужна регистрация
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
	password = input('Ваш пароль от аккаунта: ')        #просим пароль
	sock.send(password.encode())
	answer = sock.recv(1024)
	if answer.decode() == 'valid':      #пароль верен
		print("ДЛЯ ЛИЧНОГО УПОМИНАНИЯ ИСПОЛЬЗУЙТЕ ФОРМАТ @ИМЯ! Таким образом у получателя сообщение будет выделяться! Его увидят все!")
		Thread(target=update_chat,args=()).start()
		
		while True:
			msg = input()
			if msg == 'exit':
				sock.send('exit_cmd'.encode())
				break
			sock.send(msg.encode())
	else:
		print('Введен неверный пароль!')

print("Подключение закрыто!")
sock.close()

