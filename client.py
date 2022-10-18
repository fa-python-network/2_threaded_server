import socket
from time import sleep
import threading

# создание и коннект соккета (установка соединения)
sock = socket.socket()
#sock.setblocking(1)
sock.connect(('localhost', int(input('Введите порт\n'))))

# получение сообщения
def message_receiver():
    while True:
        msg = sock.recv(1024).decode()
        if msg=='exit':
            break
        else:
            print(msg)

# создание потока-демона для получения сообщения
tr = threading.Thread(target = message_receiver, daemon=True)
tr.start()

# отправка сообщения
while True:
    msg = input("Введите сообщение. Если хотите выйти, то напишите exit\n")
    sleep(1)
    if msg=='exit':
        sock.send(msg.encode('utf-8'))
        break
    else:
        sock.send(msg.encode('utf-8'))

# закрытие соединения
sock.close()
