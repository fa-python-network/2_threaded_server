# coding=utf-8
import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, addr, conn):
        threading.Thread.__init__(self)
        self.csocket = conn
        print ("Новое подключение: ", addr)

    def run(self):
        print ("Подключение от : ", addr[0])
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'exit' or msg == '':
                break
            print ("Сообщение :", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print ("Клиет ", addr[0], " отключился...")

ip = "127.0.0.1"
port = 8080
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
print("Включение сервера")
print("Ожидание подключения пользователя..")
while True:
    server.listen(1)
    conn, addr = server.accept()
    thread = ClientThread(addr[0], conn)
    thread.start()
