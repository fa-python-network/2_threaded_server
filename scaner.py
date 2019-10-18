import socket
from threading import Thread


global lst
lst = []
global full_lst
full_lst = {}

def check(par):
    for i in range(655*par, 655*par+655):
        sock = socket.socket()
        try:
            sock.connect(('localhost', i))
            print(str(i)+" порт открыт")
            lst.append(i)
            sock.close()
            full_lst[i] = "opened"
        except:
            print(str(i) + " порт закрыт")
            full_lst[i] = "closed"


threads = []
for i in range(0, 100):
    x = Thread(target=check, args=(i, ))
    threads.append(x)
    x.start()

for i in threads:
    i.join()

print(sorted(lst))
