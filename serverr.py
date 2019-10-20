import socket
port = 9090
sock = socket.socket()
try:
	sock.bind(('',port))
except OSError:
	sock.bind(('',0))
	port = sock.getsockname()[1]
	print(f"use purt {port}")
sock.listen()
while True:
	conn, addr = sock.accept()
	print(addr)
	msg = ""

	while True:
		data = conn.recv(1024)
		if not data:
			break
		print(data.decode())
conn.close()

