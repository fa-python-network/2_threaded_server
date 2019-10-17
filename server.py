import socket
import threading
import logging

sock = socket.socket()
logging.basicConfig(filename = "exp.log", filemode = "w", level = logging.INFO)

client_host_port = 1024
while client_host_port != 65536:
	try:
		logging.info(f'Сервер пытается подключиться к порту: {client_host_port}')
		sock.bind(('', client_host_port))
		break
	except:
		logging.error(f'При подключении к порту {client_host_port} возникла ошибка')
		client_host_port += 1

sock.listen(100)

print('Порт: ', client_host_port)
logging.info(f'Подключено к порту: {client_host_port}\n')

def lazy_output(addr, data):
	print(f"Пользователь {addr} закончил сессию")
	print("Пользовательский ввод: ", data, f"Пользователь: {addr}\n")
	logging.info(f"Пользователь {addr} заканчивает сессию\n")

def user_input(conn, addr):
	msg = ''
	while True:
		data = conn.recv(1024).decode()
		logging.info(f"Пользовательский ввод: {data}. Пользователь: {addr}\n")
		if not data:
			lazy_output(addr, data)
			break
		msg+=data
		conn.send(data.encode())
		lazy_output(addr, data)
		break
count = 0
while True:
	count += 1
	conn, addr = sock.accept()
	print(f"Новое подключение: {addr}\n")
	logging.info(f"Новое подключение: {addr}")
	Th = threading.Thread(target = user_input, args = (conn, addr))
	logging.info(f"Поток №{count}\n")
	Th.start()
conn.close()