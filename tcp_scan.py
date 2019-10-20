import threading
import socket
from tqdm import tqdm

adr = 'localhost'
free_port = []
start = 0
finish = 65535
NumbersOfThreads=3000
one_percent= int((finish-start)/100)
all_port = [i for i in range(start, finish)]
procent = 0
pbar = tqdm(total=100)


def port_connect(adr, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    if conn.connect_ex((adr, port)):
        return port
    else:
        return False


def port_thread():
    while all_port:
        global procent
        global loading
        port = all_port.pop()
        procent += 1
        if procent % one_percent == 0:
            pbar.update(1)
        if port_connect(adr, port):
            free_port.append(port)
    pbar.close()

threads = [threading.Thread(target=port_thread) for i in range(NumbersOfThreads)]

[i.start() for i in threads]
[i.join() for i in threads]
print("\n")
lenght=len(free_port)
print(f"Список открытых портов (всего {lenght}):")
print(sorted(free_port))
print(len(free_port))