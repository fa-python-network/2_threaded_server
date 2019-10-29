import socket
import threading
def client(n):
	print(addr)

	msg = ''

	while True:
		data = conn.recv(1024)
		if not data:
			break
		msg += data.decode()
		conn.send(data)
	print(msg)

sock = socket.socket()
sock.bind(('', 9090))	
sock.listen(0)
while True:
	conn, addr = sock.accept()
	
	p1 = threading.Thread(target=client, name="t1", args=["1"])
	p1.start()

conn.close()
