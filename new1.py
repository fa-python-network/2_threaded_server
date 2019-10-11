import socket
from threading import Thread
from time import sleep


def check(port, lst):
	sock = socket.socket()
	try:
		sock.connect(('localhost', port))
		lst.append(port)
		print(f'{port} svoboden')
	except OSError:
		print(f'{port} zanyat')
		pass
	finally:
		sock.close()
		
		
lst = []
threads=[]
for i in range(1, 65536):
	threads.append(Thread(target=check, args=(i, lst)))

for t in threads:
	t.start()
for t in threads:
	t.join()
	
print()

print(lst)