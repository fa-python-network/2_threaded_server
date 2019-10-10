
import socket, threading
class ClientThread(threading.Thread):
	def __init__(self,clientAddress,clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		print ("New connection added: ", clientAddress)
	def run(self):
		print ("Connection from : ", clientAddress)
		msg = ''
		while True:
			data = self.csocket.recv(1024)
			msg = data.decode()
			if msg=='bye':
				break
			print ("from client", msg)
		print ("Client at ", clientAddress , " disconnected...")
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket()
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
	server.listen(1)
	clientsock, clientAddress = server.accept()
	newthread = ClientThread(clientAddress, clientsock)
	newthread.start()