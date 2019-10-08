import socket

ip = 'localhost'
port = 9100

sock = socket.socket()

sock.connect((ip,port))

while True:
	sock.send("Hello from client!".encode())

	data = sock.recv(1024)
	print(data.decode())
	
	action = input()
	
	if action == "exit":
		sock.send(action.encode())

print("Подключение закрыто!")
sock.close()

