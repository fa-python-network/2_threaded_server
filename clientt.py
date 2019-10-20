import socket

sock = socket.socket()
i=False
while not i:
	try:
		print("host:")
		host = input()
		if host == "":
			host='localhost'
		print("port: ")
		port = input()
		if port == "":
			port=9090

		sock.connect((host, int(port)))
		print("enter a message")
		print("enter exit to exit")
		msg = input()
		while msg!='exit':
			sock.send(msg.encode())
			msg = input()
			i=True
	except Keyboardinterrupt:
		break
sock.close()



			
