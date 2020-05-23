import socket

sock = socket.socket()


address = input("Aдрес сервера - ")

# безопасный ввод данных по умолчанию
if address == '':
    address = 'localhost'
port = int(input("Введите порт: "))
sock.connect((address, port))


msg = ["PINGUIN #1", "PINGUIN #2", "PINGUIN #3", "EXIT"]

# Пользователь считает пингвинов и уходит

for i in range(len(msg)):
    sock.send(msg[i].encode())
    data = sock.recv(1024)
    print(data.decode())
sock.close()
