import socket, csv, threading, time

def manage(conn):
	conn.send("\nYou can manage the program: \n	Print 'STOP' to stop the programm\n 	Print 'PAUSE' to pause the threading\n  	Print 'SHOW LOGS' to print all logs from file\n 	Print 'DEL LOGS' to delete all logs from the file\n 	Print 'DEL USR' to delete all data about users from the file")

class ClientThreading(threading.Thread):
	def __init__(self,addr,conn,port):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.port = port

		print("New connection added with address: " + str(addr)+' : ' +str(port))

	def run(self):
		print("Connection from: ", str(self.addr) + ':' + str(self.port))
		with open ("log.txt", 'a') as f:
			f.write(str(self.addr))
			f.write('\n')

		af = 0
		
		with open ("users.csv", 'r') as f:
			csv_reader = csv.reader(f)
			for line in csv_reader:
				if line[0] == self.addr:
					self.conn.send("Hello, "+line[1] + ' ')
					af = 1


		if af == 0:
			with open ("users.csv", 'a') as f:
				writer = csv.writer(f)
				username = ''
				self.conn.send("Hello! Please, enter your name: ")
				username = self.conn.recv(1024).decode()
				writer.writerow([self.addr,username])
				

f = 0
sock = socket.socket()   
hostt = []
while True:
	try:
		host_str = str(raw_input("Enter the IP adress: "))  
		hostt = host_str.split(".")
		for i in hostt:
			try:
				if 0<=int(i)<=255:
					host.append(int(i))
				else:
					print("The IP is incorrect. Try again.")
					break
			except TypeError:
				print("The IP is incorrect. Try again.")
				break
		break
	except ValueError:
		print("The IP is incorrect. Try again.")   

num_sock = int(input("Enter the socket number: "))
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
k = 0
i = True
while i == True:
	sock.listen(1)
	conn, (ip, port) = sock.accept()
	newthread = ClientThreading(ip, conn, port)
	newthread.start()
	time.sleep(3)
	manage(conn)
	while True:
		messg = conn.recv(1024)
		print(messg.decode())
		if messg.decode() == "STOP":
			conn.send("All done")
			i = False
			break
		elif messg.decode() == "PAUSE":
			conn.send("All done")
			newthread.join()
		elif messg.decode() == "SHOW LOGS":
			with open ("log.txt", 'r') as f:
				for line in f:
					conn.send(line)
				conn.send("All done")
		elif messg.decode() == "DEL LOGS":
			f = open("log.txt", 'w')
			f.close()
			conn.send("All done")
		elif messg.decode() == "DEL USR":
			f = open("users.csv", 'w')
			f.close()	
			conn.send("All done")
		elif k != 0:
			conn.send("Something went wrong. Try again")
		k += 1			