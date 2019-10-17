import socket, threading
class ClientThread(threading.Thread):
    def __init__(self,clientAddr,clientsock):
        threading.Thread.__init__(self)
        self.csocket = clientsock
        print ("Новое соединение создано: ", clientAddr)
    def run(self):
        print ("Подключение : ", clientAddr)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='exit':
              break
            print ("От клиента: ", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Клиент ", clientAddr , " отсоеденился")
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Сервер запущен")
print("Ожидается подключение клиентов")
while True:
    server.listen(1)
    clientsock, clientAddr = server.accept()
    newthread = ClientThread(clientAddr, clientsock)
    newthread.start()
