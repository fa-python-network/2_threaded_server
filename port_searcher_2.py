import threading
import socket
import progressbar


def check(host, start, end):
	sock = socket.socket()
	for i in range(start, end+1):
		try:
			sock.connect((host, i))
			print(i)
			sock.close()
		except:
			continue


potoks = int(input('Введите кол потоков: '))
host = input('Введите хост: ')
ports = 65535
progress = progressbar.ProgressBar(widgets=[' ' * (len(str(ports)) + 1),progressbar.Timer(), progressbar.Bar(), progressbar.ETA()])

for i in progress(range(0,potoks)):
	if i == 0:
		threading.Thread(target = check,args = (host,int(ports / potoks) * i, int(ports / potoks) * (i+1))).start() 	#threading.Thread(target = check, args = ('localhost', k[i][0], k[i][1] )).start()
	if i != potoks - 1 and i != 0:
		threading.Thread(target = check, args = (host,int(ports / potoks) * i+1, int(ports / potoks) * (i+1)) ).start()
	if i == potoks - 1 and i != 0:
		threading.Thread(target = check, args = (host,int(ports / potoks) * i+1, ports)).start()
