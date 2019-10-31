import socket,time,threading,sys
from queue import Queue

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()
status = 0
ports = []
def progressbar(it, prefix="", file=sys.stdout):
    size=10
    count = len(it)
    def show(j):
        x = int(size*j/count)
        percent=(j/count)*100
        file.write('Please,wait! It will take some time ({}{}) {:.1f}/{}% \r'.format("1"*x,"0"*(10-x),j / count * 100,100))
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
        con = s.connect(('127.0.0.1', port))
        with print_lock:
            ports.append(str(port))
        con.close()
    except:
        pass
    status += 1

def threader():
    while True:
        global v
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()
startTime = time.time()

for x in range(220):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


for worker in range(1, 65536):
    q.put(worker)
for i in progressbar(range(65536), ""):
    while i > status: continue
print('Done!')
print("Open ports: " + ", ".join(ports) + ".") 
