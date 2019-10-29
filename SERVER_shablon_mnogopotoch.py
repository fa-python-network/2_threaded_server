import socket
import threading
import random


sock = socket.socket()
port = 8080
try:
	sock.bind(('', port))
except:
	port = random.randint(8080,8300)
	sock.bind(('', port))
print("Свободный порт:", port)
sock.listen(1)


def reader(conn, addr, lst):
	while True:
		msg = conn.recv(1024).decode()
		if msg != 'exit':
			for i in lst:
				if i != conn:
					i.send((msg).encode('utf-8'))
		else:
			lst.remove(conn)
			break
	conn.close()


def main(lst):
	conn, addr = sock.accept()
	threading.Thread(target  = reader, args = (conn, addr, lst), daemon=True).start()
	lst.append(conn)
	#print(len(lst))
	main(lst)


lst = []
main(lst)
	
