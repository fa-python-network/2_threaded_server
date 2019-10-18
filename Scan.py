from tqdm import tqdm
import socket
import threading
from queue import Queue


def Scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip,port))
        #print(' Port: {0} it is open.'.format(port))
        ports.append(port)
        connect.close()
    except:
        pass


q = Queue()
lock = threading.Lock()
ports = []       
ip = input("Enter the ip: ")
for i in tqdm(range(1024, 65536)):
    potoc = threading.Thread(target=Scan_port, args=(ip,i))
    potoc.start()
    
print(sorted(ports))


    
    
