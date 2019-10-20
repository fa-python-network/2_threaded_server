import socket
import time
import sys
import threading

class Client:
    def __init__(self,sock,port):
        self.sock=sock
        self.port=port
        self.client_start()

    def client_start(self): 
        threading.Thread(target=self.recive).start()
        while True:
            msg=input()
            if msg=="exit":
                break
            else:
                self.sock.send(msg.encode())
        self.sock.close()

    def recive(self):
        while True:
        	try:
        		self.data=self.sock.recv(1024)
        		print(self.data.decode())
        		if not self.data:
        			sys.exit(0)
        	except (ConnectionError, OSError):
        		print('До свидания')
        		break

sock=socket.socket()
port=int(input("Введите номер порта: "))
if not(port>=0 and port <=65535):
    port=9090
sock.connect(('localhost',port))
clie_=Client(sock,port)

