import socket
from threading import Thread


def client(conn, addr):
    client_name = conn.recv(1024)
    while True:
        data = conn.recv(1024)
        if not data:
            return
        if data.decode() == "exit":
            conn.close()
            print("Клиент " + client_name.decode() + " вышел")
            return
        conn.send(data)


sock = socket.socket()
port = input("Введите номер порта ")
try:
    port = int(port)
except ValueError:
    port = 4448
except OSError:
    port += 11
sock.bind(('', port))

while True:
    stp = input("Для выхода напишите exit,для продолжение нажмите любую кнопку")
    if stp == 'exit':
        sock.close()
        break
    sock.listen(1)
    conn, addr = sock.accept()
    Thread(target=client, args=(conn, addr)).start()
