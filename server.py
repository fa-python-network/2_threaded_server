import socket

sock=socket.socket()

sock.bind(("", 8082))
sock.listen(1)

conn,addr = sock.accept()
while True:
	data = conn.recv(1024).decode()
	if not data:
		break
	conn.send(data.encode())

conn.close()
