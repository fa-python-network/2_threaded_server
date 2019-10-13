import socket
import time
import threading
import sys
from queue import Queue


socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()
status = 0
ports = []
target = '127.0.0.1'
def progressbar(it, prefix="", file=sys.stdout):
    size=40
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
    
def portscan(port):
    s = socket.socket()
    global status, ports
    try:
        con = s.connect((target, port))
        with print_lock:
            ports.append(port)
        con.close()
    except:
        pass
    status += 1

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()

for x in range(200):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
for worker in range(1, 65536):
    q.put(worker)

for i in progressbar(range(65536), "Progress: "):
    while i > status: continue
for port in ports:
    print('Port', port, 'is open!')
