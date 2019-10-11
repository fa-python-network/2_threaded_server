import socket
from threading import Thread 


def check():
	while True:
		try:
			data = sock.recv(1024)
			msg = data.decode()
			print(msg)
		except:
			break


try:
	sock = socket.socket()
	print('kakoy host?')
	x = input()
	print('kakoy port?')
	y = int(input())
	sock.connect((x, y))
except:
	x = 'localhost'
	y = 9095
	sock.connect((x, y))

Thread(target=check).start()

msg = ''
while msg !="close":
	msg = input()
	if msg !='close':
		sock.send(msg.encode())




msg = 'client disconnected'
sock.send(msg.encode())
data = sock.recv(1024)

sock.close()