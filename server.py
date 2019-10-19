
import socket, threading
from datetime import datetime
def accept_client():
	while True:
		cl_sock, cl_addr = serv_sock.accept()
		clients_list.append(cl_sock)
		print('New connection:', cl_addr)
		name = cl_sock.recv(1024).decode()
		print('New client:', name)
		thread_client = threading.Thread(target = bc_usr, args=[cl_sock])
		thread_client.start()
def bc_usr(cl_sock):
	while True:
		try:
			data = cl_sock.recv(1024)
			if data:
				b_usr(cl_sock, data)
		except Exception as x:
			print(x)
			break

def b_usr(cs_sock, msg):
	#print(msg.decode()) #Если хотите загадить консоль сообщениями от клиетов, то милости просим убрать решетку.
	with open('chat_history.txt', 'a', encoding = 'utf-8') as f:
		print(f"[{datetime.now().time()}] {msg.decode()}", file = f) #В консоли сервера сообщения отображаться не будут, чтобы не засорять. Они будут в консолях клиентов, а также в специальном лог-файле.
	for client in clients_list:
		if client != cs_sock:
			client.send(msg)
   
clients_list = []
serv_sock = socket.socket()
serv_sock.bind(('localhost', 9128))
serv_sock.listen(1)
print('Server starting!' + '\nSearch the client...')
thread_ac = threading.Thread(target = accept_client)
thread_ac.start()