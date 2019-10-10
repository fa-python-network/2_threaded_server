
import socket
from time import sleep
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket()
client.setblocking(1)
client.connect((SERVER, PORT))
# client.sendall(bytes("This is from Client",'UTF-8'))
while True:
	# in_data = client.recv(1024)
	# print("From Server :" ,in_data.decode())
	out_data = input()
	client.send(out_data.encode())
	if out_data=='bye':
		break
client.close()