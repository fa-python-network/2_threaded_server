import socket
import threading
from time import sleep
def sendmsg(who, msg):
    sleep(0.1)
    msg_len = str(len(msg))
    while len(msg_len) < 5:
        msg_len = msg_len + "+"
    who.send((msg_len + msg).encode())


def checkmsg(who):
    msg_len = who.recv(5).decode()
    if msg_len == "":
        return ""
    msg_len = int(msg_len.replace('+', ''))
    msg = who.recv(msg_len*2).decode()
    return msg


def printmsg():
    while True:
        try:
            data = checkmsg(sock)
            print(data)
        except (KeyboardInterrupt, ConnectionAbortedError):
            print("Соединение разорвано.")
            break






host = 'localhost'
port = 9090
while True:
    host = input('Введите адрес хоста или localhost: \n')
    if host == 'localhost':
        host = '127.0.0.1'
        break
    if host == '':
        break
    host_l = host.split('.')
    if (0 <= int(host_l[0]) <= 255) and (0 <= int(host_l[1]) <= 255) and (0 <= int(host_l[2]) <= 255) and (0 <= int(host_l[3]) <= 255):
        break
    else:
        print('Введен неверный формат адреса.')

while True:
    port = input('Введите номер порта от 1024 до 49151: \n')
    port = int(port)
    if 1023 < port < 49152:
        break
    else:
        print('Неверный номер порта.')

sock = socket.socket()
sock.connect((host, port))  # Подключение к серверу



checkdata = threading.Thread(target=printmsg)
checkdata.start()
flag = True
while flag:
    try:
        msg = input()
        if msg == "exit":
            flag = False
            checkdata = None
        sendmsg(sock, msg)
    except ConnectionAbortedError:
        print('Соединение закрыто.')
        break

sock.close()