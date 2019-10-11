import socket
from threading import Thread
#ready

def progress_bar():
	global scannedports
	lastupdate = 0
	while True:
		if scannedports == 65536:
			print(f'\n\n\n\n\nРезультат - открытые порты:\n')
			for port in opened_ports:
				print(f'{port} ')
			break
		if lastupdate != scannedports:
			lastupdate = scannedports
			show_perc = round(scannedports/65537*100,2)
			active_part = "#"*(int(show_perc)//1)
			passive_part = " "*(100-(int(show_perc)//1))
			progress_line = "|"+active_part+passive_part+"|"
			print(f'{progress_line}\n')
			print(f'Прогресс: {show_perc}%')
	

def scan_port_now(ip,lborder,rborder):
	global scannedports
	for port in range(lborder,rborder+1):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		check = sock.connect_ex((ip,port))
		if check == 0:
		   print(f'Порт {port} открыт!')
		   opened_ports.append(port)
		sock.close()
		scannedports+=1

ip = input('Порты какого IP проверить? ')

if not ip or ip == 'localhost':
	ip = '127.0.0.1'
	

scannedports = 0
opened_ports = []

print('Начинаю работу...')

Thread(target=progress_bar,args=()).start()

lborder = 0
rborder = 65

while True:
	if rborder > 65535:
		rborder = 65535
	Thread(target=scan_port_now,args=(ip,lborder,rborder)).start()
	lborder+=66
	rborder+=66
	if rborder == 65535:
		break