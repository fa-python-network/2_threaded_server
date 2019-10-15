import socket
from threading import Thread
import pickle
import os
import sys

def listen_port():
	global sock

	sock.listen(3)

	while True:
		conn, addr = sock.accept()
		
		print("Новый клиент!")
		Thread(target=one_client,args=(conn,addr)).start()

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
				with open('history.txt','r') as f:
					sendhistory = f.read()
					sendhistory = pickle.dumps(sendhistory)
					conn.send(sendhistory)
				while True:
					msg = conn.recv(1024)
					if msg.decode() == 'exit_cmd':
						msg = f'{username.decode()} покинул этот чат.'
						connected_users.remove(conn)
						conn.close()
						with open ('history.txt','a') as f:
							f.write(msg+"\n");
						for user in connected_users:
							if user != conn:
								user.send(msg.encode())
						break
					msgpart1 = f'[{username.decode()}]: '
					msgpart2 = msg.decode()
					msgsend = msgpart1 + msgpart2
					with open ('history.txt','a') as f:
						f.write(msgsend+"\n");
					for user in connected_users:
						if user != conn:
							try:
								user.send(msgsend.encode())
							except:
								pass
							
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

listen_thread = Thread(target=listen_port,args=())
listen_thread.start()

print('\n\n\nГлавная панель управления сервером:\n')
print('Меню действий:\n\n')

print('[1] Вывести историю сообщений')
print('[2] Вывести базу клиентов')
print('[3] Очистить историю сообщений')
print('[4] Очистить базу клиентов')
print('[6] Прекратить прослушивание портов')
print('[7] Закрыть сервер')

while True:
	action = input()
	
	if action == '1':
		
		with open('history.txt','r') as f:
			sendhistory = f.read()
			print(sendhistory)
		print('\n\n\nГлавная панель управления сервером:\n')
		print('Меню действий:\n\n')

		print('[1] Вывести историю сообщений')
		print('[2] Вывести базу клиентов')
		print('[3] Очистить историю сообщений')
		print('[4] Очистить базу клиентов')
		print('[6] Прекратить прослушивание портов')
		print('[7] Закрыть сервер')
	
	if action == '7':
		sys.exit()
		
	if action == '2':
		print(db)
		
	if action == '3':
		with open ('history.txt','w') as f:
			f.write('')
		print('Готово!')
			
	if action == '4':
		db = {}
		with open(db_file,'wb') as f:
			db = pickle.dump(db,f)
		print('Готово!')