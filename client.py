import socket
import threading
from time import sleep


sock = socket.socket()

try:
    num_port = int(input("Введите номер порта: "))
    assert 1024 < num_port < 65535, "Введенный порт рекомендуется не использовать или он занят."
except (AssertionError, TypeError, ValueError) as e:
    print("Будет введен порт по умолчанию 9091")
    num_port = 9091

sock.connect(('localhost', num_port))
print("Успешно")
msg = ''

while msg != 'exit':
    msg = input()
    sock.send(msg.encode())
    inf = sock.recv(1024)
    print(inf.decode())


sock.close()
