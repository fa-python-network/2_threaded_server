import socket
from threading import Thread

def one_client(conn,addr):
	print("Стартовал новый поток")
	data = conn.recv(1024)
	if not data:
		conn.close()
		
	print(data.decode())
	conn.send("Hello from server!".encode())

sock = socket.socket()

port = 9100

sock.bind(('',port))
sock.listen(3)

while True:
	conn, addr = sock.accept()
	
	print("Новый клиент!")
	Thread(target=one_client,args=(conn,addr)).start()
	