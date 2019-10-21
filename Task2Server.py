import socket, threading,os
lock=threading.Lock()
lock2=threading.Lock()
lock3=threading.Lock()
class Client(threading.Thread):
	def __init__(self,addr,conn,port):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.port = port
		self.login=''

		

	def run(self):
		check=False
		print(str(self.addr)+' is connected. Port is ' +str(self.port))
		nameflag=0
		with lock:
			
			names = open('names.txt','r')

			
			for i in names: #check ip in names.txt
				
				if str(i.split(',')[0])[2:-1]==self.addr:#if ip is known
					nameflag=1#user is known
					name=i.split(',')[1][2:-1]
					while check==False:
						message=str(f"Hello, {name}! Password please").encode()#send Hello, username!Password please
						self.conn.send(message)
						password_txt=(self.conn.recv(1024)).decode()
						if i.split(',')[2][2:-3]==password_txt:
						#If password is right       
								print("\nPassword is right")
								check=True
								self.login=name						

			names.close()
		if nameflag==0:
			with lock3:
				self.conn.send(("Hello, stranger! What is your name,password?").encode())
				name_pass=self.conn.recv(1024).decode()
				name=name_pass[0:name_pass.find(',')]
				password=name_pass[name_pass.find(',')+1:]
				names = open('names.txt','a')
				names.write(str([self.addr,name,password])+"\n")
				users.append(name)#all users
				names.close()#file with logins and passwords
				check=True
				self.login=name
		self.actions()
	def global_message(self,gl_msg):#message to file and to every user
		with lock2:#send to global chat file
			global_chat = open('global_chat.txt','a')
			global_chat.write((f"{self.login} global: {gl_msg}"+"\n"))
			for userss in users:#send to all
				if userss!=self.name:
					userss.conn.send((f"{self.name} global: {gl_msg}").encode)
	def message_to_user(self,target_user,us_msg):
		with lock2:
			for userss in users:#send to user
				if userss==target_user:
					userss.conn.send((f"{self.name} private: {us_msg}").encode)                
	def actions(self):#Choose what to do
		self.conn.send(('Enter the commands: '+', '.join(actions_list)).encode())
	
		while True:
			command = self.conn.recv(1024).decode()
			if command == actions_list[1]:
				global_chat = open('global_chat.txt','r')
				for z in global_chat:
					self.conn.send(z.encode())
	        
			elif command == actions_list[2]:
				self.conn.send("Enter a message".encode())
				msg_glob=(self.conn.recv(1024)).decode()
				self.global_message(msg_glob)
			elif command == actions_list[0]:
				os.abort()
		
		
sock = socket.socket()
users=[]
actions_list=["quit","print global chat","sent global message"]
num_sock = int(input("Enter the socket number: "))


while True:
	try:
		sock.bind(("", num_sock))
	except :
		num_sock=num_sock+1
	else:
		break
print(num_sock)

while True:
	sock.listen(10)
	conn, (ip, port) = sock.accept()
	newthread = Client(ip, conn, port)
	newthread.start()
