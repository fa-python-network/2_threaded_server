import socket 
import threading
from time import sleep
import sys
 
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=int(input('Please enter your port number from 1024 to 65535: '))
if not (port >= 1024 and port <= 65535):
    port=9091
sock.connect(('localhost',port))


class Client():
    def __init__(self, sock, port):
        threading.Thread.__init__(self)
        self.sock = sock
        self.port = port

        self.username = input('Please enter your username: ')
        self.thread_cl()

    def thread_cl(self):
        threading.Thread(target = self.recv_msg).start() #Создаю поток
        HEADERSIZE = 10
        while True:
             
            msg = input(f"Enter your message, dear {self.username} : ")
            #msg = f"{len(msg):<{HEADERSIZE}}" + msg
            if msg == 'exit' :
                self.sock.close()
                break
            else:
                self.sock.send(msg.encode())
        self.sock.close()
   
    def recv_msg(self):

#'''Функция создана для принятия сообщения'''

        while True:
            self.data = self.sock.recv(1024)
            print(self.data.decode())
        if not self.data:
            print('Disconnect')
            sys.exit(0)        
          
Cl = Client(sock,port)

