import socket


sock = socket.socket()

port = 9100

sock.bind(('',port))
sock.listen(3)

while True:
	conn, addr = sock.accept()
	
	data = conn.recv(1024)
	if not data:
		conn.close()
		
	print(data.decode())
	conn.send("Hello from server!".encode())
	