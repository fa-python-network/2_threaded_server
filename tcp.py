import socket
import threading


def sck(port, host):
	sock = socket.socket()
	try:
		sock.connect((host, port))
		print(f"free port {port}")
	except OSError:
		pass
	finally:
		sock.close()


print("host:")
host = input()
if host == "":
	host='localhost'

for i in range(1, 65536):
	threading.Thread(target=sck, args = [i, host]).start()