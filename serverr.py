import socket
import threading

sock = socket.socket()
port = 9090

class T(threading.Thread):
	def __init__(self,conn,addr):
		super().__init__()
		self.conn = conn
		self.addr = addr

	def run(self):
		msg = ""

		while True:
			data = self.conn.recv(1024)
			if not data:
				break
			self.conn.send
			print(data.decode())


try:
	sock.bind(('',port))
except OSError:
	sock.bind(('',0))
	port = sock.getsockname()[1]
	print(f"{port}")
sock.listen()
while True:
	conn,addr = sock.accept()
	print(addr)
	T(conn, addr).start()
conn.close()