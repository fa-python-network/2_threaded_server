import socket
import threading


sock = socket.socket()
sock.connect(('localhost', int(input('Введите порт: '))))


def reader():
	while True:
		msg = (sock.recv(1024).decode())
		if msg != 'exit':
			print(msg)
		else:
			break

s1 = threading.Thread(target = reader)
s1.setDaemon(True)
s1.start()

right = 1
while right:
	msg = input()
	if msg != 'exit':
		sock.send( msg.encode('utf-8'))
	else:
		sock.send( msg.encode('utf-8'))
		right = 0

sock.close()

