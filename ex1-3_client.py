import socket, csv, threading

def mssg (conn):
	msg = ''
	data = conn.recv(1024)
	msg += data.decode()
	print('ill send ')
	conn.send(msg.upper().encode())
	conn.send(" ")

class ClientThreading(threading.Thread):
	def __init__(self,addr,conn,port):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.port = port

		print("New connection added with address: " + str(addr)+':' +str(port))

	def run(self):
		print("Connection from: ", str(self.addr) + ':' + str(self.port))
		af = True
		while True:
			if af == True:
				self.conn.send("Your adress now: ")
				mssg(self.conn)
				af = False
			else:
				self.conn.send("Write your message: ")
				mssg(self.conn)
				
		self.conn.close()
		print(msg)

sock = socket.socket()
                                                       
num_sock = int(input("Enter the socket number: "))
host_str = str(raw_input("Enter the host: "))
f = 0
try:   
	sock.bind((host_str, num_sock))
except socket.error:
		print("This Adress already in use. This is free one: ")
		for i in range(1024,65536):
			try:
				sock.bind((host_str, i))
				f = i
				break
			except socket.error:
				pass

if f == 0:
	print(num_sock)
else:
	num_sock = f
	print(num_sock)

while True:
	sock.listen(1)
	conn, (ip, port) = sock.accept()
	newthread = ClientThreading(ip, conn, port)
	newthread.start()