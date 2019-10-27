import socket, threading


class ClientThread(threading.Thread):
	def __init__(self, clientAddress, clientsocket):
		threading.Thread.__init__(self)
		self.socket = clientsocket
		print("New connection: ", clientAddress)

	def run(self):
		print("Connection from: ", clientAddress)
		msg=""
		while True:
			data = self.socket.recv(1024)
			msg= data.decode()
			if msg=="bye":
				break
			print("message from client: ", msg)
			self.socket.send(msg.encode())
		print("Client ", clientAddress, " disconnected!")


host="127.0.0.1"
port=8080
server = socket.socket()
server.bind((host, port))

print("Server started")
print("Server is waiting client")
while True:
	server.listen(1)
	clientsock, clientAddress = server.accept()
	newthread = ClientThread(clientAddress, clientsock)
	newthread.start()