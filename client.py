import socket
import re
# Валидация портов
while True:
    port = input('Введите порт от 1024 до 65535: \n')
    if not port.isnumeric():
        print('Ошибка')
    elif 1023 <= int(port) <= 65535:
        break
    else:
        print('Ошибка: порт не входит в нужный диапазон')
# Валидация айпи
while True:
    ip = input('Введите ip сервера или оставьте пустым для значения localhost: \n')
    if ip == '':
        ip = 'localhost'
        break
    elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) == None:
        print('Ошибка')
    else:
        break
    
sock = socket.socket()
sock.setblocking(1)
sock.connect((ip, int(port)))
# Аутентификация
# print(sock.recv(1024).decode())
aut = sock.recv(1024).decode()
print(aut)
if (aut == 'Input your name:'):
    sock.send(input().encode())
    print(sock.recv(1024).decode())
    sock.send(input().encode())
else:
    print(sock.recv(1024).decode())
    while True:
        sock.send(input().encode())
        answer = sock.recv(1024).decode()
        print(answer)
        if answer[0] == 'C':
            break

# Отправка сообщений на сервер
while True:
    msg = input("Input message: ")
    if msg == "exit":
        sock.close()
        break
    sock.send(msg.encode())
    data = sock.recv(1024)
