import socket

def send_msg(conn: socket.socket,msg):
	"""
	отправка сообщений
	"""
	header=len(msg)
	formated_msg = f'{header:4}{msg}'.encode()
	conn.send(formated_msg)

def recv_msg(conn: socket.socket):
	"""
	принятие сообщений
	"""
	header=conn.recv(4).decode()
	msg=conn.recv(int(header))
	return msg.decode()

sock=socket.socket()

#host=socket.gethostbyname(socket.gethostname())

port = 9090      		# проверка порта на занятость
while port!=65525:
	try:
		sock.bind(('',port))
		print('The port is {}'.format(port))
		break
	except:
		print('The port {} is not available. Checking new one...')
		port+=1

clients=[]

sock.listen()
sock.setblocking(1)

exit = False
print('SERVER IS STARTED\n')

while not exit:
	try:
		conn,addr = sock.accept()

		if addr[0] not in clients:
			clients.append(addr[0])

		print('the ip of a new client is {}'.format(addr[0]))
		print('AAAAAA')
		msg=recv_msg(conn)
		print(msg)

		for i in clients:
			if addr[0]!=i:
				send_msg(i,msg)
	except:
		print('SERVER IS STOPPED')
		exit=True

sock.close()


