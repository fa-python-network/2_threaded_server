import socket
import socket
import json
import hashlib
import pickle
from threading import Thread      
from loger import Logfile

'''
def msgreciever(conn) ->str: #получения текстового сообщения с фиксированным заголовком
	msg_len = int(conn.recv(2), 10)
    return conn.recv(msg_len).decode()

def msgsending(conn, msg: str):   #отправкa сообщения с заголовком фиксированной длины
	msg = f"{len(msg):<{self.size}}" + msg
    conn.send(bytes(msg),"utf-8")
'''





def checkPasswrd(passwd, userkey) -> bool:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key == userkey

def generateHash(passwd) -> bytes:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key
def check_port(port):
		global sock
		while True:	
 			try:	
 				sock.bind(('',port))	
 				break
 			except:
				 port+=1		
		print(f'Занял порт {port}') 

def identification(conn,addr):
	try:
		open('users.json').close()
	except FileNotFoundError:
		open('users.json', 'a').close()
	with open('users.json', "r") as f:
		try:
			connectedUsers = json.load(f)
			name = connectedUsers[str(addr[0])]['name']
			conn.send(pickle.dumps(["pass","Введите свой пароль: "]))
			passwd = pickle.loads(conn.recv(1024))[1]
			conn.send(pickle.dumps(["accepted",f"Вошли успешно!"])) if checkPasswrd(passwd,connectedUsers[str(addr[0])]['password']) else identification(addr,conn)
		except:
			conn.send(pickle.dumps(["auth",f"Привет. Я тебя не знаю. Скажи мне свое имя: "]))
			name = pickle.loads(conn.recv(1024))[1]
			conn.send(pickle.dumps(["pass","Введите свой пароль: "]))
			passwd = generateHash(pickle.loads(conn.recv(1024))[1])
			conn.send(pickle.dumps(["accepted",f"Здравствуйте, {name}"]))
			with open("users.json", "w", encoding="utf-8") as f:
				json.dump({addr[0] : {'name': name, 'password': passwd} },f)
	# try:
	# 	open('users.json').close()
	# except:
	# 	open('users.json','w').close()
	# 	print("Here")
	# with open('users.json','r', encoding="utf-8") as f:
	# 	try:
	# 		d = json.load(f)
	# 		# conn.send(f'Здравствуйте, {name}'.encode())
	# 		conn.send("Введите свой пароль: ".encode('utf-8'))
	# 		passwd = conn.recv(1024).decode()
	# 		print(passwd)
	# 		print(self.Pswdcheck(passwd,d[ad[0]]['password']))
	# 	except:
	# 		conn.send('Это неизвестный пользователь. Скажите мне ваше имя: '.encode())
	# 		name = conn.recv(1024).decode()
	# 		conn.send(" Придумайте себе пароль:".encode())
	# 		passwd = HashGenerator(conn.recv(1024).decode())
	# 		with open('users.json','w', encoding="utf-8") as g:
	# 			json.dump({ad[0] : {'name': name, 'password': passwd} },g)
	# return ("Здравствуйте,", name,"!")


def listenClient(conn,addr):
	identification(conn,addr)
	while True:
		message = conn.recv(1024)
		if message:
				print(message.decode())
		else:
			conn.close()
			break

l = Logfile()
l.serverstart()
try:
	port=int(input("Ваш порт:"))
	if not 0 <= port <= 65535:
		raise ValueError
except ValueError:
		port = 9090

sock = socket.socket()
check_port(port) 
sock.listen(5)
while True:
	conn, addr = sock.accept()
	Thread(target=listenClient, args=(conn,addr)).start()


conn.close()
l.serverend()
