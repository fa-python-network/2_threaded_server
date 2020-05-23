import socket

sock = socket.socket()

while True:
    try:
        address = input("Введите адресок сервера: ")
        if address == '':
            address = 'localhost'
        while True:
            port = int(input("Введите портик: "))
            if 1024 <= port <= 65535:
                break
        sock.connect((address, port))  # Подключение к серверу
    except (socket.error, ValueError):
        print("Повторите плиз")
    else:
        break

# массив для имитации трёх сообщений от пользователя
msg = ["Здарова бандиты!", "хочу курочку из кфс", "exit"]

# Цикл для имитации ввода сообщений пользователем
for i in range(len(msg)):
    sock.send(msg[i].encode())
    data = sock.recv(1024)
    print(data.decode())

sock.close()
