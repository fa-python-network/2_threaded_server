import socket
import sys
import logging
import threading

log_file = logging.FileHandler('myserver.log')
console_out= logging.StreamHandler()

logging.basicConfig(handlers = (log_file, console_out), format = '[%(asctime)s | %(levelname)s] : %(message)s', datefmt='%m.%d.%Y %H:%M:%S', level = logging.INFO)

class Server(socket.socket):

	def __init__(self):
		self.sock = socket.socket()
		self.port = 9090
		self.host = '127.0.0.1'
		self.threads=[]
		self.lock = threading.Lock()
		self.data=""

	@property
	def sending(msg, sock):
		sock.send(msg.encode())

	@property 
	def receiving(sock):
		sock.recv(1024).decode()

	def close_server(self):
		logging.info("Stop server")

		#Очистка логов
		with open('myserver.log', 'w'):
			pass

		self.sock.close()
		sys.exit()

		#Очистка файла идентификации
		f = open('clients.txt', 'r+')
		f.truncate()
		

	def register(self, conn, addr):
		self.sending("Input your name")
		name = self.receiving(conn)
		self.sending("Input your password")
		password = self.receiving(conn)
		with open('clients.txt', 'w') as file:
			file.write("{addr[0]}:{name}:{password}:\n")

	def login(self, conn, addr):
		with open('clients.txt', 'r+') as file:
			for line in file:
				if addr[0] in line:
					line=line.split(":")
					password = line[2]

		self.sending("Type password")
		passwd = self.receiving(conn)
		if passwd == password:
			conn.sending("Welcome", conn)
			self.receiving(conn)
		else:
			conn.sending("Wrong password", conn)
			self.login(conn, addr)

	def bind(self):
		while True:
			try:
				sock.bind(('', self.port))
				break
			except:
				self.port+=1
		logging.info("Server started")

	def listen(self, count):
		self.sock.listen(count)

		#пауза
		socket.settimeout(0.1)
		
		logging.info("Server is listenning")

	def connecting(self):
		thread = threading.Thread(target=self.connecting)
		self.threads.append(thread)

		conn, addr = self.sock.accept()
		logging.info("Client connection")
		thread.start()

		self.hi(conn, addr)

	def hi(self, conn, addr):
		with open('clients.txt', 'r+') as file:
			for line in file:
				if addr[0] not in line:
					self.sending("Register", conn)
					self.register(conn, addr)
				else:
					self.sending("Login", conn)
					self.login(conn, addr)

		with open('clients.txt', 'r+') as file:
			for line in file:
				if addr[0] in line:
					line=line.split(":")
					name = line[1]

		msg = "Hello " + name
		self.sending(msg, conn)

		self.chatting(conn)

	def chatting(self, conn, addr):

		send=threading.Thread(target=self.send_msg_to_chat, args=[conn])
		recv = threading.Thread(target = self.recv_msg_from_chat, args=[conn, addr])

		send.start()
		recv.start()

	def recv_msg_from_chat(self, conn, addr):
		while True:
			data = self.receiving(conn)
			logging.info("Receive message")
			self.data = self.data + data + '\n'

	def send_msg_to_chat(self, conn):
		while True:
			with self.lock:
				self.sending(self.data, conn)
				logging.info("Send message to clients")

sock = Server()

try:
	sock.bind()
	print(port)
	sock.listen(5)
	while True:
		sock.connecting()
except:
	sock.close_server()

