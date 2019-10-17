import socket
import json
import threading

def send_msg(conn: socket.socket,msg):
	header=len(msg)
	formated_msg = f'{header:4}{msg}'.encode()
	conn.send(formated_msg)

def recv_msg(conn: socket.socket):
	header=conn.recv(4).decode()
	msg=conn.recv(int(header))
	return msg.decode()

def iden(conn: socket.socket, addr):
	with open('login.json', 'r') as A:
		login=json.loads(A)
		for i in login['clients']:
			if addr[0]==i['ip']:
				send_msg(conn,"Hello, {}".format(i['name']))

			else:
				with open('login.json', 'a') as A:
					login=json.dumps(A)
					send_msg(conn,'Create a name')
					name=recv_msg(conn)
					send_msg(conn,'Create a Password')
					pswd=recv_msg(conn,)
					new_client={'ip': addr[0], 'name': name, 'password': pswd}
					login['clients'].append(new_client)
					json.dumps(login)


def handle(conn: socket.socket):
	data=''
	while True:
		iden(conn,addr)
		msg= recv_msg(conn)
		send_msg(conn,msg)
		data+=msg
		if not msg:
			conn.close()
		return data

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
		conn,addr=sock.accept()
		tr=threading.Thread(target=handle, args=[conn])
		print('Подключен клиент {}'.format(addr[0]))

finally:
	conn.close()


	