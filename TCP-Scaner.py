import socket
import threading
import time


def scan_port(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip,port))
        print('Port :',port,' is open.')
        connect.close()
    except:
        pass


ip = 'localhost'


for i in range(65535):
    potoc = threading.Thread(target=scan_port, args=(ip,i))
    potoc.start()




