import socket, os , hashlib, json, pickle, sys, sqlite3
from datetime import datetime
from contextlib import closing
from threading import Thread
from time import sleep

class Server:

	'''
	init 
	:log - файл логировани
	:users = списко пользователей json
	:clients = все клиенты из json
	:status = None
	'''
	def __init__(self,log = "file.log", users = "users.json", clients = [], status = None):
		self.__log = log
		self.__users = users
		self.clients = clients
		self.port =  int(input("Порт:"))
		self.sock = None
		self.status = status
		self.state = "active"
		self.messages = []
		if os.path.isfile("messages.db") == False : self.createMessagesDataBase()
		self.start()

	'''
	запуск сервера
	'''
	def start(self):
		self.sock = socket.socket()
		while True:	
 			try:	
 				self.sock.bind(('',self.port))	
 				break
 			except:
 				self.port+=1		
		print(f'Занял порт {self.port}')
		self.sock.listen(5)
		Thread(target=self.menu).start()
		while True:
			while self.state != "paused":
				conn, addr = self.sock.accept()
				self.serverStarted(addr)
				Thread(target = self.listenToClient,args = (conn,addr)).start()
				self.clients.append(conn)

	def menu(self):
		while True:
			state = int(input(
			"""
Здравствуйте, чем я могу вам помочь?
1.Отключение сервера
2.Прекратить прослушивать порты
3.Показ логов
4.Очистка логов
5.Очистка файла идентификации. \n"""
			))
			if state == 1:
				os._exit
			if state == 2:
				self.state = "inactive" if self.status == "active" else "active"
			elif state == 3:
				try:
					with open(self.__log, "r") as f:
						for line in f:
							print(line)
				except FileNotFoundError:
					print("Еще нет логов")
			elif state == 4:
				open(self.__log, 'w').close()
			elif state == 5:
				open(self.__users, 'w').close()
			else:
				print("Повторите еше раз!")
				sleep(1.5)
				os.system('cls' if os.name=='nt' else 'clear')
	def broadcast(self,msg, conn): 
		for sock in self.clients:
			if sock != conn:
				data = pickle.dumps(["message",msg])
				sock.send(data)
			
	'''
	проверка пароля пользователя
	'''
	def checkPasswrd(self, passwd, userkey) -> bool:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key == userkey

	'''
	генерация пароля пользователя
	'''
	def generateHash(self, passwd) -> bytes:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key
	
	'''
	прослушка пользователя
	'''
	def listenToClient(self, conn, address):
		self.checkUser(address,conn)
		while True:
				data = conn.recv(1024)
				if data:
					status , data = pickle.loads(data)
					if status == "message":
						self.insertMessagesIntoDataBase(data)
						self.broadcast(data, conn)
				else:
					conn.close()
					self.clients.remove(conn)
					self.serverStopped(address)
					break

	'''
	логирование пользователя, когда он подключаестя
	'''
	def serverStarted(self,ip):
		with open(self.__log, "a", encoding="utf-8") as f:
			print(f"{datetime.now().time()} Server Launched {ip}", file=f)
	'''
	логирование пользователя, когда он отключается от сервера
	'''
	def serverStopped(self,ip):
		with open(self.__log, "a", encoding="utf-8") as f:
			print(f"{datetime.now().time()} Server Stopped {ip}", file = f)

	'''
	выгрузка базы данных
	'''
	def loadMessagesDataBase(self,sock) -> list:
		conn = sqlite3.connect("messages.db")
		cursor = conn.cursor()
		for row in cursor.execute("SELECT * FROM messages"):
			sleep(0.3)
			sock.send(pickle.dumps(["message",row[0]]))
			

	# добавление в базу данных
	def insertMessagesIntoDataBase(self, messages):
		conn = sqlite3.connect("messages.db")
		cursor = conn.cursor()
		cursor.execute(f'INSERT INTO messages VALUES ("{messages}")')
		conn.commit()
	'''
	создание базы данных
	'''
	def createMessagesDataBase(self):
		conn = sqlite3.connect("messages.db")
		cursor = conn.cursor()
		cursor.execute("""CREATE TABLE messages
                  		  (message)
               		   """)
		conn.commit()

	'''
	проверка пользователя( БОЖЕ РЕФАКТОР НЕ ЗАВЕЗЛИ)
	'''
	def checkUser(self, addr, conn):
		try:
			open(self.__users).close()
		except FileNotFoundError:
			open(self.__users, 'a').close()
		with open(self.__users, "r") as f:
			try:
				conn.send(pickle.dumps(["nameRequest",""]))
				client = pickle.loads(conn.recv(1024))[1]
				users = json.load(f)
				try:
					name = users[client]
					conn.send(pickle.dumps(["passwd","Введите свой пароль: "]))
					passwd = pickle.loads(conn.recv(1024))[1]
					conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"])) if self.checkPasswrd(passwd,name['password']) else self.checkUser(addr,conn)
				except: self.unknownUser(conn,users)
			except:
				conn.send(pickle.dumps(["nameRequest",""]))
				client = pickle.loads(conn.recv(1024))[1]
				conn.send(pickle.dumps(["passwd","Я тебя не знаю, введите свой пароль: "]))
				passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
				conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
				with open(self.__users, "w", encoding="utf-8") as f:
					json.dump({client : {'password': passwd} },f)
		self.loadMessagesDataBase(conn)
	def unknownUser(self,conn, users):
		conn.send(pickle.dumps(["nameRequest",""]))
		client = pickle.loads(conn.recv(1024))[1]
		conn.send(pickle.dumps(["passwd","Я тебя не знаю, ведите свой пароль: "]))
		passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
		conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
		users[client] = {'password': passwd}
		print(users)
		with open(self.__users, "w", encoding="utf-8") as f:
			json.dump(users,f)


server = Server()
