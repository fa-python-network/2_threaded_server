import socket
from threading import Thread


global lst1
lst1 = []
global lst2
lst2 = {}

def check(par):
    for i in range(655*par, 655*par+655):
        sock = socket.socket()
        try:
            sock.connect(('localhost', i))
            print(str(i)+" порт открыт")
            lst1.append(i)
            sock.close()
            lst2[i] = "opened"
        except:
            print(str(i) + " порт закрыт")
            lst2[i] = "closed"


threads = []
for i in range(0, 100):
    x = Thread(target=check, args=(i, ))
    threads.append(x)
    x.start()

for i in threads:
    i.join()

print(sorted(lst1))
def check(par):
    for i in range(655*par, 655*par+655):
        sock = socket.socket()
        try:
            sock.connect(('localhost', i))
            print(str(i)+" порт открыт")
            lst1.append(i)
            sock.close()
            lst2[i] = "opened"
        except:
            print(str(i) + " порт закрыт")
            lst2[i] = "closed"


threads = []
for i in range(0, 100):
    x = Thread(target=check, args=(i, ))
    threads.append(x)
    x.start()

for i in threads:
    i.join()

print(sorted(lst))
