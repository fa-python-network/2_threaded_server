import socket
from threading import Thread
from os import system
bar = ""
provereno = 1


def check(port, lst):
	global provereno, bar
	sock = socket.socket()
	try:
		sock.connect(('localhost', port))
		lst.append(port)
		#print(f'{port} svoboden')
	except OSError:
		#print(f'{port} zanyat')
		pass
	finally:
		provereno += 1
		if provereno % 600 == 0:
			system('cls')	
			bar += "#"
			print(bar)
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