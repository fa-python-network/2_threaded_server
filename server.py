import socket
import json

sock = socket.socket()

port = 9090      		# проверка порта на занятость
while port!=65525:
	try:
		sock.bind(('',port))
		print('The port is {}'.format(port))
		break
	except:
		print('The port {} is not available. Checking new one...')
		port+=1

sock.listen(0)			
sock.setblocking(1)



while True:
	conn,addr=sock.accept()
	print('Now connected to {}'.format(addr[0]))
	with open('data.json', 'r+') as f:				#проверка Ip клиента (сохранен ли он в файле)
		data=json.loads(f.read())
		for i in data['Clients']:
			if addr[0]==i['IP']:
				conn.send('Hello, {}!'.format(i['Name']).encode())
				while True:
					conn.send('\nEnter your password, please.'.encode())
					pswd=conn.recv(1024).decode()
					if pswd==i['Password']:
						conn.send('Correct password. Well done!'.encode())
						break
					else:
						conn.send('Wrong password. Try again!'.encode())
				break
		else:										# создание нового клиента
			conn.send('Create an account'.encode())
			new_name=conn.recv(1024).decode()
			conn.send('Create a password'.encode())
			new_pswd=conn.recv(1024).decode()
			new_client={'IP': addr[0], 'Name': new_name, 'Password': new_pswd} 	# запись новые данные в файл
			data['Clients'].append(new_client)
			f.write(json.dumps(data))

	msg=''							# чтение сообщений от клиента
	while True:
		data = conn.recv(1024)
		if not data:
			break
		msg+=data.decode()+' '
		print('The IP {} send message: [{}]'.format(addr[0], msg))
conn.close()