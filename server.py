import socket	   #сам сокет
from threading import Thread		#работа с потоками
import pickle	   #храним базу клиентов + отправка истории чата клиенту
import os		   #выключение сервера
import sys		  #системные методы

def listen_port():	  #только слушаем порт
	global sock, thread_is_alive		#передаем сокет + проверка нужности потока

	if thread_is_alive == True:
		sock.listen(3)	  #слушаем порт
	else:
		return

	while True:		 
		if thread_is_alive == True:	 #нужен ли нам поток сейчас - принимать запросы?
			conn, addr = sock.accept()
			
			print("Новый клиент!")
			Thread(target=one_client,args=(conn,addr)).start()      #запускаем поток на клиента
		else:
			print('Остановка потока listen_port!')
			break

def one_client(conn,addr):      #поток для работы с клиентом
	global connected_users, thread_is_alive
	connected_users.append(conn)        #добавляем клиента в список активных
	print("Стартовал новый поток")
	while True:
		if thread_is_alive == True:     #если поток нужен, то даем ему работать
			username = conn.recv(1024)
		else:
			print('Успешная остановка потока! one_client')
			break
		
		if username.decode() in db.keys():      #ести ли уже такой пользователь?
			password = db[username.decode()]
			conn.send('ask_pass'.encode())
			userpassword = conn.recv(1024)
			if password == userpassword.decode():       #совпал ли пароль?
				conn.send('valid'.encode())
				with open('history.txt','r') as f:      #отправляем клиенту историю чата
					sendhistory = f.read()
					sendhistory = pickle.dumps(sendhistory)
					conn.send(sendhistory)
				while True:         #процесс обработки сообщений
					if thread_is_alive == True:
						msg = conn.recv(1024)
					else:
						print('Успешная остановка потока! one_client')
						break
					
					if msg.decode() == 'exit_cmd':      #если клиент хочет выйти из чата
						msg = f'{username.decode()} покинул этот чат.'
						connected_users.remove(conn)    #удаляем клиента из активных
						conn.close()
						with open ('history.txt','a') as f:     #добавляем запись в историю
							f.write(msg+"\n");
						for user in connected_users:        #рассылаем новое сообщение всем, кроме адресанта
							if user != conn:
								user.send(msg.encode())
						break
					msgpart1 = f'[{username.decode()}]: '
					msgpart2 = msg.decode()
					msgsend = msgpart1 + msgpart2
					with open ('history.txt','a') as f:
						f.write(msgsend+"\n");
					for user in connected_users:        #рассылка всем, кроме адресанта, плюс проверка на реальность участника (не разорвал ли кто-то соединение принудительно - не через exit)
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
			conn.send('reg_req'.encode())       #если пользователь новый
			password = conn.recv(1024)
			db.update({username.decode():password.decode()})
			with open(db_file,'wb') as f:       #записываем в базу
				pickle.dump(db,f)
			conn.send('reg_end'.encode())
			conn.close()
			break

sock = socket.socket()      #сам сокет

thread_is_alive = True

db_file = 'clients.pickle'      #база данных клиентов
db = {}
connected_users = []        #список активных клиентов

#читаем базу
if os.path.getsize(db_file) > 0:        #если файл есть
	with open(db_file,'rb') as f:
		db = pickle.load(f)
else:
	db = {}
		
print(f'База клиентов и их пароли:\n',db)

port = 9100

sock.bind(('',port))

listen_thread = Thread(target=listen_port,args=())      #начинаем слушать порт
listen_thread.start()

while True:         #главный поток - прием команд от пользователя - администратора сервера
	print('\n\n\nГлавная панель управления сервером:\n')
	print('Меню действий:\n\n')

	print('[1] Вывести историю сообщений')
	print('[2] Вывести базу клиентов')
	print('[3] Очистить историю сообщений')
	print('[4] Очистить базу клиентов')
	print('[6] Прекратить прослушивание портов')
	print('[7] Закрыть сервер')

	action = input()        #прием команды
	
	if action == '1':       #если нужно вывести историю сообщений
		
		with open('history.txt','r') as f:
			sendhistory = f.read()
			print(sendhistory)
	
	if action == '6':       #прекратить слушать порт
		thread_is_alive = False     #волшебная переменная, которая анализируется во всех потоках
		print('Прослушивание портов остановлено!')
	
	if action == '7':       #закрыть сервер принудительно
		thread_is_alive = False
		os.abort()
		
	if action == '2':       #вывести базу клиентов
		print(db)
		
	if action == '3':       #очистить историю сообщений
		with open ('history.txt','w') as f:
			f.write('')
		print('Готово!')
			
	if action == '4':       #очистить базу клиентов
		db = {}
		with open(db_file,'wb') as f:
			pickle.dump(db,f)
		print('Готово!')