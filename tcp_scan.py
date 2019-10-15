import threading
import socket

HOST = 'localhost'
free_port = []
START = 4000
END = 5000
HOWMUCH = 400

all_port = [i for i in range(START, END)]


def port_connect(adr, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn.connect_ex((HOST, port)):
        return port
    else: 
        return False


def port_thread():
    while all_port:
        port = all_port.pop()
        if port_connect(adr,port):
            free_port.append(port)
    





adr = HOST
threads = [threading.Thread(target=port_thread) for i in range(HOWMUCH)]

[i.start() for i in threads]
[i.join() for i in threads]


print (free_port)

