import socket

sock = socket.socket()

host = input('Введите имя хоста: ')
if host == 'localhost':
    pass
else:
    if any(c.isalpha() for c in host) == True:
        print('Введено некорректное имя хоста.По умолчанию выбран локальный хост')
        host = 'localhost'
    else:
        host_lst = host.split('.')           
        for i in host_lst:
            if 0 <= int(i) <= 255:
                pass
            else:
                host = 'localhost'
                print('Введено некорректное имя хоста.По умолчанию выбран локальный хост')

try:
    port = int(input('Введите номер порта: '))
    if 0 <= port <= 65535:
        pass
    else:
        print('Введен некорректный номер порта.Номер порта по умолчанию 9090')
        port = 9090
        
except ValueError:
    print("Некорректный номер порта. Номер порта по умолчанию 9090")
    port = 9090  

sock.connect((host, port))

print('Напишите exit для завершения работы с сервером')
msg = ''

while True:
    if msg != 'exit':
        print('Введите сообщение:')
        msg = input()
        sock.send(msg.encode())
        data = sock.recv(1024)
    else:
        break
    
sock.close()
print('Работа с сервером завершена.') 

