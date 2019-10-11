import socket

def port_scan(host, port):
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.5)
	try:
		connect = sock.connect((host, port))
		print("Port ", port, " openned")
		connect.close()
	except:
		pass

host="127.0.0.1"

import threading
for i in range(1000):
	potoc=threading.Thread(target = port_scan, args=(host, i))
	potoc.start()
	