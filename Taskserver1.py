import socket
while True:
	print("Choose port")
	port=int(input())
	if 65535>=port>=1024:
		break
	print("Wrong port, try again!")
sock = socket.socket()
sock.bind(('', int(port)))

print("Port is ",port)
sock.listen(1)
conn, addr = sock.accept()

port=input()