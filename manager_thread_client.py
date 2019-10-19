import socket

sock = socket.socket()
host = []
f = 0
while True:
	try:
		num_sock = int(raw_input('Enter the socket number: '))
		if 1024<=num_sock<=65535:
			break
		else:
			print("The socket number is incorrect. Try again.")
	except ValueError:
		print("The socket number is incorrect. Try again.")


while True:
	try:
		host_str = raw_input('Enter the host adress: ')
		hostt = host_str.split(".")
		for i in hostt:
			try:
				if 0<=int(i)<=255:
					host.append(int(i))
				else:
					print("The host adress is incorrect. Try again.")
					break
			except TypeError:
				print("The host adress is incorrect. Try again.")
				break
		break
	except ValueError:
		print("The host adress is incorrect. Try again.")

sock.connect((host_str, num_sock))
sock.send(host_str.encode())
data = sock.recv(1024123)
print(data.decode())


while True:
	msg = raw_input()
	sock.send(msg.encode())
	data = sock.recv(1024123)
	print(data.decode())
	if msg == 'STOP':
		break

sock.close()