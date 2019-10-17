import socket
import sys
import threading
import pickle


class Server():
    def __init__(self, clients=[]):
        self.clients=clients
        self.port=int(input("Port: "))
        self.sock=None
        self.work_server()

    def work_server(self):
        self.sock=socket.socket()
        while True:
            try:
                self.sock.bind(('',self.port))
                break
            except:
                self.port+=1
        print(f'Got port #{self.port}')
        self.sock.listen(5)
        HEADERSIZE=10
        while True:
            conn,addr=self.sock.accept()
            print(f"Connection from client with IP {addr[0]} has been established")
            threading.Thread(target=self.connect_with_client,args=(conn,addr)).start()
            msg=f"Welcome to the server,{addr}!"
            msg=f"{len(msg):<{HEADERSIZE}}"+msg
            conn.send(bytes(msg,"utf-8"))
            self.clients.append(conn)
            

    def connect_with_client(self,conn,addr):
        while True:
            data=conn.recv(1024).decode()
            if not data:
                conn.close();
                break
            else:
                print(f"Message:{data} is from {addr}")

SE=Server()
        
