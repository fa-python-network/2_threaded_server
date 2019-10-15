import socket
from myserver import Myserver
from time import sleep
import re


while True:
    inputPort = input('Vvedite port nomber or press Enter if you want port 9090: ')
    if inputPort == '':
        inputPort = 9090
        break
    elif not inputPort.isnumeric():
        print('try again')
    elif not  1024 < int(inputPort) <= 65535:
        print('try again')
    else:
        inputPort = int(inputPort)
        break
while True:
    inputHost = input('Vvedite host or press Enter if you want localhost: ')
    if inputHost == '':
        inputHost = 'localhost'
        break
    elif re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', inputHost) == None:
       print('try again')
    else:
        break
sock = Myserver()
sock.setblocking(1)
sock.connect((inputHost, inputPort))
print("Connection with server")
aut = sock.newmessage()
print(aut)
if aut == 'Hello, You\'re new, please enter you name ': #регистрация нового пользователя
    sock.sendmessage(input())
    print(sock.newmessage())
    sock.sendmessage(input())
else: #ввод пароля
    while True:
        sock.sendmessage(input())
        aut = sock.newmessage()
        if aut[0] != 'I':
            print(aut)
            break
        print(aut)

while True:
    msg = input("Vvedite: ")
    sock.sendmessage(msg)
    if msg == "exit":
        sock.close()
        print('stop connection')
        break


