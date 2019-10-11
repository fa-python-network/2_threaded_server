import socket
sock = socket.socket()
import random
from threading import Thread 
connected_users = []


def new_client(conn, addr):
	print("Hello, dude ", addr[0])
	while True:
		data = conn.recv(1024)
		if not data:
			break
		msg = data.decode()
		if msg != 'client disconnected':
			print(addr, msg)
			for user in connected_users:
				if conn != user:
					po = str(addr) + str(msg)
					user.send(po.encode())
		else:
			try:
				connected_users.remove(conn)
			except:
				break
	conn.close()


try:
	port = 9095
	sock.bind(('localhost', port))
except:
	port = random.randint(1024,65535)
	sock.bind(('', port))
sock.listen(0)
print("port№", port)
msg = ''


while True:
	conn, addr = sock.accept()
	connected_users.append(conn)
	Thread(target=new_client, args=(conn, addr)).start()
