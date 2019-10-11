import socket
from threading import Thread
import pickle
import os


def one_client(conn,addr):
	global connected_users
	connected_users.append(conn)
	print("Стартовал новый поток")
	while True:
		username = conn.recv(1024)
		if username.decode() in db.keys():
			password = db[username.decode()]
			conn.send('ask_pass'.encode())
			userpassword = conn.recv(1024)
			if password == userpassword.decode():
				conn.send('valid'.encode())
				while True:
					msg = conn.recv(1024)
					if msg.decode() == 'exit_cmd':
						msg = f'{username} покинул этот чат.'
						connected_users.remove(conn)
						conn.close()
						for user in connected_users:
							if user != conn:
								user.send(msg.encode())
						break
					msgpart1 = f'[{username.decode()}]: '
					msgpart2 = msg.decode()
					msgsend = msgpart1 + msgpart2
					for user in connected_users:
						if user != conn:
							user.send(msgsend.encode())
				break
			else:
				conn.send('error'.encode())
				conn.close()
				break
		else:
			#registration required
			conn.send('reg_req'.encode())
			password = conn.recv(1024)
			db.update({username.decode():password.decode()})
			with open(db_file,'wb') as f:
				pickle.dump(db,f)
			conn.send('reg_end'.encode())
			conn.close()
			break

sock = socket.socket()

db_file = 'clients.pickle'
db = {}
connected_users = []

#читаем базу
if os.path.getsize(db_file) > 0:
	with open(db_file,'rb') as f:
		db = pickle.load(f)
else:
	db = {}
		
print(f'База клиентов и их пароли:\n',db)

port = 9100

sock.bind(('',port))
sock.listen(3)

while True:
	conn, addr = sock.accept()
	
	print("Новый клиент!")
	Thread(target=one_client,args=(conn,addr)).start()
	