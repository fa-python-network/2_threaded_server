import threading
import socket
import time

lock = threading.Lock()

def scanner(port, host):


	sock = socket.socket()
	try:
		sock.connect((host, port))
		print("Порт {} открыт".format(port))
	except:
		pass
	finally:
		sock.close()

host=input('Введите имя хоста/IP: ')

time_start = time.time()
for port in range(65535):
	
	t = threading.Thread(target=scanner, args=[port, host])
	time.sleep(0.00000000001)
	t.start()	

time_res = time.time() - time_start
print(time_res)