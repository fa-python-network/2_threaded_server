import socket


ip = input('Порты какого IP проверить? ')

if not ip or ip == 'localhost':
    ip = '127.0.0.1'
    

print('Начинаю работу...')

for port in range(0,65536):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check = sock.connect_ex((ip,port))
    if check == 0:
       print(f'Порт {port} открыт!')
    sock.close()
        
        
print('Сканирование завершено!')
wait = input()