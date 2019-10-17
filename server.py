
import socket, threading
class ClThread(threading.Thread):
	def __init__(self,clAddr,clSock):
		threading.Thread.__init__(self)
		self.CSock = clSock
		print ("New connection added: ", clAddr)
	def run(self):
		print ("We have new client: ", clAddr)
		msg = ''
		addr = clAddr
		while True:
			data = self.CSock.recv(1024)
			msg = data.decode()
			if msg=='bye':
				break
			print ("Message from client:", msg)
		print ("Client:", addr , " disconnect.")
server = socket.socket()
server.bind(("", 9095))
print("Server started")
print("Search the client...")
while True:
	server.listen(1)
	clSock, clAddr = server.accept()
	N_T = ClThread(clAddr, clSock)
	N_T.start()
