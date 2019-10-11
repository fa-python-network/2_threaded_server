import socket
from threading import Thread 


sock = socket.socket()
print('kakoy host?')
x = input()
l = []
proveren = 0

def lol(y, y1):
	global l,proveren
	for y in range (y,y1):
		try:
			sock = socket.socket()
			sock.connect((x, y))
			print(y, "port svoboden!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			l.append(y)
			sock.close()
			proveren += 1
		except:
			print(y, "port zanyat")
			proveren += 1
			continue
for z in range(0,660):
	Thread(target=lol, args=(z*100, z*100+100)).start()
#lol(9090,9100)
while True:
	if proveren >= 66000:
		print(l)
		break
		