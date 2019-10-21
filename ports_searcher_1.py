import socket
import progressbar
import threading

k = []
host = input('Введите имя хоста: ')

progress = progressbar.ProgressBar(widgets=[progressbar.Timer(), progressbar.Bar(), progressbar.ETA()])

for i in progress(range(0,65536)):
	sock = socket.socket()
	try:
		sock.connect((host, i))
		k.append(i)
		sock.close()
	except:
		continue

print(k)

