import socket
import time
import sys
import threading


class Client:
    def __init__(self,sock,port):
        self.sock=sock
        self.port=port
        self.name=input("What is your name ?")
        self.work_client()

    def work_client(self): 
        threading.Thread(target=self.recv).start()
        HEADERSIZE=10
        while True:
            msg=input("Message: ")
            msg=f"{len(msg):<{HEADERSIZE}}"+msg
            if msg=="exit":
                break
            else:
                self.sock.send(msg.encode())
        self.sock.close()
        
    def recv(self):
        while True:
            self.data=self.sock.recv(1024) #got data from server
            print(self.data.decode())
            if not self.data:
                sys.exit(0)   
    
sock=socket.socket()
port=int(input("Port: "))
if not(port>=0 and port <=65535):
    port=9090
sock.connect(('localhost',port))
CL=Client(sock,port)



