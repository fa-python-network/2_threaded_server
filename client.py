import socket

sock = socket.socket()

while True:
    try:
        address = input("Введите адрес сервера: ")
        if address == '':
            address = 'localhost'
        while True:
            port = int(input("Введите порт (диапозон 1024-65535): "))
            if 1024 <= port <= 65535:
                break
        sock.connect((address, port))  # Подключение к серверу
    except (socket.error, ValueError):
        print("Повторите ввод!")
    else:
        break

# массив для имитации сообщений от пользователя
msg = ["Привет", "Это моя вторая лабоработная работа", "Спасибо за внимание", "exit"]

# Цикл для имитации ввода сообщений пользователем
for i in range(len(msg)):
    sock.send(msg[i].encode())
    data = sock.recv(1024)
    print(data.decode())

sock.close()
