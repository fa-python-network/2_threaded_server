import socket
from time import sleep

sock = socket.socket()

host = input('Введите имя хоста:')
if host == 'localhost':
    pass
else:
    if any(c.isalpha() for c in host) == True:
        print('некорректное имя хоста.По умолчанию локальный хост')
        host = 'localhost'
    else:
        host_lst = host.split('.')
        for i in host_lst:
            if 0 <= int(i) <= 255:
                pass
            else:
                host = 'localhost'
                print('Некорректное имя хоста.По умолчанию локальный хост')

try:
    port = int(input('номер порта:'))
    if 0 <= port <= 65535:
        pass
    else:
        print('некорректный номер порта. порт по умолчанию 9090')
        port = 9090

except ValueError:
    print("Некорректный номер порта. по умолчанию 9090")
    port = 9090

sock.connect((host, port))

print('exit для завершения работы с сервером')
msg = ''