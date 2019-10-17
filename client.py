import socket, sys, pickle
from threading import Thread
from time import sleep
from getpass import getpass

class Client: 

    '''
    init status - отслеживает статус приложения
    Возможные состояния: auth, passwd, finish, success 
    '''

    def __init__(self, sock, port, status = None):
        self.sock = sock
        self.port = port
        self.status = status
        self.name = input("Напишите ваше имя:")
        self.start()  


    def start(self):
        Thread(target=self.recv).start()
        '''
        Проверяю какой статус приложения и что от него 
        вообще хочет server и что он ему прислал
        '''
        while self.status != 'finish':
            if self.status:
               if self.status == "auth":
                   self.auth()
               elif self.status == "passwd":
                   self.sendPasswd()
               elif self.status == "success":
                   self.success()
               elif self.status == "nameRequest":
                   self.nameRequest()
               else:
                   msg = input()
                   if msg == "exit": 
                       self.status = "finish"
                       break
                   sendM = pickle.dumps(["message",f'{self.name} > {msg}'])
                   self.sock.send(sendM)

        self.sock.close()

    '''
    запрос имени
    '''
    def nameRequest(self):
        self.sock.send(pickle.dumps(["nameRequest",self.name]))
        sleep(1.5)

    '''
    отправка пароля
    '''
    def sendPasswd(self):
        passwd = getpass(self.data)
        self.sock.send(pickle.dumps(["passwd",passwd]))
        sleep(1.5)


    def auth(self):
        name = input(self.data)
        self.sock.send(pickle.dumps(["auth",name]))
        sleep(1.5)


    def success(self):
        print(self.data)
        self.status = "ready"


    def recv(self):
        while True:
            try:
                self.data = self.sock.recv(1024)
                if not self.data: sys.exit(0)
                status = pickle.loads(self.data)[0]
                self.status = status
                if self.status == "message":
                    print(pickle.loads(self.data)[1])
                else:
                    self.data = pickle.loads(self.data)[1]
            except OSError:
                break

sock = socket.socket()
sock.setblocking(True)
port =  int(input("Порт:"))
port = port if (port >= 0 and port <= 65535)  else  9090
sock.connect((input('Имя хоста:'), port))           
l = Client(sock, port)
