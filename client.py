import socket
from re import match

while True:																# ввод IP клиента		
	host= r'[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.'
	client_host=input('Enter your IP: ')
	if client_host=='':
		break
	elif client_host=='localhost':
		break
	elif client_host and match(host,client_host):
		break
	else:
		print('You made a mistake try again')


while True:											# проверка порта 
	client_port=int(input('Enter port: '))
	if 1024<=client_port<=65525:
		break
	else:
		print('You made a mistake. Try again!')

sock = socket.socket()
sock.setblocking(1)
sock.connect((client_host,int(client_port)))
print('Connected to server')

def send_msg(conn: socket.socket, msg):
	"""
	отправка сообщений
	"""
	header=len(msg)
	formated_msg = f'{header:4}{msg}'.encode()
	sock.send(formated_msg)

def recv_msg(conn:socket.socket):
	"""
	получение сообщений
	"""	
	header=conn.recv(4).decode()
	msg=conn.recv(int(header))
	return msg

send_msg(sock, input('Enter your name, please: '))

msg=''
while True:
	msg=input('Message: ')
	print('Sending your message to server')
	if 'exit' in msg:
		send_msg(sock,msg)
		break
	send_msg(sock,msg)

sock.close()

