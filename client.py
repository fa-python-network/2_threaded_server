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

def auten():
	"""
	аутентификация пользователя
	"""
	answer=recv_msg()
	if 'Hello' in answer:
		pswd_ans=recv_msg()
		print('Password: ')
		while True:
			send_msg(input())
			if 'Lets' in recv_msg():
				print('Correct')
				break
			print('Again')
	elif "Create" in answer:
		print(answer)
		send_msg(input('New Name: '))
		print(recv_msg())
		send_msg(input('New password: '))


msg=''
while True:
	msg=input('Message: ')
	if 'exit' in msg:
		send_msg(sock,msg)
		break
	send_msg(sock,msg)
sock.close()

