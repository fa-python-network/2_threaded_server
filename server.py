import socket
import threading

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


def handle(conn, addr):
	"""
	подключение клиента 
	"""
	client_name=recv_msg(conn)
	data=''
	while True:
		msg= recv_msg(conn)
		print('Got a message [{}] from [{}]'.format(msg, client_name))
		data+=msg
		if 'exit' in msg: 
			conn.close()
			print('Client [{}] is turned off'.format(client_name))
			return 

		send_msg(conn,data)

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

try:
	while True:
		conn,addr=sock.accept()							# при подключении клиента создается новый поток
		tr=threading.Thread(target=handle, args=(conn, addr))
		tr.start()
		print('Подключен клиент {}'.format(addr[0]))

finally:
	conn.close()


	