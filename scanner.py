import socket
from threading import Thread


def progress_bar():
    global scannedports
    lastupdate = 0
    while True:
        if scannedports == 65537:
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
        sock.close()
        scannedports+=1

ip = input('Порты какого IP проверить? ')

if not ip or ip == 'localhost':
    ip = '127.0.0.1'
    
borders = [[0,10000],[10001,20000],[20001,30000],[30001,40000],[40001,50000],[50001,60000],[60001,65536]]

scannedports = 0


print('Начинаю работу...')

Thread(target=progress_bar,args=()).start()

for elem in borders:
    Thread(target=scan_port_now,args=(ip,elem[0],elem[1])).start()