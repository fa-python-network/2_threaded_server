import socket
import sys
import threading
import pickle


class Server(threading.Thread):
    def __init__(self, clients = []):
        super().__init__(daemon = True)
        self.clients = clients
        self.port = int(input("Please enter your port from 1024 to 65535: "))
        self.sock = None
        self.work_serv()

    def work_serv(self):
        self.sock = socket.socket()
        while True:
            try:
                self.sock.bind(('',self.port))
                break
            except:
                self.port += 1
        print(f'Got your port  {self.port}')
        self.sock.listen(5)
        HEADERSIZE = 10

        while True:
            conn, addr = self.sock.accept()
            print(f"Connection from client with IP {addr[0]} has been established")
            threading.Thread(target = self.conn_client,args = (conn,addr)).start()
            msg = f"Welcome to the server,{addr}!"
            msg = f"{len(msg):<{HEADERSIZE}}" + msg
            conn.send(bytes(msg,"utf-8"))
            self.clients.append(conn)

    def conn_client(self,conn,addr):
#Connection to the usr
        while True:
            data = conn.recv(1024).decode()
            if not data:
                conn.close()
                break
            else:
                print(f"Message: {data} is from {addr}")


serv=Server()
