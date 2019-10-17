import socket

while True:									# ввод IP клиента		
	client_host=input('Enter your IP: ')
	if client_host=='':
		break
	elif client_host=='localhost':
		break
	else:
		parts=client_host.strip('.',4)
		for i in parts:
			if 0<=int(i)<=255:
				break
			else:
				print('You made a mistake. Try again!')

while True:									# проверка порта 
	client_port=int(input('Enter port: '))
	if 1024<=client_port<=65525:
		break
	else:
		print('You made a mistake. Try again!')


sock = socket.socket()
sock.setblocking(1)
sock.connect((client_host,int(client_port)))

auten=sock.recv(1024).decode()				# аутентификация
if 'Create' in auten:
	print(auten)
	sock.send(input('Name: ').encode())			# создание имени нового клиента
	sock.send(input('Password: ').encode())		# создание пароля нового клиента
else:
	print(auten)
	while True:
		sock.send(input('Password: ').encode())  # введение пароля известного клиента
		anw = sock.recv(1024).decode()
		if 'C' == anw[0]:						# проверка введенного пароля
			print(anw)
			break
		print(anw)
		print(sock.recv(1024).decode())


msg=''											# отправка сообщений серверу
while True:
	print('Message:')
	msg=input()
	if 'exit' in msg:
		sock.send(msg.encode())
		break
	sock.send(msg.encode())
#print(sock.recv(1024).decode())

sock.close()
