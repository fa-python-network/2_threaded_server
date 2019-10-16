import socket
import threading

class Client(socket.socket):

	def __init__(self):
		self.sock = socket.socket()
		self.lock = threading.Lock()

	@property
	def sending(msg, sock):
		sock.send(msg.encode())

	@property 
	def receiving(sock):
		sock.recv(1024).decode()

	def register(self, sock):
		name = input()
		self.sending(name, sock)
		password = input()
		self.sending(password, sock)

	def login(self,sock, msg):
		print(msg)
		password = input()
		self.sending(password, sock)
		mes = self.receiving(sock)
		if mes == "Welcome":
			pass
		else:
			self.login(sock, "Input correct password")

	def connection(self):
		self.host = input("Input host: ")
		port= input("Input port: ")
		if self.host=="":
			self.host = "127.0.0.1"
		if port == "":
			self.port=9090
		else:
			self.port=int(port)
		self.sock.connect((self.host, self.port))
		print("Connection")

	def hi(self):
		data = self.receiving(self.sock)
		if data == "Register":
			self.register(self.sock)
		elif data == "Login":
			self.login(self.sock, "Input passwd")
		data = self.receiving(self.sock)
		print(data)

	def chatting(self):
		print("Input quit if you want to exit")
		send1 = threading.Thread(target=self.send_msg_to_chat)
		recv1 = threading.Thread(target=self.recv_msg_from_chat)

		send1.start()
		recv1.start()

	def recv_msg_from_chat(self):
		while True:
			data = self.receiving(self.sock)
			if not data:
				continue
			else:
				print(data)

	def send_msg_to_chat(self):
		with self.lock:
			msg=input()
		while msg!="quit":
			self.sending(msg, self.sock)
			msg=input()

	def closing(self):
		self.sock.close()
		print("Stop connecting")

	def run(self):
		self.connection()
		self.hi()
		self.chatting()

sock = Client()
sock.run()




