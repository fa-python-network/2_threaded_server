import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, clientAddr, csocket):
        threading.Thread.__init__(self)
        self.lsocket = csocket

    def run(self):

        clmsg = ''
        while True:
            data = self.lsocket.recv(1024)
            clmsg = data.decode()
           
           


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 9090))
print("server start")
print("Waiting for client request...")
while True:
    server.listen(1)
    csocket, clientAddr = server.accept()
    thr = ClientThread(clientAddr, clientsock)
    thr.start()

