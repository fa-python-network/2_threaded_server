import socket
import sys
import pickle
from threading import Thread

STATUS = None


def recv():
        while True:
            try:
                global sock
                global STATUS
                data = sock.recv(1024)
                if not data: sys.exit(0)
                status = pickle.loads(data)
                STATUS = status
                
            except OSError:
                break

try:
    port=int(input("ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError :
    port = 9090

sock = socket.socket()
sock.setblocking(True)
sock.connect(('localhost', port))
Thread(target=recv).start()
while True:
    if STATUS != None and STATUS == "exit":
        break
    elif STATUS:
        if STATUS[0] == "auth":
            name = pickle.dumps(["auth", input(STATUS[1])])
            sock.send(name)
            STATUS = None
        elif STATUS[0] == "pass":
            passwd = pickle.dumps(["pass", input(STATUS[1])])
            sock.send(passwd)
            STATUS = None
        elif STATUS[0] == "accepted":
            print(STATUS[1])
            STATUS = "typing"
        else:
            msg = input()
            if msg != "exit":             
                sock.send(msg.encode())
            else: 
                break
sock.close()
    # while STATUS:
    #     if STATUS == "auth":
    #         name = pickle.dumps(["auth", input("1")])
    #         sock.send(name)
    #         STATUS = None
    #     elif STATUS == "pass":
    #         passwd = pickle.dumps(["pass", input("2")])
    #         sock.send(passwd)
    #         STATUS = None
    #     elif STATUS == "accepted":
    #         STATUS == "typing"
    #     # msg = input()
    #     # sock.send(msg)
